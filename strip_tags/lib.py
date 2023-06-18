import re
from typing import Iterable, Optional

from bs4 import BeautifulSoup, NavigableString

# Elements that should be followed by a newline, derived from
# https://www.w3.org/TR/2011/WD-html5-20110405/rendering.html#display-types
NEWLINE_ELEMENTS = (
    # display: block; default in the spec
    "address",
    "article",
    "aside",
    "blockquote",
    "body",
    "center",
    "dd",
    "dir",
    "div",
    "dl",
    "dt",
    "figure",
    "figcaption",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hgroup",
    "hr",
    "html",
    "legend",
    "listing",
    "menu",
    "nav",
    "ol",
    "p",
    "plaintext",
    "pre",
    "section",
    "summary",
    "ul",
    "xmp",
    # And <li> too, which default to display: list-item; in the spec:
    "li",
)

DISPLAY_NONE_SELECTORS = [
    "[hidden]",
    "area",
    "base",
    "basefont",
    "command",
    "datalist",
    "head",
    "input[type=hidden]",
    "link",
    "menu[type=context]",
    "meta",
    "noembed",
    "noframes",
    "param",
    "rp",
    "script",
    "source",
    "style",
    "track",
    "title",
]


def strip_tags(
    input: str,
    selectors: Optional[Iterable[str]] = None,
    *,
    minify: bool = False,
    first=False
) -> str:
    soup = BeautifulSoup(input, "html5lib")
    if not selectors:
        selectors = ["body"]
    output = []

    # Remove elements with display: none
    for none_selector in DISPLAY_NONE_SELECTORS:
        for tag in soup.select(none_selector):
            tag.decompose()

    # Replace each image with its alt text
    for img in soup.select("img[alt]"):
        img.replace_with(img["alt"])

    # Extract text from selected elements
    break_out = False
    for selector in selectors:
        for tag in soup.select(selector):
            # Output just the text content of this tag
            output.append(minify_node(tag, minify))
            if tag.name in NEWLINE_ELEMENTS:
                output.append("\n")
            # If the tag has a tail, output that too
            if tag.tail:
                output.append(tag.tail)
            if first:
                break_out = True
                break
        if break_out:
            break

    return "".join(output).strip()


def minify_node(node, minify):
    # Recursively process a tag or NavigableString
    if isinstance(node, NavigableString):
        if minify:
            return _whitespace_re.sub(repl, node).strip()
        else:
            return node
    elif node.name == "pre":
        return str(node.text)  # keep <pre> tags as-is
    else:
        return "".join(minify_node(child, minify) for child in node.contents)


_whitespace_re = re.compile(r"\s+")


def repl(m):
    newline_count = m.group(0).count("\n")
    if newline_count >= 2:
        return "\n\n"
    elif newline_count == 1:
        return "\n"
    else:
        return " "
