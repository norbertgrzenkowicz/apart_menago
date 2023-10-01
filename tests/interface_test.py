import logging
from src.interface import Interface


def test_interface(caplog):
    with caplog.at_level(logging.DEBUG):
        assert Interface().scrap_data() is True
