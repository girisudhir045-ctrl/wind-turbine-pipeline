"""
Storage layer: persists cleaned data + summary stats (+ anomalies) to
a database.

For a PoC, SQLite is a defensible, zero-setup choice - mention in the
README that production would likely use Postgres/Redshift/a warehouse,
and that this function's interface wouldn't need to change much to
swap the backend (just the connection string), IF you write it using
SQLAlchemy or Spark's own JDBC writer rather than something
SQLite-specific.

Two reasonable implementation paths:
    1. Convert Spark DataFrame -> pandas -> write with SQLAlchemy
       (simplest for a PoC-scale dataset)
    2. Use Spark's df.write.jdbc(...) directly (more "production-like"
       but requires a JDBC driver for SQLite, which is extra setup -
       probably not worth it for a few-hour PoC)

TODO (you): implement save_to_db() - pick one path and justify it.
"""
from pyspark.sql import DataFrame


def save_to_db(df: DataFrame, table_name: str, db_path: str = "data/warehouse.db") -> None:
    """
    Persist a DataFrame to a table in the (SQLite, for this PoC)
    database, replacing any existing table of the same name.
    """
    raise NotImplementedError
