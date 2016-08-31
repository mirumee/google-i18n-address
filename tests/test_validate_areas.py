from __future__ import unicode_literals
import json
import re
import pytest

try:
    from unittest import mock
except ImportError:
    import mock

from i18naddress import validate_areas, ValidationData

PL_DATA = {
    'PL': {'name': 'POLAND', 'zip': '\d{2}-\d{3}', 'sub_keys': 'D', 'sub_names': 'Lower Silesian'},  # noqa
    'PL/D': {'name': 'Lower Silesia', 'zip': '53-\d{3}', 'sub_names': 'Wroclaw', 'sub_keys': 'WRO'},  # noqa
    'PL/D/WRO': {'name': 'Wroclaw', 'sub_names': 'Altstadt~Oder Stadtteil', 'sub_keys': 'AS~OS'},  # noqa
    'PL/D/WRO/AS': {'name': 'Altstad'},
    'PL/D/WRO/OS': {'name': 'Oder Stadtteil'}
}

ALL_REQUIRE = {
    'AR': {'require': 'ACDNOSZ'}
}

@pytest.fixture(autouse=True)
def save_test_data(tmpdir):
    data_dir = tmpdir.join('data')
    json.dump(ALL_REQUIRE, data_dir.join('ar.json').open('w'))
    json.dump(PL_DATA, data_dir.join('pl.json').open('w'))


@pytest.mark.parametrize('kwargs, errors', [
    ({'country_code': 'DE'}, {'country_code': 'invalid'}),
    ({'country_code': 'AR'},
     {'country_area': 'required', 'city': 'required', 'city_area': 'required',
      'postal_code': 'required', 'street_address': 'required'}),
    ({'country_code': 'PL', 'country_area': 'Invalid'},
     {'country_area': 'invalid_choice'}),
    ({'country_code': 'PL', 'country_area': 'D', 'city': 'Invalid'},
     {'city': 'invalid_choice'}),
    ({'country_code': 'PL', 'country_area': 'D', 'city': 'WRO', 'city_area': 'Invalid'},
     {'city_area': 'invalid_choice'}),
    ({'country_code': 'PL', 'country_area': 'D', 'city': 'WRO', 'city_area': 'AS',
      'postal_code': '53-335', 'street_address': 'Ab'}, {}),
    ({'country_code': 'PL', 'postal_code': '77-777'}, {}),
    ({'country_code': 'PL', 'country_area': 'D', 'postal_code': '77-777'},
     {'postal_code': 'invalid'}),
    ({'country_code': 'PL', 'postal_code': '77777'}, {'postal_code': 'invalid'}),
])
def test_validate_areas_errors(kwargs, errors):
    assert validate_areas(**kwargs)[0] == errors


def test_validation_data():
    validation_data = validate_areas(
        country_code='PL', country_area='D', city='WRO', city_area='AS')[1]
    assert validation_data == ValidationData(
        require=[], postal_code_regexp=re.compile(
            '53-\\d{3}', re.IGNORECASE), postal_code_example=None,
        country_area_keys=['D'], country_area_choices=[('D', 'Lower Silesian')],
        city_keys=['WRO'], city_choices=[('WRO', 'Wroclaw')],
        city_area_keys=['AS', 'OS'], city_area_choices=[
            ('AS', 'Altstadt'), ('OS', 'Oder Stadtteil')])
