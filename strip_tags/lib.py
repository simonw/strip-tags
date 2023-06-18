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

SELF_CLOSING_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "command",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

BUNDLES = {
    "hs": ("h1", "h2", "h3", "h4", "h5", "h6"),
    "metadata": ("title", "meta"),
    "structure": {"header", "nav", "main", "article", "section", "aside", "footer"},
}

ATTRS_TO_KEEP = {
    "a": {"href"},
    "img": {"alt"},
    "meta": {"name", "value"},
}


def strip_tags(
    input: str,
    selectors: Optional[Iterable[str]] = None,
    *,
    minify: bool = False,
    first: bool = False,
    keep_tags: Optional[Iterable[str]] = None,
    all_attrs: bool = False,
) -> str:
    soup = BeautifulSoup(input, "html5lib", multi_valued_attributes=False)
    if not selectors:
        selectors = ["body"]
    output = []

    keep_tags = keep_tags or []

    if keep_tags:
        # Expand any bundles
        expanded_keep_tags = []
        for tag in keep_tags:
            if tag in BUNDLES:
                expanded_keep_tags.extend(BUNDLES[tag])
            else:
                expanded_keep_tags.append(tag)
        keep_tags = expanded_keep_tags

    # Remove elements with display: none
    for none_selector in DISPLAY_NONE_SELECTORS:
        if none_selector not in keep_tags:
            for tag in soup.select(none_selector):
                tag.decompose()

    # Replace each image with its alt text
    if "img" not in keep_tags:
        for img in soup.select("img[alt]"):
            img.replace_with(img["alt"])

    # Extract text from selected elements
    break_out = False
    for selector in selectors:
        for element in soup.select(selector):
            # Output just the text content of this element
            output.append(process_node(element, minify, keep_tags, all_attrs))
            if element.name in NEWLINE_ELEMENTS:
                output.append("\n")
            # If the element has a tail, output that too
            if element.tail:
                output.append(element.tail)
            if first:
                break_out = True
                break
        if break_out:
            break

    return "".join(output).strip()


def process_node(node, minify, keep_tags, all_attrs=False):
    # Recursively process a tag or NavigableString
    if isinstance(node, NavigableString):
        if minify:
            minified = _whitespace_re.sub(repl, node)
            if minified == "\n":
                minified = " "
            return minified
        else:
            return node
    elif node.name == "pre":
        s = str(node.text)
        if "pre" in keep_tags:
            return tag_with_attributes(node, s, all_attrs)
        else:
            return s
    else:
        bits = [
            process_node(child, minify, keep_tags, all_attrs) for child in node.contents
        ]
        s = "".join(bits)
        if node.name in keep_tags:
            s = tag_with_attributes(node, s, all_attrs)
        return s


_whitespace_re = re.compile(r"\s+")


def repl(m):
    newline_count = m.group(0).count("\n")
    if newline_count >= 2:
        return "\n\n"
    elif newline_count == 1:
        return "\n"
    else:
        return " "


def tag_with_attributes(node, content, all_attrs=False):
    # Returns e.g. <article id="foo" class="bar"> with subset of attributes
    to_keep = {"id", "class"}
    to_keep.update(ATTRS_TO_KEEP.get(node.name) or [])
    bits = [f"<{node.name}"]
    for key, value in dict(node.attrs).items():
        if all_attrs or (key in to_keep):
            bits.append(f'{key}="{value}"')
    output = " ".join(bits) + ">" + content
    if node.name not in SELF_CLOSING_TAGS:
        output += f"</{node.name}>"
    return output
