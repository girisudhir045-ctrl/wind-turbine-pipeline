# Wind Turbine Data Pipeline (PoC)

## Overview
This is a small pipeline I built to take raw hourly readings from a wind
turbine farm, clean up whatever's wrong with them, work out how each
turbine's doing day to day, and flag anything that looks off compared to
the rest of the fleet. Everything ends up in a local SQLite database at
the end so it's easy to poke around and check.

## Architecture
It's a straight line, five steps:

1. **`ingest.py`** reads in the raw CSVs and gets them into a consistent shape
2. **`clean.py`** deals with the messy stuff — bad values, missing hours, gaps in readings
3. **`stats.py`** works out each turbine's daily min, max, and average power
4. **`anomalies.py`** flags any turbine that's way out of line with everyone else that day
5. **`storage.py`** saves it all to SQLite

`pipeline.py` just calls these one after another — it doesn't actually do anything itself, on purpose. That way each step can be tested on its own without needing the whole pipeline running.

## Assumptions
There were a few spots in the brief where I had to just make a call, so here's my thinking on each one.

**Missing data comes in two flavours, and I treated them differently.** Sometimes a row's there but a value's blank — that gets forward-filled from the last good reading. Other times the row's just not there at all, like the sensor never reported that hour. For that one I had to build out what the "full" hourly schedule should look like and compare against it to spot the gap, then fill it the same way.

**I went with forward-fill rather than interpolation, mostly because of time.** If I'm honest, interpolation is probably the smarter choice here — wind speed doesn't just jump and hold steady, so forward-fill can leave a slightly unrealistic flat patch if there's a longer gap. It was the simpler thing to get right quickly though, and it's an easy swap later.

**I'm keeping "bad sensor reading" and "genuine anomaly" as two separate ideas.** A negative power reading isn't the turbine having a weird day, it's just broken data, so that gets cleaned out early. An anomaly is something else — it's about a turbine actually behaving strangely, which felt like it deserved its own logic rather than getting lumped in with basic cleaning.

**Honestly, the anomaly bit is the part I went back and forth on the most.** The brief says "deviated from expected output" but doesn't really say expected *compared to what*. Compared to itself, historically? Or compared to the other turbines on the same day? I ended up going with comparing turbines to each other on the same day, mainly because with only a month of data, comparing a turbine to its own past felt a bit shaky — there's not really a clean stretch of "normal" history to measure against without it circling back on itself. Comparing turbines side by side on the same day felt more solid and was easier to test properly too. It's not the only valid way to do it though — if I were building this properly I'd want to sit down with whoever actually owns turbine maintenance and ask which question they actually care about.

**I bucketed everything by calendar day rather than a rolling 24 hours.** Just simpler — every reading belongs to exactly one day, no overlap to think about.

## How to run
```bash
pip install -r requirements.txt
python -m src.pipeline
```

## How to test
```bash
pytest -v
```
The tests all use small, made-up data with problems built in on purpose — nulls, missing hours, one turbine way off from the rest. The real month of data I was given is actually completely clean, so testing against it wouldn't really prove anything.

## Productionising this
This is very much a PoC, so a few things I'd change if this were actually going into production:

- **Get it scheduled properly** — something like Airflow, running daily, and only pulling in new files instead of reprocessing the whole month every single time.
- **Ditch SQLite** — it's fine for a demo but won't hold up with real concurrent writes or real data volume. Something like Postgres or Redshift instead.
- **Actually alert someone** — right now anomalies just quietly sit in a table. Nobody's going to check that every day. It should ping someone on Slack or by email instead.
- **Plan for the fleet changing** — new turbines get added, sensors change, that shouldn't mean rewriting code every time.
- **Think about streaming** — if catching anomalies quickly actually matters, a daily batch job isn't fast enough. Something like Spark Structured Streaming would make more sense.

## What I'd do differently with more time
- Swap forward-fill for interpolation
- Actually build out the "compare a turbine to its own history" version of anomaly detection too, and see how it compares to what I did
- Write a proper test that runs the whole pipeline end to end, not just each piece separately