#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages


def get_version():
    init = open(os.path.join(os.path.dirname(__file__), 'sshec2', '__init__.py')).read()
    return re.compile(r'''__version__ = ['"]([0-9.]+)['"]''').search(init).group(1)


requires = ['boto3==1.4.4',
            'botocore==1.5.40',
            'future']


setup_options = dict(
    name='sshec2',
    version=get_version(),
    description='Utility for ssh login to EC2 instances.',
    author='Shinji Fujimoto',
    url='https://github.com/s-fujimoto/sshec2',
    scripts=['bin/sshec2'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)


setup(**setup_options) 