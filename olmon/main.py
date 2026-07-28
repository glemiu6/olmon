#!/usr/bin/env python3
# olmon/main.py
import argparse
import sys

from olmon import __version__
from olmon.commands.compare import compare_command
from olmon.commands.db import db_stats_command, db_update_command
from olmon.commands.fit import fit_command
from olmon.commands.init import init_config
from olmon.commands.models import inspect_command, models_command
from olmon.commands.ps import ps_command, stop_command
from olmon.commands.recommend import recommend_command
from olmon.commands.search import search_command
from olmon.commands.status import status_command
from olmon.commands.top import top_command
from olmon.commands.uninstall import uninstall
from olmon.commands.update import check_for_update, update
from olmon.commands.watch import watch_command
from olmon.config import OlmonConfig


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="olmon",
        description="A lightweight CLI to monitor Ollama models and usage",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
        Examples:
        $ olmon init
        $ olmon uninstall
        $ olmon update
        $ olmon status
        $ olmon models --sort size
        $ olmon ps
        $ olmon watch --interval 3
        $ olmon inspect llama3:latest
        """,
    )
    parser.add_argument("--version", action="version", version=f"{__version__}")
    parser.add_argument(
        "--host", "-H", default=None, metavar="<url>", help="Ollama API URL (overrides config)"
    )
    parser.add_argument(
        "--no-color", action="store_true", default=False, help="Disable color output for piping"
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command", metavar="<command>")
    subparsers.add_parser("init", help="Create default config file")
    subparsers.add_parser("uninstall", help="Uninstall olmon")
    subparsers.add_parser("update", help="Update olmon to the latest version")
    # status
    subparsers.add_parser("status", help="Show Ollama status")

    # models
    models_parser = subparsers.add_parser("models", help="List installed models")
    models_parser.add_argument(
        "--sort", "-s", default=None, metavar="<field>", help="Sort by: name, size, date"
    )
    models_parser.add_argument(
        "--filter", "-f", default=None, metavar="<query>", help="Filter by name or family"
    )
    models_parser.add_argument("--json", action="store_true", default=False, help="Output as JSON")

    # inspect
    inspect_parser = subparsers.add_parser("inspect", help="Show details of a model")
    inspect_parser.add_argument("name", metavar="<name>", help="Model name")

    # ps
    subparsers.add_parser("ps", help="Show running models")

    # watch
    watch_parser = subparsers.add_parser("watch", help="Live dashboard")
    watch_parser.add_argument(
        "--interval",
        "-i",
        default=None,
        type=int,
        metavar="<seconds>",
        help="Refresh rate in seconds",
    )

    # stop
    stop_parser = subparsers.add_parser("stop", help="Unload model from VRAM")
    stop_parser.add_argument(
        "model",
        metavar="<model>",
        help="Model name",
    )

    # compare
    compare_parser = subparsers.add_parser("compare", help="Compare models side by side")
    compare_parser.add_argument(
        "models",
        nargs="+",  # one or more values
        metavar="<model>",
        help="Models to compare (e.g. qwen2.5:7b llama3.2:latest gemma4:latest)",
    )

    # top
    top_parser = subparsers.add_parser("top", help="htop-style live view of running models")
    top_parser.add_argument(
        "--interval", "-i", default=None, type=int, help="Refresh rate in seconds"
    )  # noqa: E501

    # db
    db_parser = subparsers.add_parser("db", help="Database commands")
    db_subparsers = db_parser.add_subparsers(
        title="Database commands", dest="db_command", metavar="< db-command>"
    )
    db_subparser_update = db_subparsers.add_parser(
        "update", help="Scrape ollama.com and refresh the local model cache"
    )
    db_subparser_update.add_argument(
        "--index-only",
        action="store_true",
        help="Only update the index, skip models",
        default=False,
    )
    db_subparsers.add_parser("stats", help="Show how many models/tags are cached")

    # fit
    fit_parser = subparsers.add_parser("fit", help="Checks if a models fits in VRAM")
    fit_parser.add_argument("model", metavar="<model>", help="Model name (e.g. llama3.2:3b)")

    # recommend
    recommend_parser = subparsers.add_parser(
        "recommend", help="Show the best models to fit in VRAM"
    )
    recommend_parser.add_argument("--vram", default=None, metavar="<size>", help="e.g. --vram 8GB")

    # search
    search_parser = subparsers.add_parser(
        "search", help="Search cached models by name or description"
    )
    search_parser.add_argument("query", metavar="<query>", help="Search term, e.g. vision")
    search_parser.add_argument(
        "--limit", "-l", default=None, type=int, metavar="<n>", help="Max results (default: 20)"
    )
    return parser.parse_args(argv)


def app():

    args = parse_args()
    config = OlmonConfig.load()

    if args.no_color or config.no_color:
        from rich.console import Console

        import olmon.display as display

        display.console = Console(no_color=True)

    check_for_update()

    match args.command:
        case "status":
            status_command(args.host)
        case "models":
            models_command(args.host, args.sort, args.filter)
        case "inspect":
            inspect_command(args.host, args.name)
        case "ps":
            ps_command(args.host)
        case "watch":
            watch_command(args.host, args.interval)
        case "init":
            init_config()
        case "uninstall":
            uninstall()
        case "update":
            update()
        case "stop":
            stop_command(args.host, args.model)

        case "compare":
            compare_command(args.host, args.models)
        case "top":
            top_command(args.host, args.interval)
        case "fit":
            fit_command(args.host, args.model)
        case "recommend":
            recommend_command(args.vram)
        case "search":
            search_command(args.query, args.limit)
        case "db":
            match args.db_command:
                case "update":
                    db_update_command(args.index_only)
                case "stats":
                    db_stats_command()
                case _:
                    parse_args(["db", "--help"])
                    sys.exit(0)

        case _:
            parse_args(["--help"])
            sys.exit(0)


if __name__ == "__main__":
    app()
