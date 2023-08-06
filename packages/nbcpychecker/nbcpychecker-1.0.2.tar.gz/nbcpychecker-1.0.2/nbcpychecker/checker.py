#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Checker.
"""

import re
from logging import getLogger
from pathlib import Path
from typing import Optional

from attrs import define, field

from .config import Config
from .errors import Error, Errors

LOGGER = getLogger("nbcpychecker")

_RE_LICENSE = re.compile(
    "".join(
        [
            r"\A",
            re.escape(
                """\
MIT License

"""
            ),
            r"""Copyright \(c\) (?P<years>[0-9,-]+) nbiotcloud

""",
            re.escape(
                """\
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
            ),
        ]
    ),
    flags=re.MULTILINE,
)

_RE_PY_COPYRIGHT = re.compile(
    "".join(
        [
            r"\A",
            re.escape(
                """\
#
# MIT License
#
"""
            ),
            r"""# Copyright \(c\) (?P<years>[0-9,-]+) nbiotcloud
""",
            re.escape(
                """\
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
            ),
        ]
    ),
    flags=re.MULTILINE,
)


@define
class Checker:

    """Checker."""

    config: Config = field(factory=Config)

    def check(self, path: Optional[Path] = None) -> Errors:
        """Run all checks."""
        path = path or Path(".")
        errors = Errors()
        self._check_copyright_header(errors, path)
        self._check_license(errors, path)
        return errors

    def _check_copyright_header(self, errors: Errors, path: Path):
        """Check Copyright Header."""
        pidx = len(path.parts)
        for filepath in path.glob("**/*.py"):
            # Exclude temp folder.
            if filepath.parts[pidx].startswith("."):
                continue
            filecontent = filepath.read_text()
            mat = _RE_PY_COPYRIGHT.match(filecontent)
            if mat:
                years = mat.group("years")
                self._check_copyright_years(errors, path, years)
            else:
                errors.append(Error(filepath, 1, "Copyright missing or broken."))

    def _check_license(self, errors: Errors, path: Path):
        """Check License."""
        filepath = path / "LICENSE"
        filecontent = filepath.read_text()
        mat = _RE_LICENSE.match(filecontent)
        if mat:
            years = mat.group("years")
            self._check_copyright_years(errors, path, years)
        else:
            errors.append(Error(filepath, 1, "License missing or broken."))

    @staticmethod
    def _check_copyright_years(errors: Errors, path: Path, years):
        pass
        # Determine Modification Years from git log
        # Compare with years
