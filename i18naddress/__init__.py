from collections import defaultdict
import json
import os
import re

COUNTRIES_VALIDATION_DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'countries_validation_data')


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
