from src.web_handler import WeekWebHandler
from src.date_functions import default_start_date, default_end_date
import threading
from itertools import product
import concurrent.futures
import src.config as config
import logging
import datetime
from src.sql_parser import SQL_parser


def compute_products(*args):
    return list(product(*[*args]))


class Interface:
    def __init__(self) -> None:
        self.web_handler = WeekWebHandler()
        self.scrapped_data = []
        self._lock = threading.Lock()
        self.reservation_input = {
            "city": config.CITY,
            "rooms": 1,
            "people": config.PEOPLE,
            "start_date": default_start_date(),
            "end_date": default_end_date(),
            "month": datetime.datetime.now().month,
            "timeofstay": config.TIMEOFSTAY,
            "save": False,
            "weekend": False,
        }
        self.products = compute_products(
            self.reservation_input["city"],
            self.reservation_input["people"],
            self.reservation_input["timeofstay"],
        )

    def scrap_data(self):
        logging.info("Amount of products: {length}".format(length=len(self.products)))
        with concurrent.futures.ThreadPoolExecutor(len(self.products)) as executor:
            _ = [
                executor.submit(
                    self.scrapped_data.append,
                    self.web_handler.get_data(
                        city=reservation_products[0][0],
                        dest_id=reservation_products[0][1],
                        rooms=self.reservation_input["rooms"],
                        people=reservation_products[1],
                        start_date=self.reservation_input["start_date"],
                        end_date=self.reservation_input["end_date"],
                        month=self.reservation_input["month"],
                        timeofstay=reservation_products[2],
                        save=self.reservation_input["save"],
                        weekend=self.reservation_input["weekend"],
                    ),
                )
                for reservation_products in self.products
            ]

        return True if len(_) > 1 else False


if __name__ == "__main__":
    scrapper = Interface()
    scrapper.scrap_data()
    SQL_parser().save_to_sql(scrapper.scrapped_data)
