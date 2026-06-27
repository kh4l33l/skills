---
name: article-eeat-pruning-audit
description: Audit a single article or page for helpful-content quality, E-E-A-T/trust signals, freshness, factual risk, and SEO pruning decisions; recommend keep, update, merge, redirect, noindex, or delete with evidence-backed reasons and concrete fixes.
license: MIT
compatibility: hermes, claude, codex
---

# Article E-E-A-T + Content Pruning Audit

Use this skill when a user asks to audit an article, blog post, landing page, or URL and decide what to do with it, especially for:

- E-E-A-T or trust-signal review
- Google helpful-content review
- content decay or outdated-content cleanup
- article-level content pruning
- deciding whether to keep, update, merge, redirect, noindex, or delete a page
- producing an editor-ready action brief grounded in facts

## Goal

Produce an article-level decision memo that tells the editor exactly what to do with the page, why, and what evidence supports the recommendation.

The audit should be grounded in:

- the page/article content itself
- available performance, backlink, and internal-link evidence when provided or retrievable
- current official Google documentation about helpful, reliable, people-first content, E-E-A-T, Search Essentials, spam policies, structured data, and quality-rater concepts
- explicit fact checks for dated, high-risk, commercial, review, technical, or compliance-sensitive claims

Do **not** present E-E-A-T as a direct Google ranking factor or as an official Google score. Treat the score in this skill as an internal prioritization heuristic only. Google frames E-E-A-T as a quality/trust concept reflected by many signals, with **Trust** as the most important element.

## Required inputs

At least one of:

- Article URL
- Article text, HTML, or markdown
- CMS draft content

Useful optional inputs:

- target keyword/query and intended audience
- business goal or conversion goal
- publication date and last-updated date
- Search Console data: clicks, impressions, CTR, average position, query/page pairs, and recent trend
- backlink or externally linked page data
- known competing/canonical pages on the same site
- author, reviewer, organization, and editorial-policy context

If analytics, backlink, or site-context evidence is unavailable, continue with a content-only audit but label the limitation clearly. Never invent traffic, rankings, backlinks, search demand, author credentials, or competitor facts.

## Workflow

### 1. Fetch and normalize the article

If a URL is provided, inspect the actual page. Extract where possible:

- title tag, H1, meta description
- visible byline, author bio link, reviewer, organization/publisher
- publish date and modified/last-reviewed date
- headings and main-content structure
- key claims, statistics, prices, dates, tool/product names, legal/regulatory statements, version references, and procedural steps
- images, alt text, screenshots, examples, demos, videos, and proof-of-use elements
- internal links, external citations, affiliate/sponsorship disclosures, CTAs
- canonical, indexability/noindex signals, redirects, and article/schema JSON-LD

Identify the likely page purpose and user/search intent.

### 2. Collect optional SEO and pruning evidence

Use available sources before making destructive recommendations:

- Search Console page metrics over a meaningful window, ideally 12 months plus recent trend
- query/page pairs to understand actual search intent
- backlinks or externally linked pages
- internal links and navigation importance
- cannibalizing pages or stronger canonical alternatives
- conversion or engagement data where available

If this evidence is missing, lower confidence for redirect/delete/noindex decisions and state what must be checked before implementation.

### 3. Check freshness and factual risk

Extract and verify time-sensitive or high-risk statements:

- dated statistics, benchmarks, prices, commission rates, availability, product features, screenshots, and UI steps
- laws, regulations, medical/financial/legal/safety guidance, or compliance claims
- software versions, APIs, plugin/theme compatibility, deprecated methods, and code snippets
- review/comparison claims such as “best”, “fastest”, “cheapest”, “recommended”, or “tested”

Classify claims as:

- `verified`
- `outdated`
- `unsupported`
- `unclear`
- `needs expert review`

For current-fact checks, use authoritative primary sources where possible and include source URLs in the audit.

### 4. Classify intent, content type, and risk

Before scoring, classify:

- **Page intent:** informational, commercial, transactional, navigational, service/support, or mixed
- **Content type:** how-to, review, comparison, opinion, news, product/service page, documentation, case study, glossary, listicle, or other
- **Risk/YMYL class:** health, finance, legal, safety, civic/news, shopping/transactional trust, or low-risk/non-YMYL
- **Required proof level:** low, medium, or high

Raise the proof level for YMYL, safety, legal/financial claims, product reviews, affiliate/commercial pages, and pages making strong factual claims.

### 5. Run an emergency trust brake

Mark the article `BLOCK` regardless of numeric score if evidence shows any of these:

- dangerous YMYL/safety advice without appropriate expert authorship, review, or reliable sourcing
- major factual contradictions, obsolete instructions that could harm users, or unsupported high-stakes claims
- affiliate, sponsorship, or commercial relationships are material but undisclosed
- title, H1, or meta description materially misrepresents what the page delivers
- the page is deceptive about author, publisher, AI/automation use, business identity, functionality, or redirects
- main content is copied, scraped, lightly rewritten, keyword-stuffed, or scaled low-value content
- for high-risk pages, users cannot tell who is responsible for the content or how to contact or verify the publisher

