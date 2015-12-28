from __future__ import unicode_literals
from functools import wraps
import json
import os

import pytest

try:
    from unittest import mock
except ImportError:
    import mock


def mock_downloader(manager_dict, countries):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(mocker, tmpdir):
            data_dir = tmpdir.join('data')
            mocker.patch('multiprocessing.pool.ThreadPool')
            mocker.patch('i18naddress.downloader.work_queue')
            mocker.patch('i18naddress.downloader.get_countries', new=lambda: countries)
            mocker.patch(
                'i18naddress.downloader.COUNTRIES_VALIDATION_DATA_DIR',
                new=str(data_dir))
            mocker.patch(
                'i18naddress.downloader.COUNTRY_PATH',
                os.path.join(str(data_dir), '%s.json'))
            manager = mocker.patch('i18naddress.downloader.manager')
            manager.dict.return_value = manager_dict
            return func(data_dir)
        return func_wrapper
    return tags_decorator


@pytest.mark.xfail(raises=ValueError)
@mock_downloader({'PL': 'data'}, ['PL'])
def test_downloader_invalid_country(data_dir):
    from i18naddress.downloader import download
    download('DE')


@mock_downloader({'PL': 'data'}, ['PL'])
def test_downloader_one_country(data_dir):
    from i18naddress.downloader import download
    download('PL')
    assert data_dir.join('pl.json').exists()
    assert data_dir.join('all.json').exists()
    assert json.load(data_dir.join('pl.json').open()) == {'PL': 'data'}
    assert json.load(data_dir.join('all.json').open()) == {'PL': 'data'}


@mock_downloader({'PL': 'data', 'US': 'data'}, ['PL', 'US'])
def test_downloader_many_countries(data_dir):
    from i18naddress.downloader import download
    download()
    assert data_dir.join('pl.json').exists()
    assert data_dir.join('us.json').exists()
    assert data_dir.join('all.json').exists()
    assert json.load(data_dir.join('pl.json').open()) == {'PL': 'data'}
    assert json.load(data_dir.join('us.json').open()) == {'US': 'data'}
    assert json.load(data_dir.join('all.json').open()) == {'PL': 'data', 'US': 'data'}
