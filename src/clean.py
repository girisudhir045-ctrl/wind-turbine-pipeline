"""
Cleaning layer: handles missing values, missing rows, and outliers.
"""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def clean_data(df: DataFrame) -> DataFrame:
    """
    Take a raw (possibly dirty) turbine readings DataFrame and return
    a cleaned version: hard-bound outliers nulled out (to be handled
    by imputation), missing rows/values still TODO.
    """
    df = df.withColumn(
        "power_output",
        F.when(F.col("power_output") < 0, None).otherwise(F.col("power_output"))
    )
    df = df.withColumn(
        "wind_speed",
        F.when(F.col("wind_speed") < 0, None).otherwise(F.col("wind_speed"))
    )
    df = df.withColumn(
        "wind_direction",
        F.when(
            (F.col("wind_direction") < 0) | (F.col("wind_direction") > 359),
            None
        ).otherwise(F.col("wind_direction"))
    )
    return df
