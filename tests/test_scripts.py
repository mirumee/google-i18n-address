from unittest.mock import patch

from i18naddress.scripts import download_json_files


@patch("i18naddress.downloader.download")
def test_download_json_files_all_countries(download_mock):
    with patch("sys.argv", ["download_json_files"]):
        download_json_files()

    download_mock.assert_called_once_with(country=None)


@patch("i18naddress.downloader.download")
def test_download_json_files_specific_country(download_mock):
    with patch("sys.argv", ["download_json_files", "--country", "US"]):
        download_json_files()

    download_mock.assert_called_once_with(country="US")
