# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os

import pytest


@pytest.fixture()
def i18n_data_dir(mocker, tmpdir):
    manager_dict = {'PL': 'datą', 'US': 'data'}
    all_countries = ['PL', 'US']
    data_dir = tmpdir.join('data')
    mocker.patch('multiprocessing.pool.ThreadPool')
    mocker.patch('i18naddress.downloader.work_queue')
    mocker.patch('i18naddress.downloader.get_countries', new=lambda: all_countries)
    mocker.patch(
        'i18naddress.downloader.COUNTRIES_VALIDATION_DATA_DIR',
        new=str(data_dir))
    mocker.patch(
        'i18naddress.downloader.COUNTRY_PATH',
        os.path.join(str(data_dir), '%s.json'))
    manager = mocker.patch('i18naddress.downloader.manager')
    manager.dict.return_value = manager_dict
    return data_dir


@pytest.mark.parametrize('country, file_names, data', [
    (None, ('pl.json', 'us.json', 'all.json'), {
        'pl.json': {'PL': 'datą'},
        'us.json': {'US': 'data'},
        'all.json': {'PL': 'datą', 'US': 'data'}}),
    ('PL', ('pl.json', 'all.json'), {
        'pl.json': {'PL': 'datą'},
        'all.json': {'PL': 'datą'}}
     ),
    pytest.mark.xfail((None, ('de.json',), None), raises=AssertionError),
    pytest.mark.xfail(('PL', ('us.json',), None), raises=AssertionError)
])
def test_downloader_invalid_country(i18n_data_dir, country, file_names, data):
    from i18naddress.downloader import download
    download(country)
    for file_name in file_names:
        assert i18n_data_dir.join(file_name).exists()
        assert json.load(i18n_data_dir.join(file_name)) == data[file_name]
