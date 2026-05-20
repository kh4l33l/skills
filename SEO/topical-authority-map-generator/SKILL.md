---
name: topical-authority-map-generator
description: >
  Build a Topical Authority Map for a website — a hierarchical strategy of pillar pages,
  content clusters, and supporting pages designed to win topical authority in Google and
  earn citations in AI answers (LLM/GEO/AEO). Trigger this skill whenever the user says
  things like "build a topical authority map", "topical map for [topic/site]", "content
  cluster strategy", "pillar and cluster plan", "what topics should I own", "build authority
  around [topic]", "what content should I write to rank for [topic]", or pastes a URL and
  asks how to expand coverage around it. Also trigger when the user asks to audit or
  restructure an existing content cluster, or wants a roadmap for becoming the go-to source
  on a topic. The skill produces a styled HTML report AND a machine-readable JSON map so
  the output can feed other SEO skills. Pulls live data from GSC, GA4, and DataForSEO when
  those tools are connected, and falls back to asking the user for data when they're not.
---

# Topical Authority Map Generator

Build a hierarchical topical authority map — a pillar page, content clusters, and supporting pages — for a target site and topic. Output a polished HTML report alongside a structured JSON file that other skills can consume.

This is a strategy skill, not a writing skill. Don't write the articles — recommend what to write, in what order, with what intent, and how to link them.

## Defaults

- **HTML report output**: `/mnt/user-data/outputs/topical-authority-map-[topic-slug]-[YYYY-MM-DD].html`
- **JSON map output**: `/mnt/user-data/outputs/topical-authority-map-[topic-slug]-[YYYY-MM-DD].json`
- **Working files**: `/home/claude/` (scratch only, not presented)

## Reference examples

The `examples/` folder contains 3 reference JSON maps, 1 rendered HTML report, and 1 history file. Consult them only when uncertain — e.g., handling a competitor map, deciding what goes in `goal_tilt`, or checking the HTML structure. Do not consult them on every run. See `examples/README.md` for which file covers which case.

## Workflow

### Step 1: Initial recon, then a targeted clarifier

Before asking anything, do a fast recon pass. The goal is to make any clarifying question specific and informed ("is this the right scope?") rather than generic ("what's your topic?").

