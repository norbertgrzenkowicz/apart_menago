from web_handler import get_data
from date_funcs import valid_date, default_start_date, default_end_date
from sqlalchemy import create_engine, text

from itertools import product
import datetime
import calendar


def compute_products(*args):
    return list(product(*[*args]))


reservation_input = {
    "city": ["W%C5%82adys%C5%82awowo"],
    # "city": ["W%C5%82adys%C5%82awowo", "Rozewie", "Jastrzebia Gora", "Karwia"],
                 "rooms": 1,
                 "people": [2, 3, 4],
                 "start_date": default_start_date(),
                 "end_date": default_end_date(),
                 "month": 9,
                #  "timeofstay": [2, 3, 5, 7, 10, 14],
                 "timeofstay": [5, 7],
                 "save": False,
                 "weekend": False}

scrapped_data = []
for reservation_products in compute_products(reservation_input["city"], reservation_input["people"], reservation_input["timeofstay"])[:2]:
    scrapped_data.append(get_data(reservation_products[0], 
                                  reservation_input["rooms"], 
                                  reservation_products[1], 
                                  reservation_input["start_date"],
                                  reservation_input["end_date"], 
                                  reservation_input["month"], 
                                  reservation_products[2], 
                                  reservation_input["save"], 
                                  reservation_input["weekend"]))


table_name = (calendar.month_name[reservation_input["month"]].lower() + "_" + str(datetime.datetime.now().year))

password = input("Postgres Password: ")
engine = create_engine(f'postgresql+psycopg://postgres:{password}@localhost:5432/test?', echo=False)
for df in scrapped_data:
    df.to_sql(table_name, con= engine, if_exists='append')
# with engine.connect() as conn:
#     conn.execute(text("SELECT * FROM " + table_name)).fetchall() 
