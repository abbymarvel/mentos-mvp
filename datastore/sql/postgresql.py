from collections import namedtuple

import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

from config.utils import get_env_value


class PostgreSQLClient:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=get_env_value("DB_HOST"),
                port=get_env_value("DB_PORT"),
                user=get_env_value("DB_USER"),
                password=get_env_value("DB_PASSWORD"),
                database=get_env_value("DB_NAME")
            )

            # Create a cursor to perform database operations
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)


    def map_cursor(self, cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple("Result", [col[0] for col in desc])
        return [dict(row) for row in cursor.fetchall()]


    def query(self, query_str: str):
        res = []
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # cursor.execute("SET SEARCH_PATH TO BABADU")
            try:
                cursor.execute(query_str)

                if query_str.strip().upper().startswith("SELECT"):
                    res = self.map_cursor(cursor)
                else:
                    res = cursor.rowcount
                    self.connection.commit()
            except Exception as e:
                res = e

        return res
    
    def to_sql_array(self, values: list) -> str:
        arr = "{"
        for i, v in enumerate(values):
            arr += str(v)
            if i != len(values) - 1:
                arr += ","
        arr += "}"
        return arr
