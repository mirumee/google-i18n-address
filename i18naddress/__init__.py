from __future__ import unicode_literals

from collections import namedtuple
import json

import os
import re

VALID_COUNTRY_CODE = re.compile(r'^\w{2,3}$')
VALIDATION_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data') 
VALIDATION_DATA_PATH = os.path.join(VALIDATION_DATA_DIR, '%s.json')

FIELD_MAPPING = {
    'A': 'street_address',
    'C': 'city',
    'D': 'city_area',
    'N': 'name',
    'O': 'company_name',
    'S': 'country_area',
    'X': 'sorting_code',
    'Z': 'postal_code'}

KNOWN_FIELDS = set(FIELD_MAPPING.values()) | {'country_code'}


def load_validation_data(country_code='all'):
    if not VALID_COUNTRY_CODE.match(country_code):
        raise ValueError(
            '%r is not a valid country code' % (country_code,))
    country_code = country_code.lower()
    path = VALIDATION_DATA_PATH % (country_code,)
    if not os.path.exists(path):
        raise ValueError(
            '%r is not a valid country code' % (country_code,))
    with open(path) as data:
        return json.load(data)


ValidationRules = namedtuple(
    'ValidationRules', [
        'country_name',
        'address_format', 'address_latin_format',
        'allowed_fields', 'required_fields', 'upper_fields',
        'country_area_type', 'country_area_choices',
        'city_type', 'city_choices',
        'city_area_type', 'city_area_choices',
        'postal_code_type', 'postal_code_matchers', 'postal_code_examples',
        'postal_code_prefix'])


def _make_choices(rules, translated=False):
    sub_keys = rules.get('sub_keys')
    if not sub_keys:
        return []
    choices = []
    sub_keys = sub_keys.split('~')
    sub_names = rules.get('sub_names')
    if sub_names:
        choices += [
            (key, value)
            for key, value in zip(sub_keys, sub_names.split('~'))
            if value]
    else:
        if not translated:
            choices += [(key, key) for key in sub_keys]
    if not translated:
        sub_lnames = rules.get('sub_lnames')
        if sub_lnames:
            choices += [
                (key, value)
                for key, value in zip(sub_keys, sub_lnames.split('~'))
                if value]
        sub_lfnames = rules.get('sub_lfnames')
        if sub_lfnames:
            choices += [
                (key, value)
                for key, value in zip(sub_keys, sub_lfnames.split('~'))
                if value]
    return choices


def _match_choices(value, choices):
    if value:
        value = value.strip().lower()
    for name, label in choices:
        if name.lower() == value:
            return name
        if label.lower() == value:
            return name


def _load_country_data(country_code):
    database = load_validation_data('zz')
    country_data = database['ZZ']
    if country_code:
        country_code = country_code.upper()
        if country_code.lower() == 'zz':
            raise ValueError(
                '%r is not a valid country code' % (country_code,))
        database = load_validation_data(country_code.lower())
        country_data.update(database[country_code])
    return country_data, database


def get_validation_rules(address):
    country_code = address.get('country_code', '').upper()
    country_data, database = _load_country_data(country_code)
    country_name = country_data.get('name', '')
    address_format = country_data['fmt']
    address_latin_format = country_data.get('lfmt', address_format)
    format_fields = re.finditer(r'%([ACDNOSXZ])', address_format)
    allowed_fields = {FIELD_MAPPING[m.group(1)] for m in format_fields}
    required_fields = {FIELD_MAPPING[f] for f in country_data['require']}
    upper_fields = {FIELD_MAPPING[f] for f in country_data['upper']}
    languages = []
    if 'languages' in country_data:
        languages = country_data['languages'].split('~')
        languages.remove(country_data['lang'])

    postal_code_matchers = []
    if 'postal_code' in required_fields:
        if 'zip' in country_data:
            postal_code_matchers.append(
                re.compile('^' + country_data['zip'] + '$'))
    postal_code_examples = country_data.get('zipex')

    city_choices = []
    city_area_choices = []
    country_area_type = country_data['state_name_type']
    city_type = country_data['locality_name_type']
    city_area_type = country_data['sublocality_name_type']
    postal_code_type = country_data['zip_name_type']
    postal_code_prefix = country_data.get('postprefix', '')
    # second level of data is for administrative areas
    country_area_choices = _make_choices(country_data)
    for language in languages:
        localized_country_data = database['%s--%s' % (
            country_code, language)]
        country_area_choices += _make_choices(
            localized_country_data, translated=True)
    country_area = _match_choices(
        address.get('country_area'), country_area_choices)
    if country_area:
        # third level of data is for cities
        country_area_data = database['%s/%s' % (
            country_code, country_area)]
        if 'zip' in country_area_data:
            postal_code_matchers.append(
                re.compile('^' + country_area_data['zip']))
        if 'zipex' in country_area_data:
            postal_code_examples = country_area_data['zipex']
        city_choices = _make_choices(country_area_data)
        for language in languages:
            localized_country_area_data = database['%s/%s--%s' % (
                country_code, country_area, language)]
            city_choices += _make_choices(
                localized_country_area_data, translated=True)
        city = _match_choices(
            address.get('city'), city_choices)
        if city:
            # fourth level of data is for dependent sublocalities
            city_data = database['%s/%s/%s' % (
                country_code, country_area, city)]
            if 'zip' in city_data:
                postal_code_matchers.append(
                    re.compile('^' + city_data['zip']))
            if 'zipex' in city_data:
                postal_code_examples = city_data['zipex']
            city_area_choices = _make_choices(city_data)
            for language in languages:
                localized_city_data = database['%s/%s/%s--%s' % (
                    country_code, country_area, city, language)]
                city_area_choices += _make_choices(
                    localized_city_data, translated=True)
    return ValidationRules(
        country_name,
        address_format, address_latin_format,
        allowed_fields, required_fields, upper_fields,
        country_area_type, country_area_choices,
        city_type, city_choices,
        city_area_type, city_area_choices,
        postal_code_type, postal_code_matchers, postal_code_examples,
        postal_code_prefix)


