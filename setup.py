#! /usr/bin/env python
import logging
from setuptools import setup, find_packages, Command


class DownloadJSONFiles(Command):

    description = 'Download all addresses data from Google i18n API'
    user_options = []
    logger = None

    def initialize_options(self):
        logging.basicConfig()
        self.logger = logging.getLogger('i18naddress.downloader')
        self.logger.setLevel(logging.DEBUG)

    def finalize_options(self):
        pass

    def run(self):
        from i18naddress.downloader import download
        download()

setup(
    name='google-i18n-address',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='Address validation helpers for Google\'s i18n address database',  # noqa
    license='BSD',
    version='1.0.3',
    url='https://github.com/mirumee/google-i18n-address',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.7.0',
    ],
    cmdclass={'update_validation_files': DownloadJSONFiles},
    zip_safe=False
)
