import os

import pytest


@pytest.fixture(autouse=True)
def patch_i18n_country_data(tmpdir, monkeypatch):
    data_dir = tmpdir.mkdir('data')
    data_path = os.path.join(str(data_dir), '%s.json')
    monkeypatch.setattr('i18naddress.I18nCountryData.COUNTRY_VALIDATION_PATH', data_path)
