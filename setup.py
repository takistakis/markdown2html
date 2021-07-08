#!/usr/bin/env python3

"""setuptools installer script for markdown2html."""

from setuptools import setup

setup(
    name='markdown2html',
    version='0.3.0',
    description='Convert a GitHub Flavored Markdown file to HTML.',
    author='Thomas Cannon',
    author_email='tcannon.mail@gmail.com',
    url='https://github.com/twcannon/markdown2html',
    license='GPLv3',
    py_modules=['markdown2html'],
    entry_points={'console_scripts': ['markdown2html=markdown2html:main']},
    install_requires=['docopt', 'Markdown', 'Pygments'],
    extras_require={'extra': 'pymdown-extensions'},
)
