# markdown2html

Yet another script that converts GitHub Flavored Markdown files to HTML.

It is inspired by [grip], and is an attempt to replicate it without its
dependencies and without the need to interact directly with GitHub, or even
being connected to the internet.  The first time it runs, [github-markdown.css]
is downloaded and stored in `~/.cache` and from then on, it can be used while
being offline.  Generated HTML is put at `/tmp` by default.

Note that GitHub doesn't use pygments anymore for syntax highlighting, so it's
difficult to generate the same CSS classes to use its colorscheme, and pygments
doesn't include a similar one.  For now, markdown2html uses the tango style
which comes built-in with pygments.

## Requirements

* [markdown]
* [pygments]
* [docopt]

Install with:

```bash
$ pip install markdown pygments docopt
```

Optionally, if [pymdown_extensions] is present, extensions [extra],
[magiclink] and [tasklist] are used.

## Usage

```
markdown2html [options] <file>

Options:
  -o, --out <file>      Write output to <file>
  -f, --force           Overwrite existing CSS file
  -p, --preview         Open generated HTML file in browser
  -i, --interval <int>  Refresh page every <int> seconds
  -q, --quiet           Show less information
  -h, --help            Show this help message and exit
```

## License

Licensed under GPLv3 or later.

[grip]: https://github.com/joeyespo/grip
[github-markdown.css]: https://github.com/sindresorhus/github-markdown-css
[markdown]: https://pythonhosted.org/Markdown
[pygments]: http://pygments.org
[docopt]: http://docopt.org
[pymdown_extensions]: https://github.com/facelessuser/pymdown-extensions
[extra]: https://facelessuser.github.io/pymdown-extensions/extensions/extra
[magiclink]: https://facelessuser.github.io/pymdown-extensions/extensions/magiclink
[tasklist]: https://facelessuser.github.io/pymdown-extensions/extensions/tasklist
