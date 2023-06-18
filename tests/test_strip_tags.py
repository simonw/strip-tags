import pytest
from click.testing import CliRunner

from strip_tags import strip_tags
from strip_tags.cli import cli

TEST_PARAMETERS = (
    ("<p>Hello <b>world</b></p>", [], "Hello world"),
    ("<p>Hello <b>world</b></p>", ["p"], "Hello world"),
    ("<p>Hello <b>world</b></p>", ["b"], "world"),
    ("<div><span>span</span><b>b</b><i>i</i>", ["span", "i"], "spani"),
    # Block level elements should have a newline
    (
        "<div><h1>H1</h1><p>Para</p><pre>pre</pre>",
        ["h1", "pre"],
        "H1\npre",
    ),
    # Various ways whitespace should be stripped
    (
        "Hello\nThis\nIs\nNewlines",
        ["--minify"],
        "Hello\nThis\nIs\nNewlines",
    ),
    (
        "Hello\nThis\n\n\nIs\nNewlines",
        ["-m"],
        "Hello\nThis\n\nIs\nNewlines",
    ),
    (
        "Hello\nThis\n\t\t \t\n\nIs\nNewlines",
        ["--minify"],
        "Hello\nThis\n\nIs\nNewlines",
    ),
    (
        "Hello  this \t has   \t spaces",
        ["--minify"],
        "Hello this has spaces",
    ),
    # Should remove script and style
    (
        "<script>alert('hello');</script><style>body { color: red; }</style>Hello",
        [],
        "Hello",
    ),
    # Test alt text replacement
    (
        '<img src="foo.jpg" alt="Foo"><img src="bar.jpg" alt="Bar">',
        [],
        "FooBar",
    ),
    # Even with --minify <pre> tag content should be unaffected
    (
        "<pre>this\n  has\n    spaces</pre>",
        ["--minify"],
        "this\n  has\n    spaces",
    ),
    # Test --first
    (
        "Ignore start<p>First paragraph</p><p>Second paragraph</p>Ignore end",
        ["p", "--first"],
        "First paragraph",
    ),
)


@pytest.mark.parametrize("input,args,expected", TEST_PARAMETERS)
@pytest.mark.parametrize("use_i_option", (False, True))
def test_strip_cli(input, args, expected, use_i_option):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Copy to avoid modifying for later tests
        args = args[:]
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
    assert result.output == expected + "\n"


@pytest.mark.parametrize("input,args,expected", TEST_PARAMETERS)
def test_strip_lib(input, args, expected):
    # Turn args into function arguments
    selectors = []
    first = False
    minify = False
    for arg in args:
        if arg in {"-m", "--minify"}:
            minify = True
        elif arg == "--first":
            first = True
        else:
            selectors.append(arg)

    result = strip_tags(input, selectors, minify=minify, first=first)
    assert result == expected
