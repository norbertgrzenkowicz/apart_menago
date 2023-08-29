import pytest
import config
import logging
from apart_menago.interface import Interface

def test_interface(caplog):
    scrapper = Interface()
    with caplog.at_level(logging.DEBUG):
        assert scrapper.scrap_data() is True
