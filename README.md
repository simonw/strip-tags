# strip-tags

[![PyPI](https://img.shields.io/pypi/v/strip-tags.svg)](https://pypi.org/project/strip-tags/)
[![Changelog](https://img.shields.io/github/v/release/simonw/strip-tags?include_prereleases&label=changelog)](https://github.com/simonw/strip-tags/releases)
[![Tests](https://github.com/simonw/strip-tags/workflows/Test/badge.svg)](https://github.com/simonw/strip-tags/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/strip-tags/blob/master/LICENSE)

Strip tags from HTML, optionally from areas identified by CSS selectors

See [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/) for more on this project.

## Installation

Install this tool using `pip`:
```bash
pip install strip-tags
```
## Usage

Pipe content into this tool to strip tags from it:
```bash
cat input.html | strip-tags > output.txt
````
Or pass a filename:
```bash
strip-tags -i input.html > output.txt
```
To run against just specific areas identified by CSS selectors:
```bash
strip-tags '.content' -i input.html > output.txt
```
This can be called with multiple selectors:
```bash
cat input.html | strip-tags '.content' '.sidebar' > output.txt
```
To return just the first element on the page that matches one of the selectors, use `--first`:
```bash
cat input.html | strip-tags .content --first > output.txt
```
To minify whitespace - reducing multiple space and tab characters to a single space, and multiple newlines and spaces to a maximum of two newlines - add `-m` or `--minify`:
```bash
cat input.html | strip-tags -m > output.txt
```
You can also run this command using `python -m` like this:
```bash
python -m strip_tags --help
```
### Keeping the markup for specified tags

When passing content to a language model, it can sometimes be useful to leave in a subset of HTML tags - `<h1>This is the heading</h1>` for example - to provide extra hints to the model.

The `-t/--keep-tag` option can be passed multiple times to specify tags that should be kept.

This example looks at the `<header>` section of https://datasette.io/ and keeps the tags around the list items and `<h1>` elements:

```
curl -s https://datasette.io/ | strip-tags header -t h1 -t li
```html
<li>Uses</li>
<li>Documentation Docs</li>
<li>Tutorials</li>
<li>Examples</li>
<li>Plugins</li>
<li>Tools</li>
<li>News</li>
<h1>
    Datasette
</h1>
Find stories in data
```
All attributes will be removed from the tags, except for the `id=` and `class=` attribute since those may provide further useful hints to the language model.

The `href` attribute on links, the `alt` attribute on images and the `name` and `value` attributes on `meta` tags are kept as well.

You can also specify a bundle of tags. For example, `strip-tags -t hs` will keep the tag markup for all levels of headings.

The following bundles can be used:

- `-t hs`: `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`
- `-t metadata`: `<title>`, `<meta>`
- `-t structure`: `<header>`, `<section>`, `<main>`, `<aside>`, `<footer>`, `<article>`, `<nav>`


## As a Python library

You can use `strip-tags` from Python code too. The function signature looks like this:

```python
def strip_tags(
    input: str,
    selectors: Optional[Iterable[str]] = None,
    *,
    minify: bool = False,
    first: bool = False,
    keep_tags: Optional[Iterable[str]] = None,
    all_attrs: bool = False,
) -> str:
```
Here's an example:
```python
from strip_tags import strip_tags

html = """
<div>
<h1>This has tags</h1>

<p>And whitespace too</p>
</div>
Ignore this bit.
"""
stripped = strip_tags(html, ["div"], minify=True, keep_tags=["h1"])
print(stripped)
```
Output:
```
<h1>This has tags</h1>

And whitespace too
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd strip-tags
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
