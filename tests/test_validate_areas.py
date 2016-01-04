from __future__ import unicode_literals
import json
import pytest

try:
    from unittest import mock
except ImportError:
    import mock

from i18naddress import validate_areas

PL_DATA = {
    'PL': {'name': 'POLAND', 'zip': '\d{2}-\d{3}', 'require': 'ACZ',
           'sub_keys': 'D~L', 'sub_names': 'Lower Silesian~Lublin'},
    'PL/D': {'name': 'Lower Silesia', 'zip': '\d{2}-\d{3}', 'zipex': '58-580'}
}

ALL_DATA = dict(PL_DATA)

@pytest.fixture(autouse=True)
def save_test_data(tmpdir):
    data_dir = tmpdir.join('data')
    json.dump(ALL_DATA, data_dir.join('all.json').open('w'))
    json.dump(PL_DATA, data_dir.join('pl.json').open('w'))


@pytest.mark.parametrize('kwargs, errors', [
    ({'country_code': 'DE'}, {'country': 'invalid'}),
    ({'country_code': 'PL'},
     {'city': 'required', 'postal_code': 'required', 'street_address': 'required'}),
    ({'country_code': 'PL', 'postal_code': '77777'},
     {'city': 'required', 'postal_code': 'invalid', 'street_address': 'required'}),
    ({'country_code': 'PL', 'postal_code': '58-580'},
     {'city': 'required', 'street_address': 'required'}),
    ({'country_code': 'PL', 'postal_code': '53-335', 'city': 'Wroclaw'},
     {'street_address': 'required'}),
    ({'country_code': 'PL', 'postal_code': '53-335',
      'city': 'Wroclaw', 'street_address': 'Ab'},{}),

])
def test_validate_areas_errors(kwargs, errors):
    assert validate_areas(**kwargs)[0] == errors
