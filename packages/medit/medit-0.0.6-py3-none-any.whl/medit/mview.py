#!/usr/bin/env python3

from pathlib import Path

import pygments.lexers
from markdown import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MView(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)
        self.css_content_markdown = "".join(
            f"<style>{open(Path(__file__).parent / path).read()}</style>"
            for path in (
                "styles/external/github-markdown-light.css",
                "styles/external/thomasf-solarized-css/solarized-light.css",
                "styles/external/solarized-light-all-sites.css",
                "styles/external/pygments-solarized-style/solarized-light.css",
                # "styles/external/github-markdown-dark.css",
                # "styles/external/thomasf-solarized-css/solarized-dark.css",
                # "styles/external/solarized-dark-all-sites.css",
                # "styles/external/pygments-solarized-style/solarized-dark.css",
            )
        )

        self.css_content = "".join(
            f"<style>{open(Path(__file__).parent / path).read()}</style>"
            for path in ("styles/external/pygments-solarized-style/solarized-light.css",)
        )

        self.css_content_unused = "".join(
            f"<style>{open(Path(__file__).parent / path).read()}</style>"
            for path in (
                #
                # Basic markdown stuff
                #
                # GitHub - html only
                # "styles/external/github-markdown-light.css",
                # "styles/external/github-markdown-dark.css",
                # dark - https://nihaojob.github.io/markdown-css-smartisan/
                # "styles/external/github-markdown.css",
                # html only, fonts not affected `.markdown` class
                # https://cdn.jsdelivr.net/npm/@naokim03/markdown-theme-solarized@1.0.2/
                # "styles/markdown.min.css",
                # https://github.com/alphapapa/solarized-everything-css
                # "styles/external/solarized-light-all-sites.css",
                # "styles/external/solarized-dark-all-sites.css",
                # html only
                # https://github.com/thomasf/solarized-css
                # "styles/solarized-light.css",
                # "styles/solarized-dark.css",  #               | light, transparent, decent
                #
                # Pygments
                #
                # pygments via `pygments-solarized-style`
                # "styles/external/solarized-light.css",  #               | light, transparent, decent
                # "styles/external/solarized-dark.css",  #               | light, transparent, decent
                # pygments defaults
                # "styles/pygments/abap.css",  #               | light, transparent, decent
                # "styles/pygments/algol.css",  #              | light/dark, transparent, bw
                # "styles/pygments/algol_nu.css",  #           | light/dark, transparent, bw
                # "styles/pygments/arduino.css",  #            | light/dark, decent
                # "styles/pygments/autumn.css",  #             | light (dark)
                # "styles/pygments/borland.css",  #            | light
                # "styles/pygments/bw.css",  #                 |
                # "styles/pygments/colorful.css",  #           | light +string
                # "styles/pygments/default.css",  #            |
                # "styles/pygments/dracula.css",  #            | dark
                # "styles/pygments/emacs.css",  #              |
                # "styles/pygments/friendly.css",  #           |
                # "styles/pygments/friendly_grayscale.css",  # |
                # "styles/pygments/fruity.css",  #             | dark
                # "styles/pygments/igor.css",  #               | light (dark)
                # "styles/pygments/inkpot.css",  #             | dark (light) +strings
                # "styles/pygments/lilypond.css",  #           | light dark
                # "styles/pygments/lovelace.css",  #           | light dark
                # "styles/pygments/manni.css",  #              | dark light +nice
                # "styles/pygments/material.css",  #           | dark
                # "styles/pygments/monokai.css",  #            | dark
                # "styles/pygments/murphy.css",  #             |
                # "styles/pygments/native.css",  #             |
                # "styles/pygments/nord.css",  #               |
                # "styles/pygments/pastie.css",  #             |
                # "styles/pygments/perldoc.css",  #            |
                # "styles/pygments/rainbow_dash.css",  #       |
                # "styles/pygments/rrt.css",  #                |
                # "styles/pygments/sas.css",  #                |
                # "styles/pygments/staroffice.css",  #         |
                # "styles/pygments/tango.css",  #              |
                # "styles/pygments/trac.css",  #               | light dark
                # "styles/pygments/vim.css",  #                |
                # "styles/pygments/vs.css",  #                 | light, transparent, decent
                # "styles/pygments/xcode.css",  #              | light, transparent, decent
                # "styles/pygments/zenburn.css",  #            | dark
            )
        )

    def show(self, content, highlight_mode):

        if highlight_mode == ".md":
            html, style = (
                markdown(
                    content,
                    extensions=[
                        "extra",
                        "codehilite",
                        "markdown_checklist.extension",
                    ],
                ),
                self.css_content_markdown,
            )
        else:
            formatter = HtmlFormatter(linenos="table", cssclass="codehilite")
            lexer = (
                pygments.lexers.YamlLexer()
                if highlight_mode in {".yaml", ".yml"}
                else pygments.lexers.BashLexer()
                if highlight_mode in {".sh"}
                else pygments.lexers.PythonLexer()
                if highlight_mode in {".py"}
                else pygments.lexers.XmlLexer()
                if highlight_mode in {".xml", ".svg", ".lbrn2"}
                else pygments.lexers.TexLexer()
            )

            html, style = highlight(content, lexer, formatter), self.css_content

        #        print(html)
        self.setHtml(
            f"""
<!doctype html>
<html lang="en">
  <meta charset="utf-8"><head>{style}</head></meta>
  <body class="markdown-body markdown">{html}</body>
</html>
        """
        )

        return

        filename = Path(__file__).parent / "index.html"

        document = Document()
        download_manager = DownloadManager()

        channel = QWebChannel()
        channel.registerObject("content", document)

        # remote file
        markdown_url = QUrl.fromUserInput(
            "https://raw.githubusercontent.com/eyllanesc/stackoverflow/master/README.md"
        )
        # local file
        # markdown_url = QUrl.fromUserInput(/path/of/markdown.md)

        download_manager.finished.connect(document.set_text)
        download_manager.start_download(markdown_url)

        # view = QWebEngineView()
        self.page().setWebChannel(channel)
        url = QUrl.fromLocalFile(filename)
        view.load(url)
