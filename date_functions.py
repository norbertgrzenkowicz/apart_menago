import datetime
import argparse


def valid_date(given_date):
    try:
        return datetime.datetime.strptime(given_date, "%Y-%m-%d")
    except ValueError:
        msg = "{0} is not a valid date.".format(given_date)
        raise argparse.ArgumentTypeError(msg)


def default_start_date():
    try:
        today: str = datetime.datetime.today()
        return today.strftime("%Y-%m-%d")
    except Exception as e:
        msg = "Error creating default date"
        raise argparse.ArgumentError(e, msg)


def default_end_date():
    try:
        today: str = datetime.datetime.today() + datetime.timedelta(days=1)
        return today.strftime("%Y-%m-%d")
    except Exception as e:
        msg = "Error creating default date"
        raise argparse.ArgumentError(e, msg)
