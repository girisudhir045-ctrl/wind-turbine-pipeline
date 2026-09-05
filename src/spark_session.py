"""
Shared SparkSession factory.
"""
import os
import sys
from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


def get_spark(app_name: str = "wind-turbine-pipeline") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[1]")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
        .getOrCreate()
    )