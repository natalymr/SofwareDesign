import os
import pytest

from utilities import cd, ls

TMP_DIR = './tmp_lsdkhfaksdjhfamfsd'

TMP_FILES = [f'tmp_{i}.txt' for i in range(10)]

START_DIR = os.getcwd()


def setup():
    os.chdir(START_DIR)
    os.mkdir(TMP_DIR)
    for file in TMP_FILES:
        with open(f'{TMP_DIR}/{file}', 'w') as f:
            f.write('lol')


def teardown():
    os.chdir(START_DIR)
    for file in TMP_FILES:
        os.remove(f'{TMP_DIR}/{file}')
    os.removedirs(TMP_DIR)


def test_ls(from_start=True):
    if from_start:
        actual = ls((TMP_DIR,))
    else:
        actual = ls()
    actual = actual.convert_to_input().get_input().split()
    actual.sort()
    assert actual == TMP_FILES


def test_cd():
    cd((TMP_DIR, ))
    test_ls(False)
