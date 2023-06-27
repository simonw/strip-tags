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
    all_attrs = False
    keep_tags = []
    args_len = len(args)
    i = 0
    while i < args_len:
        # This is so we can grab the pair of "-t", "x" if needed:
        arg = args[i]
        if arg in {"-m", "--minify"}:
            minify = True
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
        first=first,
        keep_tags=keep_tags,
        all_attrs=all_attrs,
    )
    assert result == expected
