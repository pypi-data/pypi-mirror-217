#!/usr/bin/env python3

"""QrM - Connect to reMarkable and modify contents
"""

# pylint: disable=invalid-name

import asyncio
import json
import logging
import os
import signal
import sys
from contextlib import suppress
from pathlib import Path

import qdarktheme
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWebEngineWidgets import QWebEngineView

from medit.utils import fs_changes, impatient, setup_logging, watchdog

CFG_FILE = "~/.medit.cfg"


def log() -> logging.Logger:
    """Returns the local logger"""
    return logging.getLogger("medit.ui")


def load_default(filename, default):
    with suppress(FileNotFoundError, json.JSONDecodeError):
        return json.load(open(os.path.expanduser(filename)))
    return default


class MEditWindow(QtWidgets.QMainWindow):
    """The one and only application window"""

    @impatient
    def __init__(self, path: Path | None) -> None:
        super().__init__()
        uic.loadUi(Path(__file__).parent / "medit.ui", self)
        # self.setStyleSheet(styleSheet)
        # self.setStyleSheet("background-color: yellow;")

        # css =  open(Path(__file__).parent / "github-markdown-light.css").read()
        # print(css)
        # self.wv_rendered.setStyleSheet(css)
        # self.setAcceptDrops(True)
        # self.config = qrm_common.load_json(qrm_common.CFG_FILE)

        # https://stackoverflow.com/questions/66066115/render-markdown-with-pyqt5

        config = load_default(CFG_FILE, {})

        self.autosave_timer = QtCore.QTimer(self)
        self.autosave_timer.timeout.connect(self.on_autosave_timer_timeout)

        self.setGeometry(*config.get("window_geometry", (50, 50, 1000, 500)))
        self.base_dir = (
            path
            and (path if path.is_dir else path.parent)
            or Path(config.get("base_dir") or ".").absolute()
        )
        self.autoload_thread = QtCore.QThread(self)
        self.autoload_thread.run = lambda: self.async_stuff()
        self.autoload_thread.start()

        # self.fs_watcher = QtCore.QFileSystemWatcher([self.base_dir.as_posix()])
        # self.fs_watcher.fileChanged.connect(self.on_file_changed_externally)
        # self.fs_watcher.directoryChanged.connect(self.on_file_changed_externally)
        # self.fs_watcher.addPaths([self.base_dir.as_posix()])
        # print(self.fs_watcher.files())

        self.fs_model = QtGui.QFileSystemModel()
        self.fs_model.setRootPath(Path.home().as_posix())

        self.open_file = None

        self.set_open_file(path if path and path.is_file() else config.get("open_file"))

        self.gb_splitter.setSizes(config.get("split_sizes", [1, 1, 1]))

        self.tv_files.setModel(self.fs_model)

        self.tv_files.selectionModel().selectionChanged.connect(self.on_tv_files_selectionChanged)

        self.tv_files.hideColumn(1)
        self.tv_files.hideColumn(2)
        self.tv_files.hideColumn(3)
        self.tv_files.setHeaderHidden(True)

        self.tv_files.setRootIndex(self.fs_model.index(self.base_dir.as_posix()))
        self.tv_files.expand(self.fs_model.index(self.base_dir.as_posix()))
        if self.open_file:
            self.tv_files.setCurrentIndex(self.fs_model.index(self.open_file.absolute().as_posix()))
        else:
            self.tv_files.setCurrentIndex(self.fs_model.index(self.base_dir.absolute().as_posix()))

        self.show()

    def async_stuff(self):
        print("Async")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # terminator = threading.Event()

        # https://stackoverflow.com/a/71956673
        _tasks = {asyncio.ensure_future(self.watch_fs_changes())}
        loop.run_forever()

    @watchdog
    async def watch_fs_changes(self) -> None:
        """Observe changes to filesystem and mark walls dirty"""
        async for changed_path in fs_changes(self.base_dir, timeout=1, postpone=True):
            log().info("file %s changed", changed_path)
            QtCore.QMetaObject.invokeMethod(
                self,
                "on_file_changed_externally",
                QtCore.Qt.ConnectionType.QueuedConnection,
                QtCore.Q_ARG(str, changed_path.as_posix()),
            )

    def reset_timer(self):
        logging.debug("reset modification timer")
        self.autosave_timer.start(300)

    @impatient
    def render_content(self):
        self.wv_rendered.show(
            self.txt_editor.text(), self.open_file and self.open_file.suffix.strip("~")
        )

    @impatient
    def on_autosave_timer_timeout(self):
        """"""
        self.autosave_timer.stop()
        self.render_content()
        self.save()

    @impatient
    def save(self):
        # if not self.dirty:
        # return
        log().info("save to %s", self.open_file)
        # self.dirty = True
        text_to_save = self.txt_editor.text()
        if not text_to_save:
            log().warning("I don't dare to overwrite with empty content..")
            return
        open(self.open_file, "w").write(text_to_save)

    @impatient
    def set_open_file(self, path):
        self.open_file = None
        block_state = self.txt_editor.blockSignals(True)
        selected_file = Path(path) if path else None
        if not path:
            return
        try:
            self.txt_editor.openFile(selected_file)
            self.open_file = selected_file
        except UnicodeDecodeError:
            self.txt_editor.setText("")
        finally:
            self.txt_editor.blockSignals(block_state)
            self.setWindowTitle(str(self.open_file))
            QtWidgets.QApplication.instance().setApplicationName(f"medit - {self.open_file.name}")

        self.render_content()

    @impatient
    def on_tv_files_selectionChanged(self, selection1, selection2) -> None:
        # print(Path(self.fs_model.filePath(selection.indexes()[0])))
        try:
            selected_path = Path(self.fs_model.filePath(selection1.indexes()[0]))
            if selected_path.is_file():
                self.set_open_file(selected_path)
        except IndexError:
            print("FILE REMOVED?")

    def on_txt_editor_textChanged(self) -> None:
        self.reset_timer()

    @impatient
    @QtCore.pyqtSlot(str)
    def on_file_changed_externally(self, file) -> None:
        print(file)

    @impatient
    def event(self, event: QtCore.QEvent) -> bool:
        # if event.type() == QtCore.QEvent.DragEnter:
        # if any(
        # Path(u.url()).suffix.lower() in {".pdf", ".epub"} for u in event.mimeData().urls()
        # ):
        # event.accept()
        # elif event.type() == QtCore.QEvent.Drop:
        # urls = [
        # path
        # for u in event.mimeData().urls()
        # if (path := Path(u.url())).suffix.lower() in {".pdf", ".epub"}
        # ]
        # print(urls)

        # elif not event.type() in {
        # QtCore.QEvent.UpdateRequest,
        # QtCore.QEvent.Paint,
        # QtCore.QEvent.Enter,
        # QtCore.QEvent.HoverEnter,
        # QtCore.QEvent.HoverMove,
        # QtCore.QEvent.HoverLeave,
        # QtCore.QEvent.KeyPress,
        # QtCore.QEvent.KeyRelease,
        # QtCore.QEvent.DragMove,
        # QtCore.QEvent.DragLeave,
        # }:
        ## log().warn("unknown event: %r %r", event.type(), event)
        # pass
        return super().event(event)

    @impatient
    def closeEvent(self, _event: QtGui.QCloseEvent) -> None:
        """save state before shutting down"""
        logging.info("got some closish signal, bye")
        # self.autoload_thread.terminate()
        # self.autoload_thread.wait()
        # self.save()
        g = self.geometry()
        # splitter =
        json.dump(
            {
                "window_geometry": (g.x(), g.y(), g.width(), g.height()),
                "editor_view_state": self.txt_editor.view_state(),
                "open_file": self.open_file and self.open_file.as_posix(),
                "base_dir": self.base_dir and self.base_dir.as_posix(),
                "split_sizes": self.gb_splitter.sizes(),
            },
            open(os.path.expanduser(CFG_FILE), "w"),
        )


def main(path: Path) -> None:
    """Typical PyQt5 boilerplate main entry point"""

    setup_logging()
    app = QtWidgets.QApplication(sys.argv)

    qdarktheme.setup_theme("light")

    window = MEditWindow(path)

    for s in (signal.SIGABRT, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
        signal.signal(s, lambda signal, frame: window.close())

    # catch the interpreter every now and then to be able to catch signals
    timer = QtCore.QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
