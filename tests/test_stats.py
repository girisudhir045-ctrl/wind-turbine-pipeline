"""
Tests for src/stats.py
"""
from src.ingest import load_raw_data
from src.stats import calculate_summary_stats


def test_calculate_summary_stats_min_max_avg(spark, tmp_path):
    csv_content = (
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,2.0\n"
        "2022-03-01 01:00:00,1,10.0,180,4.0\n"
        "2022-03-01 02:00:00,1,10.0,180,6.0\n"
    )
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(csv_content)
    df = load_raw_data(spark, [str(csv_path)])

    result = calculate_summary_stats(df).collect()

    assert len(result) == 1
    row = result[0]
    assert row.turbine_id == 1
    assert row.min_power == 2.0
    assert row.max_power == 6.0
    assert row.avg_power == 4.0


def test_calculate_summary_stats_groups_by_turbine(spark, tmp_path):
    csv_content = (
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,2.0\n"
        "2022-03-01 00:00:00,2,10.0,180,8.0\n"
    )
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(csv_content)
    df = load_raw_data(spark, [str(csv_path)])

    result = calculate_summary_stats(df).collect()

    assert len(result) == 2
    powers = {row.turbine_id: row.avg_power for row in result}
    assert powers[1] == 2.0
    assert powers[2] == 8.0