A `BLOCK` verdict means “do not publish or keep indexed as-is”; it does not automatically mean delete.

### 6. Assess Google helpful-content and E-E-A-T alignment

Use Google’s official self-assessment concepts and quality-rater framing:

- Does the content provide original information, reporting, research, analysis, or substantial value beyond rewriting sources?
- Is it complete and comprehensive for the intended task/query?
- Is it written for people first, not mainly to attract search traffic?
- Is the creator clear (`Who`), is the production method transparent where relevant (`How`), and is the purpose useful to users (`Why`)?
- Does it show first-hand experience or expertise appropriate to the topic and content type?
- For reviews/comparisons, does it show real use/testing, decision factors, evidence, alternatives, and rationale?
- Would a reader trust the article’s facts, sourcing, author, site, commercial disclosures, and transaction/support context?
- Is the main content easy to use and not obstructed by ads, popups, broken UX, or misleading page elements?

### 7. Score the article

Score each dimension from 0 to 10. Higher is better. Every score must include a one-sentence evidence note.

| Dimension | What to evaluate |
|---|---|
| Freshness & factual accuracy | Current facts, dates, versions, laws, pricing, screenshots, dead tools, broken procedures, unsupported claims. |
| Main content quality & completeness | Originality, depth, structure, clarity, examples, insight beyond obvious summaries, spelling/style, complete answer to intent. |
| User value & intent fit | Whether the article helps a real reader solve the task today, satisfies likely search intent, and avoids thin/generic content. |
| E-E-A-T / trust evidence | First-hand experience, expert review, author identity, credentials, citations, transparent corrections/editorial policy, reputation signals, disclosures. |
| SEO & consolidation risk | Title/H1/meta fit, internal links, schema, cannibalization, indexability, backlinks, traffic potential, whether it should remain indexed. |

Overall score = average of the five dimensions × 10.

Use the score as a prioritization aid, not as a substitute for judgment. Any emergency trust brake overrides the score.

### 8. Choose the pruning action

Choose exactly one primary action and explain why:

- **KEEP** when the article is current, useful, trusted, unique, and either performs or serves a clear strategic/user purpose. Minor fixes only.
- **UPDATE** when the topic remains relevant/searchable and the page has value, but facts, examples, screenshots, sections, source support, or author/trust signals are stale or incomplete.
- **MERGE** when another page on the same site covers the same or very similar intent and consolidation would create a stronger canonical page. Preserve unique useful sections and 301 the weaker URL if removing it.
- **REDIRECT** when the page is obsolete or redundant but has meaningful backlinks, history, or a close replacement page. Use a relevant 301 target, not the homepage by default.
- **NOINDEX** when the content should remain available to users/internal audiences but should not compete in search: historical archive, thin utility page, duplicate support page, or low-search-value content that still has user value.
- **DELETE / 410** when the page has no meaningful traffic, backlinks, strategic value, or recoverable user value; the topic is out-of-scope/obsolete; or the content is inaccurate enough to damage trust. Human-review before deletion.

Never recommend deletion solely because traffic is low. Check backlinks, internal importance, strategic value, search demand, and replacement/redirect options.

### 9. Produce implementation instructions

For update/merge/keep recommendations, include concrete changes:

- claims to fix, with source URLs
- sections to add, remove, rewrite, or consolidate
- experience/proof to add: screenshots, benchmarks, tested steps, original data, case study, author notes, methodology
- trust signals: byline, author bio, reviewer, citations, disclosure, last-reviewed date, editorial policy link, corrections process
- SEO changes: title/meta/H1, internal links, schema fields, canonical/redirect/noindex actions
- acceptance criteria so an editor/developer knows when the fix is done

## Output format

Return a concise, evidence-led memo:

```markdown
# Article Audit: <title or URL>

## Decision
**Recommended pruning action:** KEEP / UPDATE / MERGE / REDIRECT / NOINDEX / DELETE
**Quality gate:** SHIP / FIX / BLOCK
**Confidence:** High / Medium / Low
**Overall score:** NN/100
**One-line reason:** <plain-English summary>

## Evidence snapshot
- URL/content inspected: <source>
- Published/updated: <dates or unknown>
- Intended query/audience: <inferred or provided>
- Performance/link evidence: <data used, or "not available">
- Key sources checked: <source URLs>

## Classification
- Intent: <informational/commercial/etc.>
- Content type: <how-to/review/etc.>
- Risk/YMYL class: <class>
- Required proof level: <low/medium/high>

## Scorecard
| Dimension | Score | Evidence |
|---|---:|---|
| Freshness & factual accuracy | N/10 | ... |
| Main content quality & completeness | N/10 | ... |
| User value & intent fit | N/10 | ... |
| E-E-A-T / trust evidence | N/10 | ... |
| SEO & consolidation risk | N/10 | ... |

## What is wrong / risky
| Issue | Evidence | Why it matters | Severity |
|---|---|---|---|

## What to do
1. <highest-leverage action> — why, exact edit, acceptance criteria.
2. <next action> — why, exact edit, acceptance criteria.
3. <next action> — why, exact edit, acceptance criteria.

## Claim/fact checks
| Claim or section | Status | Source/evidence | Required edit |
|---|---|---|---|

## E-E-A-T / trust fixes
- Who: <byline/author/entity fixes>
- How: <methodology/AI/editorial disclosure/fact-check process>
- Why: <people-first purpose and reader value>
- Trust: <citations, reviewer, policy, contact/support, corrections>

## SEO/content pruning notes
- Keep indexed? yes/no/conditional
- Merge/redirect/noindex/delete details: <target URL, rationale, safeguards>
- Internal links to add/update: <list>
- Schema/meta changes: <list>

## Caveats
- <missing data, assumptions, or human expert review needed>
```

