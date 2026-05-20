# Examples

Reference outputs for the topical-authority-map-generator skill. These files exist to show what good output looks like — they are **not** templates to copy from. Always generate fresh content from the user's actual data.

## When to consult these examples

Read the relevant example only when:

- **Uncertain about JSON field semantics** — e.g., what goes in `goal_tilt`, when `url` is `null`, how to phrase `rationale`
- **Uncertain about HTML structure** — e.g., what badges look like, how the cluster tables are laid out
- **Handling an unusual case** — competitor mapping, brand-new site, missing data sources

Do NOT consult these examples on every run. They cost context and you don't need them once the JSON schema in SKILL.md is fresh in your head.

## The files

### `example-1-commercial-high-confidence.json`
**The happy path.** FooGallery on fooplugins.com — full data from GSC, GA4, DataForSEO, and page scraping. Commercial goal. Single strong pillar (the FooGallery product page) with 5 clusters: comparisons, use cases, tutorials, feature deep-dives, and definitions/FAQ. Shows what a high-confidence, commercial-tilted map looks like: heavy on comparison and listicle pages, "expand" status outnumbers "new", clear quick-wins backed by GSC data.

### `example-1-commercial-high-confidence.html`
The rendered HTML report for example 1. Reference for visual structure, badge styling, table layout, and section ordering. Mirrors the visual style of the other foo-* skill reports — light theme, Tailwind via CDN, scannable, print-friendly.

### `example-2-informational-medium-confidence.json`
A photography blog mapping "image SEO for photographers." GA4 is missing (data_confidence: medium). Informational goal. Single pillar that doesn't exist yet (status: new). Mostly "new" page status — the site has thin existing coverage. Heavier on definitional and tutorial content; fewer comparison pages. Demonstrates how the map shifts when the goal is informational rather than commercial.

### `example-3-competitor-low-confidence.json`
A reverse-engineered map of envira-gallery.com (a competitor of FooGallery). No GSC or GA4 access — DataForSEO only (data_confidence: low). Shows how to handle the competitor-mapping edge case: the `action_plan` is empty (it's an analysis artifact, not a build plan), `internal_linking.rules` explicitly notes N/A, and `notes` fields cross-reference back to the FooGallery map where competitive responses live.

### `example-history.json`
Three entries in `topical-authority-maps-history.json`. Shows the file format and demonstrates the regeneration case — the third entry is a regeneration of the first entry's topic (same site, same topic_slug, ~2 months later). When you encounter a prior map on the same site+topic during Step 1 recon, this is what you're looking at.

### `example-render.py`
A working Python script that renders the HTML report from a JSON map. Use it as a starting template — adapt the file paths to your run, but the helper functions (`status_badge`, `priority_badge`, `llm_badge`, `page_label`) and the overall structure (load JSON → build cluster sections → compute summary counts → write HTML) transfer directly. Demonstrates the render-from-JSON pattern that Step 5 mandates.

## What to imitate, what to ignore

**Imitate:**
- The level of specificity in `notes` fields (concrete reasoning tied to data, not generic SEO advice)
- The `rationale` format for pillars (one line with actual GSC numbers when available)
- The status mix — most maps should be heavier on "expand" than "new"
- The action_plan size — ~5 quick wins, ~6 medium-term, ~3 strategic is a healthy shape
- The HTML's collapsible cluster sections (`<details>` tags) — keeps the report scannable for large maps

**Don't imitate:**
- The specific keyword volumes or impression counts — those are fabricated for these examples. Always use the user's actual data.
- The exact page titles — those are FooPlugins-specific.
- The cluster themes — those depend entirely on the topic being mapped.
