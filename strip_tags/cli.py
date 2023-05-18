import click
from bs4 import BeautifulSoup
import click
import html5lib

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
@click.argument("input", type=click.File("r"), default="-")
@click.option("selectors", "-s", multiple=True, help="CSS selectors for page areas")
def cli(input, selectors):
    "Strip tags from HTML"
    parser = BeautifulSoup(input, "html5lib")
    if not selectors:
        selectors = ["body"]
    for selector in selectors:
        for tag in parser.select(selector):
            # Output just the text content of this tag
            click.echo(tag.text, nl=tag.name in NEWLINE_ELEMENTS)
            # If the tag has a tail, output that too
            if tag.tail:
                click.echo(tag.tail, nl=False)
