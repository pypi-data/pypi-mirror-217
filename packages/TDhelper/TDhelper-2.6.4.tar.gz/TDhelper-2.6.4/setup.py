#!/usr/bin/env python
# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="TDhelper",
    version="2.6.4",
    keywords=("pip", "TDhelper", "featureextraction"),
    description="reconsitution web.permissionHelper cls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://gitee.com/TonyDon/pyLib",
    author="TangJing",
    author_email="yeihizhi@163.com",
    packages=setuptools.find_packages(exclude=["UnitTest"]),
    classifiers=[],
    install_requires=["asgiref==3.4.1",
"bleach==4.1.0",
"certifi==2020.4.5.1",
"cffi==1.14.6",
"chardet==3.0.4",
"colorama==0.4.4",
"crypto==1.4.1",
"cryptography==3.4.8",
"dnspython==1.16.0",
"docutils==0.17.1",
"et-xmlfile==1.1.0",
"gyp-next==0.4.0",
"idna==2.9",
"importlib-metadata==4.8.1",
"jdcal==1.4.1",
"keyring==23.2.1",
"mysql-connector-python==8.0.19",
"Naked==0.1.31",
"openpyxl==3.0.4",
"packaging==21.0",
"pkginfo==1.7.1",
"protobuf==3.6.1",
"pycparser==2.20",
"pycryptodome==3.9.7",
"Pygments==2.10.0",
"pymongo==3.10.1",
"pyparsing==2.4.7",
"python-dateutil==2.8.1",
"pytz==2021.1",
"pywin32-ctypes==0.2.0",
"PyYAML==5.4.1",
"readme-renderer==30.0",
"requests==2.23.0",
"requests-toolbelt==0.9.1",
"rfc3986==1.5.0",
"shellescape==3.8.1",
"six==1.15.0",
"sqlparse==0.4.1",
"tqdm==4.62.3",
"typing-extensions==3.10.0.2",
"urllib3==1.25.9",
"webencodings==0.5.1",
"xlrd==1.1.0",
"zipp==3.5.0"
],
entry_points = {
        'console_scripts': [
            #'foo = demo:test',
            #'bar = demo:test',
            'saas = TDhelper.shellScripts.saasHelper:CMD'
        ],
        'gui_scripts': [
            #'baz = demo:test',
        ]
    }
)
