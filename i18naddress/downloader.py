import io
import json
import logging
from multiprocessing.pool import ThreadPool
from multiprocessing import JoinableQueue, Manager
import os

import requests

from . import COUNTRIES_VALIDATION_DATA_DIR

MAIN_URL = 'http://i18napis.appspot.com/address/data'
COUNTRY_PATH = os.path.join(COUNTRIES_VALIDATION_DATA_DIR, '%s.json')

logger = logging.getLogger(__name__)
work_queue = JoinableQueue()
manager = Manager()


def fetch(url):
    logger.debug(url)
    data = requests.get(url).json()
    return data


def process(key):
    url = '%s/%s' % (MAIN_URL, key)
    data = fetch(url)
    lang = data.get('lang')
    languages = data.get('languages')
    if languages is not None:
        langs = languages.split('~')
        langs.remove(lang)
        for lang in langs:
            work_queue.put('%s--%s' % (key, lang))
    if 'sub_keys' in data:
        sub_keys = data['sub_keys'].split('~')
        for sub_key in sub_keys:
            work_queue.put('%s/%s' % (key, sub_key))
    return data


def worker(data):
    while True:
        try:
            key = work_queue.get()
        except EOFError:
            break
        try:
            address_data = process(key)
        except Exception:
            logger.exception('Can\'t download %s', key)
            work_queue.put(key)
        else:
            data[key] = address_data
        work_queue.task_done()


def serialize(obj, path):
    with io.open(path, 'w', encoding='utf8') as output:
        data_str = json.dumps(dict(obj), ensure_ascii=False)
        output.write(unicode(data_str))
        return data_str


def download(processes=16):
    if not os.path.exists(COUNTRIES_VALIDATION_DATA_DIR):
        os.mkdir(COUNTRIES_VALIDATION_DATA_DIR)
    data = manager.dict()
    countries = fetch(MAIN_URL)['countries'].split('~')
    countries = ['PL']
    for country in countries:
        work_queue.put(country)
    workers = ThreadPool(processes, worker, initargs=(data,))
    work_queue.join()
    workers.terminate()
    logger.debug('Queue finished')
    with io.open(COUNTRY_PATH % 'all', 'w', encoding='utf8') as all_output:
        all_output.write(u'{')
        for country in countries:
            country_dict = {}
            for key, address_data in data.items():
                if key[:2] == country:
                    country_dict[key] = address_data
            logger.debug('Saving %s', country)
            country_json = serialize(country_dict, COUNTRY_PATH % country.lower())
            all_output.write(country_json[1:-1])
            if country != countries[-1]:
                all_output.write(u',')
        all_output.write(u'}')
