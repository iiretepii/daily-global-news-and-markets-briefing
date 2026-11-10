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
