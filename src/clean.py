"""
Cleaning layer: handles missing values, missing rows, and outliers.

This is graded on YOUR reasoning, so the notes below are prompts, not
answers. Write your final decisions in the README, not just in code
comments.

Two distinct problems to solve here, don't conflate them:

1. MISSING VALUES  - a row exists, but wind_speed / power_output / etc
   is null. Options: drop the row, forward-fill, interpolate between
   neighbouring readings (recommended for hourly time series - it's
   more defensible than forward-fill since it accounts for trend).

2. MISSING ROWS - an expected hourly reading for a turbine is simply
   absent (sensor didn't report at all). To catch this you need to
   generate the *expected* timestamp grid per turbine (e.g. hourly
   from min to max timestamp) and left-join your actual data onto it -
   the gaps become nulls you can then treat like problem #1, or leave
   as explicit gaps depending on your chosen strategy.

3. OUTLIERS - values that are physically implausible or statistically
   extreme. Suggested split:
   - hard sanity bounds (e.g. wind_speed >= 0, power_output >= 0,
     0 <= wind_direction < 360) - these are unambiguous, just clip or
     null them out
   - statistical outliers - could reuse the same 2-stddev logic as the
     anomaly detector, OR use a simpler IQR/z-score rule here and save
     the 2-stddev rule specifically for "anomalies" as the brief
     defines them. State which you picked and why.

TODO (you): implement clean_data() using your chosen strategy above.
"""
from pyspark.sql import DataFrame


def clean_data(df: DataFrame) -> DataFrame:
    """
    Take a raw (possibly dirty) turbine readings DataFrame and return
    a cleaned version: missing rows/values handled, outliers handled.

    Should be a pure function - no I/O - so it's easy to unit test
    with small synthetic DataFrames.
    """
    raise NotImplementedError
