"""
Ingestion layer: reads the raw per-group CSVs and returns a single,
schema-normalised Spark DataFrame.

Expected raw schema (per CSV):
    timestamp        string   e.g. "2022-03-01 00:00:00"
    turbine_id       int
    wind_speed       double   (m/s)
    wind_direction   int      (degrees, 0-359)
    power_output     double   (MW)

TODO (you): decide + implement
    - explicit schema definition (don't let Spark infer it - it's slow
      and can silently guess wrong types on messy data)
    - timestamp parsing to a proper TimestampType
    - a `source_file` or `ingested_at` column if you want lineage/audit
      info (nice to mention in the design doc even if you skip it)
"""
from pyspark.sql import DataFrame, SparkSession


def load_raw_data(spark: SparkSession, paths: list[str]) -> DataFrame:
    """
    Read one or more raw turbine CSVs and return them unioned into a
    single DataFrame with a normalised schema.

    Parameters
    ----------
    spark : SparkSession
    paths : list[str]
        Paths to the raw CSV files (e.g. data/raw/data_group_*.csv)

    Returns
    -------
    DataFrame
        Columns: timestamp (timestamp), turbine_id (int),
        wind_speed (double), wind_direction (int), power_output (double)
    """
    raise NotImplementedError
