import time
from datetime import date

import sqlalchemy as db
import pandas as pd
from abc import ABC


class BaseDbMapper(ABC):
    """
    Database mapper to map and insert report data to sql database.
    """

    def __init__(self, connection_string: str, sql_table_name: str, schema: str=None):
        self._db_engine = db.create_engine(connection_string, echo=False)
        self._db_metadata = db.MetaData()
        self.sql_table_name = sql_table_name
        self.schema = schema

    def transform_df_to_sql_data(
            self, report_df: pd.DataFrame, **kwargs: dict
    ) -> pd.DataFrame:
        """
        Method to apply transformation to dataframe to map to sql table column data types and default values.
        :param report_df: Dataframe with data to be inserted in db
        :param kwargs: keyword arguments with additional fields.
        """
        pass

    def insert_dataframe_into_database(
            self,
            report_data_df: pd.DataFrame,
    ):
        """
        Method to insert dataframe to sql table.
        :param report_data_df: Dataframe with data to be inserted in db
.
        """
        try:
            with self._db_engine.connect() as db_connection:
                start = time.time()

                # db_table = db.Table(
                #     self.sql_table_name,
                #     self._db_metadata,
                #     schema=self.schema,
                #     autoload=True,
                #     autoload_with=db_connection,
                # )
                #
                #
                # # transform data to map sql table column types and default values.
                # report_data_df_sql_mapped = self.transform_df_to_sql_data(
                #     report_data_df, **{"run_id": run_id}
                # )
                # Insert data into sql table.
                chunks = [
                    report_data_df[i: i + 10]  # noqa: E203
                    for i in range(0, report_data_df.shape[0], 10)
                ]
                for chunk in chunks:
                    try:
                        chunk.to_sql(
                            self.sql_table_name,
                            db_connection,
                            schema=self.schema,
                            index=False,
                            if_exists="append",
                            chunksize=5000,
                        )
                    except Exception as ex:
                        print(ex)
                        raise ex

                db_connection.close()

        except Exception as ex:
            print(ex)
            raise ex

    def read_from_table(
            self, query: str, params=None, parse_dates=None
    ) -> pd.DataFrame:
        """
        Method to read data from sql database
        :param query: Query to fetch data
        :param params: parameters to be applied on query
        :param parse_dates: collection of fields to be parsed as date
        :return: dataframe containing the query result.
        """
        with self._db_engine.connect() as db_connection:
            df = pd.read_sql_query(
                query, con=db_connection, params=params, parse_dates=parse_dates
            )
            return df


class ProductsDBMapper(BaseDbMapper):
    """
    Generic class to use the abstract class methods.
    """

    def transform_df_to_sql_data(
            self, products_df: pd.DataFrame, **kwargs: dict
    ) -> pd.DataFrame:

        pass





