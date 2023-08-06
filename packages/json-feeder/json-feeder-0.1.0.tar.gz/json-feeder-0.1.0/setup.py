import os

from setuptools import setup

VERSION = "0.1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="json-feeder",
    description="A framework for generate JSON feeds",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Brenton Cleeland",
    url="https://github.com/sesh/feeder",
    project_urls={
        "Issues": "https://github.com/sesh/feeder/issues",
        "CI": "https://github.com/sesh/feeder/actions",
        "Changelog": "https://github.com/sesh/feeder/releases",
    },
    version=VERSION,
    packages=["feeder"],
    install_requires=["thttp"],
    python_requires=">=3.8",
    license="MIT License",
    entry_points="""
        [console_scripts]
        feeder=feeder.cli:cli
    """,
)
