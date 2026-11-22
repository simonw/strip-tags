import pytest
from click.testing import CliRunner
import pathlib
from strip_tags import strip_tags
from strip_tags.cli import cli
import yaml

# load from tests.yaml
TEST_PARAMETERS = [
    (d["input"], d["args"], d["expected"].strip())
    for d in yaml.safe_load((pathlib.Path(__file__).parent / "tests.yaml").read_text())
]


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
    removes = []
    first = False
    minify = False
    remove_blank_lines = False
    all_attrs = False
    keep_tags = []
    args_len = len(args)
    i = 0
    while i < args_len:
        # This is so we can grab the pair of "-t", "x" if needed:
        arg = args[i]
        if arg in {"-m", "--minify"}:
            minify = True
            remove_blank_lines = True
        elif arg == "--first":
            first = True
        elif arg == "--all-attrs":
            all_attrs = True
        elif arg == "-t":
            # Skip next token
            i += 1
            if i < args_len:
                keep_tags.append(args[i])
            else:
                raise ValueError('Expected an argument after "-t"')
        elif arg == "-r":
            i += 1
            if i < args_len:
                removes.append(args[i])
            else:
                raise ValueError('Expected an argument after "-t"')
        else:
            selectors.append(arg)
        i += 1

    result = strip_tags(
        input,
        selectors,
        removes=removes,
        minify=minify,
        remove_blank_lines=remove_blank_lines,
        first=first,
        keep_tags=keep_tags,
        all_attrs=all_attrs,
    )
    assert result == expected


@pytest.mark.parametrize("use_i_option", (False, True))
@pytest.mark.parametrize(
    "encoding,charset,text",
    [
        ("utf-8", None, "日本語のテキスト"),
        ("utf-8-sig", None, "日本語のテキスト"),
        ("utf-16", None, "日本語のテキスト"),
        ("windows-1252", "windows-1252", "café — résumé"),
        ("windows-1252", "iso-8859-1", "café — résumé"),
        ("windows-1252", "windows-1252", "Â£"),
        ("windows-1252", None, "café — résumé"),
        ("shift_jis", "shift_jis", "日本語のテキスト"),
    ],
)
def test_cli_encoding(encoding, charset, text, use_i_option):
    runner = CliRunner()
    html = '<meta charset="{}">'.format(charset) if charset else ""
    html += "<h1>{}</h1>".format(text)
    data = html.encode(encoding)
    with runner.isolated_filesystem():
        if use_i_option:
            with open("input.html", "wb") as fp:
                fp.write(data)
            result = runner.invoke(cli, ["-i", "input.html"])
        else:
            result = runner.invoke(cli, [], input=data)
    assert result.exit_code == 0
    assert result.output == text + "\n"
