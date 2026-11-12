# Daily Global News & Markets Briefing

Two scheduled Claude briefings, written unattended every day, saved to Google Drive, and turned into two-host audio episodes by Gemini Notebook (formerly NotebookLM). Each briefing is the only source document for its episode, so it is written as an audio-first script: the document order is the run-of-show, with a short steering header at the top.

The briefings are written for a banking-fluent senior executive at a large bank who wants a firm-wide view of the outside world: what happened, what moved markets, what is priced in, what it means for the firm, and what to watch. They use public reporting only.

| Briefing | Schedule (ET) | Model | Length |
|---|---|---|---|
| Morning Global News/Markets Briefing | Daily, 4:29am | Claude Opus 5.5 | ~3,500–4,600 words |
| Afternoon Global News/Markets Briefing | Weekdays, 2:50pm | Claude Sonnet 5.5 | ~1,800–2,500 words, only what changed since the morning |

Prompts:

- [`prompts/morning-global-news-markets-briefing.md`](prompts/morning-global-news-markets-briefing.md)
- [`prompts/afternoon-global-news-markets-briefing.md`](prompts/afternoon-global-news-markets-briefing.md)

## What each episode covers

The morning briefing opens with The Good News, then The Morning in Sixty Seconds, the Top Five stories, What Moved Markets, equities, rates and the Fed, global markets and commodities, credit and banking, a `{{FIRM}} Watch` section with a read-through by line of business, the US, a region-by-region world pass, Beyond the Headlines, and the day's calendar. On Saturday the markets sections become a Week in Review, and on Sunday a Week Ahead.

The afternoon briefing is a delta update: the stories that moved since the morning, markets into the close, credit, banking and the firm, Washington and the world, and what to watch tonight and tomorrow.

On Caveman Thursdays the hosts deliver the whole episode in caveman speak. The briefing text itself stays normal. Delete section 6B if that isn't for you.

## Placeholders

The prompts are templates. Fill these in before scheduling, either by hand or with the script below.

| Placeholder | What goes there |
|---|---|
| `{{FIRM}}` | The firm the listener works for (or follows) |
| `{{FIRM_TICKER}}`, `{{FIRM_TICKER_LOWER}}` | Its stock ticker, upper and lower case |
| `{{FIRM_SEARCH_NAMES}}` | Every name the firm goes by, plus the CEO's name, for news searches |
| `{{FIRM_BUSINESSES}}` | Its major lines of business, as a sentence |
| `{{FIRM_NEWSROOM_URL}}` | A readable, dated newsroom page, if it has one |
| `{{FIRM_SEC_CIK}}` | Its SEC CIK number, for 8-K exhibits |
| `{{PEER_BANKS}}`, `{{PEER_TICKERS}}` | US peer banks to compare against, by name and ticker |
| `{{GLOBAL_PEER_BANKS}}` | Global peers worth mentioning where relevant |
| `{{BRIEFINGS_FOLDER_ID}}` | Google Drive folder that holds the briefings |
| `{{TRACKER_FOLDER_ID}}` | Its "Story Tracker" subfolder |
| `{{WORLDNEWS_ACCOUNT}}` | Name of your World News API account in Composio |

```
cp config.example.json config.json   # edit the values
python3 scripts/fill_placeholders.py config.json filled/
```

The script reports any placeholder left unfilled and warns if a filled prompt goes over the 64 KB limit on scheduled-task prompts. Both prompts sit close to that limit, so long values (especially `{{FIRM_BUSINESSES}}`) can push them over; new rules have to replace old text rather than add to it. Keep `config.json` and `filled/` out of version control.

## How a run works

1. **Load memory.** The run reads the latest story tracker and the two most recent briefings from Drive. Continuing stories are told as updates: lead with what's new, recap in a sentence or two at most, and say how the story moved.
2. **Research in parallel.** The lead agent launches subagents in one message (ten in the morning, five in the afternoon), one per coverage area, and runs a front-page sweep itself. Each subagent gets a self-contained brief with its sources, caps and tracked storylines, and returns ranked, dated, sourced findings ending with a `SELF-COUNT` line.
3. **Consolidate and verify.** The lead deduplicates findings and checks each against the Aired Items Log so nothing repeats without a real new development. Every headline fact and number is confirmed against a primary source or two independent outlets.
4. **Quality gate.** Word count, attribution, nonpartisanship, no buy or sell recommendations, and the audio checks (below). The lead revises until the draft passes.
5. **Save.** The briefing goes to Drive as a Google Doc titled `YYYY-MM-DD - <Briefing name>`, plus a fresh tracker (`YYYY-MM-DD - Story Tracker`, with `PM` for the afternoon run). Earlier trackers are never edited.
6. **Report.** The run ends with a Run Report: time and quota per agent, coverage, connector status, breakage and repeats caught. If a connector breaks, the run sends a push notification.

