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

from invoke import Collection, task

from docs import docs
# from tests import qa


@task
def clean(ctx):
    """
    Cleanup the current build artifacts
    """
    ctx.run('rm -rf build/')
    ctx.run('rm -rf dist/')
    ctx.run('rm -rf pymbs.egg-info/')


@task(clean)
def build(ctx):
    """
    Build a distribution for PyPi
    """
    ctx.run('python setup.py sdist bdist_wheel')


@task
def deploy_test(ctx):
    """
    Upload a distribution to TEST PyPi
    """
    ctx.run("twine upload --repository-url "
            "https://test.pypi.org/legacy/ dist/*"
            )


@task
def deploy(ctx):
    """
    Upload a distribution to PyPi
    """
    ctx.run("twine upload dist/*")


namespace = Collection(
    build,
    clean,
    deploy,
    deploy_test,
    docs,
)
#    qa
