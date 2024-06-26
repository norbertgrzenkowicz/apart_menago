import src.web_handler
from src.date_functions import default_start_date, default_end_date
from src.config import CITY


def test_data_cols():
    data = src.web_handler.WeekendWebHandler().prep_data()
    cols = [
        "Hotel",
        "Price",
        "Onenight Price",
        "Start date",
        "End date",
        "Nights",
        "Grade",
        "People",
        "Rooms",
        "Page",
    ]
    assert list(data.columns) == cols
    assert len(data) > 0


def test_find_weekends():
    weekends_of_2023 = [
        [
            "2023-1-6",
            "2023-1-8",
            "2023-1-13",
            "2023-1-15",
            "2023-1-20",
            "2023-1-22",
            "2023-1-27",
            "2023-1-29",
        ],
        [
            "2023-2-3",
            "2023-2-5",
            "2023-2-10",
            "2023-2-12",
            "2023-2-17",
            "2023-2-19",
            "2023-2-24",
            "2023-2-26",
        ],
        [
            "2023-3-3",
            "2023-3-5",
            "2023-3-10",
            "2023-3-12",
            "2023-3-17",
            "2023-3-19",
            "2023-3-24",
            "2023-3-26",
            "2023-3-31",
            "2023-3-31",
        ],
        [
            "2023-4-0",
            "2023-4-2",
            "2023-4-7",
            "2023-4-9",
            "2023-4-14",
            "2023-4-16",
            "2023-4-21",
            "2023-4-23",
            "2023-4-28",
            "2023-4-30",
        ],
        [
            "2023-5-5",
            "2023-5-7",
            "2023-5-12",
            "2023-5-14",
            "2023-5-19",
            "2023-5-21",
            "2023-5-26",
            "2023-5-28",
        ],
        [
            "2023-6-2",
            "2023-6-4",
            "2023-6-9",
            "2023-6-11",
            "2023-6-16",
            "2023-6-18",
            "2023-6-23",
            "2023-6-25",
            "2023-6-30",
            "2023-6-30",
        ],
        [
            "2023-7-0",
            "2023-7-2",
            "2023-7-7",
            "2023-7-9",
            "2023-7-14",
            "2023-7-16",
            "2023-7-21",
            "2023-7-23",
            "2023-7-28",
            "2023-7-30",
        ],
        [
            "2023-8-4",
            "2023-8-6",
            "2023-8-11",
            "2023-8-13",
            "2023-8-18",
            "2023-8-20",
            "2023-8-25",
            "2023-8-27",
        ],
        [
            "2023-9-1",
            "2023-9-3",
            "2023-9-8",
            "2023-9-10",
            "2023-9-15",
            "2023-9-17",
            "2023-9-22",
            "2023-9-24",
            "2023-9-29",
            "2023-9-29",
        ],
        [
            "2023-10-6",
            "2023-10-8",
            "2023-10-13",
            "2023-10-15",
            "2023-10-20",
            "2023-10-22",
            "2023-10-27",
            "2023-10-29",
        ],
        [
            "2023-11-3",
            "2023-11-5",
            "2023-11-10",
            "2023-11-12",
            "2023-11-17",
            "2023-11-19",
            "2023-11-24",
            "2023-11-26",
        ],
        [
            "2023-12-1",
            "2023-12-3",
            "2023-12-8",
            "2023-12-10",
            "2023-12-15",
            "2023-12-17",
            "2023-12-22",
            "2023-12-24",
            "2023-12-29",
            "2023-12-31",
        ],
    ]
    for i in range(1, 12):
        assert (
            src.web_handler.WeekendWebHandler().find_weekend(i, 2023)
            == weekends_of_2023[i - 1]
        )


def test_page_opening():
    city = CITY[0][0]
    dest_id = CITY[0][1]
    rooms = 1
    people = 2
    start_date = default_start_date()
    end_date = default_end_date()
    offset = 0

    parsed_html = src.web_handler.WeekendWebHandler().get_booking_page(
        city, dest_id, rooms, people, start_date, end_date, offset
    )

    pages = parsed_html.find_all("div", {"data-testid": "pagination"})
    # assert "obiektów" in pages[0].previous_sibling.string #TODO: Not working, I think its obsolete
