#!/usr/bin/env python3
# olmon/main.py
import argparse
import sys

from olmon import __version__
from olmon.commands.models import models_command
from olmon.commands.ps import ps_command
from olmon.commands.status import status_command
from olmon.commands.watch import watch_command


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="olmon",
        description="A lightweight CLI to monitor Ollama models and usage",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
        Examples:
        $ olmon status
        $ olmon models --sort size
        $ olmon ps
        $ olmon watch --interval 3
        $ olmon inspect llama3:latest
        """,
    )
    parser.add_argument("--version",action="version",version=f"{__version__}")
    parser.add_argument(
        "--host","-H",
        default=None,
        metavar="<url>",
        help="Ollama API URL (overrides config)"
    )

    subparsers = parser.add_subparsers(title="Commands",dest="command",metavar="<command>")

    #status
    subparsers.add_parser("status",help="Show Ollama status")

    #models
    models_parser = subparsers.add_parser("models",help="List installed models")
    models_parser.add_argument("--sort",'-s',default=None,metavar="<field>",
                               help="Sort by: name, size, date")
    models_parser.add_argument("--filter","-f",default=None,metavar="<query>",
                               help="Filter by name or family")

    # inspect
    inspect_parser = subparsers.add_parser("inspect",help="Show details of a model")
    inspect_parser.add_argument("name",metavar="<name>",help="Model name")

    #ps
    subparsers.add_parser("ps",help="Show running models")

    #watch
    watch_parser = subparsers.add_parser("watch",help="Live dashboard")
    watch_parser.add_argument("--interval",'-i',default=None,type=int,metavar="<seconds>",
                              help="Refresh rate in seconds")

    return parser.parse_args(argv)


def app():

    args = parse_args()
    if args.command == "status":
        status_command(args.host)
    elif args.command == "models":
        models_command(args.host,args.sort,args.filter)
    elif args.command == "ps":
        ps_command(args.host)
    elif args.command == "watch":
        watch_command(args.host,args.interval)
    else:
        parse_args(["--help"])
        sys.exit(0)


if __name__ == "__main__":
    app()