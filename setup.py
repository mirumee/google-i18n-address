#! /usr/bin/env python
import io
import logging
import sys
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]
    test_args = []

    def initialize_options(self):
        """
        Initialize pytest_args.

        Args:
            self: (todo): write your description
        """
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        """
        Finalize options.

        Args:
            self: (todo): write your description
        """
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """
        Run test.

        Args:
            self: (todo): write your description
        """
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
        """
        Initialize the options.

        Args:
            self: (todo): write your description
        """
        logging.basicConfig()
        self.logger = logging.getLogger('i18naddress.downloader')
        self.logger.setLevel(logging.DEBUG)

    def finalize_options(self):
        """
        Finalize options. options. options.

        Args:
            self: (todo): write your description
        """
        pass

    def run(self):
        """
        Runs the address

        Args:
            self: (todo): write your description
        """
        from i18naddress.downloader import download
        download(country=self.country)


def get_long_description():
    """
    Get the long description of readme.

    Args:
    """
    with io.open('README.rst', encoding='utf-8') as readme_file:
        readme = readme_file.read()
    # add GitHub badge in PyPi
    return readme.replace(
        '|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons|', #  noqa
        '|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons| |GitHub|') #  noqa

setup(
    name='google-i18n-address',
    long_description=get_long_description(),
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='Address validation helpers for Google\'s i18n address database',
    license='BSD',
    version='2.4.0',
    url='https://github.com/mirumee/google-i18n-address',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=['requests>=2.7.0'],
    tests_require=['mock', 'pytest-cov', 'pytest'],
    cmdclass={'update_validation_files': DownloadJSONFiles, 'test': PyTest},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment',
        'Topic :: Software Development :: Internationalization'
    ]
)
