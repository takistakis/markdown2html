#!/usr/bin/env python3

# Forked from: Panagiotis Ktistakis <panktist@gmail.com>
# This version maintainer: Thomas Cannon <tcannon.mail@gmail.com>
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

"""
Usage: markdown2html [options]

Convert a GitHub Flavored Markdown file to HTML, using
markdown, pygments and the latest github-markdown.css from
https://github.com/sindresorhus/github-markdown-css

Options:
  --file <file>     Use file <file>
  --file_dir <path> Use directory instead of file <path>
  --out <file>      Write output to <file>
  --force           Overwrite existing CSS file
  --preview         Open generated HTML file in browser
  --interval <int>  Refresh page every <int> seconds
  --nav             Create navigation at beginning of html file
  --quiet           Show less information
  --help            Show this help message and exit
"""

import logging
import os
import re
import sys
import urllib.request
import webbrowser

import markdown

TEMPLATE = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    %s
    <title>%s</title>
    <link rel="stylesheet" href="%s">
    <style>
      .markdown-body {
        border: 1px solid #ddd;
        border-radius: 3px;
        max-width: 888px;
        margin: 64px auto 51px;
        padding: 45px;
      }
    </style>
  </head>
  <body>
    <article class="markdown-body">
      %s
    </article>
  </body>
</html>
"""


def download_css(path):
    """Get latest github-markdown.css and store it at `path`."""
    url = ('https://raw.githubusercontent.com/sindresorhus/'
           'github-markdown-css/gh-pages/github-markdown.css')
    try:
        with urllib.request.urlopen(url) as r, open(path, 'wb') as f:
            f.write(r.read())
    except urllib.error.URLError:
        logging.warning("Unable to download CSS file")


def render(text, title, csspath, interval):
    """Convert a Markdown string to an HTML page.

    The following Markdown extensions are used to support most GFM features:
    codehilite, fenced_code, sane_lists, tables.
    """
    extensions = [
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.sane_lists',
        'markdown.extensions.tables',
    ]

    configs = {
        'markdown.extensions.codehilite': {
            'guess_lang': False,
            'noclasses': True,
            'pygments_style': 'tango',
        },
    }

    try:
        import pymdownx
    except ImportError:
        logging.info("Module pymdownx not found")
    else:
        extensions.remove('markdown.extensions.fenced_code')
        extensions.append('pymdownx.extra')
        extensions.append('pymdownx.magiclink')
        extensions.append('pymdownx.tasklist')

    body = markdown.markdown(text, extensions=extensions,
                             extension_configs=configs)
    # Don't use the line-height style from pygments
    body = body.replace(' style="line-height: 125%"', '')
    refresh = '<meta http-equiv="refresh" content="%s">' % interval
    refresh = refresh if interval is not None else ''
    html = TEMPLATE % (refresh, title, csspath, body)
    return html


def run(file=None, file_dir=None, out=None, force=False, preview=False, interval=None, nav=False):
    """Generate an HTML file from a Markdown one."""
    mdfiles = []
    outfile = []
    
    # Find appropriate files
    if file_dir is not None:
        if not os.path.exists(file_dir):
            logging.error("No such top directory: %s", file_dir)
            sys.exit(1)
        mdfiles = [os.path.join(root, name)
            for root, dirs, files in os.walk(file_dir)
            for name in files
            if name.endswith((".md"))]
        outfile=os.path.dirname(file_dir)
    elif file is not None:
        if not os.path.isfile(file):
            logging.error("No such file: %s", file)
            sys.exit(1)
        mdfiles = [file]
        outfile = out
    else:
        logging.error("Must choose a file or directory path")
        sys.exit(1)

    # CSS
    csspath = os.path.expanduser('~/.cache/github-markdown.css')
    if force or not os.path.isfile(csspath):
        logging.info("Downloading github-markdown.css...")
        download_css(csspath)

    # Navigation
    navigation = []
    if nav:
        navigation = '### Project Links\n'
        for curfile in mdfiles:
            curfilename  = os.path.basename(curfile)
            curpathnames = os.path.dirname(curfile).split('\\')
            dir_level    = len(os.path.dirname(file_dir).split('\\')) if file_dir is not None else len(os.path.dirname(file).split('\\'))
            navigation   += str('    '*(len(curpathnames)-dir_level)) \
                        + '* ['+str(curpathnames[-1])+']' \
                        + '(file:\\\\\\' \
                        + str(curfile.replace('md','html').replace((file_dir if file_dir is not None else file), out) or '/tmp/%s.html' % os.path.splitext(curfilename)[0]) \
                        +')\n'
        logging.info(navigation)
    # Loop through files and rander to HTML
    for curfile in mdfiles:
        curfilename = os.path.basename(curfile)
        htmlpath = curfile.replace('md','html').replace((file_dir if file_dir is not None else file), out) or '/tmp/%s.html' % os.path.splitext(curfilename)[0]
        if not os.path.exists(htmlpath):
            try:
                os.makedirs(os.path.dirname(htmlpath))
            except OSError as exc:
                logging.error("Error creating file path for %s", htmlpath)
        logging.info("Converting %s to HTML...", curfilename)
        title = []
        with open(curfile) as f:
            text  = str(f.read())
            title = re.match(r"^\#\s(.*)", text).group(1)
            print(title)
            text  = text.replace("### Project Links", str(navigation))
        html = render(text, title=(title if title is not None else curfilename), csspath=csspath, interval=interval)
        with open(htmlpath, 'w') as f:
            f.write(html)

        # Preview
        if preview:
            browser = webbrowser.get().name
            logging.info("Opening %s in %s...", htmlpath, browser)
            webbrowser.open(htmlpath)


def main():
    """Parse arguments and run."""
    from docopt import docopt
    args = docopt(__doc__)

    logging.basicConfig(format='%(message)s')
    if args['--quiet']:
        logging.root.setLevel(logging.WARNING)
    else:
        logging.root.setLevel(logging.INFO)

    run(
        args['--file'],
        args['--file_dir'],
        args['--out'],
        args['--force'],
        args['--preview'],
        args['--interval'],
        args['--nav'],
    )


if __name__ == '__main__':
    main()
