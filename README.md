# Wind Turbine Data Pipeline (PoC)

## Overview
<!-- 2-3 sentences: what this does, at a glance -->

## Architecture
<!-- Bullet flow or diagram:
     raw CSVs -> ingest -> clean -> stats + anomalies -> storage (SQLite) -->

## Assumptions
<!-- Be explicit and honest - this is what they're grading. Cover: -->
- **Missing values:** <!-- drop vs impute, and how -->
- **Missing rows:** <!-- how you detect + handle a fully absent hourly reading -->
- **Outlier definition:** <!-- hard bounds vs statistical, and where each is applied -->
- **Anomaly definition:** <!-- per-turbine vs cross-turbine comparison, and why -->
- **Time window:** <!-- calendar day vs rolling 24h, and why -->
- **Incremental ingestion:** <!-- how you'd avoid reprocessing the whole file each day, even if the PoC doesn't fully implement it -->

## How to run
```bash
pip install -r requirements.txt
python -m src.pipeline
```

## How to test
```bash
pytest
```

## Productionising this (for the follow-up interview)
<!-- A few bullets on what you'd change for a real deployment: -->
- Scheduling / orchestration (e.g. Airflow, incremental/watermarked ingestion)
- Swapping SQLite for a real warehouse
- Data quality monitoring / alerting on anomalies
- Handling schema drift, scaling to more turbines
- Streaming vs batch trade-offs
