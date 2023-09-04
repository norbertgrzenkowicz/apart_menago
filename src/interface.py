from src.web_handler import get_data
from src.date_functions import default_start_date, default_end_date
import threading
from itertools import product
import concurrent.futures
import src.config as config
import logging
from src.sql_parser import SQL_parser


def compute_products(*args):
    return list(product(*[*args]))


class Interface:
    def __init__(self) -> None:
        self.scrapped_data = []
        self._lock = threading.Lock()
        self.reservation_input = {
            "city": config.CITY,
            "rooms": 1,
            "people": config.PEOPLE,
            "start_date": default_start_date(),
            "end_date": default_end_date(),
            "month": config.MONTH,
            "timeofstay": config.TIMEOFSTAY,
            "save": False,
            "weekend": False,
        }

    def scrap_data(self):
        products = compute_products(
            self.reservation_input["city"],
            self.reservation_input["people"],
            self.reservation_input["timeofstay"],
        )
        logging.info("Amount of products: {length}".format(length=len(products)))
        with concurrent.futures.ThreadPoolExecutor(len(products)) as executor:
            _ = [
                executor.submit(
                    self.scrapped_data.append,
                    get_data(
                        reservation_products[0][0],
                        reservation_products[0][1],
                        self.reservation_input["rooms"],
                        reservation_products[1],
                        self.reservation_input["start_date"],
                        self.reservation_input["end_date"],
                        self.reservation_input["month"],
                        reservation_products[2],
                        self.reservation_input["save"],
                        self.reservation_input["weekend"],
                    ),
                )
                for reservation_products in products
            ]

        return True if len(_) > 1 else False


if __name__ == "__main__":
    scrapper = Interface()
    scrapper.scrap_data()
    SQL_parser(scrapped_data=scrapper.scrapped_data)
