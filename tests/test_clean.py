"""
Tests for src/clean.py
"""
from src.clean import clean_data, fill_missing_timestamps, impute_missing_values


def test_clean_data_nulls_negative_power(dirty_readings_df):
    result = clean_data(dirty_readings_df)
    row = result.filter(result.turbine_id == 1).filter(result.wind_speed == 11.0).first()
    assert row.power_output is None


def test_fill_missing_timestamps_exposes_gap(spark, dirty_readings_df):
    result = fill_missing_timestamps(spark, dirty_readings_df)
    missing_row = result.filter(
        (result.turbine_id == 2) & (result.timestamp == "2022-03-01 01:00:00")
    ).first()
    assert missing_row is not None
    assert missing_row.power_output is None


def test_impute_missing_values_forward_fills(spark, dirty_readings_df):
    cleaned = clean_data(dirty_readings_df)
    full = fill_missing_timestamps(spark, cleaned)
    imputed = impute_missing_values(full)
    result = imputed.filter(imputed.turbine_id == 2).orderBy("timestamp").collect()
    # turbine 2's missing hour should be forward-filled from hour 0
    assert result[1].wind_speed is not None