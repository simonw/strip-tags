import click

from strip_tags import strip_tags


@click.command()
@click.version_option()
@click.argument("selectors", nargs=-1)
@click.option("-i", "--input", type=click.File("r"), default="-")
@click.option("-m", "--minify", is_flag=True, help="Minify whitespace")
@click.option("--first", is_flag=True, help="First element matching the selectors")
def cli(selectors, input, minify, first):
    """
    Strip tags from HTML, optionally from areas identified by CSS selectors

    Example usage:

        cat input.html | strip-tags > output.txt

    To run against just specific areas identified by CSS selectors:

        cat input.html | strip-tags .entry .footer > output.txt
    """
    final = strip_tags(input, selectors, minify=minify, first=first)
    click.echo(final)
