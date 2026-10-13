"""CLI shell. Lean analysis and refactoring are not implemented."""

import argparse
import json
import sys
from collections.abc import Sequence
from importlib.metadata import version


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="beautiproof",
        description="BeutiProof development scaffold. Analysis is not implemented.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {version('beutiproof')}")
    commands = parser.add_subparsers(dest="command")
    for command, description in (
        ("check", "Reserved project analysis command."),
        ("suggest", "Reserved refactoring command."),
    ):
        subparser = commands.add_parser(command, help=description)
        subparser.add_argument("project", help="Project root. No analysis runs in this scaffold.")
        subparser.add_argument("--format", choices=("text", "json"), default="text")
        subparser.add_argument("--file", help="Reserved project-relative file selector.")
        subparser.add_argument("--theorem", help="Reserved theorem selector.")
        if command == "suggest":
            subparser.add_argument("--provider", help="Reserved provider name. No provider runs.")
    arguments = parser.parse_args(argv)
    if arguments.command is None:
        parser.print_help()
        return 2
    operation = "Project analysis" if arguments.command == "check" else "Refactoring"
    message = f"{operation} is not implemented in this scaffold."
    if arguments.format == "json":
        print(
            json.dumps(
                {
                    "schema_version": "0.1.0",
                    "status": "unsupported",
                    "stage": "scaffold",
                    "analysis_available": False,
                    "error": {"code": "not_implemented", "message": message},
                }
            )
        )
    else:
        print(message, file=sys.stderr)
    return 2
