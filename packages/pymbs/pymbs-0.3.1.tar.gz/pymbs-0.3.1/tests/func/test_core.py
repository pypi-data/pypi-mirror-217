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

import os

from pandas.util.testing import assert_frame_equal
import pytest

from pymbs import core


class TestRunCollatCf(object):
    """Functional tests for core._run_collat_cf(group_id, repline_num=0)
    """

    def test_single_repline_group(self, ref_data, terms_sheet):
        core.config.terms_sheet = terms_sheet
        ref_cf_g3 = ref_data('cf_group_3_core')
        test_cf_g3 = core._run_collat_cf("3")

        ref_cf_keys = sorted(list(ref_cf_g3.keys()))
        test_cf_keys = sorted(list(test_cf_g3.keys()))
        assert ref_cf_keys == test_cf_keys

        for scenario in test_cf_g3:
            ref_cf = ref_cf_g3[scenario]
            test_cf = test_cf_g3[scenario]
            assert_frame_equal(ref_cf, test_cf)


class TestGetWALs(object):
    """Functional tests for

    core._get_wals(
        group_id=ALL_GROUPS,
        precicion=config.round.precision,
        data_frame_flag=False
    )
    """

    def test_no_model_file(
            self, caplog, capsys, ref_deal,
            remove_file, temp_data_dir, terms_sheet):
        core.config.terms_sheet = terms_sheet
        core.config.model.clear()
        with pytest.raises(SystemExit) as wrapped_e:
            core._get_wals()
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 78

        captured = capsys.readouterr()
        assert captured.out == (
            f"\nNo model has been loaded yet. "
            f"Please load a model before continuing.\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # core.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.core'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            f"No model has been loaded yet. "
            f"Please load a model before continuing."
        )
