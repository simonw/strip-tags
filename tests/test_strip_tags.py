from click.testing import CliRunner
from strip_tags.cli import cli
import pytest


@pytest.mark.parametrize(
    "input, selectors, expected",
    (
        ("<p>Hello <b>world</b></p>", [], "Hello world\n"),
        ("<p>Hello <b>world</b></p>", ["p"], "Hello world\n"),
        ("<p>Hello <b>world</b></p>", ["b"], "world\n"),
        ("<div><span>span</span><b>b</b><i>i</i>", ["span", "i"], "spani\n"),
        # Block level elements should have a newline
        ("<div><h1>H1</h1><p>Para</p><pre>pre</pre>", ["h1", "pre"], "H1\npre\n"),
        # Various ways whitespace should be stripped
        ("Hello\nThis\nIs\nNewlines", ["--minify"], "Hello\nThis\nIs\nNewlines\n"),
        ("Hello\nThis\n\n\nIs\nNewlines", ["-m"], "Hello\nThis\n\nIs\nNewlines\n"),
        (
            "Hello\nThis\n\t\t \t\n\nIs\nNewlines",
            ["--minify"],
            "Hello\nThis\n\nIs\nNewlines\n",
        ),
        (
            "Hello  this \t has   \t spaces",
            ["--minify"],
            "Hello this has spaces\n",
        ),
        # Should remove script and style
        (
            "<script>alert('hello');</script><style>body { color: red; }</style>Hello",
            [],
            "Hello\n",
        ),
    ),
)
@pytest.mark.parametrize("use_i_option", (False, True))
def test_strip(input, selectors, expected, use_i_option):
    runner = CliRunner()
    with runner.isolated_filesystem():
        args = selectors[:]
        kwargs = {}
        if use_i_option:
            # Create temp file
            with open("input.html", "w") as fp:
                fp.write(input)
                args.extend(["-i", "input.html"])
        else:
            kwargs["input"] = input
        result = runner.invoke(cli, args, **kwargs)
    assert result.exit_code == 0
    assert result.output == expected
