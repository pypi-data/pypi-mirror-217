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

from decimal import Decimal as dec

from pandas.util.testing import assert_frame_equal
import pytest

from pymbs import core
from pymbs.exceptions import AssumedCollatError, CollatError


class TestLoadAssumedCollat(object):
    """Unit tests for core._load_assumed_collat()
    """

    def test_load_assumed_collat(self, ref_data, terms_sheet):
        ref_ac = ref_data('ac')
        test_ac = core._load_assumed_collat()
        assert_frame_equal(ref_ac, test_ac)

    def test_no_terms_sheet(self, caplog, capsys):
        core.config.terms_sheet = None
        with pytest.raises(SystemExit) as wrapped_e:
            core._load_assumed_collat()
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 78

        captured = capsys.readouterr()
        assert captured.out == (
            "\nNo deal has been loaded yet. "
            "Please load a deal before continuing.\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # core.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.core'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            "No deal has been loaded yet. "
            "Please load a deal before continuing."
        )


class TestLoadPrepaymentScenarios(object):
    """Unit tests for core._load_prepayment_scenarios(series_id, group_id)
    """

    def test_load_prepayment_scenarios(self, project_dir, terms_sheet):
        core.config.project_dir = project_dir
        core.config.terms_sheet = terms_sheet
        series_id = core.config.terms_sheet['deal']['series_id']
        group_id = "3"
        ref_dict = {
            "group_id": "3",
            "prepayment_benchmark": "PSA",
            "speeds": ["0", "100", "300", "485", "750", "1000"]
        }

        scenario_group = core._load_prepayment_scenarios(series_id, group_id)
        assert ref_dict == scenario_group

    def test_no_pps_json(self, caplog, capsys, empty_project, terms_sheet):
        series_id = core.config.terms_sheet['deal']['series_id']
        group_id = "3"
        core.config.project_dir = empty_project

        with pytest.raises(SystemExit) as wrapped_e:
            core._load_prepayment_scenarios(series_id, group_id)

        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 66

        captured = capsys.readouterr()
        assert captured.out == (
            f"\nNo Prepayment Scenario exists for Series "
            f"{series_id} at "
            f"{empty_project}/{series_id}/{series_id}_pps.json\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # core.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.core'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            f"No Prepayment Scenario exists for Series "
            f"{series_id} at {empty_project}/{series_id}/{series_id}_pps.json"
        )

    def test_group_missing(self, project_dir, terms_sheet):
        core.config.project_dir = project_dir
        core.config.terms_sheet = terms_sheet
        series_id = core.config.terms_sheet['deal']['series_id']
        missing_group = "5"

        scenario_group = core._load_prepayment_scenarios(
            series_id, missing_group
        )
        assert scenario_group is None


class TestRunCollatCf(object):
    """Unit tests for core._run_collat_cf(group_id, repline_num=0)
    """

    @pytest.mark.xfail(reason="Issue #1")
    def test_multi_repline_group(self, terms_sheet):
        core.config.terms_sheet = terms_sheet
        core.config.terms_sheet['assumed_collateral']['data'].insert(
            2, ["2", 2, dec(42000000.0), dec(4.5), 180, dec(5.125), 176, 3]
        )
        core._run_collat_cf("2")

    def test_specific_repline(self, terms_sheet):
        core.config.terms_sheet = terms_sheet
        core.config.terms_sheet['groups']['2']['collateral']['assumed'].append(
            {
                "repline": dec("2"),
                "upb": dec("42000000"),
                "coupon": dec("4.5"),
                "original_term": dec("180"),
                "wac": dec("5.125"),
                "wam": dec("176"),
                "wala": dec("3")
            }
        )
        core._run_collat_cf(2, 2)

    def test_group_missing(self, terms_sheet):
        core.config.terms_sheet = terms_sheet
        with pytest.raises(
                CollatError,
                match=(
                    r'Could not locate collateral for Group \'5\'\.'
                    r' Please check the Terms Sheet.'
                )):
            core._run_collat_cf(5)

    def test_repline_missing(self, terms_sheet):
        core.config.terms_sheet = terms_sheet
        with pytest.raises(AssumedCollatError, match=r".*2 for Group '2'.*"):
            core._run_collat_cf(2, 2)


class TestRunReplineCf(object):
    """Unit tests for core._run_repline_cf(repline)
    """
