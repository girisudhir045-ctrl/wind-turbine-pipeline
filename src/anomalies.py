"""
Anomaly detection layer.

Brief's rule: flag turbines whose output is outside 2 standard
deviations from "the mean" over a time window - but the brief doesn't
say *whose* mean. This is the key ambiguity in the whole assessment -
pick one, document it, and be ready to discuss the other in interview.

Option A - PER-TURBINE (temporal): compare each turbine's readings in
    the window against that SAME turbine's own mean/stddev over a
    longer baseline (e.g. the full month). Answers: "is turbine 7
    behaving unlike itself?" Needs a baseline period to compute
    mean/stddev from - can't compute mean/stddev from a single 24h
    window and then check the same window against it (that's circular
    - almost nothing would ever be flagged as extreme relative to
    itself over such a short span unless you use a longer baseline).

Option B - CROSS-TURBINE (peer comparison): within a single time
    window, compare each turbine's avg output against the mean/stddev
    ACROSS ALL turbines in that same window. Answers: "is turbine 7 an
    outlier relative to its peers right now?" Simpler to implement,
    works fine even with just a 24h window, and arguably more useful
    operationally (peers should behave similarly if wind conditions
    are shared across the farm).

Recommendation for a PoC under time pressure: Option B is simpler to
implement AND justify. Document that Option A is the "true" temporal
anomaly detection you'd add in production with more historical
baseline data.

TODO (you): implement detect_anomalies() using your chosen option.
Remember: since the provided dataset has no real anomalies, you'll
need to inject a synthetic one (see tests/conftest.py) to prove this
function actually works.
"""
from pyspark.sql import DataFrame


def detect_anomalies(stats_df: DataFrame) -> DataFrame:
    """
    Parameters
    ----------
    stats_df : DataFrame
        Output of calculate_summary_stats() - one row per
        turbine per window.

    Returns
    -------
    DataFrame
        Subset of turbines/windows flagged as anomalous, with an
        added column explaining the deviation (e.g. z-score).
    """
    raise NotImplementedError
