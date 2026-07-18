# olmon/scraper.py
"""Scrapes https://ollama.com/library since there is no public API for the
model library (only for models already pulled locally).

Two pages are scraped:
  - /library                 -> one card per base model (name, description,
                                 capability badges, pull count, tag count)
  - /library/<model>/tags    -> every pullable tag/variant for that model
                                 (size on disk, context window, digest)

The parser keys off `<a href="/library/...">` patterns rather than CSS
classes, since hrefs are far less likely to change than styling. If
ollama.com reorganizes the library pages, PULLS_TAGS_RE / SIZE_RE / etc.
below are the places to fix first — run `olmon db update` and compare
`olmon db stats` before/after to sanity check.
"""

import re

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://ollama.com"
LIBRARY_URL = f"{BASE_URL}/library"
USER_AGENT = "olmon-db-scraper/1.0 (+https://github.com/glemiu6/olmon)"

CAPABILITY_WORDS = {"tools", "vision", "thinking", "embedding", "cloud", "audio"}
INPUT_TYPES = ["Text", "Vision", "Audio", "Embedding"]

# e.g. "8b", "405b", "8x7b", "0.5b", "270m" — size/param badges on model cards
SIZE_TAG_RE = re.compile(r"^\d+(\.\d+)?(x\d+)?[bm]$", re.IGNORECASE)

# tail of a library card's text, e.g. "117.1M Pulls 93 Tags Updated 1 year ago"
PULLS_TAGS_RE = re.compile(
    r"([\d.,]+\s*[KM]?)\s*Pulls\s*(\d+)\s*Tags?\s*Updated\s*(.+)$", re.IGNORECASE
)
SIZE_RE = re.compile(r"([\d.]+)\s*(GB|MB)\b", re.IGNORECASE)
CONTEXT_RE = re.compile(r"(\d+)K\s*context", re.IGNORECASE)
DIGEST_RE = re.compile(r"\b([0-9a-f]{12})\b")
AGO_RE = re.compile(r"(\d+\s+(?:year|month|week|day|hour|minute)s?\s+ago|now)", re.IGNORECASE)


class ScrapeError(Exception):
    pass


def _parse_count(text: str) -> int:
    """'117.1M' -> 117100000, '43.2K' -> 43200, '3,783' -> 3783"""
    text = text.strip().replace(",", "")
    mult = 1
    if text[-1:].upper() == "M":
        mult, text = 1_000_000, text[:-1]
    elif text[-1:].upper() == "K":
        mult, text = 1_000, text[:-1]
    try:
        return int(float(text) * mult)
    except ValueError:
        return 0


def _parse_size_bytes(text: str) -> int | None:
    m = SIZE_RE.search(text)
    if not m:
        return None
    value, unit = float(m.group(1)), m.group(2).upper()
    return int(value * (1024**3 if unit == "GB" else 1024**2))


def _fetch_soup(url: str) -> BeautifulSoup:
    try:
        resp = httpx.get(url, headers={"User-Agent": USER_AGENT}, timeout=15, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        raise ScrapeError(f"Failed to fetch {url}: {e}") from e
    return BeautifulSoup(resp.text, "html.parser")


def fetch_library_index() -> list[dict]:
    """Scrape the /library page for every base model listed there."""
    soup = _fetch_soup(LIBRARY_URL)
    results: list[dict] = []
    seen: set[str] = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not isinstance(href, str) or not href.startswith("/library/"):
            continue
        name = href.removeprefix("/library/")
        if ":" in name or "/" in name or not name or name in seen:
            continue  # skip tag-specific links, nested paths, dupes

        text = a.get_text(separator=" ", strip=True)
        m = PULLS_TAGS_RE.search(text)
        if not m:
            continue  # this /library/xxx link isn't a full model card

        pulls_text, tag_count_text, updated_text = m.groups()
        before = text[: m.start()].strip()
        tokens = before.split()
        if not tokens or tokens[0] != name:
            continue

        capabilities = [t for t in tokens[1:] if t.lower() in CAPABILITY_WORDS]
        description = " ".join(
            t
            for t in tokens[1:]
            if t.lower() not in CAPABILITY_WORDS and not SIZE_TAG_RE.match(t.strip(",."))
        )

        seen.add(name)
        results.append(
            {
                "name": name,
                "description": description,
                "capabilities": ",".join(capabilities),
                "pulls": _parse_count(pulls_text),
                "tag_count": int(tag_count_text),
                "updated_text": updated_text.strip(),
            }
        )

    if not results:
        raise ScrapeError("No models parsed from /library — page layout may have changed")
    return results


def fetch_model_tags(model_name: str) -> list[dict]:
    """Scrape /library/<model>/tags for every pullable variant."""
    soup = _fetch_soup(f"{BASE_URL}/library/{model_name}/tags")
    results: list[dict] = []
    seen: set[str] = set()
    prefix = f"/library/{model_name}:"

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not isinstance(href, str) or not href.startswith(prefix):
            continue
        full_name = href.removeprefix("/library/")
        if full_name in seen:
            continue

        text = a.get_text(separator=" ", strip=True)
        digest_m = DIGEST_RE.search(text)
        context_m = CONTEXT_RE.search(text)
        ago_m = AGO_RE.search(text)
        input_type = next((t for t in INPUT_TYPES if t in text), None)

        tag = full_name.split(":", 1)[1]
        is_default = tag == "latest" or bool(re.search(r"\blatest\b", text))

        seen.add(full_name)
        results.append(
            {
                "full_name": full_name,
                "model_name": model_name,
                "tag": tag,
                "size_bytes": _parse_size_bytes(text),
                "context_length": int(context_m.group(1)) * 1000 if context_m else None,
                "input_type": input_type,
                "digest": digest_m.group(1) if digest_m else None,
                "is_default": int(is_default),
                "updated_text": ago_m.group(1) if ago_m else None,
            }
        )

    return results
