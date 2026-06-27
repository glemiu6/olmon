#!/usr/bin/env python3
# olmon/main.py
import argparse
import sys

from olmon import __version__
from olmon.commands.init import init_config
from olmon.commands.models import inspect_command, models_command
from olmon.commands.ps import ps_command, stop_command
from olmon.commands.status import status_command
from olmon.commands.uninstall import uninstall
from olmon.commands.update import check_for_update, update
from olmon.commands.watch import watch_command


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
    models_parser.add_argument(
        "--json",action="store_true", default=False, help="Output as JSON"
    )

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

    #stop
    stop_parser = subparsers.add_parser("stop", help="Unload model from VRAM")
    stop_parser.add_argument(
        "model",
        metavar="<model>",
        help="Model name",
    )

    return parser.parse_args(argv)


def app():

    args = parse_args()
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
            stop_command(args.host,args.model)
        case _:
            parse_args(["--help"])
            sys.exit(0)


if __name__ == "__main__":
    app()
