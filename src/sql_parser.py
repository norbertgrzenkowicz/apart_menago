import datetime
import calendar
from sqlalchemy import create_engine  # , text
import src.clients
import pandas as pd


class SQL_parser:
    def __init__(self) -> None:
        _password = input("Postgres Password: ")
        self._engine = create_engine(
            f"postgresql+psycopg://postgres:{_password}@localhost:5432/test?",
            echo=False,
        )

    def save_to_sql(self, scrapped_data, scrapped_month):
        table_name = (
            calendar.month_name[scrapped_month].lower()
            + "_"
            + str(datetime.datetime.now().year)
        )

        for df in scrapped_data:
            df.to_sql(table_name, con=self._engine, if_exists="append")

    def sql_to_csv(self):
        pd.read_sql_query(src.clients.DUPA_QUERY[0], con=self._engine).to_csv("out.csv")


if __name__ == "__main__":
    SQL_parser().sql_to_df()
