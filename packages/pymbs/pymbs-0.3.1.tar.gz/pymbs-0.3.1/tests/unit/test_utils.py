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

import decimal
import json

from pymbs import utils

"""
NOTE: The coverage report for the pymbs.utils module shows 72% coverage.
All of the line numbers shown in the "Missing" column of the report, with
the exception of the last one, refer to the _parse_waterfall and
_parse_expression functions. These two functions provide some very basic
parsing functionality to PyMBS in lieu of using a DSL and related DSL parser.

We expect these functions to 1. Remain unchanged until and 2. Be removed when
we implement the DSL for PyMBS, so we are not going to expend effort to test
these two functions in the interim.
"""


class TestRoundDec(object):
    """Unit tests for
    utils._round_dec(decimal_value, precision=config.round_precision)
    """

    def test_precision_exceeded_rounding(
            self, caplog, capsys, ref_data, terms_sheet):
        utils.config.terms_sheet = terms_sheet
        ctx = decimal.getcontext()
        ctx.prec = 18
        ctx.Emax = 12
        ctx.Emin = -10
        round_to = 18
        test_value = decimal.Decimal('12.1234567890123456')

        utils._round_dec(test_value, 18)

        captured = capsys.readouterr()
        max_allowed_precision = 16
        config_url = "https://brianfarrell.gitlab.io/pymbs/pymbs.config.html"
        quantize_url = (
            "https://docs.python.org/3/library/decimal.html"
            "#decimal.Decimal.quantize"
        )

        assert captured.out == (
            f"\nYou have requested that the decimal value {test_value} "
            f"be rounded to {round_to} places, but the total precision "
            f"allowed by your PyMBS configuration is {ctx.prec}.  "
            f"The resulting value would be nonsensical, so PyMBS has rounded "
            f"the value to {max_allowed_precision} places instead.\n\n"
            f"For more information on configuring PyMBS, please see "
            f"{config_url}\n\n"
            f"For more information on the error encountered, please see "
            f"{quantize_url}\n\n"
        )

        # There will be 2 log records. The first one will be for setting
        # core.config.terms_sheet.  The second one will be for
        # the expected error in this test.
        assert len(caplog.records) == 2
        assert caplog.records[1].name == 'pymbs.utils'
        assert caplog.records[1].levelname == 'WARNING'
        assert caplog.records[1].message == (
            f"You have requested that the decimal value {test_value} "
            f"be rounded to {round_to} places, but the total precision "
            f"allowed by your PyMBS configuration is {ctx.prec}.  "
            f"The resulting value would be nonsensical, so PyMBS has rounded "
            f"the value to {max_allowed_precision} places instead. "
            f"For more information on configuring PyMBS, please see "
            f"{config_url} "
            f"For more information on the error encountered, please see "
            f"{quantize_url}"
        )


class TestDecimalEncoder(object):
    """Unit tests for
    utils.DecimalEncoder(o)
    """

    def test_default_encoding(self):
        test_decimal = decimal.Decimal('12.12345')
        test_float = 21.54321
        test_string = '12.67890'
        test_list = ['a', 1, 'b', 2, 'c', '3']
        test_dict = {
            "td": test_decimal,
            "tf": test_float,
            "ts": test_string,
            "tl": test_list
        }

        test_object = {
            "test_decimal": test_decimal,
            "test_float": test_float,
            "test_string": test_string,
            "test_list": test_list,
            "test_dict": test_dict
        }

        test_json_serialized = json.dumps(
            test_object, cls=utils.DecimalEncoder, separators=(',', ':'))

        test_json_deserialized = json.loads(test_json_serialized)

        assert type(test_json_deserialized['test_decimal']) == str
        assert type(test_json_deserialized['test_float']) == float
        assert type(test_json_deserialized['test_string']) == str
        assert type(test_json_deserialized['test_list']) == list
        assert type(test_json_deserialized['test_dict']) == dict
        assert type(test_json_deserialized['test_dict']['td']) == str
        assert type(test_json_deserialized['test_dict']['tf']) == float
        assert type(test_json_deserialized['test_dict']['ts']) == str
        assert type(test_json_deserialized['test_dict']['tl']) == list

        assert test_json_deserialized['test_decimal'] == '12.12345'
        assert test_json_deserialized['test_dict']['td'] == '12.12345'
