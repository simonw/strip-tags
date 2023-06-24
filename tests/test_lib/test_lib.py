import pathlib

import pytest
import yaml

from strip_tags import strip_tags

# load from tests.yaml
TEST_PARAMETERS = [
    (d["input"], d["args"], d["expected"].strip())
    for d in yaml.safe_load((pathlib.Path(__file__).parent / "cases.yaml").read_text())
]


@pytest.mark.parametrize("input,args,expected", TEST_PARAMETERS)
def test_strip_lib(input, args, expected):
    # Turn args into function arguments
    selectors = []
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
        else:
            selectors.append(arg)
        i += 1

    result = strip_tags(
        input,
        selectors,
        minify=minify,
        first=first,
        keep_tags=keep_tags,
        all_attrs=all_attrs,
    )
    assert result == expected
    assert result == expected
    assert result == expected
    assert result == expected
    assert result == expected
    assert result == expected
