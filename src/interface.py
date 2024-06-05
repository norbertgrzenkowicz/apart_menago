from src.web_handler import WeekWebHandler
from src.date_functions import default_start_date, default_end_date
import threading
from itertools import product
import concurrent.futures
import src.config as config
import logging
import datetime
from src.sql_parser import SQL_parser
import argparse


def compute_products(*args):
    return list(product(*[*args]))


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


class Interface:
    def __init__(
        self,
        city=config.CITY,
        rooms=1,
        people: list = config.PEOPLE,
        start_date=default_start_date(),
        end_date=default_end_date(),
        month=datetime.datetime.now().month,
        timeofstay=config.TIMEOFSTAY,
        save=False,
        weekend=False,
    ):
        self.web_handler = WeekWebHandler()
        self.scrapped_data = []
        self._lock = threading.Lock()
        self.reservation_input = {
            "city": config.CITY,
            "rooms": rooms,
            "people": people,
            "start_date": start_date,
            "end_date": end_date,
            "month": month,
            "timeofstay": timeofstay,
            "save": save,
            "weekend": weekend,
        }
        self.products = compute_products(
            self.reservation_input["city"],
            self.reservation_input["people"],
            self.reservation_input["timeofstay"],
        )
        setup_logging()

    def scrap_data(self):
        logging.info("Amount of products: {length}".format(length=len(self.products)))
        for reservation_products in self.products:
            logging.info("Products: {}".format(reservation_products))

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
    parser = argparse.ArgumentParser(description="Run your Booking script")

    parser.add_argument(
        "--city",  # TODO: Not working yet!
        help="City name",
        default=("Władysławowo", config.CITY),
    )
    parser.add_argument(
        "--start_date", help="start date in Y-M-D formula", default=default_start_date()
    )
    parser.add_argument(
        "--end_date", help="end date in Y-M-D formula", default=default_end_date()
    )
    parser.add_argument(
        "--people", help="amount of people on a stay", default=config.PEOPLE
    )
    parser.add_argument("--rooms", help="amount of rooms on a stay", default=1)
    parser.add_argument(
        "--month", help="1-12 int of months", default=datetime.datetime.now().month
    )  # TODO: figure out if this month arg is useful somehow
    parser.add_argument(
        "--timeofstay",
        help="amount of nights on a single stay",
        default=config.TIMEOFSTAY,
    )
    parser.add_argument(
        "--save",
        help="If specified data will be saved in database",
        action="store_true",
    )  # TODO: dunno if useful, update: i think its useless
    parser.add_argument(
        "--weekend",
        help="If specified only weekends will be listed",
        action="store_true",
    )  # TODO: useful but might not be in working state

    args = parser.parse_args()
    scrapper = Interface(
        city=args.city,  # TODO: validate input to check f.e. if city is in config.CITY
        rooms=args.rooms,
        people=args.people,
        start_date=args.start_date,
        end_date=args.end_date,
        month=args.month,
        timeofstay=args.timeofstay,
        save=args.save,
        weekend=args.weekend,
    )
    scrapper.scrap_data()
    if args.save:
        SQL_parser().save_to_sql(scrapper.scrapped_data, 0)
