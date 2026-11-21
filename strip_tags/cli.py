import click
from bs4.dammit import EncodingDetector

from strip_tags import strip_tags


@click.command()
@click.version_option()
@click.argument("selectors", nargs=-1)
@click.option(
    "removes",
    "-r",
    "--remove",
    multiple=True,
    help="Remove content in these selectors",
)
@click.option("-i", "--input", type=click.File("rb"), default="-", help="Input file")
@click.option("-m", "--minify", is_flag=True, help="Minify whitespace")
@click.option("keep_tags", "-t", "--keep-tag", multiple=True, help="Keep these <tags>")
@click.option("--all-attrs", is_flag=True, help="Include all attributes on kept tags")
@click.option("--first", is_flag=True, help="First element matching the selectors")
def cli(selectors, removes, input, minify, keep_tags, all_attrs, first):
    """
    Strip tags from HTML, optionally from areas identified by CSS selectors

    Example usage:

        cat input.html | strip-tags > output.txt

    To run against just specific areas identified by CSS selectors:

        cat input.html | strip-tags .entry .footer > output.txt
    """
    content = input.read()
    if not EncodingDetector.find_declared_encoding(content, is_html=True):
        try:
            content = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            # Let the HTML parser handle other encodings.
            pass
    final = strip_tags(
        content,
        selectors,
        removes=removes,
        minify=minify,
        remove_blank_lines=minify,
        first=first,
        keep_tags=keep_tags,
        all_attrs=all_attrs,
    )
    click.echo(final)
