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

from contextlib import contextmanager
from pathlib import Path
import pickle
import shutil

import pytest

import pymbs

REFERENCE_DEAL = 'fhl2618'
NO_DEAL = 'no_deal'

test_dir = Path(__file__).parent
data_dir = Path(test_dir, 'data')
input_data_dir = Path(data_dir, 'input')
output_data_dir = Path(data_dir, 'output')
reference_data_dir = Path(data_dir, 'reference')


@pytest.fixture
def project_dir():
    project_dir_path = input_data_dir
    return project_dir_path


@pytest.fixture
def empty_project():
    empty_project_dir = Path(input_data_dir, 'empty_deal')
    return empty_project_dir


@pytest.fixture
def temp_data_dir():
    temp_data_path = Path(data_dir, 'temp')
    return temp_data_path


@pytest.fixture
def terms_sheet(scope="session", autouse=True):
    pymbs.config.project_dir = Path(input_data_dir)
    ts = pymbs.load_deal(REFERENCE_DEAL)
    return ts


@pytest.fixture
def ref_data():
    def get_data(data_set):
        data_set_path = Path(reference_data_dir, f"{data_set}.pickle")
        with open(data_set_path, 'rb') as data_pickle:
            data = pickle.load(data_pickle)
        return data
    return get_data


@pytest.fixture
def ref_deal():
    return REFERENCE_DEAL


@pytest.fixture
def no_deal():
    return NO_DEAL


@pytest.fixture()
def no_deal_ts(project_dir, no_deal):
    no_deal_ts = Path(project_dir, no_deal, f"{no_deal}_ts.json")
    return no_deal_ts


@pytest.fixture
def remove_file():
    @contextmanager
    def rm_file(src, temp_data_path):
        temp_location = shutil.move(src, str(temp_data_path))
        try:
            yield temp_location
        finally:
            shutil.move(temp_location, src)

    return rm_file
