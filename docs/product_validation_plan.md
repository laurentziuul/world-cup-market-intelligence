# Product Validation Plan

This document defines the product-validation plan for World Cup Market Intelligence and the broader Mayior Event Intelligence direction.

The goal is to validate whether the Daily Brief and event-intelligence workflow are useful enough to become a paid research product.

The product remains research-only.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Current product

Current product:

- World Cup Market Intelligence Daily Brief

Current strategic umbrella:

- Mayior Event Intelligence

Current public assets:

- public landing page
- stable dashboard
- Polymarket dashboard
- trends dashboard
- sample public brief
- latest generated brief
- Pro landing page
- alert format documentation
- GitHub repository

---

## Product hypothesis

The core hypothesis is:

People who follow prediction markets, event markets, crypto narratives or sports-related market movement may pay for a structured daily intelligence brief if it saves time and highlights important changes.

The product does not need to predict winners.

It needs to help users understand:

- what changed
- where probability moved
- where liquidity moved
- where volume moved
- which catalysts may matter
- which teams require manual review
- whether the data is fresh, stale or missing

---

## What we are validating

We are validating demand for:

- daily brief format
- market movement summaries
- catalyst watchlists
- team review priority
- freshness-aware interpretation
- Telegram or Discord alert delivery
- weekly or daily research reports
- custom reports for communities or creators

We are not validating:

- betting tips
- guaranteed signals
- prediction claims
- trading advice
- automated betting systems

---

## Target users

Potential target users:

- prediction-market users
- crypto users
- sports-data enthusiasts
- event-driven traders
- market researchers
- newsletter writers
- content creators
- Telegram community owners
- Discord community owners
- people who monitor Polymarket-style markets
- people who want structured event intelligence

---

## Target communities

Possible places to validate:

- Polymarket communities
- prediction-market Twitter/X
- crypto Twitter/X
- sports analytics communities
- football data communities
- private Telegram groups
- private Discord servers
- Substack writers
- crypto newsletter operators
- small research communities
- event-driven trading communities

---

## Validation offer

The first offer should be simple:

World Cup Market Intelligence Daily Brief

A daily research note that summarizes:

- top probability movers
- top liquidity movers
- top volume movers
- teams requiring manual review
- catalyst watchlist
- data freshness status
- dashboard links

Positioning:

- saves research time
- highlights what changed
- helps prioritize manual review
- research-only
- not betting advice

---

## Free sample

Use this as the lead magnet:

- https://laurentziuul.github.io/world-cup-market-intelligence/briefs/sample_world_cup_market_brief.md

Use this as the current generated example:

- https://laurentziuul.github.io/world-cup-market-intelligence/briefs/latest.md

Use this as the product page:

- https://laurentziuul.github.io/world-cup-market-intelligence/pro/

Use this as the main dashboard:

- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

---

## Feedback questions

Ask targeted users:

1. Is this brief easy to understand?
2. Which section is most useful?
3. Which section is useless?
4. Would this save you time if it was updated daily?
5. Would you prefer Telegram, Discord, email or web dashboard?
6. Would you pay 19-49 EUR/month during the World Cup cycle?
7. Would you pay for a weekly report instead of a daily report?
8. What data is missing?
9. What would make this worth paying for?
10. What would make you ignore it completely?

---

## Strong positive signals

Positive validation signals:

- people ask for the next report
- people ask to be added to a Telegram or email list
- people share the sample brief
- people ask for custom watchlists
- people ask for specific teams
- people say it saves time
- people would pay 19-49 EUR/month
- community owners ask for a custom report
- content creators ask to use the data in posts or videos

---

## Weak signals

Weak signals:

- people say it is interesting but do not ask for more
- people like the dashboard but ignore the brief
- people only want free content
- people focus on predictions or betting tips
- people do not understand the value
- people say it is too complex
- people do not know what to do with the information

---

## First 7-day validation sprint

