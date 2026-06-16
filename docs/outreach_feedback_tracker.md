# Outreach Feedback Tracker

This document explains how to track product-validation feedback for World Cup Market Intelligence and the broader Mayior Event Intelligence direction.

The goal is to learn whether the Daily Brief is useful enough to become a paid research product.

The product remains research-only.

It is not betting advice.

It is not investment advice.

It is not financial advice.

It is not a prediction engine.

Powered by Mayior Capital.

---

## Tracker file

Feedback tracker:

- data/manual/outreach_feedback.csv

This CSV should be updated manually during outreach.

It is intentionally simple.

No CRM is needed at this stage.

---

## Why this tracker exists

The goal is to avoid vague validation.

Instead of saying:

- people liked it
- people did not respond
- maybe it is useful

We want to track:

- who received the sample
- what type of user they are
- what link was sent
- whether they responded
- which section they found useful
- whether they would want daily updates
- whether they showed payment intent
- what follow-up is needed

---

## CSV columns

### date

Date when the message was sent or updated.

Example:

- 2026-06-16

### contact_or_community

Name of the person, group, community or account.

Examples:

- private Telegram contact
- crypto Telegram group
- football analytics Discord
- newsletter writer
- X account
- LinkedIn contact

### channel

Where the outreach happened.

Examples:

- Telegram
- Discord
- X/Twitter
- LinkedIn
- Email
- WhatsApp
- Reddit
- Manual conversation

### profile_type

Type of person or audience.

Examples:

- prediction-market user
- crypto user
- football fan
- sports-data person
- content creator
- community owner
- researcher
- trader
- newsletter writer
- unknown

### link_sent

Which link was sent.

Examples:

- sample brief
- latest brief
- Pro page
- trends dashboard
- GitHub repo
- public landing page

### response_status

Current response status.

Allowed values:

- pending
- replied
- no reply
- follow-up sent
- interested
- not interested
- wants more
- payment discussion
- custom report lead

### interest_level

Use one of:

- unknown
- no interest
- mild curiosity
- useful but free only
- wants more reports
- payment intent
- custom report lead

### useful_section

Which section they found useful.

Examples:

- top probability movers
- liquidity movers
- volume movers
- catalyst watchlist
- team review priority
- freshness status
- dashboard links
- sample brief
- Pro page
- none
- unknown

### main_feedback

Short summary of what they said.

Examples:

- too long
- useful but needs real data
- wants Telegram alerts
- wants team-specific watchlist
- wants weekly report
- likes catalyst section
- does not understand prediction markets
- wants betting picks only

### payment_intent

Use one of:

- unknown
- no
- maybe
- yes 19 EUR
- yes 49 EUR
- yes custom report
- wants free trial first

### preferred_delivery

Use one of:

- unknown
- Telegram
- Discord
- Email
- Substack
- dashboard only
- PDF
- Markdown
- WhatsApp

### follow_up_action

What to do next.

Examples:

- follow up in 2 days
- send next brief
- ask payment question
- ask preferred delivery
- offer 7-day trial
- ask for custom report needs
- no follow-up

### notes

Any extra useful context.

---

## How to update the CSV

Open:

- data/manual/outreach_feedback.csv

Add one row per person or community.

Example row:

- 2026-06-16
- private Telegram contact
- Telegram
- crypto user
- sample brief
- replied
- wants more reports
- catalyst watchlist
- likes catalyst section, wants shorter summary
- maybe
- Telegram
- send next brief
- asked for daily version

---

## Minimum validation target

For the first validation sprint, aim for:

- 30 to 50 outreach messages
- at least 10 replies
- at least 3 people asking for the next brief
- at least 1 person showing payment intent
- at least 1 community or creator interested in custom report format

---

## Strong positive signal

Strong positive signals:

- asks for the next report
- asks to join a Telegram list
- asks for alerts
- asks for custom watchlist
- asks for a team-specific version
- asks how often it updates
- asks how much it costs
- says it saves research time
- wants to share it with a community

---

## Weak signal

Weak signals:

- says it is interesting but does not ask for more
- only likes the dashboard visually
- does not understand what to do with it
- asks only for betting picks
- ignores research-only positioning
- wants it free only
- no response after follow-up

---

## How to interpret results

### If people want daily updates

Build:

- simple daily delivery workflow
- Telegram alert output
- daily brief archive
- email/Telegram list

### If people want shorter content

Build:

- one-page short brief
- Telegram summary
- top 3 movers only

### If people want deeper research

Build:

- weekly report
- custom team watchlists
- group-stage report
- custom community pack

### If people only want betting picks

Do not pivot into betting advice.

Either educate them on research-only positioning or ignore that segment.

### If nobody understands the product

Simplify:

- headline
- Pro page
- sample brief
- daily summary
- target user

---

## Manual workflow

Daily validation workflow:

1. Generate latest brief.
2. Share sample or latest brief.
3. Ask for feedback.
4. Log every response in CSV.
5. Send follow-up if relevant.
6. Review tracker after 7 days.
7. Decide whether to build alerts, email delivery or custom reports.

Useful commands:

- python scripts/generate_daily_brief.py
- git status

---

## 7-day review

After 7 days, review:

- total messages sent
- total replies
- number of people asking for more
- payment intent count
- custom report leads
- most useful section
- most common objection
- preferred delivery channel

Decision options:

- continue daily brief
- simplify product
- build Telegram alerts
- create custom report offer
- pivot to another vertical
- pause monetization

---

## Final note

The tracker is not bureaucracy.

It is the difference between guessing and learning.

The goal is to turn feedback into product direction.

Powered by Mayior Capital.

