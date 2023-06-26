import pathlib
from typing import Iterable, List, NamedTuple, Optional, Union

import pytest

from strip_tags import strip_tags

HTML_FILES_DIR = pathlib.Path(__file__).parent / "html_files"


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
    Case(
        id="lists bundle",
        expected="""<ul>
      <li>Source code</li>
      <li>©</li>
      <li>2002</li>
      <li>2003</li>
      <li>2004</li>
      <li>2005</li>
      <li>2006</li>
      <li>2007</li>
      <li>2008</li>
      <li>2009</li>
      <li>2010</li>
      <li>2011</li>
      <li>2012</li>
      <li>2013</li>
      <li>2014</li>
      <li>2015</li>
      <li>2016</li>
      <li>2017</li>
      <li>2018</li>
      <li>2019</li>
      <li>2020</li>
      <li>2021</li>
      <li>2022</li>
      <li>2023</li>
    </ul>""",
        input="""<div id="ft">
    <ul>
      <li><a href="https://github.com/simonw/simonwillisonblog">Source code</a></li>
      <li>&copy;</li>
      <li><a href="/2002/">2002</a></li>
      <li><a href="/2003/">2003</a></li>
      <li><a href="/2004/">2004</a></li>
      <li><a href="/2005/">2005</a></li>
      <li><a href="/2006/">2006</a></li>
      <li><a href="/2007/">2007</a></li>
      <li><a href="/2008/">2008</a></li>
      <li><a href="/2009/">2009</a></li>
      <li><a href="/2010/">2010</a></li>
      <li><a href="/2011/">2011</a></li>
      <li><a href="/2012/">2012</a></li>
      <li><a href="/2013/">2013</a></li>
      <li><a href="/2014/">2014</a></li>
      <li><a href="/2015/">2015</a></li>
      <li><a href="/2016/">2016</a></li>
      <li><a href="/2017/">2017</a></li>
      <li><a href="/2018/">2018</a></li>
      <li><a href="/2019/">2019</a></li>
      <li><a href="/2020/">2020</a></li>
      <li><a href="/2021/">2021</a></li>
      <li><a href="/2022/">2022</a></li>
      <li><a href="/2023/">2023</a></li>
    </ul>
</div>""",
        keep_tags=["lists"],
    ),
    Case(
        id="fix missing ul - https://github.com/simonw/strip-tags/pull/18#issuecomment-1600465929",
        marks=[
            pytest.mark.xfail(reason="https://github.com/simonw/strip-tags/issues/21")
        ],
        expected="""<ul>
      <li>Source code</li>
      <li>©</li>
      <li>2002</li>
      <li>2003</li>
      <li>2004</li>
      <li>2005</li>
      <li>2006</li>
      <li>2007</li>
      <li>2008</li>
      <li>2009</li>
      <li>2010</li>
      <li>2011</li>
      <li>2012</li>
      <li>2013</li>
      <li>2014</li>
      <li>2015</li>
      <li>2016</li>
      <li>2017</li>
      <li>2018</li>
      <li>2019</li>
      <li>2020</li>
      <li>2021</li>
      <li>2022</li>
      <li>2023</li>
    </ul>""",
        input="""<div id="ft">
    <ul>
      <li><a href="https://github.com/simonw/simonwillisonblog">Source code</a></li>
      <li>&copy;</li>
      <li><a href="/2002/">2002</a></li>
      <li><a href="/2003/">2003</a></li>
      <li><a href="/2004/">2004</a></li>
      <li><a href="/2005/">2005</a></li>
      <li><a href="/2006/">2006</a></li>
      <li><a href="/2007/">2007</a></li>
      <li><a href="/2008/">2008</a></li>
      <li><a href="/2009/">2009</a></li>
      <li><a href="/2010/">2010</a></li>
      <li><a href="/2011/">2011</a></li>
      <li><a href="/2012/">2012</a></li>
      <li><a href="/2013/">2013</a></li>
      <li><a href="/2014/">2014</a></li>
      <li><a href="/2015/">2015</a></li>
      <li><a href="/2016/">2016</a></li>
      <li><a href="/2017/">2017</a></li>
      <li><a href="/2018/">2018</a></li>
      <li><a href="/2019/">2019</a></li>
      <li><a href="/2020/">2020</a></li>
      <li><a href="/2021/">2021</a></li>
      <li><a href="/2022/">2022</a></li>
      <li><a href="/2023/">2023</a></li>
    </ul>
</div>""",
        keep_tags=["lists"],
        selectors=["ul", "li", "ol"],
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
