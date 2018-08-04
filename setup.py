import os

from setuptools import setup, find_packages

VERSION_FILE = 'VERSION'


def read_version():
    with open(VERSION_FILE, 'r') as fp:
        return tuple(map(int, fp.read().split('.')))


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="cgp-bouncer",
    description="Simple email whitelist checker backed by the AWS Secrets Manager",
    packages=find_packages(),  # include all packages
    url="https://github.com/ucsc-cgp/bouncer",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=['boto3 >=1.6.0, <2',
                      'six >=1.11, <2'],
    license='Apache License 2.0',
    include_package_data=True,
    zip_safe=True,
    author="Jesse Brennan",
    author_email="brennan@ucsc.edu",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    version='{}.{}.{}'.format(*read_version()),
    keywords=['genomics', 'secret', 'client', 'whitelist', 'NIHDataCommons'],
)