class InvalidAddress(ValueError):
    def __init__(self, message, errors):
        super(InvalidAddress, self).__init__(message)
        self.errors = errors


def _normalize_field(name, rules, data, choices, errors):
    value = data.get(name)
    if name not in rules.allowed_fields:
        data[name] = ''
    elif not value and name in rules.required_fields:
        errors[name] = 'required'
    elif choices:
        value = _match_choices(value, choices)
        if value is not None:
            data[name] = value
        else:
            errors[name] = 'invalid'
    if not value:
        data[name] = ''


def normalize_address(address):
    errors = {}
    try:
        rules = get_validation_rules(address)
    except ValueError:
        errors['country_code'] = 'invalid'
    else:
        cleaned_data = address.copy()
        country_code = cleaned_data.get('country_code')
        if not country_code:
            errors['country_code'] = 'required'
        else:
            cleaned_data['country_code'] = country_code.upper()
        _normalize_field(
            'country_area', rules, cleaned_data, rules.country_area_choices,
            errors)
        _normalize_field(
            'city', rules, cleaned_data, rules.city_choices, errors)
        _normalize_field(
            'city_area', rules, cleaned_data, rules.city_area_choices, errors)
        _normalize_field(
            'postal_code', rules, cleaned_data, [], errors)
        postal_code = address.get('postal_code', '')
        if rules.postal_code_matchers and postal_code:
            for matcher in rules.postal_code_matchers:
                if not matcher.match(postal_code):
                    errors['postal_code'] = 'invalid'
                    break
        _normalize_field(
            'street_address', rules, cleaned_data, [], errors)
        _normalize_field(
            'sorting_code', rules, cleaned_data, [], errors)
    if errors:
        raise InvalidAddress('Invalid address', errors)
    return cleaned_data


def _format_address_line(line_format, address, rules):

    def _get_field(name):
        value = address.get(name, '')
        if name in rules.upper_fields:
            value = value.upper()
        return value
    replacements = {'%%%s' % code: _get_field(field_name)
                    for code, field_name in FIELD_MAPPING.items()}

    fields = re.split('(%.)', line_format)
    fields = [replacements.get(f, f) for f in fields]
    return ''.join(fields).strip()


def get_field_order(address, latin=False):
    """
    Returns expected order of address form fields as a list of lists.
    Example for PL:
    >>> get_field_order({'country_code': 'PL'})
    [[u'name'], [u'company_name'], [u'street_address'], [u'postal_code', u'city']]
    """
    rules = get_validation_rules(address)
    address_format = (
        rules.address_latin_format if latin else rules.address_format)
    address_lines = address_format.split('%n')
    replacements = {'%%%s' % code: field_name
                    for code, field_name in FIELD_MAPPING.items()}
    all_lines = []
    for line in address_lines:
        fields = re.split('(%.)', line)
        single_line = [replacements.get(field) for field in fields]
        single_line = list(filter(None, single_line))
        all_lines.append(single_line)
    return all_lines


def format_address(address, latin=False):
    rules = get_validation_rules(address)
    address_format = (
        rules.address_latin_format if latin else rules.address_format)
    address_line_formats = address_format.split('%n')
    address_lines = [
        _format_address_line(lf, address, rules)
        for lf in address_line_formats]
    address_lines.append(rules.country_name)
    address_lines = filter(None, address_lines)
    return '\n'.join(address_lines)


def latinize_address(address, normalized=False):
    if not normalized:
        address = normalize_address(address)
    cleaned_data = address.copy()
    country_code = address.get('country_code', '').upper()
    dummy_country_data, database = _load_country_data(country_code)
    if country_code:
        country_area = address['country_area']
        if country_area:
            key = '%s/%s' % (country_code, country_area)
            country_area_data = database.get(key)
            if country_area_data:
                cleaned_data['country_area'] = country_area_data.get(
                    'lname',
                    country_area_data.get('name', country_area))
                city = address['city']
                key = '%s/%s/%s' % (country_code, country_area, city)
                city_data = database.get(key)
                if city_data:
                    cleaned_data['city'] = city_data.get(
                        'lname',
                        city_data.get('name', city))
                    city_area = address['city_area']
                    key = '%s/%s/%s/%s' % (
                        country_code, country_area, city, city_area)
                    city_area_data = database.get(key)
                    if city_area_data:
                        cleaned_data['city_area'] = city_data.get(
                            'lname',
                            city_area_data.get('name', city_area))
    return cleaned_data
