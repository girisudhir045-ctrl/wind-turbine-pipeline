"""
Ingestion layer: reads the raw per-group CSVs and returns a single,
schema-normalised Spark DataFrame.

Expected raw schema (per CSV):
    timestamp        string   e.g. "2022-03-01 00:00:00"
    turbine_id       int
    wind_speed       double   (m/s)
    wind_direction   int      (degrees, 0-359)
    power_output     double   (MW)
"""
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

SCHEMA = StructType([
    StructField("timestamp", StringType(), True),
    StructField("turbine_id", IntegerType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("wind_direction", IntegerType(), True),
    StructField("power_output", DoubleType(), True),
])


def load_raw_data(spark: SparkSession, paths: list[str]) -> DataFrame:
    """
    Read one or more raw turbine CSVs and return them unioned into a
    single DataFrame with a normalised schema.
    """
    df = spark.read.csv(paths, header=True, schema=SCHEMA)
    df = df.withColumn("timestamp", F.to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss"))
    return df