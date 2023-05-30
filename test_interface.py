import pytest
from mod_home import *
from mod_login import *

def test_open_login():
    assert LoginWindow()

def test_open_home():

    assert MainWindow()
