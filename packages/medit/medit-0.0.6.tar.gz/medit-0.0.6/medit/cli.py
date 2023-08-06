#!/usr/bin/env python3

"""Markup Editor
"""

import importlib.metadata
import logging
import shutil
import sys
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections.abc import Sequence
from contextlib import suppress
from pathlib import Path

from medit.ui import main as ui_main
from medit.utils import setup_logging


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Cool git like multi command argument parser"""
    parser = ArgumentParser(__doc__)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--info", action="store_true")

    parser.set_defaults(func=fn_ui)
    parser.add_argument("path", type=Path, nargs="?")

    return parser.parse_args(argv)


def logger() -> logging.Logger:
    """Named logger"""
    return logging.getLogger("medit.cli")


def extract_version() -> str:
    """Returns either the version of installed package or the one
    found in nearby pyproject.toml"""
    with suppress(FileNotFoundError, StopIteration):
        with open(
            Path(__file__).parent.parent / "pyproject.toml", encoding="utf-8"
        ) as pyproject_toml:
            version = (
                next(line for line in pyproject_toml if line.startswith("version"))
                .split("=")[1]
                .strip("'\"\n ")
            )
            return f"{version}-dev"
    return importlib.metadata.version(__name__.split(".", maxsplit=1)[0])


__version__ = extract_version()


def shorten_home(path: Path | str) -> Path:
    """Reverse of expanduser"""
    return Path(Path(path).as_posix().replace(str(Path.home()), "~"))


def fn_info(_args: Args) -> None:
    """Entry point `info`"""
    print(f"Version: {__version__} (at {shorten_home(Path(__file__).parent)})")
    print(
        f"Python: {'.'.join(map(str, sys.version_info[:3]))}"
        f" (at {shorten_home(sys.executable)})"
    )


def fn_ui(args: Args) -> None:
    ui_main(args.path if hasattr(args, "path") else None)


def main() -> int:
    """Entry point for everything else"""
    args = parse_args()
    return fn_info(args) if args.info else fn_ui(args)


if __name__ == "__main__":
    main()
