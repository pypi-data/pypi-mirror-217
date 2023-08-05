# Copyright (C) 2022 Steven Clontz and Oscar Levin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from pathlib import Path
from single_version import get_version

log = logging.getLogger("ptxlogger")

VERSION = get_version("pretext", Path(__file__).parent.parent)

CORE_COMMIT = '4da2a0f824785143c917c0f16007cbd0d48ba88d'

# List of templates, build formats, and assets that are supported by the CLI.
NEW_TEMPLATES = ["book", "article", "demo", "hello", "slideshow"]
BUILD_FORMATS = [
    "html",
    "pdf",
    "latex",
    "epub",
    "kindle",
    "braille",
    "html-zip",
    "webwork-sets",
    "webwork-sets-zipped",
]
ASSETS = [
    "ALL",
    "webwork",
    "latex-image",
    "sageplot",
    "asymptote",
    "interactive",
    "youtube",
    "codelens",
    "datafile",
]


def activate() -> None:
    """
    This function was provided by the original `pretext` package
    deployed to PyPI by Alex Willmer. Thanks to their generosity,
    we were allowed to adopt this namespace as of 1.0, so we raise an error here
    to help anyone who might have upgraded from the original package.
    """
    raise RuntimeError(
        "As of version 1.0, the `pretext` PyPI package has been "
        + "transferred to PreTeXtBook.org. Install a <1.0 version to use the "
        + "pretext.activate() feature from the original `pretext` package."
    )