### Story tracker

The tracker is a plain-text Google Doc holding active and dormant storylines, reference figures (index levels, yields, spreads, FX, commodities, the firm's stock and the bank index), a Good News Log, an Aired Items Log covering everything aired in the last 14 days, and a Metaphor Log. It is capped at about 4,000 words.

## The agents

Each run has one lead agent and a set of research subagents launched together in Step A. The lead owns everything that needs the whole picture: memory, the front-page sweep, consolidation, verification, drafting, the quality gate, saving and the Run Report. Subagents own one coverage area each and return findings, never prose for the briefing. Search and Alpha Vantage caps below are hard per-agent limits; FMP and built-in WebFetch are uncapped.

### Morning (ten subagents)

| Agent | Coverage | What it does | WebSearch cap | Alpha Vantage cap |
|---|---|---|---|---|
| Lead | Area 10, plus orchestration | Loads the tracker and the last two briefings, briefs and launches the subagents, runs the front-page sweep of readable outlets and checks what blocked outlets are leading with, holds both World News API calls, consolidates and verifies, refreshes overnight levels just before writing, drafts, runs the quality gate, saves to Drive, writes the new tracker and the Run Report | 8 sweep + 20 reserve | 3 |
| Geopolitics, Conflict & Security | Area 1 | Wars and ceasefires, diplomacy, sanctions, foreign elections, terrorism and security incidents | 20 | 0 |
| US Politics & Policy | Area 2 | White House, Congress, courts, agencies, executive actions, state-level moves, fiscal and trade policy | 18 | 0 |
| Regional Roundup | Area 3 | Europe, Asia-Pacific, the Middle East and Africa, and Latin America, for stories not covered elsewhere | 20 | 0 |
| Science, Tech, Health, Climate & Society | Area 4 | Science and public health, disasters and weather, energy transition, non-AI tech, social and cultural stories | 15 | 0 |
| US Equities | Area 5 | Index closes, sectors, breadth, single-stock movers, the VIX and futures; starts with FMP index quotes, ESUSD, the sector snapshot and the earnings calendar | 8 | 3 |
| Rates, the Fed & the Economy | Area 6 | The Treasury curve and two-to-ten spread, fed funds pricing, Fed speakers, SOFR, mortgage rates, data against consensus, today's calendar and auctions | 8 | 2 |
| Global Markets, FX, Commodities & Crypto | Area 7 | Asian closes, the European session, foreign bond yields, the dollar and EM currencies, oil, gas, metals, bitcoin and ether | 8 | 3 |
| Credit, Capital Markets & Banking | Area 8 | Spreads and issuance, leveraged loans and private credit, M&A and ECM, bank news and stocks against the KBW index, consumer and commercial credit, payments, regulation | 20 | 2 |
| `{{FIRM}}` | Area 9 | Firm news across every line of business, the stock against the bank index and peers, executive commentary, legal and regulatory matters, competitor moves; says plainly when the window was quiet | 22 | 2 |
| Good News | Area 11 | Two to four verified, substantive positive developments over 72 hours, checked against the Good News Log and the tracker's unused candidates | 20 | 0 |

### Afternoon (five subagents)

The afternoon run is a delta update, so the eleven coverage areas collapse into five broader passes, each told what the morning already aired and asked only for what changed since then.

| Agent | Coverage | What it does | WebSearch cap | Alpha Vantage cap |
|---|---|---|---|---|
| Lead | Area 10, plus orchestration | Same role as the morning lead; sets the window from the morning briefing's Drive timestamp and checks whether each event the morning flagged for today has happened | 6 sweep + 12 reserve | 2 |
| World & US News | Areas 1–4 | One lighter pass over geopolitics, US politics, the regions, and science and society since the morning | 20 | 0 |
| US Markets, Rates & the Economy | Areas 5–6 | Intraday index levels against the previous close and the morning's futures, sectors, intraday yields, Fed pricing, data and Fed speakers since the morning, after-the-close earnings | 10 | 3 |
| Global Markets, Credit & Banking | Areas 7–8 | European closes, the dollar, oil, gold and crypto, plus credit, deal and bank news since the morning, including bank earnings released today | 14 | 3 |
| `{{FIRM}}` | Area 9 | The firm's intraday move against the bank index and peers, and anything reported about the firm since the morning across its businesses | 14 | 2 |
| Good News | Area 11 | One or two new verified positive stories, skipping anything already aired | 10 | 0 |

In both runs the lead can also launch a single web-fetch subagent when it needs more than about six pages read during verification, because the lead has no built-in WebFetch in scheduled runs.

### Why fan out to subagents

The short answer is that one agent cannot read enough, fast enough, without drowning in what it read. A morning run reads well over a hundred pages across eleven coverage areas. If the lead did that itself, every article, data page and failed fetch would sit in its context, and by the time it reached drafting the material it needs to weigh would be competing with thousands of lines of raw page text. Each subagent instead absorbs its own pages and hands back eight to twelve ranked, dated, sourced findings. The lead starts consolidation with a clean, comparable set of inputs rather than a transcript of the research.

Parallelism matters because the run is unattended and on a clock. Ten areas researched one after another would push the 4:29am run well past the point where the episode is useful before the workday; launched in a single message, they run concurrently and the wall-clock time is set by the slowest area, not the sum of all of them.

The split also makes the rules enforceable. Each subagent gets a self-contained brief with its own scope, source list, tracked storylines and hard caps on WebSearch, Perplexity, Parallel fetch and Alpha Vantage. The free Alpha Vantage tier allows about 25 calls a day across both runs, and the built-in WebSearch limit is shared by every agent in the run, so a single agent with one big budget would tend to spend it on whatever it found first. Per-agent caps keep coverage balanced, and the `SELF-COUNT` line each subagent ends with lets the lead audit usage against the caps and report any overrun by name.

It separates gathering from checking. The lead did not collect the findings it verifies, so Step B works as a genuine second look: every headline fact and number is confirmed against a primary source or two independent outlets before it can air, and the lead cross-checks the subagents against its own front-page sweep to catch anything the specialists missed or over-weighted.

It degrades gracefully. A connector failure or a dead source costs one coverage area, which the lead can fill from its reserve, rather than stalling the whole run.

Finally, the shape of the fan-out follows the job. The morning briefing is a full survey of the last 24 hours, so it gets ten narrow specialists. The afternoon is a delta over a few hours of news, so five broader agents cover it at lower cost without losing the separation between news, markets, banking, the firm and good news.

## Setup

### Scheduled tasks

Create two scheduled tasks in Claude and paste one filled prompt into each.

| Task | Cron | Model | Notifications |
|---|---|---|---|
| Morning Global News/Markets Briefing | `CRON_TZ=America/New_York 29 4 * * *` | Opus | Push on |
| Afternoon Global News/Markets Briefing | `CRON_TZ=America/New_York 50 14 * * 1-5` | Sonnet | Push on |

Both run unattended, so give them automatic approval if your organization allows it.

### Connectors

| Purpose | Connector | Notes |
|---|---|---|
| Memory and output | Google Drive | Create a briefings folder with a "Story Tracker" subfolder |
| Market data | FMP (Financial Modeling Prep) | Primary. The prompt lists which endpoints and symbols worked on a lower-tier plan; adjust for yours |
| Market data backup | Alpha Vantage | Free tier, about 25 calls a day, split 15 morning and 10 afternoon |
| Web search | Built-in WebSearch, then anonymous Parallel Search, then Perplexity | Perplexity is billed and used only as a last resort |
| Page fetch | Built-in WebFetch, then anonymous Parallel Search, then Parallel Search (Auth) | The Auth connector's search is never used |
| News discovery | World News API via Composio | Optional; two searches per run. The briefing never depends on it |

Every search must name the date, every capped tool keeps a running tally, and paywalled or blocked outlets are reached only through syndicated wire copy or cited search excerpts, never by working around the block.

### Audio

Upload each day's Google Doc to Gemini Notebook as the episode's only source. The `EPISODE_OVERVIEW` line at the top is under 500 characters, so it can also be pasted into the customize box as-is. The five `DIRECTOR_NOTES` lines below it steer tone, continuity, priorities, segment coverage and framing.

## Audio-first rules

- **Document order is run-of-show.** The hosts work top to bottom.
- **Audio Rule of Two.** At most two contrast numbers per story or instrument, rounded. The rest is described by direction; full figures go to the tracker.
- **Say each thing once.** Overviews name stories without retelling them; drivers are explained once.
- **No pipeline talk.** Connector failures and agent chatter stay in the Run Report, never in the briefing.
- **Anthropic disclosure once**, at the first Anthropic story.
- **A plain thematic thread, not a running metaphor.** An optional image may appear only in the opening two sentences of the overview and the final sentence.

## Notes

- The source lists (which sites are readable, which serve stale pages, which FMP endpoints work) reflect testing in October and November 2026. Sites change; expect to adjust them.
- Nothing here is investment advice. The prompts forbid buy, sell or hold recommendations and require market views to be framed as what is priced in.