**Recon pass** (skip whichever doesn't apply):

1. If the user named a site but no specific topic, hit GSC for the top 20 pages and top 20 queries over the last 90 days — this tells you what the site is actually known for.
2. If the user named a topic but no site, you don't have enough to recon — go straight to asking for the site.
3. If both site and topic are given, fetch the homepage and 1–2 obvious topic-relevant pages to confirm the topic is real on this site, and run a quick DataForSEO `keyword_ideas` call on the topic to gauge search landscape.
4. Check `/home/claude/topical-authority-maps-history.json` for any prior maps on this site+topic.

Keep recon to ~5 tool calls. The point is signal for the clarifier, not the full data pull (that's Step 2).

**Then the clarifier** — only ask what isn't already clear. Phrase it specifically using what recon surfaced:

> "Quick check before I dig in:
>
> 1. **Topic scope** — based on the site, I'm planning to map `[X]`. The closest existing coverage I can see is `[page A]` and `[page B]`. Is `[X]` the right scope, or should I go broader (e.g., `[broader option]`) or narrower (e.g., `[narrower option]`)?
>
> 2. **Goal** — what are you trying to accomplish with this topic? Drive more product signups/trials, become the definitive informational source on it (great for SEO + AI citations), or a mix of both?
>
> 3. *(if history showed a prior map)* I generated a map for this site+topic on `[date]`. Want to regenerate from scratch, or build on top of the prior version?"

Drop any sub-question that's already answered. If the user's original prompt nailed scope and goal both, skip the clarifier entirely and go straight to Step 2.

**Classifying the goal answer.** The user will answer in plain English. Classify into:
- **commercial** — "drive trials/signups/sales", "convert", "more downloads", anything bottom-of-funnel
- **informational** — "own the topic", "rank for everything", "AI citations", "authority", anything top-of-funnel
- **mixed** — both, or anything ambiguous. If they say something like "mostly trials but some informational content too," set goal=`mixed` and `goal_tilt`=`commercial`.

The goal shapes the map heavily:
- **commercial** maps lean toward bottom-of-funnel: comparison pages, alternatives-to-X, use-case landing pages, pricing/feature breakdowns. Fewer pages overall, higher commercial intent per page.
- **informational** maps lean toward top-of-funnel: definitive guides, how-tos, listicles, definitions, FAQs. More pages, broader keyword coverage, stronger LLM citation potential.
- **mixed** maps blend both — usually a commercial pillar with informational clusters feeding into it.

Individual pillars can have their own goal that differs from the map-wide goal (e.g., a mostly-informational map with one commercial pillar for the product). Set this per pillar in the JSON when it varies.

Do NOT ask about GSC/GA4/DataForSEO access. You already tried them in recon — if they failed there, mention it in the clarifier ("GSC isn't returning data for this site — do you have a CSV export or summary you can share?") and let the user respond in the same turn.

### Step 2: Pull data from available tools

Try each in order. Note which succeeded and which didn't — the report will declare its data sources. Reuse what was already fetched in Step 1's recon rather than re-querying.

**GSC (via `foo-analytics` or equivalent):**
- Top 100 pages for the site over the last 90 days (clicks, impressions, position)
- Top 200 queries for the site over the last 90 days
- If the topic is narrow, filter queries to those containing topic-relevant terms

**GA4 (via `foo-analytics` or equivalent):**
- Top 50 landing pages by sessions over the last 90 days
- Engagement rate per page (helps distinguish "high traffic" from "high quality traffic")
- **Property ID handling**: GA4 calls require a property ID. Check (in this order): user-provided context in the current conversation → memory of prior conversations → ask the user once. Do not assume an ID. If the user can't or won't provide one, proceed without GA4 — this is the most common reason data_confidence drops from high to medium, so flag it explicitly.

**DataForSEO** — call endpoints in this order of preference. The first two are far more useful than `keyword_ideas` for topic-specific work:

1. **`dataforseo_labs_google_related_keywords`** — the best tool for niche topic exploration. Pass a single anchor keyword (the topic head term), set `depth: 2`, filter `keyword_data.keyword_info.search_volume >= 50`, order by volume descending. Returns the actual related queries searchers use, with volume, difficulty, intent, and SERP feature data (look at `serp_info.serp_item_types` to see if AI Overview is present — that's a strong LLM citation signal). Limit 30–40 results.

2. **`dataforseo_labs_google_historical_keyword_data`** — when you have a hand-picked list of candidate target queries (from related_keywords or GSC) and want to confirm volume + trend on each. Send up to 20 keywords in one call. The response includes `monthly_searches` so you can see if a term is trending up or down. This is what you use to make priority calls — high volume + upward trend = P1.

3. **`dataforseo_labs_google_keyword_ideas`** — only useful for broad seed-keyword exploration ("what other topic clusters might exist near this one?"). Returns category-grouped suggestions that are often only loosely related. Don't rely on this for the core map; use it sparingly to spot adjacent topic territories.

4. **`dataforseo_labs_google_search_intent`** — pull intent classification (informational / commercial / transactional / navigational) for the top 30 keywords by volume. This drives the `intent` field on each page in the JSON.

5. **For competitor maps**, add `dataforseo_labs_google_competitors_domain` and `dataforseo_labs_google_ranked_keywords` to pull what the competitor ranks for.

Limit total DataForSEO calls to ~5–6 for a typical map. Each call costs real money and the returns diminish quickly past the first few.

**Live page scraping (`web_fetch`):**
- Fetch the site's relevant existing pages on the topic (homepage section, hub pages, top blog posts). Don't fetch everything — fetch what the GSC top-pages list surfaced as topic-relevant. Aim for 5–10 pages.
- For each, extract H1, H2/H3 structure, and any internal links between them. This is your existing topical graph.
- **Permission model:** `web_fetch` only works on URLs the user explicitly provided in the conversation, URLs returned from `web_search`, or URLs the user has granted standing permission for (e.g., "you can fetch any page on my site"). If a fetch fails with a permissions error, do not retry the same URL — instead, either (a) try one obvious URL the user has clearly authorized (their own domain when the topic is about their own site), or (b) skip page scraping entirely and flag it in the data sources section. Don't burn calls hammering a wall.
- **Fallback when scraping is unavailable:** infer existing page structure from URL paths in GSC top-pages data plus the page titles surfaced in the GSC query data. This is partial — flag the report accordingly.

**If a tool isn't available**, don't fail silently. Tell the user what's missing and ask if they can paste in the data (GSC top queries CSV, sitemap URL, etc.) or proceed with reduced confidence. The report should clearly label which sections are evidence-based vs. inference-based.

### Step 2.5: Confidence gate

Before building the map, assess `data_confidence` based on what Step 2 actually returned. Use these rules:

- **high** — GSC ✓, GA4 ✓, DataForSEO ✓, page-scrape ✓. All four sources returned usable data.
- **medium** — three of four returned usable data. Most commonly: GSC + DataForSEO + page-scrape but no GA4 (no property ID), or all the analytics but no page scrape.
- **low** — two or fewer returned usable data. Common case: a competitor map where you don't own GSC/GA4 for that domain.

**If `data_confidence` is anything other than `high`, STOP. Do not proceed to Step 3.** Surface to the user:

1. Which sources returned data and which didn't (one line each)
2. The specific gap and what it means for the map ("without GA4 I can't tell which traffic actually engages — priority calls will be based on GSC clicks alone, which is a partial substitute")
3. What would close the gap ("share your GA4 property ID and I'll re-pull" / "paste the GSC export" / "give me permission to fetch pages on your domain")
4. A clear question: "do you want to (a) provide the missing data, (b) proceed at this confidence level anyway, or (c) cancel?"

Wait for an explicit answer before continuing. If they say proceed, note their acceptance in the report's data sources section ("user confirmed proceeding at medium confidence").

This gate exists because a map built on shaky data leads to confidently-wrong recommendations — better to pause for 30 seconds and confirm than to ship a 25-page plan with bad priority calls.

### Step 3: Build the map

This is the analytical step. Synthesize the inputs into a hierarchy:

**Core Topic** — one sentence defining the semantic scope of the map. What does the site want to be known for?

**Pillar Page(s)** — 1 or 2 comprehensive hub pages. Each pillar:
- Has a clear target keyword theme (usually short-head, high-volume, mid-intent)
- Either maps to an existing strong page (prefer expanding) or is a recommended new page
- Includes a one-line rationale tying it to the data (GSC impressions, search volume, current position)

**Content Clusters** — 5–10 sub-topic groups under the pillar(s). Each cluster:
- Has a cluster theme and 3–8 recommended supporting pages
- For each supporting page: working title, target query/intent, content type (guide, tutorial, listicle, comparison, FAQ, definition), and status (exists / expand / new)
- Listicles and comparison pages get explicit callouts — these are the highest-leverage formats for LLM citations
- Tag each page with a priority: P1 (quick win, data-backed), P2 (medium effort, clear opportunity), P3 (strategic, longer-term)

**Internal Linking Strategy** — concrete recommendations: which pages link to the pillar, which clusters cross-link, anchor text guidance. Reference the existing internal link graph from Step 2.

**LLM Citation Notes** — for each cluster, briefly note what makes it citable by AI answer engines: definitive lists, comparison tables, clear definitions, structured data opportunities, source-quality signals (E-E-A-T, dates, author).

Prioritization rule of thumb: business impact × search opportunity × feasibility ÷ effort. Pages that already exist and are close to ranking are almost always your P1s.

### Step 4: Write the JSON map

Save to the JSON output path. Schema:

```json
{
  "schema_version": "1.0",
  "meta": {
    "site": "https://example.com/",
    "topic": "WordPress image galleries",
    "generated_at": "2026-05-20",
    "goal": "commercial | informational | mixed",
    "goal_tilt": "commercial | informational | null",
    "data_sources": ["gsc", "ga4", "dataforseo", "page_scrape"],
    "data_confidence": "high | medium | low"
  },
  "core_topic": {
    "definition": "...",
    "audience": "..."
  },
  "pillars": [
    {
      "id": "pillar-1",
      "title": "...",
      "url": "https://example.com/...",
      "status": "exists | expand | new",
      "goal": "commercial | informational | mixed",
      "target_keywords": ["..."],
      "rationale": "GSC: 12,400 impressions/90d at avg pos 8.2",
      "clusters": ["cluster-1", "cluster-2"]
    }
  ],
  "clusters": [
    {
      "id": "cluster-1",
      "theme": "...",
      "pillar_id": "pillar-1",
      "pages": [
        {
          "id": "page-1",
          "title": "...",
          "url": "https://example.com/... | null",
          "status": "exists | expand | new",
          "intent": "informational | commercial | transactional | navigational",
          "type": "guide | tutorial | listicle | comparison | faq | definition",
          "target_query": "...",
          "priority": "P1 | P2 | P3",
          "llm_citation_potential": "high | medium | low",
          "notes": "..."
        }
      ]
    }
  ],
  "internal_linking": {
    "rules": ["..."],
    "specific_recommendations": [
      {"from": "url-or-id", "to": "url-or-id", "anchor_guidance": "..."}
    ]
  },
  "action_plan": {
    "quick_wins": ["page-1", "page-3"],
    "medium_term": ["page-5", "page-7"],
    "strategic": ["page-9"]
  }
}
```

This is the schema other skills can rely on. Keep field names stable. If a value is unknown, use `null` rather than omitting the field.

**Schema versioning rules:**
- The current version is `1.0`. Always emit `schema_version` in the meta block.
- **Additive changes** (new optional fields): bump to `1.1`, `1.2`, etc. Downstream consumers should ignore unknown fields.
- **Breaking changes** (renamed fields, removed fields, changed value types): bump major version (`2.0`) and update this section. Don't ship a breaking change without updating the version and noting it in the skill.

### Step 5: Render the HTML report

**Generate the HTML programmatically from the JSON.** Don't write the HTML by hand — for a 25-page map that's error-prone, slow, and creates drift between the two artifacts. Write a small Python rendering script that:

1. Loads the JSON map you just wrote
2. Iterates pillars and clusters to build the table sections
3. Uses helper functions for status badges, priority badges, LLM-citation badges, and page-label lookup
4. Computes summary counts (P1/P2/P3, expand/new/exists, high-LLM count) directly from the data rather than hard-coding them
5. Writes the final HTML to the output path

Two reasons this matters: (1) the JSON and HTML stay mechanically consistent — change the JSON, re-run the script, HTML updates exactly — and (2) it scales without effort. A 50-page map renders identically to a 5-page one.

Use Tailwind via CDN. Self-contained file, responsive, print-friendly. Mirror the visual style of the other foo-* skill reports (clean, scannable, light theme, generous whitespace).

Required sections, in order:

1. **Header** — site, topic, date, goal (with tilt if set)
2. **Executive Summary** — 3–5 bullets: the recommended pillar strategy, the top 3 quick wins, the headline opportunity, expected impact in qualitative terms (no fabricated numbers)
3. **Data Sources Used** — explicit list of what was pulled (GSC ✓, GA4 ✓, DataForSEO ✓, page scrape ✓, user-provided notes). Be honest about what's missing. Include the `data_confidence` rating with a one-line explanation. If the user accepted proceeding at less-than-high confidence at the Step 2.5 gate, note that here.
4. **Core Topic & Audience**
5. **The Map** — visual hierarchy. Pillar(s) as top-level cards; each pillar shows its clusters; each cluster is a `<details>` block so large maps stay scannable. Each cluster's pages render as a table with columns: Title (with the page's `notes` shown below as small text), Status, Type, Intent, Priority, LLM Citation, Target Query. Use color/badges for status (green=exists, amber=expand, blue=new) and priority (red=P1, orange=P2, indigo=P3).
6. **Prioritized Action Plan** — three columns (Quick wins, Medium-term, Strategic) with counts in each header, ordered lists below
7. **Internal Linking Recommendations** — bulleted rules + a table of specific from→to suggestions with anchor guidance
8. **LLM Citation & AI Visibility Opportunities** — a focused section listing every page flagged `llm_citation_potential: high`, with brief rationale and schema-markup recommendations
9. **Next Steps** — short list, including specific next-skill handoffs ("pair page-X with the seo-title-optimizer-v2 skill") and "regenerate this map in 60–90 days as data evolves"

### Step 6: Update the map history

Append a record to `/home/claude/topical-authority-maps-history.json` (create as `{"maps":[]}` if it doesn't exist). This lets you (and other skills) see what maps have been generated, when, and what state they were in — useful for regeneration and for cross-referencing with downstream actions (was that recommended page actually built?).

Each history record:

```json
{
  "generated_at": "2026-05-20",
  "site": "https://example.com/",
  "topic": "WordPress image galleries",
  "topic_slug": "wordpress-image-galleries",
  "goal": "commercial",
  "schema_version": "1.0",
  "html_path": "/mnt/user-data/outputs/topical-authority-map-wordpress-image-galleries-2026-05-20.html",
  "json_path": "/mnt/user-data/outputs/topical-authority-map-wordpress-image-galleries-2026-05-20.json",
  "data_confidence": "high",
  "pillar_count": 2,
  "cluster_count": 7,
  "total_pages": 38,
  "quick_win_count": 5
}
```

The history check itself happens up in Step 1's recon — by the time you're writing here, you've already decided this is a fresh map or a regeneration.

### Step 7: Present the files

After saving everything, present them to the user using `present_files` with the HTML first (it's what they want to look at) and the JSON second.

## Important Principles

- **Never fabricate metrics.** If you don't have GSC data, don't invent impression counts. Say "no data available" or omit the metric. Same for DataForSEO volumes.
- **Prefer expanding existing pages over creating new ones.** A page already ranking on page 2 is a faster win than a new page from zero. The "expand" status should outnumber "new" in most maps.
- **Listicles and comparisons earn the LLM citations.** Bias supporting content toward these formats unless commercial intent demands a landing-page format.
- **Be honest about confidence.** If GSC/GA4/DataForSEO weren't available, label the report's confidence accordingly and tell the user what data would sharpen it.
- **Generic by design.** This skill should work for any site, not just FooPlugins. Don't hard-code domain assumptions in the output.
- **Keep the JSON stable.** Other skills will consume it. Adding fields is fine; renaming or removing them breaks downstream consumers.

## Edge cases

- **User gives just a topic, no site**: ask for the site once. Without it there's no existing-content audit possible.
- **Site is brand new with no GSC data**: lean entirely on DataForSEO + competitor analysis. Flag this clearly in the report's Data Sources section.
- **User wants a map for a competitor / site they don't own**: skip GSC/GA4 (they don't have access). Use DataForSEO's `_ranked_keywords` and `_relevant_pages` for that domain instead. Note this in the report.
- **Very broad topic** (e.g., "WordPress" alone): push back once and suggest narrowing. Maps that try to cover everything end up covering nothing.
