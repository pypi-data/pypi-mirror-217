#!/usr/bin/env python3
# https://stackoverflow.com/questions/40002373/qscintilla-based-text-editor-in-pyqt5-with-clickable-functions-and-variables

from pathlib import Path

from PyQt6 import Qsci, QtCore, QtGui
from PyQt6.QtGui import QImage, QPainter


class MEditor(Qsci.QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)

        font = QtGui.QFont()
        font.setFamily("Source Code Pro Semibold")
        if font.exactMatch():
            print("Font set successfully")
        else:
            print("Font not found, using closest match", font.family())
        font.setFixedPitch(True)
        font.setPointSize(20)
        self.setFont(font)
        self.setMarginsFont(font)
        # self.zoomIn()
        # self.zoomOut()

        # Margin 0 is used for line numbers
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.boundingRect("000").width() + 6)
        # self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QtGui.QColor("#eee8d5"))
        self.setMarginsForegroundColor(QtGui.QColor("#93a1a1"))
        # self.setMarginBackgroundColor(1, QtGui.QColor("lightgray"))

        # self._marker = None
        # Clickable margin 1 for showing markers
        # self.setMarginSensitivity(1, True)
        # self.connect(self,
        #    SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
        #    self.on_margin_clicked)
        # self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        # self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)

        self.setBraceMatching(self.BraceMatch.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#eee8d5"))

        self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, "Courier".encode())

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # self.setWrapMode(self.WrapMode.WrapWord)
        self.setWrapMode(self.WrapMode.WrapNone)
        self.setEolMode(self.EolMode.EolUnix)
        self.setEolVisibility(False)
        self.setWhitespaceVisibility(self.WhitespaceVisibility.WsVisible)

        # self.image = QImage("logo_mk.png")
        # painter = QPainter()
        # painter.begin(self.image)
        # painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        # painter.fillRect(self.image.rect(), QtGui.QColor(0, 0, 0, 100))
        # painter.end()

    # def paintEvent(self, e):
    # painter = QPainter()
    # painter.begin(self.viewport())
    # painter.drawImage(QtCore.QPoint(0, 0), self.image)
    # painter.end()
    # super().paintEvent(e)

    def openFile(self, path):
        suffix = path.suffix.lower().strip("~")
        lexer = (
            Qsci.QsciLexerMarkdown()
            if suffix in {".md", ".markdown"}
            else Qsci.QsciLexerYAML()
            if suffix in {".yaml", ".yml"}
            else Qsci.QsciLexerBash()
            if suffix in {".sh"}
            else Qsci.QsciLexerPython()
            if suffix in {".py"}
            else Qsci.QsciLexerXML()
            if suffix in {".xml", ".svg"}
            else None
        )
        if lexer:
            lexer.setFont(self.font())
            # lexer.setPaper(QtGui.QColor("#073642"))
            # lexer.setDefaultPaper(QtGui.QColor("#073642"))
            lexer.setPaper(QtGui.QColor("#fdf6e3"))
            lexer.setDefaultPaper(QtGui.QColor("#fdf6e3"))

        self.setLexer(lexer)

        with open(path) as textFile:
            self.setText(textFile.read())

    def view_state(self):
        # In Qt5/PyQt5 how do I restore exact visible area and cursor
        #  position of QTextEdit?:
        # https://stackoverflow.com/questions/67751888

        # relative approach
        # try:
        # hPos = hBar.value() / hBar.maximum()
        # except ZeroDivisionError:
        # hPos = 0
        # try:
        # vPos = vBar.value() / vBar.maximum()
        # except ZeroDivisionError:
        # vPos = 0

        state = {
            "cursor_position": self.getCursorPosition(),
            "zoom": 0,  # TODO: how to get?
            "hbar_pos": self.horizontalScrollBar().value(),
            "vbar_pos": self.verticalScrollBar().value(),
        }
        return state

    def set_view_state(self, state):
        if not state:
            return
        self.setCursorPosition(*state["cursor_position"])
        # hBar.setValue(hPos * hBar.maximum())  # relative approach
        # vBar.setValue(vPos * vBar.maximum())
        self.horizontalScrollBar().setValue(state["hbar_pos"])
        self.verticalScrollBar().setValue(state["vbar_pos"])
