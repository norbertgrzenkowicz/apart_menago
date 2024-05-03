import sys
import os

sys.path.append("../src")

import src.interface
import src.sql_parser
import logging


def test_sql_save(caplog):
    scrapper = src.interface.Interface()
    scrapper.scrap_data()

    with caplog.at_level(logging.DEBUG):
        result = src.sql_parser.SQL_parser().save_to_sql(scrapper.scrapped_data, 0)

    assert result == 0
