from bs4 import BeautifulSoup
import click
import re

# Elements that should be followed by a newline, derived from
# https://www.w3.org/TR/2011/WD-html5-20110405/rendering.html#display-types
NEWLINE_ELEMENTS = (
    # display: block; default in the spec
    "address",
    "article",
    "aside",
    "blockquote",
    "body",
    "center",
    "dd",
    "dir",
    "div",
    "dl",
    "dt",
    "figure",
    "figcaption",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hgroup",
    "hr",
    "html",
    "legend",
    "listing",
    "menu",
    "nav",
    "ol",
    "p",
    "plaintext",
    "pre",
    "section",
    "summary",
    "ul",
    "xmp",
    # And <li> too, which default to display: list-item; in the spec:
    "li",
)


@click.command()
@click.version_option()
@click.argument("selectors", nargs=-1)
@click.option("-i", "--input", type=click.File("r"), default="-")
@click.option("-m", "--minify", is_flag=True, help="Minify whitespace")
def cli(selectors, input, minify):
    """
    Strip tags from HTML, optionally from areas identified by CSS selectors

    Example usage:

        cat input.html | strip-tags > output.txt

    To run against just specific areas identified by CSS selectors:

        cat input.html | strip-tags .entry .footer > output.txt
    """
    parser = BeautifulSoup(input, "html5lib")
    if not selectors:
        selectors = ["body"]
    output = []
    for selector in selectors:
        for tag in parser.select(selector):
            # Output just the text content of this tag
            output.append(tag.text)
            if tag.name in NEWLINE_ELEMENTS:
                output.append("\n")
            # If the tag has a tail, output that too
            if tag.tail:
                output.append(tag.tail)
    final = "".join(output).strip()
    if minify:
        final = minify_whitespace(final)
    click.echo(final)


_whitespace_re = re.compile(r"\s+")


def minify_whitespace(text):
    def repl(m):
        newline_count = m.group(0).count("\n")
        if newline_count >= 2:
            return "\n\n"
        elif newline_count == 1:
            return "\n"
        else:
            return " "

    return _whitespace_re.sub(repl, text).strip()
