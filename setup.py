#! /usr/bin/env python
import logging
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class DownloadJSONFiles(Command):

    description = 'Download all addresses data from Google i18n API'
    user_options = [('country=', 'c', 'Download data only for this country')]
    country = None
    logger = None

    def initialize_options(self):
        logging.basicConfig()
        self.logger = logging.getLogger('i18naddress.downloader')
        self.logger.setLevel(logging.DEBUG)

    def finalize_options(self):
        pass

    def run(self):
        from i18naddress.downloader import download
        download(country=self.country)

setup(
    name='google-i18n-address',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='Address validation helpers for Google\'s i18n address database',  # noqa
    license='BSD',
    version='1.0.5',
    url='https://github.com/mirumee/google-i18n-address',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests>=2.7.0'],
    cmdclass={'update_validation_files': DownloadJSONFiles, 'test': PyTest},
    tests_require=['mock', 'pytest-cov', 'pytest'],
    zip_safe=False
)
