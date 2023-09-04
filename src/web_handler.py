#! /usr/bin/env python3.6
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import calendar

# from re import search
from src.date_functions import default_start_date, default_end_date
from itertools import chain
from numpy import arange
import src.config as config
import logging

BOOKING_PAGE_RESULTS = 25


def find_weekend(month=1, year=datetime.datetime.now().year):
    workday_1st, month_length = calendar.monthrange(year, month)

    days_to_1st_friday = workday_1st if workday_1st == 6 else 5 - workday_1st

    fridays = [day for day in range(days_to_1st_friday, month_length + 1, 7)]
    friday_dates = [
        "{year}-{month}-{day}".format(year=year, month=month, day=day)
        for day in fridays
    ]
    week_end_dates = [
        "{year}-{month}-{day}".format(
            year=year, month=month, day=(day if day + 2 > month_length else day + 2)
        )
        for day in fridays
    ]

    return list(chain(*zip(friday_dates, week_end_dates)))


def get_booking_page(city, dest_id, rooms, people, startdate, enddate, offset):
    """
    Make request to booking page and parse html
    :param offset:
    :return: html page
    """
    logging.debug(
        "Scrapping booking.com with params: \n city: {city}, dest_id: {dest_id}, rooms: {rooms}, people: {people}, startdate: {startdate}, enddate: {enddate}, offset: {offset}".format(  # noqa: E501
            city=city,
            dest_id=dest_id,
            rooms=rooms,
            people=people,
            startdate=startdate,
            enddate=enddate,
            offset=offset,
        )
    )
    url: str = (
        "https://www.booking.com/searchresults.pl.html?"
        "ss={city}&"
        "ssne={city}&"
        "ssne_untouched={city}&"
        "label=gen173nr-1BCAEoggI46AdIM1gEaLYBiAEBmAEeuAEXyAEM2AEB6AEBiAIBqAIDuAKVrsikBsACAdICJGRjNGFhMGUzLTk0ZjEtNDA4MS05YjkzLWIyZmEzYTMxMWFkNtgCBeACAQ&"
        "aid=304142&"
        "lang=pl&"
        "sb=1&"
        "src_elem=sb&"
        "src=searchresults&"
        "dest_id={dest_id}&"
        "dest_type=city&"
        "checkin={startdate}&"
        "checkout={enddate}&"
        "group_adults={people}&"
        "no_rooms={rooms}&"
        "group_children=0&"
        "nflt=review_score%3D90"
        "privacy_type%3D3&=&=&=&"
        "offset={offset}".format(
            city=city,
            dest_id=dest_id,
            people=people,
            rooms=rooms,
            startdate=str(startdate).split(" ")[0],
            enddate=str(enddate).split(" ")[0],
            offset=offset,
        )
    )
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
    city="W%C5%82adys%C5%82awowo",
    dest_id=-535939,
    rooms=1,
    people=2,
    start_date=default_start_date(),
    end_date=default_end_date(),
    timeofstay=2,
    offset=0,
):
    """
    Prepare data for saving
    :return: pd.DataFrame
    """
    df_list = []

    logging.info(f"Preparing data for {city} since {start_date} till {end_date}")
    parsed_html = get_booking_page(
        city, dest_id, rooms, people, start_date, end_date, offset
    )

    # pages = parsed_html.find_all("div", {"data-testid": "pagination"})

    # count = int(search(r'\d+', pages[0].previous_sibling.string).group())
    offsets = arange(
        0, 25 if 25 < config.MAX_OFFSET else config.MAX_OFFSET, BOOKING_PAGE_RESULTS
    )

    for offset in offsets:
        logging.debug("offset: {offset}".format(offset=offset))
        parsed_html = get_booking_page(
            city, dest_id, rooms, people, start_date, end_date, offset
        )

        prices = parsed_html.find_all(
            "span", {"data-testid": "price-and-discounted-price"}
        )
        prices_ = pd.Series(
            "".join(x for x in price.string if x.isdigit()) for price in prices
        )

        titles_ = pd.Series(
            title.string
            for title in parsed_html.find_all("div", {"data-testid": "title"})
        )

        scores_ = pd.Series(
            grade.next_element.string.replace(",", ".")
            for grade in parsed_html.find_all("div", {"data-testid": "review-score"})
        )

        data = pd.DataFrame(
            {
                "Hotel": titles_,
                "Price": prices_,
                "Onenight Price": [int(x) // timeofstay for x in prices_],
                "Start date": start_date,
                "End date": end_date,
                "Nights": timeofstay,
                "Grade": scores_,
                "People": people,
                "Rooms": rooms,
                "Page": offset // BOOKING_PAGE_RESULTS + 1,
            }
        )

        data["Grade"] = pd.to_numeric(data["Grade"], downcast="float")
        data["Price"] = pd.to_numeric(data["Price"], downcast="unsigned")

        df_list.append(data)

    df = pd.concat(df_list, axis=0, ignore_index=True)
    return df


def get_data(
    city="W%C5%82adys%C5%82awowo",
    dest_id=-535939,
    rooms=1,
    people=2,
    start_date=default_start_date(),
    end_date=default_end_date(),
    month=0,
    timeofstay=2,
    save=False,
    weekend=False,
):
    """
    Get all accomodations in Pooland and save them in file
    :return: month.xlsx file
    """
    start_date = str(start_date).split(" ")[0]
    end_date = str(end_date).split(" ")[0]

    # logging.info("Pokoje ze śniadaniami w ", city[0])
    # logging.info("Liczba pokoi: ", rooms)
    # logging.info("Liczba osób dorosłych: ", people)
    # logging.info("Od: ", start_date)
    # logging.info("Do: ", end_date)
    # logging.info("Miesiac: ", calendar.month_name[month])
    # logging.info("Ilość nocy: ", timeofstay)

    curr_month = datetime.datetime.now().month

    assert curr_month <= month

    if weekend:
        logging.info("Scrapping only weekend dates...")
        it = iter(pd.Series(find_weekend(month)))
        nocleg_series = pd.Series([*zip(it, it)])
    elif month != 0:
        start = (
            "2023-{month}-01".format(month=month) if month > curr_month else start_date
        )
        end = pd.Series(pd.date_range(start, periods=1, freq="M"))[0]
    elif month == 0:
        start, end = start_date, end_date

    nocleg_series = pd.Series(
        pd.date_range(
            start, end=end, freq="{timeofstay}D".format(timeofstay=timeofstay)
        )
    )

    list_of_dfs = []
    # The reason we have double append(prep_data())
    # is because in weekends we prep data by two:
    # 01.07-03.07. -> 07.07-09.07.
    # IN other scenarios we use shifting window by 1
    # 01-07.-03.07. -> 03.07. -> 05.07.
    if weekend:
        for elem in nocleg_series:
            start_date, end_date = elem[0], elem[1]
            list_of_dfs.append(
                prep_data(
                    city=city,
                    dest_id=dest_id,
                    rooms=rooms,
                    people=people,
                    start_date=start_date,
                    end_date=end_date,
                    timeofstay=timeofstay,
                    offset=0,
                )
            )
    else:
        for i in range(1, len(nocleg_series)):
            start_date, end_date = nocleg_series[i - 1], nocleg_series[i]
            list_of_dfs.append(
                prep_data(
                    city=city,
                    dest_id=dest_id,
                    rooms=rooms,
                    people=people,
                    start_date=start_date,
                    end_date=end_date,
                    timeofstay=timeofstay,
                    offset=0,
                )
            )

    list_of_dfs = pd.concat(list_of_dfs, axis=0, ignore_index=True)
    logging.info("Gathering Data ended.")
    return list_of_dfs
