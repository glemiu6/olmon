import sys

from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn

from olmon.db import get_connection, get_stat, now_iso, upsert_model, upsert_tag
from olmon.display import console, format_size, print_error
from olmon.scraper import ScrapeError, fetch_library_index, fetch_model_tags


def db_update_command(index_only: bool = False) -> None:
    console.print("[bold]Fetching the model index from ollama.com/library...[/bold]")

    try:
        models = fetch_library_index()
    except ScrapeError as e:
        print_error(str(e))
        sys.exit(1)

    conn = get_connection()
    scraped_at = now_iso()

    for model in models:
        model["scraped_at"] = scraped_at
        upsert_model(conn, model)
    conn.commit()

    if index_only:
        conn.close()
        console.print(f"[bold green]✓[/bold green]Cached {len(models)} models (index only)")
        console.print("[dim]Run without --index-only to also fetch per-tag size[/dim]")
        sys.exit(0)

    failures = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scraping tags...", total=len(models))
        for model in models:
            progress.update(task, description=f"Scraping {model['name']}")
            try:
                tags = fetch_model_tags(model["name"])
                for tag in tags:
                    tag["scraped_at"] = scraped_at
                    upsert_tag(conn, tag)
                conn.commit()
            except ScrapeError:
                failures += 1
                print_error(f"Failed to fetch tags for {model['name']}")
            progress.advance(task)
    conn.close()
    console.print(f"[bold green]✓[/bold green] Cached {len(models)} models")
    if failures:
        console.print(f"[yellow]![/yellow] Could not fetch tags for {failures} model(s)")
    sys.exit(0)


def db_stats_command() -> None:
    conn = get_connection()
    stats = get_stat(conn)
    conn.close()

    console.print("[bold]olmon model database[/bold]")
    console.print(f"  Path         {stats['db_path']}")
    console.print(f"  Models       {stats['model_count']}")
    console.print(f"  Tags cached  {stats['tag_count']}")
    console.print(f"  Last update  {stats['last_scrape'] or 'never — run: olmon db update'}")
    console.print(f"  DB size      {format_size(stats['db_size'])}")
    sys.exit(0)
