"""
Cleaning layer: handles missing values, missing rows, and outliers.
"""
from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F


def clean_data(df: DataFrame) -> DataFrame:
    """
    Hard-bound outlier check: null out physically impossible values
    so they get handled by imputation later.
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


def fill_missing_timestamps(spark: SparkSession, df: DataFrame) -> DataFrame:
    """
    Build the expected hourly timestamp grid per turbine and left-join
    the actual data onto it, exposing missing sensor readings as nulls.
    """
    bounds = df.select(
        F.min("timestamp").alias("min_ts"),
        F.max("timestamp").alias("max_ts")
    ).first()

    full_range = spark.range(1).select(
        F.explode(
            F.sequence(
                F.lit(bounds["min_ts"]),
                F.lit(bounds["max_ts"]),
                F.expr("interval 1 hour")
            )
        ).alias("timestamp")
    )

    turbine_ids = df.select("turbine_id").distinct()
    expected_grid = full_range.crossJoin(turbine_ids)

    full_df = expected_grid.join(df, on=["timestamp", "turbine_id"], how="left")
    return full_df


def impute_missing_values(df: DataFrame) -> DataFrame:
    """
    Forward-fill missing values per turbine, ordered by time.
    """
    window = Window.partitionBy("turbine_id").orderBy("timestamp")

    df = df.withColumn("wind_speed", F.last("wind_speed", ignorenulls=True).over(window))
    df = df.withColumn("wind_direction", F.last("wind_direction", ignorenulls=True).over(window))
    df = df.withColumn("power_output", F.last("power_output", ignorenulls=True).over(window))

    return df