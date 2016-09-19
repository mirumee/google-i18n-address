# coding: utf-8
from __future__ import unicode_literals
import pytest

from i18naddress import validate_areas

@pytest.mark.parametrize('kwargs, errors', [
    ({'country_code': 'AR'},
     {}),
    ({'country_code': 'CH', 'country_area': 'Invalid', 'city': 'Zürich',
      'postal_code': '8022', 'street_address': 'Kappelergasse 1'},
     {'country_area': 'invalid_choice'}),
    ({'country_code': 'CN', 'country_area': '北京市', 'postal_code': '100084',
      'city': 'Invalid', 'street_address': '中关村东路1号'},
     {'city': 'invalid_choice'}),
    ({'country_code': 'CN', 'country_area': '云南省', 'postal_code': '677400',
      'city': '临沧市', 'city_area': 'Invalid', 'street_address': '...'},
     {'city_area': 'invalid_choice'}),
    ({'country_code': 'DE', 'city': 'Berlin', 'postal_code': '77-777',
      'street_address': 'Kurfurstendamm 1'},
     {'postal_code': 'invalid'}),
    ({'country_code': 'PL', 'city': 'Wrocław', 'postal_code': '77777',
      'street_address': 'Tęczowa 7'},
     {'postal_code': 'invalid'}),
    ({'country_code': 'KR'},
     {'country_area': 'required', 'postal_code': 'required',
      'city': 'required', 'street_address': 'required'}),
    ({'country_code': 'XX'},
     {'country': 'invalid'})])
def test_validate_areas_errors(kwargs, errors):
    assert validate_areas(**kwargs)[0] == errors


@pytest.mark.parametrize('kwargs', [
    {'country_code': 'CN', 'country_area': '北京市', 'postal_code': '100084',
      'city': '海淀区', 'street_address': '中关村东路1号'},
    {'country_code': 'CN', 'country_area': '云南省', 'postal_code': '677400',
      'city': '临沧市', 'city_area': '凤庆县', 'street_address': '中关村东路1号'},
    {'country_code': 'KR', 'country_area': '서울특별시', 'postal_code': '135-984',
      'city': '강남구', 'street_address': '역삼동 737번지 강남파이낸스센터'},
    {'country_code': 'PL', 'city': 'Warszawa', 'postal_code': '00-374',
      'street_address': 'Aleje Jerozolimskie 2'}])
def test_validate_known_addresses(kwargs):
    assert validate_areas(**kwargs)[0] == {}
