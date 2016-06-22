
from local_ci import utils

def test_slugify():
    assert utils.slugify('ownport/python:2.7') == 'ownport-python-2-7'
