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

Contact: one.chillindude@me.com
"""

from invoke import task
import os

SPHINX_OPTS = None
SPHINX_BUILD = 'sphinx-build'
SPHINX_SOURCE_DIR = 'docs/source'
SPHINX_BUILD_DIR = 'docs/build'
SPHINX_CONFIG_PATH = os.path.abspath('docs/source')
MODULE_PATH = 'pymbs'


@task
def clean(ctx):
    """
    Remove the current Documentation set.
    """
    ctx.run(f"rm -rf {SPHINX_BUILD_DIR}/*")


@task(clean, help={'builder': "Specify which doc builder to use."})
def build(ctx, builder='html'):
    """
    Build the Documentation.
    """
    ctx.run(f"sphinx-apidoc -e -o {SPHINX_SOURCE_DIR} {MODULE_PATH}")

    ctx.run(f"{SPHINX_BUILD} "
            f"-b {builder} "
            f"-c {SPHINX_CONFIG_PATH} {SPHINX_SOURCE_DIR} {SPHINX_BUILD_DIR}")
