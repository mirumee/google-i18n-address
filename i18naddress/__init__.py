from collections import defaultdict
import json
import os
import re

COUNTRIES_VALIDATION_DATA_DIR = os.path.join(
    os.path.dirname(__file__), 'data')


class I18nCountryData(object):

    REQUIRE_MAPPING = (
        ('A', 'street_address'),
        ('C', 'city'),
        ('D', 'city_area'),
        ('N', 'name'),
        ('O', 'company_name'),
        ('S', 'country_area'),
        ('Z', 'postal_code'))
    COUNTRY_VALIDATION_PATH = os.path.join(
        COUNTRIES_VALIDATION_DATA_DIR, '%s.json')

    def __init__(self, country_code='all'):
        try:
            country_code = country_code.lower()
        except ArithmeticError:
            raise ValueError('Wrong country code.')
        try:
            self._data = defaultdict(dict, json.load(
                open(self.COUNTRY_VALIDATION_PATH % country_code)))
        except IOError:
            raise ValueError(
                '%s is not supported country code' % country_code)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            item = '/'.join(item)
        return self._data[item]

    def get_validation_dict(self, *args, **kwargs):
        area_choices_prefix = kwargs.get(
            'sub_area_prefix', 'sub_area')
        country_data = self[args]
        sub_area_keys = country_data.get('sub_keys')
        sub_area_names = country_data.get(
            'sub_lnames', country_data.get('sub_names', sub_area_keys))
        if sub_area_keys:
            sub_area_keys = sub_area_keys.split('~')
            sub_area_choices = zip(
                sub_area_keys, sub_area_names.split('~'))
        else:
            sub_area_keys = []
            sub_area_choices = []
        validation_data = {
            area_choices_prefix + '_choices': sub_area_choices,
            area_choices_prefix + '_keys': sub_area_keys}
        if 'zip' in country_data:
            validation_data['postal_code_regexp'] = re.compile(
                country_data['zip'])
        if 'zipex' in country_data:
            validation_data['postal_code_example'] = country_data['zipex']
        if 'require' in country_data:
            require_mapping = dict(self.REQUIRE_MAPPING)
            validation_data['require'] = tuple(
                require_mapping[l] for l in country_data['require'])
        return validation_data


def validate_areas(country_code, country_area=None, city=None, city_area=None,
                   postal_code=None, street_address=None):
    validation_data = {
        'country_area_keys': [], 'city_keys': [], 'city_area_keys': [],
        'postal_code_regexp': None, 'postal_code_example': None,
        'require': []}
    errors = {}
    try:
        i18n_country_data = I18nCountryData(country_code)
    except ValueError:
        errors['country'] = 'invalid'
    else:
        validation_data.update(i18n_country_data.get_validation_dict(
            country_code, sub_area_prefix='country_area'))

        if validation_data['country_area_keys'] and country_area:
            if country_area not in validation_data['country_area_keys']:
                errors['country_area'] = 'invalid_choice'
            else:
                validation_data.update(i18n_country_data.get_validation_dict(
                    country_code, country_area,
                    sub_area_prefix='city'))

        if validation_data['city_keys'] and city:
            if city not in validation_data['city_keys']:
                errors['city'] = 'invalid_choice'
            else:
                validation_data.update(i18n_country_data.get_validation_dict(
                    country_code, country_area, city,
                    sub_area_prefix='city_area'))

        if validation_data['city_area_keys'] and city_area:
            if city_area not in validation_data['city_area_keys']:
                errors['city_area'] = 'invalid_choice'
            else:
                validation_data.update(i18n_country_data.get_validation_dict(
                    country_code, country_area, city))

        if validation_data['postal_code_regexp'] and postal_code:
            if not validation_data['postal_code_regexp'].match(postal_code):
                errors['postal_code'] = 'invalid'

        required_fields = validation_data['require']
        if not street_address and 'street_address' in required_fields:
            errors['street_address'] = 'required'
        if not city and 'city' in required_fields:
            errors['city'] = 'required'
        if not city_area and 'city_area' in required_fields:
            errors['city_area'] = 'required'
        if not country_area and 'country_area' in required_fields:
            errors['country_area'] = 'required'
        if not postal_code and 'postal_code' in required_fields:
            errors['postal_code'] = 'required'

    return errors, validation_data
