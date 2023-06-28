#! /usr/bin/env python3.6
import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter
from argcomplete.completers import EnvironCompleter
import requests
import datetime
# from bthread import BookingThread
from bs4 import BeautifulSoup
# from file_writer import FileWriter
import pandas as pd
import calendar


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


def get_booking_page(rooms, people, startdate, enddate):
    """
    Make request to booking page and parse html
    :param offset:
    :return: html page
    """
    url: str = (
        "https://www.booking.com/searchresults.pl.html?"
        "ss={city}&"
        "ssne={city}&"
        "ssne_untouched={city}&"  # W%C5%82adys%C5%82awowo&
        "label=gen173nr-1BCAEoggI46AdIM1gEaLYBiAEBmAEeuAEXyAEM2AEB6AEBiAIBqAIDuAKVrsikBsACAdICJGRjNGFhMGUzLTk0ZjEtNDA4MS05YjkzLWIyZmEzYTMxMWFkNtgCBeACAQ&"
        "aid=304142&"
        "lang=pl&"
        "sb=1&"
        "src_elem=sb&"
        "src=searchresults&"
        "dest_id=-535939&"
        "dest_type=city&"
        "checkin={startdate}&"
        # "checkin=2023-07-13&"
        "checkout={enddate}&"
        # "checkout=2023-07-18&"
        "group_adults={people}&"
        "no_rooms={rooms}&"
        "group_children=0&"
        "nflt=review_score%3D90"
        .format(
            city="W%C5%82adys%C5%82awowo",
            people=people,
            rooms=rooms,
            startdate=str(startdate).split(" ")[0],
            enddate=str(enddate).split(" ")[0]
        ))
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )
    html = r.content
    parsed_html = BeautifulSoup(html, "lxml")
    return parsed_html


def prep_data(
    rooms=1,
    people=2,
    start_date=default_start_date(),
    end_date=default_end_date(),
    timeofstay=2
):
    """
    Prepare data for saving
    :return: hotels: set()
    """
    # offset: int = 15
    # session = requests.Session()
    print("prep_data", start_date, end_date)
    parsed_html = get_booking_page(
        rooms, people, start_date, end_date
    )

    scrapped_data = [[], [], []]

    prices = parsed_html.find_all(
        "span", {"data-testid": "price-and-discounted-price"})

    for price in prices:
        scrapped_data[0].append(
            ''.join(x for x in price.string if x.isdigit()))

    for title in parsed_html.find_all("div", {"data-testid": "title"}):
        if title.string is not None:
            scrapped_data[1].append(title.string)

    for grade in parsed_html.find_all("div", {"data-testid": "review-score"}):
        if grade.next_element.string is not None:
            scrapped_data[2].append(
                grade.next_element.string.replace(",", "."))

    data = {
        "Hotel": scrapped_data[1],
        "Price": scrapped_data[0],
        "Onenight Price": [int(x) // timeofstay for x in scrapped_data[0]],
        "Start date": start_date,
        "End date": end_date,
        "Nights": timeofstay,
        "Grade": scrapped_data[2],
        "People": people,
        "Rooms": rooms
    }

    df = pd.DataFrame(data)
    df["Grade"] = pd.to_numeric(df["Grade"], downcast="float")
    df["Price"] = pd.to_numeric(df["Price"], downcast="unsigned")
    return df


def get_data(
    rooms=1,
    people=2,
    start_date=default_start_date(),
    end_date=default_end_date(),
    month=0,
    timeofstay=2
):
    """
    Get all accomodations in Pooland and save them in file
    :return: hotels-in-macedonia.{txt/csv/xlsx} file
    """
    print("Pokoje ze śniadaniami")
    print("Liczba pokoi ", rooms)
    print("Liczba osób dorosłych: ", people)
    print("Od: ", start_date)
    print("Do: ", end_date)
    print("Miesiac: ", calendar.month_name[month])
    print("Ilość nocy: ", timeofstay)

    if month == 0 and start_date == default_start_date():
        datetime_series = pd.Series(
            pd.date_range("2023-07-01", periods=3, freq="M"))
        datetime_series2 = pd.Series(
            pd.date_range("2023-07-01", end=datetime_series[2],
                          freq="{timeofstay}D".format(timeofstay=timeofstay)))
    elif month != 0:
        datetime_series = pd.Series(
            pd.date_range("2023-{month}-01".format(month=month), periods=1, freq="M"))
        datetime_series2 = pd.Series(
            pd.date_range("2023-{month}-01".format(month=month), end=datetime_series[0],
                          freq="{timeofstay}D".format(timeofstay=timeofstay)))

    i = 0
    list_of_dfs = []
    while i + 1 < len(datetime_series2) - 1:
        list_of_dfs.append(prep_data(rooms=rooms, people=people,
                                     start_date=datetime_series2[i],
                                     end_date=datetime_series2[i+1],
                                     timeofstay=timeofstay))
        i += 1

    list_of_dfs = pd.concat(list_of_dfs, axis=0, ignore_index=True)

    pd.DataFrame(list_of_dfs).to_excel(
        calendar.month_name[month] + ".xlsx")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--rooms",
        help="Add the number of rooms to the booking request.",
        default=1,
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "-p",
        "--people",
        help="Add the number of people to the booking request.",
        default=2,
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "-s",
        "--startdate",
        help="The start date for the booking (format: YYYY-MM-DD)",
        default=default_start_date(),
        type=valid_date,
    )
    parser.add_argument(
        "-e",
        "--enddate",
        help="The end date for the booking (format: YYYY-MM-DD)",
        default=default_end_date(),
        type=valid_date,
    )
    parser.add_argument(
        "-m",
        "--month",
        help="Month date for the booking",
        default=0,
        type=int,
    )
    parser.add_argument(
        "-tos",
        "--timeofstay",
        help="Low many nights you want to stay",
        default=4,
        type=int,
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    get_data(args.rooms, args.people,
             args.startdate, args.enddate, args.month, args.timeofstay)
