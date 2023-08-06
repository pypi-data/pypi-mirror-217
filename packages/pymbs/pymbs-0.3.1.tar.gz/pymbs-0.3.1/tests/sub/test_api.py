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
import os

from pandas.util.testing import assert_frame_equal
import pytest

from pymbs import api
from pymbs.exceptions import CollatError


class TestLoadDeal(object):
    """Subcutaneous tests for api.load_deal(series_id)
    """

    def test_no_terms_sheet(self, caplog, capsys, no_deal, no_deal_ts):
        api.config.terms_sheet = None
        with pytest.raises(SystemExit) as wrapped_e:
            api.load_deal(no_deal)
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 66

        captured = capsys.readouterr()
        assert captured.out == (
            f"\nNo Terms Sheet exists for Series {no_deal} at {no_deal_ts}\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # api.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.api'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            f"No Terms Sheet exists for Series {no_deal} at {no_deal_ts}"
        )


class TestLoadAssumedCollat(object):
    """Subcutaneous tests for api.load_assumed_collat()
    """

    def test_load_assumed_collat(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        ref_ac = ref_data('ac')
        test_ac = api.load_assumed_collat()
        assert_frame_equal(test_ac, ref_ac)


class TestLoadModel(object):
    """Subcutaneous tests for api.load_deal()
    """

    def test_no_terms_sheet(self, caplog, capsys):
        api.config.terms_sheet = None
        with pytest.raises(SystemExit) as wrapped_e:
            api.load_model()
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 78

        captured = capsys.readouterr()
        assert captured.out == (
            "\nNo deal has been loaded yet. "
            "Please load a deal before continuing.\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # api.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.api'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            "No deal has been loaded yet. "
            "Please load a deal before continuing."
        )

    def test_no_model_file(
            self, caplog, capsys, ref_deal,
            remove_file, temp_data_dir, terms_sheet):
        api.config.terms_sheet = terms_sheet
        model_file = (
            f"{api.config.project_dir}{os.sep}{ref_deal}{os.sep}"
            f"{ref_deal}_model.json"
        )
        with remove_file(model_file, temp_data_dir):
            with pytest.raises(SystemExit) as wrapped_e:
                api.load_model()
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 66

        captured = capsys.readouterr()
        assert captured.out == (
            f"\nNo Model exists for Series {ref_deal} at {model_file}\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # api.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.api'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            f"No Model exists for Series {ref_deal} at {model_file}"
        )

    def test_load_model(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        test_model = api.load_model()
        ref_model = ref_data('model')
        assert test_model['groups'].keys() == ref_model['groups'].keys()
        assert test_model['indices'].keys() == ref_model['indices'].keys()

        for group in test_model['groups']:
            assert test_model['groups'][group].keys() == \
                ref_model['groups'][group].keys()
            assert test_model['groups'][group]['tranches'].keys() == \
                ref_model['groups'][group]['tranches'].keys()
            if group != 'R':
                ref_keys = [
                    'collat_cf',
                    'collateral',
                    'first_payment_date',
                    'gmc_info',
                    'pricing_speed',
                    'schedules',
                    'tranches',
                    'waterfall'
                ]
                for key in test_model['groups'][group].keys():
                    assert key in ref_keys
                assert len(test_model['groups'][group]['collat_cf']) == 0
                assert test_model['groups'][group]['waterfall'] == \
                    ref_model['groups'][group]['waterfall']
            else:
                assert len(test_model['groups'][group].keys()) == 2
                assert 'tranches' in test_model['groups'][group].keys()


class TestRunCollatCF(object):
    """Subcutaneous tests for
    api.load_deal(group_id=ALL_GROUPS, repline_num=-1)
    """

    def test_run_all_groups(self, ref_data, terms_sheet):
        """Call the function without any arguments.
        This should run the cash flows for all groups in the Terms Sheet
        EXCEPT Group 0 (The Residuals)
        """
        api.config.terms_sheet = terms_sheet
        ref_cf = ref_data('cf_group_all_api')
        test_cf = api.run_collat_cf()
        assert test_cf.keys() == ref_cf.keys()
        for group in test_cf:
            assert test_cf[group].keys() == ref_cf[group].keys()
            for prepay_scenario in test_cf[group]:
                assert_frame_equal(
                    test_cf[group][prepay_scenario],
                    ref_cf[group][prepay_scenario]
                )

    def test_run_one_group(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        ref_cf = ref_data('cf_group_3_api')
        test_cf = api.run_collat_cf(3)
        assert test_cf.keys() == ref_cf.keys()
        for prepay_scenario in test_cf['3']:
            assert_frame_equal(
                test_cf['3'][prepay_scenario],
                ref_cf['3'][prepay_scenario]
            )

    def test_run_two_groups(self, caplog, capsys, terms_sheet):
        """Pass two groups to the function as a list.
        This should NOT be allowed.
        """
        api.config.terms_sheet = terms_sheet
        group_id = [2, 3]
        with pytest.raises(
                CollatError,
                match=(
                    r'Could not locate collateral for Group \'\[2, 3\]\'\.'
                    r' Please check the Terms Sheet.'
                )):
            # Attempt to request running two groups in the deal by passing
            # them to the function call as a list objest.
            # (This shouldn't be allowed.)
            api.run_collat_cf(group_id)

    def test_specific_repline(self, terms_sheet):
        api.config.terms_sheet = terms_sheet
        api.config.terms_sheet['groups']['2']['collateral']['assumed'].append(
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
        api.run_collat_cf(2, 2)


class TestRunWALs(object):
    """Subcutaneous tests for
    api.show_wals(group_id=ALL_GROUPS, precision=config.precision)
    """

    def test_default_precision_group_all(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        api.config.round_precision = 10
        api.load_model()
        ref_wals = ref_data('wals_10dec_group_all_api')
        test_wals = api.run_wals()
        assert test_wals == ref_wals

    def test_rounded_precision_1dec(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        api.load_model()
        ref_wals = ref_data('wals_1dec_group_all_api')
        test_wals = api.run_wals(precision=1)
        assert test_wals == ref_wals

    def test_rounded_precision_5dec_1group(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        api.load_model()
        ref_wals = ref_data('wals_5dec_group_3_api')
        test_wals = api.run_wals(3, 5)
        assert test_wals == ref_wals


class TestLoadTranches(object):
    """Subcutaneous tests for api.load_tranches(group_id=ALL_GROUPS)"""

    def test_no_terms_sheet(self, caplog, capsys):
        api.config.terms_sheet = None
        with pytest.raises(SystemExit) as wrapped_e:
            api.load_model()
        assert wrapped_e.type == SystemExit
        assert wrapped_e.value.code == 78

        captured = capsys.readouterr()
        assert captured.out == (
            "\nNo deal has been loaded yet. "
            "Please load a deal before continuing.\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # api.config.terms_sheet = None.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.api'
        assert caplog.records[1].levelname == 'ERROR'
        assert caplog.records[1].message == (
            "No deal has been loaded yet. "
            "Please load a deal before continuing."
        )

    def test_all_groups(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        ref_tranches = ref_data('tranches_group_all')
        test_tranches = api.load_tranches()
        assert_frame_equal(test_tranches, ref_tranches)

    def test_one_group(self, ref_data, terms_sheet):
        api.config.terms_sheet = terms_sheet
        ref_tranches = ref_data('tranches_group_1')
        test_tranches = api.load_tranches(1)
        assert_frame_equal(test_tranches, ref_tranches)
