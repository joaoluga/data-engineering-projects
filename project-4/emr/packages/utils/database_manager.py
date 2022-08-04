from sqlalchemy import create_engine
import pandas
from packages.utils.logger import Logger


class DatabaseManager:
    def __init__(
        self, database="analytics", user="admin", passwd="admin", host="pg_analytics", conn_string=None
    ):

        conn_string = conn_string or f"postgresql://{user}:{passwd}@{host}/{database}"
        self.__alchemy_conn = create_engine(conn_string).connect()
        self.__alchemy_conn.autocommit = True
        self.__logger = Logger()

    def create_table_with_pandas_df(self, df, table_name, schema_name="public"):
        self.__logger.info(f"Creating table: {schema_name}.{table_name}")
        df.to_sql(
            table_name,
            con=self.__alchemy_conn,
            schema=schema_name,
            if_exists="replace",
            index=True,
        )

    def __execute_query(self, query):
        return self.__alchemy_conn.execute(query)

    def create_schema(self, schema_name):
        self.__execute_query(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    def create_table_as_query(
        self, table_name, query, schema_name="public", drop_on_create=False
    ):
        if drop_on_create:
            self.drop_table(table_name=table_name, schema_name=schema_name)
        self.__execute_query(
            f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} AS {query}"
        )

    def drop_table(self, table_name, schema_name="public"):
        self.__execute_query(f"DROP TABLE IF EXISTS {schema_name}.{table_name}")

    def get_df(self, query):
        result = self.__alchemy_conn.execute(query)
        return pandas.DataFrame(result.fetchall())
