# Wind Turbine Data Pipeline (PoC)

## Overview
This is a proof-of-concept batch pipeline that ingests hourly wind turbine
sensor readings (wind speed, wind direction, power output) from CSV files,
cleans the data, computes daily summary statistics per turbine, flags
turbines whose output deviates significantly from their peers, and persists
the results to a local SQLite database.

## Architecture

`pipeline.py` orchestrates the above; each module is independently testable
with no business logic living in the orchestrator itself.

## Assumptions
- **Missing rows vs missing values**: both are handled. A missing hourly
  reading for a turbine (row entirely absent) is detected by comparing
  against the expected hourly grid; a present row with a null field
  (e.g. wind_speed) is imputed via forward-fill.
- **Imputation strategy**: forward-fill was used for missing values, rather
  than interpolation, for simplicity in this PoC. Interpolation would be
  a more statistically defensible choice for continuous sensor data and
  is something I'd swap in with more time.
- **Outlier definition**: I distinguish between hard-bound outliers
  (physically impossible values - e.g. negative power output, wind
  direction outside 0-359 degrees) applied during cleaning, and statistical
  outliers (the 2-stddev rule) applied separately during anomaly
  detection. These serve different purposes: one guards against sensor
  errors, the other flags genuine behavioural deviation.
- **Anomaly scope - cross-turbine (peer) comparison**: I compare each
  turbine's daily average power output against the mean and standard
  deviation across all turbines on that same day, rather than against
  each turbine's own historical baseline. This was simpler to implement
  and test given a single month of data with no obvious "normal" baseline
  period to train against. The alternative (per-turbine/temporal
  comparison) is equally valid and would answer a different question -
  "is turbine X behaving unlike itself?" rather than "is turbine X an
  outlier among its peers today?" - and is worth discussing further.
- **Time window**: I used calendar-day buckets (`to_date(timestamp)`)
  rather than a rolling 24-hour window, for simplicity and easier
  reasoning about results.

## How to run
```bash
pip install -r requirements.txt
python -m src.pipeline
```

## How to test
```bash
pytest -v
```
All five core modules (ingest, clean, stats, anomalies, storage) have unit
tests using small, hand-crafted synthetic data with deliberate edge cases
(nulls, missing hours, negative values, an injected outlier turbine) rather
than the full clean dataset, so the logic is actually exercised.

## Productionising this
For a real deployment, I'd change:
- **Scheduling / orchestration**: run via Airflow (or similar) on a daily
  schedule, with incremental/watermarked ingestion so each run only
  processes new files rather than reprocessing the whole month.
- **Storage**: swap SQLite for a proper warehouse (Postgres/Redshift/
  Snowflake) - SQLite doesn't handle concurrent writes or scale well.
- **Monitoring/alerting**: wire the anomalies table to actually notify
  someone (Slack/email/PagerDuty) rather than just sitting in a table.
- **Schema evolution & scaling**: handle new turbines being added, sensor
  schema changes, and a growing turbine fleet without code changes -
  e.g. schema registry, more defensive ingestion.
- **Streaming vs batch**: if near-real-time anomaly detection matters,
  this could move to a streaming architecture (e.g. Spark Structured
  Streaming) rather than daily batch.

## What I'd do differently with more time
- Interpolation instead of forward-fill for missing values
- Discuss/implement per-turbine (temporal) anomaly detection as a second
  option alongside cross-turbine, and compare results
- Add integration/end-to-end test for `pipeline.py` itself, not just
  per-module unit tests