## Official Google sources to use

Use current versions of these sources when making claims about Google guidance:

- Google Search Central — Creating helpful, reliable, people-first content: `https://developers.google.com/search/docs/fundamentals/creating-helpful-content`
- Google Search Central — Google Search's guidance on using generative AI content: `https://developers.google.com/search/docs/fundamentals/using-gen-ai-content`
- Google Search Central — SEO Starter Guide: `https://developers.google.com/search/docs/fundamentals/seo-starter-guide`
- Google Search Central — Search Essentials: `https://developers.google.com/search/docs/essentials`
- Google Search Central — Spam policies: `https://developers.google.com/search/docs/essentials/spam-policies`
- Google Search Central — General structured data guidelines: `https://developers.google.com/search/docs/appearance/structured-data/sd-policies`
- Google Search Central — Article structured data: `https://developers.google.com/search/docs/appearance/structured-data/article`
- Google Search Central — Influence your byline dates in Google Search: `https://developers.google.com/search/docs/appearance/publication-dates`
- Google Search Central — ProfilePage structured data: `https://developers.google.com/search/docs/appearance/structured-data/profile-page`
- Google Search Central — Organization structured data: `https://developers.google.com/search/docs/appearance/structured-data/organization`
- Google Search Central — Fact check structured data: `https://developers.google.com/search/docs/appearance/structured-data/factcheck`
- Google Search Central — Review snippet structured data: `https://developers.google.com/search/docs/appearance/structured-data/review-snippet`
- Google Search Central — Write high quality reviews: `https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews`
- Google Search Central Blog — E-A-T gets an extra E for Experience: `https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t`
- Google Search Quality Rater Guidelines PDF: `https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf`

Use the Quality Rater Guidelines conceptually for page purpose, main content quality, reputation, E-E-A-T, YMYL scrutiny, and Needs Met. Rater guidelines do not directly control rankings.

## Content-pruning tool pattern

Some public content-pruning tools describe a useful article-level workflow:

- discover pages from a sitemap, CMS feed, or crawl
- audit each article independently
- score freshness, editorial quality, user value, SEO, and risk
- identify obsolete facts, missing recent information, weak trust signals, and thin/generic sections
- assign a clear action such as delete, update, noindex, or keep
- provide a human-readable justification and work queue

Use this as workflow inspiration only, not as official SEO doctrine.

## Public prompt/skill research notes

Public E-E-A-T prompts and skills are useful but uneven. Borrow categories carefully:

- content and quality
- expertise and experience
- page experience
- people-first focus
- search-engine-first warning signs
- `Who`, `How`, and `Why`
- author credibility
- topical/supporting content gaps
- confidence labels and prioritized remediation

Avoid copying spammy prompt baggage, promotional instructions, fake precision, fake credentials, manufactured backlinks, or unsupported ranking claims.

## Pitfalls

- Do not fabricate facts, source checks, traffic, backlinks, author credentials, or Google claims.
- Do not recommend deleting a URL without checking backlinks/redirect options or clearly stating that link data is missing.
- Do not treat low traffic as proof of low quality.
- Do not recommend fake author bios, fake expert reviewers, fake testing, fake reviews, or manufactured backlinks.
- Do not present a generic checklist as an audit; cite page-specific evidence.
- Do not overstate what Google says. E-E-A-T is a quality concept, not a direct ranking-factor knob.
- For YMYL or legal/medical/financial/safety content, raise the evidence bar and recommend expert review when needed.
- Do not use structured data to describe content that is not visible on the page.
- Do not update dates merely to look fresh; require substantive updates.

## Verification checklist

Before finalizing an audit, verify:

- The article was actually inspected, or the audit is explicitly marked as based on provided text only.
- Every score has page-specific evidence.
- Every recommendation maps to a specific issue and acceptance criterion.
- Google claims are tied to official sources.
- Any delete/noindex/redirect recommendation includes safeguards and confidence level.
- Caveats identify missing analytics, backlink, competitor, or expert-review data.
- The output distinguishes pruning action from quality gate: e.g. `NOINDEX + BLOCK`, `UPDATE + FIX`, or `KEEP + SHIP`.
