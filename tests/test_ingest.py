"""
Tests for src/ingest.py
"""
from src.ingest import load_raw_data


def test_load_raw_data_schema(spark, tmp_path):
    csv_content = (
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,3.0\n"
    )
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(csv_content)

    df = load_raw_data(spark, [str(csv_path)])

    assert dict(df.dtypes)["timestamp"] == "timestamp"
    assert dict(df.dtypes)["power_output"] == "double"


def test_load_raw_data_unions_multiple_files(spark, tmp_path):
    csv1 = tmp_path / "a.csv"
    csv1.write_text(
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,3.0\n"
    )
    csv2 = tmp_path / "b.csv"
    csv2.write_text(
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,2,11.0,190,3.5\n"
    )

    df = load_raw_data(spark, [str(csv1), str(csv2)])

    assert df.count() == 2
    assert sorted(row.turbine_id for row in df.select("turbine_id").collect()) == [1, 2]