"""
Anomaly detection: flag turbines whose average power output is more
than 2 standard deviations from the mean across all turbines in the
same day (peer comparison, not self-comparison).
"""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import Window


def detect_anomalies(stats_df: DataFrame) -> DataFrame:
    window = Window.partitionBy("day")

    df = stats_df.withColumn("peer_mean", F.avg("avg_power").over(window))
    df = df.withColumn("peer_stddev", F.stddev("avg_power").over(window))
    df = df.withColumn(
        "is_anomaly",
        F.abs(F.col("avg_power") - F.col("peer_mean")) > 2 * F.col("peer_stddev")
    )

    return df.filter(F.col("is_anomaly"))