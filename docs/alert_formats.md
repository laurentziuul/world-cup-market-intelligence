# Alert Formats

This document defines short alert formats for World Cup Market Intelligence.

These alerts are designed for:

- Telegram
- Discord
- email snippets
- private community posts
- manual daily brief distribution
- future automation

The alerts are research-only.

They are not betting advice.

They are not investment advice.

They are not financial advice.

They are not prediction signals.

Powered by Mayior Capital.

---

## Alert principles

Alerts should be:

- short
- readable
- structured
- research-only
- linked to dashboards when possible
- clear about uncertainty
- clear when manual review is needed

Alerts should not say:

- bet this
- guaranteed edge
- lock
- free money
- prediction
- sure win
- trade this
- buy or sell

The correct language is:

- movement detected
- review priority
- catalyst watch
- liquidity spike
- manual review required
- data may be stale
- research-only

---

## 1. Probability mover alert

Use this when a team has a notable probability move.

Format:

- Team
- Probability change
- Current probability
- Signal label
- Review priority
- Possible catalyst
- Dashboard link
- Research-only note

Example:

World Cup Market Intelligence Alert

Team: Example Team A

Movement: +4.2 percentage points in 24h

Current probability: 12.8%

Signal: moderate positive move

Review priority: High

Possible catalyst: squad update / match result / narrative shift

Interpretation: probability movement deserves manual review, especially if supported by liquidity and volume.

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Research-only. Not betting advice.

---

## 2. Negative probability mover alert

Use this when a team has a notable negative probability move.

Example:

World Cup Market Intelligence Alert

Team: Example Team B

Movement: -3.1 percentage points in 24h

Current probability: 7.4%

Signal: moderate negative move

Review priority: Medium

Possible catalyst: injury watch / poor result / lower market confidence

Interpretation: negative movement may reflect new information, narrative pressure or market overreaction.

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Research-only. Not betting advice.

---

## 3. Liquidity spike alert

Use this when liquidity increases meaningfully.

Example:

Liquidity Spike Alert

Team: Example Team C

Liquidity change: +38%

Current liquidity: example value

Signal: liquidity expansion

Review priority: High

Interpretation: higher liquidity can make a market move more meaningful, but it does not prove correctness.

Check together with:

- probability movement
- volume movement
- catalyst notes
- market structure

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Research-only. Not investment or betting advice.

---

## 4. Volume spike alert

Use this when volume increases meaningfully.

Example:

Volume Spike Alert

Team: Example Team D

Volume change: +52%

Current volume: example value

Signal: volume spike

Review priority: High

Interpretation: volume spike may indicate increased attention or narrative pressure.

Manual review needed before interpretation.

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Research-only. Not betting advice.

---

## 5. Catalyst watch alert

Use this when a catalyst note matches market movement.

Example:

Catalyst Watch Alert

Team: Example Team E

Catalyst type: injury watch

Catalyst note: player availability uncertainty

Matched signal: moderate negative move

Review priority: Medium

Interpretation: catalyst notes may help explain market movement, but they do not prove causality.

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Research-only. Not betting advice.

---

## 6. Team review priority alert

Use this when a team enters high manual review priority.

Example:

Team Review Priority Alert

Team: Example Team F

Review priority: High

Net signal score: positive

Positive signals: multiple

Negative signals: limited

Catalyst matches: present

Interpretation: this team deserves manual review because market movement and catalyst context are aligned.

This does not mean the team is a bet.

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Research-only. Not betting advice.

---

## 7. Stale data warning alert

Use this when data freshness is stale or metadata is missing.

Example:

Data Freshness Warning

Status: stale or partially missing data

Issue: generated outputs may not reflect the latest market state

Interpretation: dashboard should be treated as historical context until refreshed.

Recommended action:

- rerun freshness check
- regenerate dashboard metadata
- regenerate trends dashboard

Commands:

- python scripts/check_data_freshness.py
- python scripts/generate_dashboard_metadata.py
- python scripts/generate_trends_dashboard.py

Research-only. Do not overinterpret stale data.

---

## 8. Daily summary alert

Use this as a short daily Telegram or Discord post.

Example:

World Cup Market Intelligence Daily Snapshot

Top probability mover: Example Team A, +4.2pp

Top liquidity mover: Example Team C, +38%

Top volume mover: Example Team D, +52%

High review priority teams: Example Team A, Example Team C, Example Team F

Catalyst watch: injury watch, squad update, narrative shift

Dashboard: https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Full daily brief: https://laurentziuul.github.io/world-cup-market-intelligence/briefs/latest.md

Research-only. Not betting advice.

---

## 9. Premium brief teaser

Use this for public marketing without giving everything away.

Example:

Today in World Cup Market Intelligence:

- 3 teams had notable probability movement
- 2 teams showed liquidity expansion
- 1 team entered high manual review priority
- catalyst watch includes squad and injury-related notes
- data freshness status: available

Read the public dashboard:

https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

Full Daily Brief available for private subscribers.

Research-only. Not betting advice.

---

## 10. Email subject formats

Possible subject lines:

- World Cup Market Intelligence Daily Brief — {{ date }}
- Market Movement Watch — {{ date }}
- Top World Cup Market Movers — {{ date }}
- Probability and Liquidity Watch — {{ date }}
- Daily Event Intelligence Brief — {{ date }}

Avoid subject lines like:

- Best bets today
- Guaranteed edge
- Bet this now
- Lock of the day
- AI predicts winner

---

## 11. Telegram formatting style

Recommended Telegram style:

World Cup Market Intelligence

Team: Example Team A

Move: +4.2pp

Signal: Moderate positive move

Review: High

Catalyst: squad update watch

Dashboard: link

Research-only. Not betting advice.

Keep Telegram alerts short.

Do not overload with tables.

---

## 12. Discord formatting style

Recommended Discord style:

**World Cup Market Intelligence Alert**

**Team:** Example Team A

**Move:** +4.2pp

**Signal:** Moderate positive move

**Review priority:** High

**Catalyst:** Squad update watch

**Dashboard:** link

Research-only. Not betting advice.

Discord can support slightly more detail than Telegram.

---

## 13. Manual review language

Use:

- deserves manual review
- requires context check
- should be watched
- movement detected
- catalyst may be relevant
- signal is informational
- liquidity supports review

Avoid:

- this will happen
- guaranteed
- must bet
- strong buy
- sure thing
- easy money
- lock

---

## 14. Future automation idea

Future script:

- scripts/generate_alerts.py

Possible outputs:

- docs/alerts/latest_telegram.txt
- docs/alerts/latest_discord.md
- docs/alerts/latest_email.md

Inputs:

- top_movers_latest.csv
- signal_summary_latest.csv
- catalyst_matches_latest.csv
- team_intelligence_latest.csv
- dashboard_metadata_latest.json

This can become part of the paid intelligence workflow.

---

## Final note

Alerts are a distribution layer.

The core value remains:

- market movement
- context
- catalyst notes
- team intelligence
- freshness status
- manual review priority

Powered by Mayior Capital.
