# markdown2html

Script that converts GitHub Flavored Markdown files/directories to HTML.

Originally forked from [https://github.com/forkbong/markdown2html]

The first time it runs, [github-markdown.css]
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
$ pip install markdown pygments docopt pymdown-extensions
```

Optionally, if [pymdown_extensions] is present, extensions [extra],
[magiclink], [tasklist], [highlight] and [tilde] are used.


## Usage

```
markdown2html [options]

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
```
if ```--nav``` is used, the .md file needs to have ```### Project Links``` somewhere in the .md file.


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
[highlight]: https://facelessuser.github.io/pymdown-extensions/extensions/highlight/
[tilde]: https://facelessuser.github.io/pymdown-extensions/extensions/tilde
