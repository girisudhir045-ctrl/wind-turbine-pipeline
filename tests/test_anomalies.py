"""
Tests for src/anomalies.py
"""
from src.anomalies import detect_anomalies
from src.stats import calculate_summary_stats
from src.ingest import load_raw_data


def test_detect_anomalies_flags_outlier_turbine(spark, tmp_path):
    # 5 turbines with similar output, 1 turbine wildly different
    csv_content = (
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,3.0\n"
        "2022-03-01 00:00:00,2,10.0,180,3.1\n"
        "2022-03-01 00:00:00,3,10.0,180,2.9\n"
        "2022-03-01 00:00:00,4,10.0,180,3.0\n"
        "2022-03-01 00:00:00,5,10.0,180,3.2\n"
        "2022-03-01 00:00:00,6,10.0,180,50.0\n"
    )
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(csv_content)

    df = load_raw_data(spark, [str(csv_path)])
    stats_df = calculate_summary_stats(df)
    anomalies_df = detect_anomalies(stats_df)

    result = anomalies_df.collect()

    flagged_turbines = [row.turbine_id for row in result]
    assert 6 in flagged_turbines
    assert 1 not in flagged_turbines
    assert 2 not in flagged_turbines