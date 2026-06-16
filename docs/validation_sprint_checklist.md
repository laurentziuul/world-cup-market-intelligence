# 7-Day Validation Sprint Checklist

This checklist defines the first 7-day validation sprint for World Cup Market Intelligence and the broader Mayior Event Intelligence direction.

The goal is to test whether the Daily Brief is useful enough to become a paid research product.

The product remains research-only.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Sprint goal

The goal of this sprint is to answer one simple question:

Would real users want a daily or weekly World Cup market-intelligence brief?

The sprint should test:

- clarity
- usefulness
- delivery preference
- repeated interest
- payment intent
- custom report interest

The goal is learning, not perfection.

---

## Core links to share

Public landing page:

- https://laurentziuul.github.io/world-cup-market-intelligence/

Pro page:

- https://laurentziuul.github.io/world-cup-market-intelligence/pro/

Sample brief:

- https://laurentziuul.github.io/world-cup-market-intelligence/briefs/sample_world_cup_market_brief.md

Latest generated brief:

- https://laurentziuul.github.io/world-cup-market-intelligence/briefs/latest.md

Trends dashboard:

- https://laurentziuul.github.io/world-cup-market-intelligence/trends-dashboard/

GitHub repo:

- https://github.com/laurentziuul/world-cup-market-intelligence

---

## Day 1 — Prepare links and product explanation

Tasks:

- verify all public links work
- open Pro page
- open sample brief
- open latest generated brief
- open trends dashboard
- read outreach messages
- select 10 warm contacts
- prepare aliases for the tracker

Commands:

- python scripts/validate_project.py
- python scripts/generate_daily_brief.py
- python scripts/analyze_outreach_feedback.py

Success criteria:

- all public links work
- sample brief is readable
- latest brief exists
- outreach tracker is ready

---

## Day 2 — Send first 10 warm messages

Tasks:

- send short DM to 10 warm contacts
- use aliases in the tracker
- log every message in outreach_feedback.csv
- do not push private names or personal data
- ask only for feedback, not money

Target people:

- crypto contacts
- prediction-market users
- football fans
- sports-data people
- content creators
- community owners

Success criteria:

- 10 messages sent
- 10 rows logged
- no private data stored

---

## Day 3 — Collect first reactions

Tasks:

- check replies
- log response status
- log useful sections
- log objections
- log preferred delivery
- follow up only where relevant

Questions to ask:

- Is the brief understandable?
- Which section is useful?
- What is missing?
- Would a daily version save time?
- Would Telegram, Discord or email be better?

Success criteria:

- at least 3 replies
- at least 1 useful product insight
- tracker updated

---

## Day 4 — Public post

Tasks:

- publish one public post on X/Twitter or LinkedIn
- optionally share in relevant Telegram or Discord groups if allowed
- include sample brief
- include Pro page
- clearly say research-only
- ask for feedback

Do not claim:

- betting edge
- prediction
- guaranteed signal
- official affiliation
- profit opportunity

Success criteria:

- one public post published
- reactions logged if any
- no overclaiming

---

## Day 5 — Improve the brief based on feedback

Tasks:

- review feedback tracker
- identify common objections
- identify most useful sections
- decide if the brief is too long
- decide if Telegram alert format is needed
- update future product direction if needed

Possible improvements:

- shorter executive summary
- top 3 movers instead of top 5
- clearer team review priority
- stronger freshness explanation
- better catalyst section
- simpler Pro page copy

Success criteria:

- at least one improvement decision
- feedback summary generated

Command:

- python scripts/analyze_outreach_feedback.py

---

## Day 6 — Offer 7-day free manual delivery

Tasks:

- ask interested people if they want the next few daily briefs
- offer manual delivery by Telegram or email
- do not automate payments yet
- log preferred delivery
- log wants-more signal

Message idea:

Would you like me to send you the next few daily briefs manually and get your feedback?

Success criteria:

- at least 1 person accepts repeated delivery
- preferred delivery channel is identified

---

## Day 7 — Ask payment-intent question

Tasks:

- ask positive responders whether they would pay
- test price points gently
- test custom report interest
- log all answers

Payment-intent questions:

- Would you pay 19 EUR/month for this during the World Cup cycle?
- Would you pay 49 EUR/month if it included alerts?
- Would you prefer a one-time tournament report?
- Would your community want a custom report?

Success criteria:

- at least 1 payment-intent answer
- clear next decision

---

## Sprint metrics

Track:

- messages sent
- replies received
- wants-more signals
- payment-intent signals
- custom report leads
- preferred delivery channel
- most useful section
- most common objection

Minimum target:

- 30 outreach messages
- 10 replies
- 3 wants-more signals
- 1 payment-intent signal

Strong result:

- 5 wants-more signals
- 2 payment-intent signals
- 1 custom report lead

---

## Decision after 7 days

### If validation is strong

Build next:

- Telegram alert generator
- short daily summary
- private delivery workflow
- custom report template
- payment page later

### If validation is mixed

Improve:

- sample brief
- Pro page
- outreach message
- target audience
- delivery format

Then run another 7-day sprint.

### If validation is weak

Do not force the product.

Possible pivots:

- crypto event intelligence
- macro event intelligence
- AI narrative intelligence
- tokenized stock event intelligence
- broader prediction-market dashboard

---

## Daily routine during sprint

Daily commands:

- python scripts/generate_daily_brief.py
- python scripts/analyze_outreach_feedback.py
- git status

Daily manual tasks:

- send or follow up
- log responses
- review objections
- update feedback summary

---

## Privacy rule

Because the repo is public, never store:

- real personal names
- phone numbers
- emails
- private Telegram handles
- private Discord IDs
- sensitive personal details

Use aliases:

- crypto_contact_01
- prediction_user_01
- telegram_group_01
- football_creator_01
- discord_owner_01

---

## Final sprint output

At the end of the sprint, the project should have:

- updated outreach_feedback.csv
- updated outreach_feedback_summary.md
- clear decision about next build step
- evidence from real user feedback
- no private data committed

---

## Final note

This sprint is not about selling aggressively.

It is about finding the truth.

The right question is:

Does this save enough time or create enough clarity that someone wants it again tomorrow?

Powered by Mayior Capital.
