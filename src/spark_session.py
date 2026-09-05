"""
Shared SparkSession factory.

Kept in its own module so both the pipeline entrypoint and the pytest
fixtures build the session the same way.
"""
from pyspark.sql import SparkSession


def get_spark(app_name: str = "wind-turbine-pipeline") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )
