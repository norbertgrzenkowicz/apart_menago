#! /usr/bin/env python3.6
import argparse
import argcomplete
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import calendar
from re import search
from date_funcs import valid_date, default_start_date, default_end_date



def find_weekend(month):

    dates = []
    if month == 0:
        start = str(default_start_date()).split(" ")[0]
        end = "2023-09-30"
    else:
        start = "2023-0{month}-01".format(month=month),
        end = "2023-0{month}-30".format(month=month)
        start = "2023-07-01"
        end = "2023-07-30"

    for i in pd.date_range(
            start=start,
            end=end):
        ind = i.to_pydatetime()
        if ind.weekday() == 4:
            dates.append(i)
        elif ind.weekday() == 6 and dates:
            dates.append(i)

    return dates


def get_booking_page(city, rooms, people, startdate, enddate, offset):
    """
    Make request to booking page and parse html
    :param offset:
    :return: html page
    """
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
        "privacy_type%3D3&=&=&=&"
        "offset={offset}"
        .format(
            city=city,
            people=people,
            rooms=rooms,
            startdate=str(startdate).split(" ")[0],
            enddate=str(enddate).split(" ")[0],
            offset=offset
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
    city="W%C5%82adys%C5%82awowo",
    rooms=1,
    people=2,
    start_date=default_start_date(),
    end_date=default_end_date(),
    timeofstay=2,
    offset=0
):
    """
    Prepare data for saving
    :return: pd.DataFrame
    """
    print("prep_data", city, start_date, end_date)
    parsed_html = get_booking_page(
        city, rooms, people, start_date, end_date, offset
    )

    pages = parsed_html.find_all(
        "div", {"data-testid": "pagination"})
    print(pages[0].previous_sibling.string)
    count = int(search(r'\d+', pages[0].previous_sibling.string).group())

    i = 0
    offsets = [0]
    df_list = []

    while (i+25 < count and i < 25):
        i += 25
        offsets.append(i)

    for offset in offsets:
        print("offset:", offset)
        parsed_html = get_booking_page(
            city, rooms, people, start_date, end_date, offset
        )

        prices = parsed_html.find_all(
            "span", {"data-testid": "price-and-discounted-price"})
        prices_ = pd.Series(''.join(x for x in price.string if x.isdigit())
                            for price in prices)

        titles_ = pd.Series(
            title.string for title in parsed_html.find_all(
                "div", {"data-testid": "title"}))

        scores_ = pd.Series(grade.next_element.string.replace(",", ".")
                            for grade in parsed_html.find_all(
            "div",
            {"data-testid": "review-score"}))

        data = pd.DataFrame({
            "Hotel": titles_,
            "Price": prices_,
            "Onenight Price": [int(x) // timeofstay for x in prices_],
            "Start date": start_date,
            "End date": end_date,
            "Nights": timeofstay,
            "Grade": scores_,
            "People": people,
            "Rooms": rooms,
            "Page": offset // 25 + 1
        })

        # if len(scrapped_data[0]) > len(scrapped_data[2]):
        #     scrapped_data[2].append("9.0")
        # print(len(scrapped_data[1]), len(
        #     scrapped_data[0]), len(scrapped_data[2]))
        # data = pd.DataFrame(data)
        # print(data)
        data["Grade"] = pd.to_numeric(data["Grade"], downcast="float")
        data["Price"] = pd.to_numeric(data["Price"], downcast="unsigned")

        df_list.append(data)

    df = pd.concat(df_list, axis=0, ignore_index=True)
    return df


def get_data(
    city="W%C5%82adys%C5%82awowo",
    rooms=1,
    people=2,
    start_date=default_start_date(),
    end_date=default_end_date(),
    month=0,
    timeofstay=2,
    save=False,
    weekend=False
):
    """
    Get all accomodations in Pooland and save them in file
    :return: month.xlsx file
    """
    start_date = str(start_date).split(" ")[0]
    end_date = str(end_date).split(" ")[0]
    print("Pokoje ze śniadaniami w ", city)
    print("Liczba pokoi ", rooms)
    print("Liczba osób dorosłych: ", people)
    print("Od: ", start_date)
    print("Do: ", end_date)
    print("Miesiac: ", calendar.month_name[month])
    print("Ilość nocy: ", timeofstay)

    if weekend:
        it = iter(pd.Series(find_weekend(month)))
        nocleg_series = pd.Series([*zip(it, it)])
    elif month != 0:
        start = "2023-{month}-01".format(month=month)
        end = pd.Series(
            pd.date_range(start, periods=1, freq="M"))[0]
    elif month == 0:
        start, end = start_date, end_date

    nocleg_series = pd.Series(
        pd.date_range(start,
                      end=end,
                      freq="{timeofstay}D".format(timeofstay=timeofstay)))

    list_of_dfs = []
    # The reason we have double append(prep_data())
    # is because in weekends we prep data by two:
    # 01.07-03.07. -> 07.07-09.07.
    # IN other scenarios we use shifting window by 1
    # 01-07.-03.07. -> 03.07. -> 05.07.
    if weekend:
        for elem in nocleg_series:
            start_date, end_date = elem[0], elem[1]
            list_of_dfs.append(prep_data(city=city, rooms=rooms, people=people,
                                         start_date=start_date,
                                         end_date=end_date,
                                         timeofstay=timeofstay,
                                         offset=0))
    else:
        for i in range(1, len(nocleg_series)):
            start_date, end_date = nocleg_series[i-1], nocleg_series[i]
            list_of_dfs.append(prep_data(city=city, rooms=rooms, people=people,
                                         start_date=start_date,
                                         end_date=end_date,
                                         timeofstay=timeofstay,
                                         offset=0))

    list_of_dfs = pd.concat(list_of_dfs, axis=0, ignore_index=True)

    return list_of_dfs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--city",
        help="Define name of the scrapped city.",
        default="W%C5%82adys%C5%82awowo&",
        type=str,
        nargs="?",
    )
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
        default=2,
        type=int,
    )
    parser.add_argument(
        "--save",
        help="Saves output to xlsx file",
        default=False,
        type=bool,
    )
    parser.add_argument(
        "--weekend",
        help="Output only weekend times",
        default=False,
        type=bool,
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    get_data(args.city, args.rooms, args.people,
             args.startdate, args.enddate, args.month, args.timeofstay, args.save,
             args.weekend)
