import pytest
from src.spark_session import get_spark
from src.ingest import load_raw_data


@pytest.fixture(scope="session")
def spark():
    session = get_spark(app_name="pytest-session")
    yield session
    session.stop()


@pytest.fixture
def dirty_readings_df(spark, tmp_path):
    csv_content = (
        "timestamp,turbine_id,wind_speed,wind_direction,power_output\n"
        "2022-03-01 00:00:00,1,10.0,180,3.0\n"
        "2022-03-01 01:00:00,1,11.0,190,-5.0\n"
        "2022-03-01 00:00:00,2,,170,2.5\n"
    )
    csv_path = tmp_path / "dirty.csv"
    csv_path.write_text(csv_content)
    return load_raw_data(spark, [str(csv_path)])