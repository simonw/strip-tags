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
## As a Python library

You can use `strip-tags` from Python code too. The function signature looks like this:

```python
def strip_tags(
    input: str,
    selectors: Optional[Iterable[str]] = None,
    *,
    minify: bool = False,
    first=False
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
stripped = strip_tags(html, ["div"], minify=True)
print(stripped)
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