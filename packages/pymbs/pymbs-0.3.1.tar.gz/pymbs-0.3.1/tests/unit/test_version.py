"""
PyMBS is a Python library for use in modeling Mortgage-Backed Securities.

Copyright (C) 2019  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

from pymbs import __version__

major = 1
minor = 2
patch = 3
version_pre_tags = ['post3', 'dev']
version_post_tag = 'a2'
test_version_tuple = __version__._version_t_ = __version__.Version(
    major, minor, patch, version_pre_tags, version_post_tag
)


class TestBasicVersion(object):
    """docstring for TestBasicVersion"""

    def test_semver_equivalent(self):
        ref_version = '1.2.3'
        test_version = __version__._basic_version(test_version_tuple)

        assert test_version == ref_version


class TestVersionToString(object):
    """docstring for TestVersionToString"""

    def test_semver_equivalent(self):
        ref_version = '1.2.3.post3.dev.a2'
        test_version = __version__._version_to_string(test_version_tuple)

        assert test_version == ref_version
