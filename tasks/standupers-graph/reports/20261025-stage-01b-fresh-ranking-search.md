# Stage 1 follow-up — fresh ranking search

Date: 2026-10-25
Status: complete; the user confirmed option A on 2026-10-25

## Surprises

- A much fresher and broader source exists at **standup.pl**: 448 catalogued comedians, current YouTube metrics, daily-updated trend rankings, and an all-time popularity sort.
- Its catalog mixes individual comedians with channels/formats such as Stand-up Polska and Kanał Komediowy, so “first 100” requires explicit entity filtering.
- Standupedia does have fresh Golden Mics results, but those are awards in selected categories—not a replacement top-100 ranking.

## Best candidate: standup.pl

The [comedian catalog](https://standup.pl/komicy) reports **448 comedians**, from major names to open-mic debutants. Its [popularity-sorted view](https://standup.pl/komicy?sort=views) orders them by displayed cumulative YouTube views and has enough entries for a current top 100.

The separate [performer ranking](https://standup.pl/komicy/ranking) says its YouTube data is updated daily and offers 24-hour, 7-day, and 30-day view-growth windows. The [30-day ranking](https://standup.pl/komicy/ranking?period=30d) currently covers more than 400 entries. Ranking and catalog pages expose names, profile links, recording counts, total views, and—on many entries—likes and comment counts.

Public catalog/ranking pages are allowed by `robots.txt`; `/api/` and `/admin/` are disallowed. The terms prohibit disruptive activity and scraping that bypasses API conditions. Acquisition should therefore use small numbers of public HTML pages, without probing disallowed endpoints.

### Important methodological difference

Standupedia’s 2023 score is duration × views for eligible stand-up recordings. Standup.pl’s popularity sort uses displayed cumulative YouTube views, while its trend ranking uses recent view growth. These are not equivalent metrics, and the new source must not be presented as merely a newer run of the old formula.

The catalog also includes groups, channels, formats, and broader comedy-adjacent performers. A freeze needs a documented inclusion rule: preferably one node per individual human comedian, with groups/formats excluded before selecting the first 100.

## Options

### A. Current all-time popularity — recommended

Use `https://standup.pl/komicy?sort=views`, filter to individual comedians, then freeze the first 100 with the retrieval date and source metrics. Optionally retain each performer’s current 30-day trend as metadata.

- **Advantages:** current data, stable enough for a long multi-batch project, broad coverage, closest to the original “first 100 by popularity” intent.
- **Trade-offs:** not Standupedia’s duration-weighted formula; YouTube popularity is still not fan similarity; entity filtering is necessary.

### B. Current 30-day growth

Use `https://standup.pl/komicy/ranking?period=30d`, with the same individual-only filter.

- **Advantages:** emphasizes who is relevant or viral now; explicitly updated daily.
- **Trade-offs:** volatile and favors active/viral output; established but currently quiet comedians can fall far down or disappear between snapshots. This is less suitable as the fixed universe for a graph built over many turns.

### C. Recompute Standupedia’s formula with current YouTube data

Keep the old eligible-recording methodology and refresh it independently.

- **Advantages:** closest methodological continuation of the original request.
- **Trade-offs:** most acquisition and cleaning work; requires reconstructing eligible recordings and exclusions, and still needs a performer universe. Not justified while option A is readily available unless formula continuity matters more than convenience.

## Other fresh sources checked

- [Golden Mics 2025 results](https://standupedia.pl/wyniki-plebiscytu-golden-mics-2025/), published 2026-03-01, include 5,084 audience votes and separate jury awards. Useful as fresh supplementary evidence/context, but category winners cannot define a top 100.
- Ticket/event recommendation pages and editorial “best” lists found in search do not provide a comparable, methodologically clear 100-performer ranking.

## Recommendation

Choose **option A** for the fixed graph universe. Keep the 30-day trend as optional node metadata rather than using it to decide membership. Record the new source and metric prominently, and leave the original 2023 Standupedia list out of the graph unless a later comparison is explicitly wanted.

No ranking has been frozen yet.
