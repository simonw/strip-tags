import pathlib
from typing import Iterable, List, NamedTuple, Optional, Union

import pytest

from strip_tags import strip_tags

HTML_FILES_DIR = pathlib.Path(__file__).parent / "html_files"
assert HTML_FILES_DIR.exists()


class Case(NamedTuple):
    id: str
    expected: Union[str, Exception]
    input: Union[str, pathlib.Path]
    marks: List[pytest.MarkDecorator] = []
    selectors: Optional[Iterable[str]] = None
    minify: bool = False
    first: bool = False
    keep_tags: Optional[Iterable[str]] = None
    all_attrs: bool = False


cases = [
    Case(
        id="simple, remove tags",
        expected="Hello World",
        input="Hello <b>World</b>",
    ),
    Case(
        id="no change",
        expected="Hello World",
        input="Hello World",
    ),
    Case(
        id="basic selectors",
        expected="World",
        input="Hello <b>World</b>",
        selectors=["b"],
    ),
    Case(
        id="nested selectors",
        marks=[
            pytest.mark.xfail(reason="https://github.com/simonw/strip-tags/issues/21")
        ],
        expected="Hello Beautiful World",
        input="Hello <b><i>Beautiful</i> World</b>",
        selectors=["b", "i"],
    ),
    Case(
        id="basic selector with class",
        expected="Hello World",
        input="<div class='header'>Hello World</div>",
        selectors=["div"],
    ),
    Case(
        id="basic selector with nested tags and class",
        expected="Hello World",
        input="<div class='header'>Hello <i>World</i></div>",
        selectors=["div"],
    ),
    Case(
        id="unnecessary minify",
        expected="Hello World",
        input="Hello <b>World</b>",
        minify=True,
    ),
    Case(
        id="keep a tag, discard inner tag",
        expected="<p>Hello World</p>",
        input="<p>Hello <b>World</b></p>",
        keep_tags=["p"],
    ),
    Case(
        id="keep tag and attr, discard inner tag",
        expected="<p class='center'>Hello World</p>",
        input="<p class='center'>Hello <b>World</b></p>",
        keep_tags=["p"],
        all_attrs=True,
    ),
    Case(
        id="discard a tag by default",
        expected="hello world",
        input="<a href='https://example.com' id='my-link'>hello world</a>",
    ),
    Case(
        id="keep href in a tag, class, and id attrs by default",
        expected="<a href='https://example.com' id='my-link' class='foo'>hello world</a>",
        input="<a href='https://example.com' id='my-link' class='foo' hx-get='/foo'>hello world</a>",
        keep_tags=["a"],
        all_attrs=False,
    ),
    Case(
        id="all attrs",
        expected="<a href='https://example.com' id='my-link' class='foo' hx-get='/foo'>hello world</a>",
        input="<a href='https://example.com' id='my-link' class='foo' hx-get='/foo'>hello world</a>",
        keep_tags=["a"],
        all_attrs=True,
    ),
]


@pytest.mark.parametrize(
    "expected, input, selectors, minify, first, keep_tags, all_attrs",
    [
        pytest.param(
            case.expected,
            case.input.read_text()
            if isinstance(case.input, pathlib.Path)
            else case.input,
            case.selectors,
            case.minify,
            case.first,
            case.keep_tags,
            case.all_attrs,
            marks=case.marks,
            id=case.id,
        )
        for case in cases
    ],
)
def test_strip_tags(expected, input, selectors, minify, first, keep_tags, all_attrs):
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            strip_tags(
                input,
                selectors,
                minify=minify,
                first=first,
                keep_tags=keep_tags,
                all_attrs=all_attrs,
            )
    else:
        assert isinstance(expected, str)
        output = strip_tags(
            input,
            selectors,
            minify=minify,
            first=first,
            keep_tags=keep_tags,
            all_attrs=all_attrs,
        )
        assert output.replace("'", '"') == expected.replace("'", '"')
