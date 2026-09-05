"""
Storage: persist DataFrames to a local SQLite database via pandas.
"""
import sqlite3
from pyspark.sql import DataFrame


def save_to_db(df: DataFrame, table_name: str, db_path: str = "data/warehouse.db") -> None:
    pandas_df = df.toPandas()
    conn = sqlite3.connect(db_path)
    pandas_df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()