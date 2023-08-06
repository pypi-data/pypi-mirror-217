#!/usr/bin/env python3

"""Stuff that doesn't go anywhere else
"""

import asyncio
import logging
import os
import time
from collections.abc import AsyncIterator, Callable, Coroutine, Iterator
from functools import wraps
from pathlib import Path
from typing import NoReturn, cast

from asyncinotify import Event, Inotify, Mask


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("medit.misc")


def watchdog(
    afunc: Callable[..., Coroutine[object, object, object]]
) -> Callable[..., Coroutine[object, object, object]]:
    """Watch for async functions to throw an unhandled exception"""

    @wraps(afunc)
    async def run(*args: object, **kwargs: object) -> object:
        """Run wrapped function and handle exceptions"""
        try:
            return await afunc(*args, **kwargs)
        except asyncio.CancelledError:
            log().info("Task cancelled: `%s`", afunc.__name__)
        except KeyboardInterrupt:
            log().info("KeyboardInterrupt in `%s`", afunc.__name__)
        except Exception:  # pylint: disable=broad-except
            log().exception("Exception in `%s`:", afunc.__name__)
            asyncio.get_event_loop().stop()
        return None

    return run


def impatient(func):
    @wraps(func)
    def run(*args: object, **kwargs: object) -> object:
        try:
            t1 = time.time()
            return func(*args, **kwargs)
        finally:
            if (duration := time.time() - t1) > 0.1:
                log().warn("%s took %.2fs!", func.__name__, duration)

    return run


async def fs_changes(
    *paths: Path,
    queue: asyncio.Queue[str] = asyncio.Queue(),
    mask: Mask = Mask.CLOSE_WRITE
    | Mask.MOVED_TO
    | Mask.CREATE
    | Mask.MODIFY
    | Mask.MOVE
    | Mask.DELETE
    | Mask.MOVE_SELF,
    postpone: bool = False,
    timeout: float = 2,
) -> AsyncIterator[Path]:
    """Controllable, timed filesystem watcher"""

    # pylint: disable=too-many-locals

    async def fuse_fn(queue: asyncio.Queue[str], timeout: float) -> None:
        await asyncio.sleep(timeout)
        await queue.put("timeout")

    def expand_paths(path: Path, recursive: bool = True) -> Iterator[Path]:
        yield path
        if path.is_dir() and recursive:
            for file_or_directory in path.rglob("*"):
                if file_or_directory.is_dir():
                    yield file_or_directory

    def task(name: str) -> asyncio.Task[str | Event]:
        """Creates a task from a name identifying a data source to read from"""
        return asyncio.create_task(
            cast(asyncio.Queue[str] | Inotify, {"inotify": inotify, "mqueue": queue}[name]).get(),
            name=name,
        )

    with Inotify() as inotify:
        for path in set(sub_path.absolute() for p in paths for sub_path in expand_paths(Path(p))):
            log().debug("add fs watch for %s", path)
            inotify.add_watch(path, mask)
        fuse = None
        changed_files = set()
        tasks = set(map(task, ("inotify", "mqueue")))

        while True:
            done, tasks = await asyncio.wait(
                fs=tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for event in done:
                event_type, event_value = event.get_name(), event.result()
                tasks.add(task(event_type))
                if event_type == "inotify":
                    assert isinstance(event_value, Event)
                    if event_value.path:
                        changed_files.add(event_value.path)
                    if postpone and fuse:
                        fuse.cancel()
                        del fuse
                        fuse = None
                    if not fuse:
                        fuse = asyncio.create_task(fuse_fn(queue, timeout))
                elif event_type == "mqueue":
                    if event_value == "timeout":
                        del fuse
                        fuse = None
                        for file in changed_files:
                            yield file
                        changed_files.clear()


def setup_logging(level: str | int = logging.DEBUG) -> None:
    '''
    def thread_id_filter(record):
        """Inject thread_id to log records"""
        record.thread_id = threading.get_native_id()
        return record

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(thread_id)s | %(message)s")
    )
    handler.addFilter(thread_id_filter)
    logger().addHandler(handler)
    logging.getLogger().setLevel(level)
    '''
    use_col = "TERM" in os.environ
    col_terminator = "\033[0m" if use_col else ""
    logging.basicConfig(
        format=f"%(levelname)s %(asctime)s.%(msecs)03d %(name)-12s│ %(message)s{col_terminator}",
        datefmt="%H:%M:%S",
        level=getattr(logging, level) if isinstance(level, str) else level,
    )
    for name, color in (
        ("DEBUG", "\033[32m"),
        ("INFO", "\033[36m"),
        ("WARNING", "\033[33m"),
        ("ERROR", "\033[31m"),
        ("CRITICAL", "\033[37m"),
    ):
        logging.addLevelName(
            getattr(logging, name),
            f"{color if use_col else ''}({name[0] * 2})",
        )


def throw(exc: Exception) -> NoReturn:
    """Make raising an exception functional"""
    raise exc
