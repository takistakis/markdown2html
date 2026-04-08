#!/usr/bin/env python3

# Copyright 2016 Panagiotis Ktistakis <panktist@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Convert a GitHub Flavored Markdown file to HTML."""

from __future__ import annotations

import argparse
import logging
import sys
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

import markdown

try:
    import pymdownx  # noqa: F401

    _HAS_PYMDOWNX = True
except ImportError:
    _HAS_PYMDOWNX = False

CSS_URL = (
    "https://raw.githubusercontent.com/sindresorhus/"
    "github-markdown-css/gh-pages/github-markdown.css"
)
CSS_CACHE_PATH = Path("~/.cache/github-markdown.css").expanduser()
REQUEST_TIMEOUT = 10

# Extensions and their configs are fixed at import time based on what's available.
if _HAS_PYMDOWNX:
    _EXTENSIONS = [
        "markdown.extensions.codehilite",
        "markdown.extensions.sane_lists",
        "markdown.extensions.tables",
        "pymdownx.extra",
        "pymdownx.highlight",
        "pymdownx.magiclink",
        "pymdownx.tasklist",
        "pymdownx.tilde",
    ]
    _EXTENSION_CONFIGS: dict = {
        "pymdownx.highlight": {
            "guess_lang": False,
            "noclasses": True,
            "pygments_style": "tango",
        },
    }
else:
    _EXTENSIONS = [
        "markdown.extensions.codehilite",
        "markdown.extensions.fenced_code",
        "markdown.extensions.sane_lists",
        "markdown.extensions.tables",
    ]
    _EXTENSION_CONFIGS = {
        "markdown.extensions.codehilite": {
            "noclasses": True,
            "pygments_style": "tango",
        },
    }

TEMPLATE = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    {refresh}
    <title>{title}</title>
    <link rel="stylesheet" href="{csspath}">
    <style>
      .markdown-body {{
        border: 1px solid #ddd;
        border-radius: 3px;
        max-width: 888px;
        margin: 64px auto 51px;
        padding: 45px;
      }}
    </style>
  </head>
  <body>
    <article class="markdown-body">
      {body}
    </article>
  </body>
</html>
"""


def download_css(path: Path) -> None:
    """Get latest github-markdown.css and store it at *path*."""
    try:
        with urllib.request.urlopen(CSS_URL, timeout=REQUEST_TIMEOUT) as r:
            path.write_bytes(r.read())
    except urllib.error.URLError:
        logging.warning("Unable to download CSS file")


def render(text: str, title: str, csspath: Path, interval: int | None) -> str:
    """Convert a Markdown string to an HTML page."""
    body = markdown.markdown(
        text,
        extensions=_EXTENSIONS,
        extension_configs=_EXTENSION_CONFIGS,
    )
    refresh = (
        f'<meta http-equiv="refresh" content="{interval}">'
        if interval is not None
        else ""
    )
    return TEMPLATE.format(refresh=refresh, title=title, csspath=csspath, body=body)


def run(
    mdpath: str,
    out: str | None = None,
    force: bool = False,
    preview: bool = False,
    interval: int | None = None,
) -> None:
    """Generate an HTML file from a Markdown one."""
    src = Path(mdpath)
    if not src.is_file():
        logging.error("No such file: %s", mdpath)
        sys.exit(1)

    htmlpath = Path(out) if out else Path(f"/tmp/{src.stem}.html")

    if force or not CSS_CACHE_PATH.is_file():
        logging.info("Downloading github-markdown.css...")
        download_css(CSS_CACHE_PATH)

    logging.info("Converting %s to HTML...", src.name)
    html = render(
        src.read_text(),
        title=src.name,
        csspath=CSS_CACHE_PATH,
        interval=interval,
    )
    htmlpath.write_text(html)

    if preview:
        logging.info("Opening %s in browser...", htmlpath)
        webbrowser.open(str(htmlpath))


def main() -> None:
    """Parse arguments and run."""
    parser = argparse.ArgumentParser(
        description=(
            "Convert a GitHub Flavored Markdown file to HTML, using markdown, "
            "pygments and the latest github-markdown.css from "
            "https://github.com/sindresorhus/github-markdown-css"
        ),
    )
    parser.add_argument("file", metavar="<file>", help="Markdown file to convert")
    parser.add_argument("-o", "--out", metavar="<file>", help="Write output to <file>")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite existing CSS file",
    )
    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        help="Open generated HTML file in browser",
    )
    parser.add_argument(
        "-i",
        "--interval",
        metavar="<int>",
        type=int,
        help="Refresh page every <int> seconds",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Show less information",
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(message)s",
        level=logging.WARNING if args.quiet else logging.INFO,
    )

    run(args.file, args.out, args.force, args.preview, args.interval)


if __name__ == "__main__":
    main()
