import logging
from src.interface import Interface


def test_interface(caplog):
    scrapper = Interface()
    with caplog.at_level(logging.DEBUG):
        assert scrapper.scrap_data() is True
