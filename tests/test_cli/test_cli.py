import pathlib

import pytest
import yaml
from click.testing import CliRunner

from strip_tags.cli import cli

# load from tests.yaml
TEST_PARAMETERS = [
    (d["input"], d["args"], d["expected"].strip())
    for d in yaml.safe_load((pathlib.Path(__file__).parent / "cases.yaml").read_text())
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
    assert result.exit_code == 0
    assert result.output == expected + "\n"
