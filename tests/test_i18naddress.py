from __future__ import unicode_literals
import json
import pytest
import re

from i18naddress import I18nCountryData

PL_DATA = {
    'PL': {'name': 'POLAND', 'zip': '\d{2}-\d{3}', 'require': 'ACZ',
           'sub_keys': 'D~L', 'sub_names': 'Lower Silesian~Lublin'},
    'PL/D': {'name': 'Lower Silesia', 'zip': '\d{2}-\d{3}', 'zipex': '58-580'}
}

US_DATA = {
    'US': {'zip': '(\d{5})(?:[ \-](\d{4}))?', 'name': 'UNITED STATES'}
}

ALL_DATA = dict(PL_DATA, **US_DATA)


@pytest.fixture(autouse=True)
def save_test_data(tmpdir):
    data_dir = tmpdir.join('data')
    json.dump(ALL_DATA, data_dir.join('all.json').open('w'))
    json.dump(PL_DATA, data_dir.join('pl.json').open('w'))
    json.dump(US_DATA, data_dir.join('us.json').open('w'))


@pytest.mark.parametrize('i18n_key, data', [
    ('PL', PL_DATA),
    ('US', US_DATA),
    ('ALL', ALL_DATA),
    pytest.mark.xfail(('DE', None), raises=ValueError),
    pytest.mark.xfail((None, None), raises=ValueError)
])
def test_country_code(i18n_key, data):
    i18n_data = I18nCountryData(i18n_key)
    assert i18n_data._data == data


def test_without_country_code():
    i18n_data = I18nCountryData()
    assert i18n_data._data == ALL_DATA


@pytest.mark.parametrize('i18n_key, data_key', [
    ('PL', 'PL'),
    (('PL', 'D'), 'PL/D'),
    ('US', 'US'),
    pytest.mark.xfail(('DE', 'DE'), raises=KeyError)
])
def test_get_item(i18n_key, data_key):
    i18n_data = I18nCountryData()
    assert i18n_data[i18n_key] == ALL_DATA[data_key]


def test_iterator():
    i18n_data = I18nCountryData('US')
    keys = [key for key, val in i18n_data]
    assert keys == ['US']


@pytest.mark.parametrize('validation_args, validation_data', [
    (('PL',), {'sub_area_keys': ['D', 'L'],
               'require': ('street_address', 'city', 'postal_code'),
               'postal_code_regexp': re.compile(
                   PL_DATA['PL']['zip'], re.IGNORECASE),
               'sub_area_choices': [('D', 'Lower Silesian'), ('L', 'Lublin')]}),
    (('PL', 'D'), {'sub_area_keys': [], 'sub_area_choices': [],
                   'postal_code_regexp': re.compile(
                       PL_DATA['PL']['zip'], re.IGNORECASE),
                   'postal_code_example': '58-580',})
])
def test_get_validation_dict(validation_args, validation_data):
    i18n_data = I18nCountryData()
    assert i18n_data.get_validation_dict(*validation_args) == validation_data
