# coding: utf-8
from __future__ import unicode_literals

import pytest

from i18naddress import (
    get_field_order, get_validation_rules, load_validation_data)


def test_invalid_country_code():
    with pytest.raises(ValueError):
        load_validation_data('XX')
    with pytest.raises(ValueError):
        load_validation_data('../../../etc/passwd')


def test_dictionary_access():
    data = load_validation_data('US')
    state = data['US/NV']
    assert state['name'] == 'Nevada'


def test_validation_rules_switzerland():
    validation_data = get_validation_rules({'country_code': 'CH'})
    assert validation_data.allowed_fields == {
        'company_name', 'city', 'postal_code', 'street_address', 'name'}
    assert validation_data.required_fields == {
        'city', 'postal_code', 'street_address'}


def test_field_order_poland():
    field_order = get_field_order({'country_code': 'PL'})
    assert field_order == [
        ['name'],
        ['company_name'],
        ['street_address'],
        ['postal_code', 'city']]


def test_field_order_china():
    field_order = get_field_order({'country_code': 'CN'})
    assert field_order == [
        ['postal_code'],
        ['country_area', 'city', 'city_area'],
        ['street_address'],
        ['company_name'],
        ['name']]


@pytest.mark.parametrize('country, levels', [
    ('CN', ['province', 'city', 'district']),
    ('JP', ['prefecture', 'city', 'suburb']),
    ('KR', ['do_si', 'city', 'district'])])
def test_locality_types(country, levels):
    validation_data = get_validation_rules({'country_code': country})
    assert validation_data.country_area_type == levels[0]
    assert validation_data.city_type == levels[1]
    assert validation_data.city_area_type == levels[2]
