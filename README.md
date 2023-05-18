# strip-tags

[![PyPI](https://img.shields.io/pypi/v/strip-tags.svg)](https://pypi.org/project/strip-tags/)
[![Changelog](https://img.shields.io/github/v/release/simonw/strip-tags?include_prereleases&label=changelog)](https://github.com/simonw/strip-tags/releases)
[![Tests](https://github.com/simonw/strip-tags/workflows/Test/badge.svg)](https://github.com/simonw/strip-tags/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/strip-tags/blob/master/LICENSE)

Strip tags from HTML, optionally from areas identified by CSS selectors

See [llm, ttok and strip-tags—CLI tools for working with ChatGPT and other LLMs](https://simonwillison.net/2023/May/18/cli-tools-for-llms/) for more on this project.

## Installation

Install this tool using `pip`:

    pip install strip-tags

## Usage

Pipe content into this tool to strip tags from it:

    cat input.html | strip-tags > output.txt

Or pass a filename:

    strip-tags -i input.html > output.txt

To run against just specific areas identified by CSS selectors:

    strip-tags '.content' -i input.html > output.txt

This can be called with multiple selectors:

    cat input.html | strip-tags '.content' '.sidebar' > output.txt

You can also use:

    python -m strip_tags --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd strip-tags
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
