# coding: utf-8
from __future__ import unicode_literals
import pytest
import re

from i18naddress import I18nCountryData


def test_invalid_country_code():
    with pytest.raises(ValueError):
        I18nCountryData('XX')
    with pytest.raises(ValueError):
        I18nCountryData('../../../etc/passwd')


def test_iterationt():
    data = I18nCountryData('PL')
    data = list(data)
    assert len(data) == 1
    assert data[0][0] == 'PL'


def test_dictionary_access():
    data = I18nCountryData('US')
    state = data['US/NV']
    assert state['name'] == 'Nevada'
    state = data[('US', 'CA')]
    assert state['name'] == 'California'


def test_validation_data_switzerland():
    validation_data = I18nCountryData('CH').get_validation_dict('CH')
    assert validation_data == {
        'require': {'street_address', 'city', 'postal_code'},
        'postal_code_regexp': re.compile(r'\d{4}', re.IGNORECASE),
        'postal_code_example': '2544,1211,1556,3030',
        'sub_area_keys': {
            'AG', 'AR', 'AI', 'BL', 'BS', 'BE', 'FR', 'GE', 'GL', 'GR', 'JU',
            'LU', 'NE', 'NW', 'OW', 'SH', 'SZ', 'SO', 'SG', 'TI', 'TG', 'UR',
            'VD', 'VS', 'ZG', 'ZH'},
        'sub_area_choices': [
            ('AG', 'Aargau'), ('AR', 'Appenzell Ausserrhoden'),
            ('AI', 'Appenzell Innerrhoden'), ('BL', 'Basel-Landschaft'),
            ('BS', 'Basel-Stadt'), ('BE', 'Bern'), ('FR', 'Freiburg'),
            ('GE', 'Genf'), ('GL', 'Glarus'), ('GR', 'Graubünden'),
            ('JU', 'Jura'), ('LU', 'Luzern'), ('NE', 'Neuenburg'),
            ('NW', 'Nidwalden'), ('OW', 'Obwalden'), ('SH', 'Schaffhausen'),
            ('SZ', 'Schwyz'), ('SO', 'Solothurn'), ('SG', 'St. Gallen'),
            ('TI', 'Tessin'), ('TG', 'Thurgau'), ('UR', 'Uri'),
            ('VD', 'Waadt'), ('VS', 'Wallis'), ('ZG', 'Zug'),
            ('ZH', 'Zürich')]}
    validation_data = I18nCountryData('CH').get_validation_dict('CH', 'ZH')
    assert validation_data == {
        'sub_area_keys': set(),
        'sub_area_choices': []}
