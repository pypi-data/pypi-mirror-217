import argparse
from importlib import import_module

from ._version import __version__
from .constants import COMMANDS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"cici {__version__}")

    subparsers = parser.add_subparsers(required=True)

    for command_name in COMMANDS:
        command = import_module(f".{command_name}", "cici.cli")
        getattr(command, f"{command_name}_parser")(subparsers=subparsers)

    args = parser.parse_args()
    args.func(parser=parser, args=args)
