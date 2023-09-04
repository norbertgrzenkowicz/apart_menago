import datetime
import calendar
from sqlalchemy import create_engine  # , text


class SQL_parser:
    def __init__(self, scrapped_data, scrapped_month) -> None:
        self.save_to_sql(scrapped_data, scrapped_month)

    def save_to_sql(self, scrapped_data, scrapped_month):
        table_name = (
            calendar.month_name[scrapped_month].lower()
            + "_"
            + str(datetime.datetime.now().year)
        )

        password = input("Postgres Password: ")
        engine = create_engine(
            f"postgresql+psycopg://postgres:{password}@localhost:5432/test?",
            echo=False,
        )
        for df in scrapped_data:
            df.to_sql(table_name, con=engine, if_exists="append")

    def extract_to_some_format(self):
        pass


if __name__ == "__main__":
    SQL_parser(scrapped_data=[], scrapped_month=9)
