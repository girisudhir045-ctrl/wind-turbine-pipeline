"""
Shared pytest fixtures.

`spark` - a local SparkSession scoped to the whole test session (Spark
sessions are expensive to start, don't create one per test).

`dirty_readings_df` - a SMALL, hand-crafted DataFrame with deliberate
problems baked in, so your clean/stats/anomaly tests have something to
actually catch. Don't test against the full month of real CSV data -
it's clean, so your outlier/anomaly logic would never be exercised.

Fill in the TODOs with rows that match what YOU decided counts as
dirty (see clean.py / anomalies.py docstrings for the categories to
cover: missing values, missing rows/timestamps, hard-bound outliers,
statistical outliers, and at least one genuine cross-turbine anomaly).
"""
import pytest
from src.spark_session import get_spark


@pytest.fixture(scope="session")
def spark():
    session = get_spark(app_name="pytest-session")
    yield session
    session.stop()


@pytest.fixture
def dirty_readings_df(spark):
    """
    TODO (you): build this with spark.createDataFrame(...) using a
    small explicit schema and ~10-20 rows covering:
      - a null wind_speed or power_output value
      - a missing hour for a turbine (i.e. just don't include that row)
      - a negative or impossible power_output (hard-bound outlier)
      - one turbine whose readings are consistently far from its
        peers in the same window (for anomaly detection to catch)
    """
    raise NotImplementedError
