# Intraday Snapshot Strategy

This document explains why and how the World Cup Market Intelligence system collects intraday Polymarket snapshots, separate from the full daily pipeline.

The project remains research-only.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Why collect intraday snapshots?

Prediction market prices are not static across a day.

Movement is concentrated around specific event windows:

- Before kickoff: markets move as team news, lineup confirmations, and pre-match sentiment emerge
- During the match: probability updates in real time as goals, red cards, and momentum shift
- After the final whistle: repricing happens quickly as outcomes resolve or future-round expectations adjust
- Hours after the match: slower secondary repricing as the broader market absorbs the result

A single daily snapshot at 08:00 misses all of this intraday movement.

The result is that the Daily Brief compares prices that are identical or near-identical, producing zero deltas and no signals.

Intraday snapshots solve this by creating a richer archive of timestamped data points.

The `compare_snapshots.py` script then has more material to work with, and the Daily Brief can reflect real probability movement.

---

## Why snapshot-only should not commit or push

The intraday snapshot runner (`scripts/run_snapshot_only.ps1`) is deliberately minimal:

- It runs only `scripts/update_snapshot.py --provider polymarket`
- It writes the snapshot to `data/processed/snapshots/` which is already listed in `.gitignore`
- It does not call git at any point
- It does not generate a Daily Brief
- It does not touch `data/private/`
- It does not commit or push

The reasons:

1. Snapshot files are local research data, not public deliverables. Committing them would bloat the repository with hundreds of timestamped CSV files.

2. Generating a public Daily Brief for every intraday snapshot would produce misleading reports with partial information.

3. The full pipeline (validate, generate brief, commit, push) runs once per day at 08:00. That is the authoritative public output.

4. Intraday snapshots are inputs to the next morning's brief, not outputs to publish.

---

## Recommended cadence for Day 2 to Day 7

This cadence is designed for Romania local time and covers the main match windows of the 2026 FIFA World Cup group stage.

| Time (Romania) | Runner | Action |
|---|---|---|
| 08:00 | `run_daily_pipeline.ps1` | Full pipeline: snapshot + brief + commit + push |
| 18:00 | `run_snapshot_only.ps1` | Snapshot only. Covers pre-evening match window |
| 21:30 | `run_snapshot_only.ps1` | Snapshot only. Covers during/post evening matches |
| 00:30 | `run_snapshot_only.ps1` | Snapshot only. Covers late matches (Americas zone) |

Windows Task Scheduler uses local time by default. Register intraday tasks as local Romania time.

These times are fixed for simplicity during the 7-day validation sprint. A match-aware dynamic scheduler may be evaluated for a future release.

---

## Match window rationale

World Cup 2026 group-stage matches are typically scheduled at these UTC times, which correspond to the following Romania local times:

| UTC kickoff | Romania local | Match zone |
|---|---|---|
| 05:00 | 07:00 | Central Asia / Middle East early |
| 18:00 | 20:00 | Europe / Africa prime time |
| 21:00 | 23:00 | Europe / Americas late |
| 00:00 | 02:00 | Americas overnight |
| 03:00 | 05:00 | Americas late / Pacific |

The 18:00 snapshot captures pre-match pricing for evening European games.

The 21:30 snapshot captures in-progress or post-match repricing for the same games.

The 00:30 snapshot captures post-match repricing for Americas games.

The 08:00 pipeline captures the overnight result and produces the authoritative Daily Brief.

---

## Known limitation: oldest-vs-newest comparison

The current `compare_snapshots.py` logic selects:

- Current: the most recently modified snapshot file
- Previous: the snapshot closest to 24 hours before the current one, with fallback to the oldest available file

This produces good results when the archive contains snapshots spread over multiple days.

However, after several days of intraday snapshots, the following limitation becomes relevant:

The "oldest available" file will be from the first day of snapshot collection (June 2026), and the comparison window will grow indefinitely rather than staying anchored to a 24-hour window.

This is acceptable for the 7-day validation sprint because:

- The primary goal is to confirm that delta is non-zero and directional
- A wider comparison window produces larger deltas, which are easier to interpret as meaningful movement
- The operator still reviews signals manually before any decision

A future release may add explicit comparison modes:

- `latest_vs_previous`: compare the two most recent snapshots
- `latest_vs_24h`: compare latest against the snapshot closest to exactly 24 hours prior
- `oldest_vs_latest`: current default, good for maximum historical context

Do not modify `compare_snapshots.py` during the validation sprint.

---

## How to register intraday tasks in Windows Task Scheduler

Run once as Administrator in PowerShell:

```powershell
# 18:00 snapshot
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"C:\Users\laure\projects\world-cup-market-intelligence-v0\scripts\run_snapshot_only.ps1`"" `
    -WorkingDirectory "C:\Users\laure\projects\world-cup-market-intelligence-v0"
$trigger = New-ScheduledTaskTrigger -Daily -At "18:00"
Register-ScheduledTask -TaskName "WorldCupMI-Snapshot-1800" -Action $action -Trigger $trigger -RunLevel Highest

# 21:30 snapshot
$trigger = New-ScheduledTaskTrigger -Daily -At "21:30"
Register-ScheduledTask -TaskName "WorldCupMI-Snapshot-2130" -Action $action -Trigger $trigger -RunLevel Highest

# 00:30 snapshot
$trigger = New-ScheduledTaskTrigger -Daily -At "00:30"
Register-ScheduledTask -TaskName "WorldCupMI-Snapshot-0030" -Action $action -Trigger $trigger -RunLevel Highest
```

Or run manually at any time:

```powershell
.\scripts\run_snapshot_only.ps1
```

---

## Research-only disclaimer

All data collected by this system is for personal market-intelligence research only.

Intraday snapshots do not constitute trading signals, betting tips, or investment advice.

Operators must apply independent judgment before any decision.

No financial edge is guaranteed.

The system is designed to observe and record, not to predict or recommend.

Powered by Mayior Capital.
