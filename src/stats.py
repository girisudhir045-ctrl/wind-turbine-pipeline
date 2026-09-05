"""
Summary statistics layer.

For each turbine, over a given time window (default: calendar day),
calculate min / max / average power_output.

Implementation notes:
    - PySpark: this is a groupBy(turbine_id, window_bucket).agg(...)
      Use `pyspark.sql.functions.window()` if you want true rolling/
      calendar windows, or just truncate the timestamp to a date with
      `F.to_date()` if a calendar-day bucket is enough (simpler, and
      defensible to state as your assumption given the brief says
      "e.g. 24 hours").
    - Keep the window size configurable (a function parameter), don't
      hardcode "24 hours" - makes it testable with smaller windows too.

TODO (you): implement calculate_summary_stats()
"""
from pyspark.sql import DataFrame


def calculate_summary_stats(df: DataFrame, window: str = "1 day") -> DataFrame:
    """
    Parameters
    ----------
    df : DataFrame
        Cleaned turbine readings.
    window : str
        Spark-style window duration string, e.g. "1 day", "24 hours".

    Returns
    -------
    DataFrame
        Columns: turbine_id, window_start, window_end,
        min_power, max_power, avg_power
    """
    raise NotImplementedError
