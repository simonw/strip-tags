from click.testing import CliRunner
from strip_tags.cli import cli
import pytest


@pytest.mark.parametrize(
    "input, selectors, expected",
    (
        ("<p>Hello <b>world</b></p>", [], "Hello world\n"),
        ("<p>Hello <b>world</b></p>", ["p"], "Hello world\n"),
        ("<p>Hello <b>world</b></p>", ["b"], "world"),
        ("<div><span>span</span><b>b</b><i>i</i>", ["span", "i"], "spani"),
        # Block level elements should have a newline
        ("<div><h1>H1</h1><p>Para</p><pre>pre</pre>", ["h1", "pre"], "H1\npre\n"),
    ),
)
def test_strip(input, selectors, expected):
    runner = CliRunner()
    args = []
    for selector in selectors:
        args.extend(["-s", selector])
    result = runner.invoke(cli, args, input=input)
    assert result.exit_code == 0
    assert result.output == expected
