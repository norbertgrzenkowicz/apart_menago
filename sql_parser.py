import datetime
import calendar
from sqlalchemy import create_engine, text


class SQL_parser:
    def __init__(self, scrapped_data) -> None:
        self.save_to_sql(scrapped_data)

    def save_to_sql(self, scrapped_data):
        table_name = (
            calendar.month_name[self.reservation_input["month"]].lower()
            + "_"
            + str(datetime.datetime.now().year)
        )

        password = input("Postgres Password: ")
        engine = create_engine(
            f"postgresql+psycopg://postgres:{password}@localhost:5432/test?", echo=False
        )
        for df in scrapped_data:
            df.to_sql(table_name, con=engine, if_exists="append")

    def extract_to_some_format(self):
        pass
