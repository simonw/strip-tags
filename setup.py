from setuptools import setup
import os

VERSION = "0.4.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="strip-tags",
    description="Strip tags from HTML, optionally from areas identified by CSS selectors",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/strip-tags",
    project_urls={
        "Issues": "https://github.com/simonw/strip-tags/issues",
        "CI": "https://github.com/simonw/strip-tags/actions",
        "Changelog": "https://github.com/simonw/strip-tags/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["strip_tags"],
    entry_points="""
        [console_scripts]
        strip-tags=strip_tags.cli:cli
    """,
    install_requires=["click", "beautifulsoup4", "html5lib"],
    extras_require={"test": ["pytest", "pytest-icdiff"]},
    python_requires=">=3.7",
)
