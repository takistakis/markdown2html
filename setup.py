#!/usr/bin/env python3

"""setuptools installer script for markdown2html."""

from setuptools import setup

setup(
    name='markdown2html',
    version='0.2.0',
    description='Convert a GitHub Flavored Markdown file to HTML.',
    author='Panagiotis Ktistakis',
    author_email='panktist@gmail.com',
    url='https://github.com/forkbong/markdown2html',
    license='GPLv3',
    py_modules=['markdown2html'],
    entry_points={'console_scripts': ['markdown2html=markdown2html:main']},
    install_requires=['docopt', 'Markdown', 'Pygments'],
    extras_require={'extra': 'pymdown-extensions'},
)
