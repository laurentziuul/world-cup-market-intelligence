\# Roadmap



World Cup Market Intelligence is an open-source event-intelligence framework.



The first use case is FIFA World Cup 2026, but the long-term goal is to build a reusable system for tracking how markets, narratives and liquidity evolve around scheduled global events.



\## v0.0 — Initial manual pipeline



Status: done



Core capabilities:



\* manual CSV data source;

\* normalized market snapshot;

\* daily Markdown brief generation;

\* basic market/narrative structure;

\* GitHub-ready open-source repository.



Current pipeline:



```text

manual CSV

&#x20;   ↓

snapshot\_latest.csv

&#x20;   ↓

daily Markdown brief

```



\## v0.1 — Public polish



Goal: make the repository easier to understand, inspect and reuse.



Planned additions:



\* project roadmap;

\* sample generated brief;

\* provider architecture documentation;

\* clearer manual CSV workflow;

\* better README structure;

\* public-facing disclaimer and methodology notes.



\## v0.2 — Static dashboard



Goal: generate a simple local dashboard from the latest snapshot.



Planned additions:



\* `scripts/generate\_dashboard.py`;

\* `dashboard/index.html`;

\* market probability table;

\* narrative table;

\* liquidity/volume section;

\* red-team notes;

\* simple visual hierarchy;

\* no server requirement.



Expected pipeline:



```text

snapshot\_latest.csv

&#x20;   ↓

generate\_dashboard.py

&#x20;   ↓

dashboard/index.html

```



\## v0.3 — Historical snapshots



Goal: track probability changes over time.



Planned additions:



\* timestamped snapshot archive;

\* 24h price change calculation;

\* multi-day market movement tracking;

\* basic trend detection;

\* historical brief context.



Expected structure:



```text

data/processed/snapshots/

&#x20;   ├── 2026-06-11.csv

&#x20;   ├── 2026-06-12.csv

&#x20;   └── ...

```



\## v0.4 — Provider abstraction



Goal: separate data providers from the intelligence engine.



Planned additions:



```text

src/wcmi/providers/

&#x20;   ├── base.py

&#x20;   ├── manual\_csv.py

&#x20;   ├── polymarket.py

&#x20;   └── generic\_api.py

```



Provider philosophy:



\* manual CSV provider should always work;

\* API providers should be optional;

\* external data availability should not break the core pipeline;

\* every provider should output the same normalized schema.



\## v0.5 — Multi-event support



Goal: adapt the framework beyond World Cup 2026.



Possible future event types:



\* elections;

\* FOMC meetings;

\* CPI/PPI releases;

\* crypto token unlocks;

\* AI product launches;

\* major court decisions;

\* geopolitical deadlines;

\* sports tournaments.



Expected structure:



```text

examples/

&#x20;   ├── world\_cup\_2026/

&#x20;   ├── fomc/

&#x20;   ├── crypto\_unlocks/

&#x20;   └── elections/

```



\## v1.0 — Reusable event intelligence framework



Goal: turn the project into a general-purpose research tool.



Core principles:



\* provider-agnostic architecture;

\* reproducible snapshots;

\* explainable signal scoring;

\* narrative-vs-price analysis;

\* red-team by default;

\* no black-box trading claims;

\* educational and research-first positioning.



\## Non-goals



This project is not intended to:



\* place trades automatically;

\* provide betting tips;

\* promise profit;

\* bypass geographic restrictions;

\* scrape copyrighted match footage;

\* act as a financial or betting advisory tool.



\## Long-term vision



The long-term vision is to build a lightweight intelligence operating system for global events.



The system should answer:



\* what is the market pricing?

\* what narrative is driving the price?

\* where is liquidity appearing?

\* what catalyst explains the move?

\* what could invalidate the signal?

\* is this structural, tactical, speculative or noise?



