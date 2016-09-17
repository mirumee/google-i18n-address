# coding: utf-8
from __future__ import unicode_literals
import pytest

from i18naddress import validate_areas

@pytest.mark.parametrize('kwargs, errors', [
    ({'country_code': 'AR'},
     {}),
    ({'country_code': 'CN', 'country_area': '北京市', 'postal_code': '100084',
      'city': 'Invalid', 'street_address': '中关村东路1号'},
     {'city': 'invalid_choice'}),
    ({'country_code': 'DE', 'city': 'Berlin', 'postal_code': '77-777',
      'street_address': 'Kurfurstendamm 1'},
     {'postal_code': 'invalid'}),
    ({'country_code': 'PL', 'city': 'Warszawa', 'postal_code': '00-374',
      'street_address': 'Aleje Jerozolimskie 2'},
     {}),
    ({'country_code': 'PL', 'city': 'Wrocław', 'postal_code': '77777',
      'street_address': 'Tęczowa 7'},
     {'postal_code': 'invalid'}),
    ({'country_code': 'XX'},
     {'country': 'invalid'})])
def test_validate_areas_errors(kwargs, errors):
    assert validate_areas(**kwargs)[0] == errors