### Day 1 — Prepare public links

Check that the following links work:

- public landing page
- Pro page
- sample brief
- latest brief
- trends dashboard
- GitHub repo

### Day 2 — Create short outreach message

Create a short message that explains:

- what the product is
- who it is for
- why it might be useful
- that it is research-only
- request for feedback

### Day 3 — Send to 10 warm contacts

Send the sample to:

- people who follow crypto
- people who follow prediction markets
- people who like football
- people who run communities
- people who understand market dashboards

Goal:

- collect honest feedback, not sell aggressively

### Day 4 — Post publicly

Post on:

- X/Twitter
- LinkedIn
- relevant Telegram/Discord communities if allowed

Goal:

- see whether anyone clicks, comments or asks questions

### Day 5 — Improve brief format

Based on feedback, improve:

- brief structure
- section order
- language clarity
- alert format
- Pro page copy

### Day 6 — Offer early access manually

Offer:

- 7-day free trial
- daily brief by Telegram or email
- no payment automation yet

Goal:

- see if people want repeated delivery

### Day 7 — Ask for payment intent

Ask directly:

- Would you pay 19 EUR/month?
- Would you pay 49 EUR/month?
- Would you prefer a one-time report?
- Would your community pay for a custom pack?

---

## Pricing validation

Initial price points to test:

- 0 EUR sample
- 19 EUR/month starter
- 49 EUR/month pro
- 99 EUR/month analyst
- 300-1500 EUR custom report

Do not build payment automation until there is clear interest.

Manual validation is enough.

---

## Possible paid packages

### Starter

Price:

- 19 EUR/month

Includes:

- daily brief
- top movers
- catalyst watchlist
- freshness status

### Pro

Price:

- 49 EUR/month

Includes:

- daily brief
- alerts
- team review priority
- weekly summary
- dashboard links

### Analyst

Price:

- 99 EUR/month

Includes:

- daily brief
- alerts
- CSV exports
- custom watchlist
- deeper weekly report

### Custom report

Price:

- 300-1500 EUR/report

Includes:

- custom market intelligence pack
- group-stage analysis
- team momentum report
- liquidity and narrative report
- community-ready summary

---

## Manual workflow

The manual workflow is:

1. Generate updated data.
2. Generate dashboard metadata.
3. Generate trends dashboard.
4. Generate daily brief.
5. Review the brief manually.
6. Send it to test users.
7. Collect feedback.
8. Improve format.
9. Repeat.

Recommended commands:

- python scripts/generate_dashboard_metadata.py
- python scripts/generate_trends_dashboard.py
- python scripts/generate_daily_brief.py

---

## Success criteria

v1.4 validation is successful if:

- at least 10 people review the sample
- at least 3 people ask for the next brief
- at least 1 person says they would pay
- at least 1 community owner or creator shows interest
- the product format becomes clearer after feedback

Strong success:

- 5 or more people join a private channel
- 2 or more people offer to pay
- 1 custom report lead appears

---

## Failure criteria

The product may need repositioning if:

- nobody understands the brief
- nobody wants repeated updates
- users only want betting picks
- users do not value research-only interpretation
- users find the dashboard more useful than the brief
- users say the topic is too narrow

If this happens, reuse the engine for another vertical.

Possible pivots:

- crypto event intelligence
- macro event intelligence
- AI narrative intelligence
- tokenized stocks event intelligence
- sports tournament intelligence

---

## Next build items after validation

Only build these if validation is positive:

- scripts/generate_alerts.py
- docs/alerts/latest_telegram.txt
- docs/alerts/latest_discord.md
- private Telegram channel
- email template
- payment page
- custom report template
- subscriber delivery workflow

---

## Final note

The goal is not to overbuild.

The goal is to learn whether the product is useful.

The fastest path is:

- sample brief
- direct outreach
- feedback
- manual delivery
- willingness-to-pay test

Powered by Mayior Capital.
