#! /usr/bin/env python
import io
import logging
from setuptools import setup, find_packages, Command


class DownloadJSONFiles(Command):

    description = "Download all addresses data from Google i18n API"
    user_options = [("country=", "c", "Download data only for this country")]
    country = None
    logger = None

    def initialize_options(self):
        logging.basicConfig()
        self.logger = logging.getLogger("i18naddress.downloader")
        self.logger.setLevel(logging.DEBUG)

    def finalize_options(self):
        pass

    def run(self):
        from i18naddress.downloader import download

        download(country=self.country)


def get_long_description():
    with io.open("README.rst", encoding="utf-8") as readme_file:
        readme = readme_file.read()
    # add GitHub badge in PyPi
    return readme.replace(
        "|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons|",  #  noqa
        "|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons| |GitHub|",
    )  #  noqa


setup(
    name="google-i18n-address",
    long_description=get_long_description(),
    author="Mirumee Software",
    author_email="hello@mirumee.com",
    description="Address validation helpers for Google's i18n address database",
    license="BSD",
    version="2.5.2",
    url="https://github.com/mirumee/google-i18n-address",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["requests>=2.7.0"],
    tests_require=["mock", "pytest-cov", "pytest"],
    cmdclass={"update_validation_files": DownloadJSONFiles},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Internationalization",
    ],
)
