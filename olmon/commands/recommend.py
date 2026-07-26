import re
import sys

from olmon.db import find_tags_under_size, get_connection
from olmon.display import print_error, print_recommend

VRAM_ARG_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*(GB|MB|G|M)?$", re.IGNORECASE)


def _parse_size(text: str) -> int | None:
    """'8GB' -> bytes, '8192MB' -> bytes, '8' -> treated as GB"""
    m = VRAM_ARG_RE.match(text.strip())
    if not m:
        return None
    value = float(m.group(1))
    unit = (m.group(2) or "GB").upper()
    return int(value * (1024**3 if unit.startswith("G") else 1024**2))


def recommend_command(vram_arg: str | None = None) -> None:
    if not vram_arg:
        print_error("Please specify --vram, e.g. olmon recommend --vram 8GB")
        sys.exit(2)

    max_bytes = _parse_size(vram_arg)
    if max_bytes is None:
        print_error(f"Could not parse --vram value '{vram_arg}' (try e.g. --vram 8GB)")
        sys.exit(2)

    conn = get_connection()
    tags = find_tags_under_size(conn, max_bytes)
    conn.close()

    if not tags:
        print_error("No cached models fit that size — try: olmon db update")
        sys.exit(1)

    print_recommend(tags, max_bytes)
    sys.exit(0)
