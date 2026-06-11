# Data Model

## Market snapshot

Each row represents one market outcome at one timestamp.

| Field | Description |
|---|---|
| snapshot_ts | UTC timestamp |
| source | Data source |
| event_slug | Polymarket event slug |
| market_slug | Polymarket market slug |
| market_id | Market identifier if available |
| question | Market question |
| outcome | Outcome label |
| current_price | Market-implied probability / price |
| volume | Reported volume |
| liquidity | Reported liquidity |
| spread | Bid/ask spread if available |
| active | Active market flag |
| closed | Closed market flag |

## Narrative map

This is manual in v0.

| Field | Description |
|---|---|
| team_or_market | Team, country, player or market |
| public_narrative | What the public seems to believe |
| market_price | Market-implied probability |
| narrative_gap | Difference between price and story |
| catalyst | News or event that may explain movement |
| failure_mode | Why the signal may be false |
| confidence | low / medium / high |
| signal_type | structural / tactical / speculative |

## Publication log

| Field | Description |
|---|---|
| date | Publication date |
| post_type | X thread / Substack / short note |
| title | Post title |
| link | URL |
| impressions | X/Substack impressions |
| bookmarks | X bookmarks |
| replies | Useful replies |
| notes | Lessons learned |
