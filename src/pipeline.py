"""
Pipeline entrypoint: wires ingestion -> cleaning -> stats -> anomalies
-> storage together. This is orchestration only - no business logic
should live here, it should all be in the other modules so each piece
stays independently testable.

Run with: python -m src.pipeline
"""
import glob

from src.spark_session import get_spark
from src.ingest import load_raw_data
from src.clean import clean_data
from src.stats import calculate_summary_stats
from src.anomalies import detect_anomalies
from src.storage import save_to_db

RAW_DATA_GLOB = "data/raw/data_group_*.csv"


def run() -> None:
    spark = get_spark()

    paths = sorted(glob.glob(RAW_DATA_GLOB))
    raw_df = load_raw_data(spark, paths)

    cleaned_df = clean_data(raw_df)
    stats_df = calculate_summary_stats(cleaned_df)
    anomalies_df = detect_anomalies(stats_df)

    save_to_db(cleaned_df, table_name="cleaned_readings")
    save_to_db(stats_df, table_name="turbine_stats")
    save_to_db(anomalies_df, table_name="anomalies")

    print(f"Pipeline complete. "
          f"{cleaned_df.count()} readings, "
          f"{stats_df.count()} stat rows, "
          f"{anomalies_df.count()} anomalies flagged.")


if __name__ == "__main__":
    run()
