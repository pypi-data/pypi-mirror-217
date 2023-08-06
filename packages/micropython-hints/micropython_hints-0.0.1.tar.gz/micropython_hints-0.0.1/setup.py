#!/usr/bin/env python
import os
import shutil
from setuptools import setup, find_packages

PROJ_NAME = "micropython_hints"
TGT_DIR = os.path.join(os.path.split(os.path.abspath(os.__file__))[0], "site-packages")

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CUR_PATH, "build")
if os.path.isdir(path):
    print("INFO DEL DIR ", path)
    shutil.rmtree(path)
path = os.path.join(CUR_PATH, "dist")
if os.path.isdir(path):
    print("INFO DEL DIR ", path)
    shutil.rmtree(path)

with open(os.path.join(CUR_PATH, "README.md"), 'r+', encoding='utf8') as f:
    long_description = f.read()

URL = f"https://github.com/miaobuao/{PROJ_NAME}"
setup(
    name         = PROJ_NAME,
    author       =  "miaobuao",
    url          =  URL,
    description  =  "MicroPython type hints",
    version      =  "0.0.1",
    license      =  "MIT License",
    author_email =  "miaobuao@outlook.com",
    long_description     = long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
)

if __name__ == '__main__':
    import sys
    action = sys.argv[1]
    if action != "install":
        exit()
    print(f"\033[31m[WARNING]: Please note that this package will be installed at `{TGT_DIR}` in a destructive manner. \
        \n\rIt is strongly recommended to install it within a virtual environment.\033[0m", end='')

    if input("continue? [y/N]: ").strip() not in ['yes', 'Y', 'y']:
        exit()

    from urllib.request import urlretrieve
    from random import random
    DLink = f"https://github.com/miaobuao/micropython_hints/releases/download/untagged-a1d97f97ef454774ea55/release-0.0.1.zip"
    path = f"tmp-{random()}.zip"
    _, m = urlretrieve(DLink, path, reporthook=print)
    print(m)
    print("extracting...")
    
    from pyzipper import ZipFile
    file = ZipFile(path)
    file.extractall(TGT_DIR)
    os.remove(path)
    print("done")