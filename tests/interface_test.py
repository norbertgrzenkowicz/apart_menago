import sys
import os

sys.path.append("../src")

import src.interface
import logging


def test_interface(caplog):
    with caplog.at_level(logging.DEBUG):
        assert src.interface.Interface().scrap_data() is True
