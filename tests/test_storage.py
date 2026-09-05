"""
Tests for src/storage.py
"""
import sqlite3
import pandas as pd

from src.storage import save_to_db
from src.ingest import load_raw_data


def test_save_to_db_writes_rows(spark, tmp_path):
    csv_content = (
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,3.0\n"
        "2022-03-01 01:00:00,2,11.0,190,3.5\n"
    )
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(csv_content)
    df = load_raw_data(spark, [str(csv_path)])

    db_path = tmp_path / "test_warehouse.db"
    save_to_db(df, table_name="readings", db_path=str(db_path))

    conn = sqlite3.connect(str(db_path))
    result = pd.read_sql("SELECT * FROM readings", conn)
    conn.close()

    assert len(result) == 2
    assert set(result["turbine_id"]) == {1, 2}