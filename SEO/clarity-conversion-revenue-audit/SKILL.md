---
name: clarity-conversion-revenue-audit
description: >
  Use Microsoft Clarity MCP data and session recordings to find revenue-impacting conversion friction,
  SEO-intent mismatches, UX bugs, and support-deflection opportunities. Trigger this skill when the user
  asks for a Clarity audit, conversion-friction review, session-recording triage, product/pricing-page UX
  analysis, or recurring behavioral analytics report focused on improving signups, purchases, upgrades,
  or lead quality.
---

# Microsoft Clarity Conversion Revenue Audit

Use this skill to turn Microsoft Clarity analytics and session recordings into a short list of implementable fixes that can improve revenue, conversions, customer trust, or support deflection.

The core principle: **Clarity is the behavioral evidence layer, not the main traffic dashboard.** Use search analytics and web analytics for demand/trend data; use Clarity to understand why visitors hesitate, mis-click, abandon, or fail to reach the next step.

## Recommended tools

- **Microsoft Clarity MCP**: Required. Use dashboard queries and session-recording filters.
- **GA4 or equivalent analytics**: Recommended for landing-page sessions, conversion events, and source/medium context.
- **Google Search Console or equivalent search data**: Recommended for query intent and landing-page opportunities.
- **Issue tracker or task tool**: Optional, for turning findings into tickets.

## Best use cases

1. **Money-page conversion friction**
   - Product pages
   - Pricing and plan-comparison pages
   - Checkout, trial, signup, demo, or upgrade paths
   - Feature pages that should route visitors toward conversion

2. **SEO intent validation**
   - Pages with strong search visibility but weak conversion behavior
   - Documentation or help pages that attract commercial-intent search traffic
   - Landing pages where users bounce, quickback, or fail to click the expected CTA

3. **Support-deflection diagnostics**
   - Help docs where users scroll excessively or leave without finding an answer
   - Sessions with dead clicks, rage clicks, repeated backtracking, or text selection around confusing instructions
   - Pages tied to recurring support questions

4. **Technical UX diagnostics**
   - JavaScript errors
   - Dead clicks or rage clicks
   - Layout shifts, slow loads, broken interactions, or mobile-only friction
   - Form, consent-banner, navigation, or pricing-table issues

5. **Campaign or revenue-drop investigation**
   - When traffic looks healthy but conversions fall
   - When a paid/organic campaign underperforms
   - When a recent site change may have introduced friction

## Constraints and request budget

Clarity exports often have strict limits, commonly including a small daily request quota, a short lookback window, and a limited number of dimensions per query. Check the current project limits before running broad analysis.

Default request budget for a scheduled audit: **3-6 Clarity calls total**.

Use calls in this order:

1. One dashboard query for the high-value page group.
2. One recording query for conversion-path pages.
3. One recording query filtered for friction signals.
4. One recording query for search/referral landing sessions on help or content pages.
5. Up to two extra calls only to confirm a high-impact issue.

Do not waste quota on generic “top traffic” summaries unless the user explicitly asks for that.

## Input handling

Ask for or infer:

- Website or product area to audit
- Priority page group, such as pricing, product pages, checkout, docs, demos, or onboarding
- Date range, usually the latest complete 1-3 days supported by Clarity
- Primary business goal: purchases, upgrades, trials, leads, onboarding completion, support reduction, or content-assisted conversion

If the user gives no scope, choose the highest-revenue or closest-to-conversion pages first.

## Workflow

### Step 1: Define the revenue path

List the pages or flows closest to the business outcome:

- Product or category landing pages
- Pricing / plan-comparison / checkout pages
- Demo / proof / case-study pages
- Docs or content pages that attract high-intent visitors
- Signup / trial / contact forms

State the exact page patterns you will inspect.

### Step 2: Pull a small dashboard snapshot

Run one focused Clarity dashboard query for the selected date range. Ask for:

- sessions and users
- device split
- engagement or active time
- scroll depth where available
- friction signals such as dead clicks, rage clicks, quickbacks, excessive scroll, or script errors

Keep the query focused on the chosen page group. Do not ask for multiple unrelated analyses in one query.

### Step 3: Pull conversion-path recordings

List recent recordings for the highest-value conversion pages. Sort by recency or duration depending on the question.

Look for:

- CTA hesitation or no CTA visibility
- pricing-table confusion
- repeated scrolling between plan details
- clicks on non-clickable elements
- users reaching proof/demo sections too late
- mobile-specific layout problems
- abandonment after viewing price, forms, or required steps

### Step 4: Pull friction-filtered recordings

List recordings filtered for one or more of:

- dead clicks
- rage clicks
- quickbacks
- excessive scroll
- JavaScript errors
- poor performance score, high layout shift, or slow load where supported

Prioritize pages closest to conversion. A bug on a low-value blog post is rarely as important as a broken interaction on pricing or checkout.

### Step 5: Validate SEO or content intent

When search traffic matters, connect search intent to behavior:

1. Use search data to identify the query intent and landing page.
2. Use Clarity recordings to check whether visitors find the expected answer or next step.
3. Look for missed assisted-conversion opportunities:
   - no product CTA on high-intent help content
   - demo links below where users usually leave
   - docs answering the question but not guiding the next action
   - page title/meta promise not matched by visible content

### Step 6: Cluster evidence into patterns

Do not dump raw session lists. Group observations into patterns such as:

- “Mobile users do not reach the pricing CTA.”
- “Visitors are clicking screenshots/cards that are not links.”
- “Search visitors reach docs, solve the immediate problem, then leave without a commercial next step.”
- “Pricing comparison creates plan-selection hesitation.”
- “A script error or consent overlay blocks the intended path.”

For each pattern, include the supporting page(s), metric(s), and recording links when available.

### Step 7: Prioritize fixes

Use this priority scale:

- **P0**: Blocks or materially hurts purchase/signup/upgrade/contact flow; broken CTA; severe mobile issue; JavaScript error on a money path.
- **P1**: High-intent pages fail to route users to the next commercial step; repeated dead/rage clicks; confusing plan or feature explanation; weak above-the-fold CTA.
- **P2**: Useful UX/content polish without clear immediate conversion impact.

Prioritize by expected business impact, confidence, implementation effort, and proximity to conversion.

## Output format

Return a concise action report:

```markdown
## Clarity Conversion Revenue Audit — <site/product> — <date range>

### Executive summary
- <1-3 bullets with the highest-leverage observations>

### Highest-impact findings
1. **<finding>**
   - Evidence: <pages, metrics, and session links>
   - Business risk/opportunity: <why this could affect purchases/signups/leads/support>
   - Recommended action: <specific fix>
   - Owner: Marketing / Content / Design / Development / Support
   - Priority: P0/P1/P2

### Recommended actions this week
1. <action with acceptance criteria>
2. <action with acceptance criteria>
3. <action with acceptance criteria>

### What to watch after changes
- <Clarity signal and analytics metric to monitor>

### Caveats
- <API limits, sample size, date range, missing conversion definitions>
```

## Good recommendations

- Add a sticky mobile CTA when recordings show visitors leave before reaching the primary CTA.
- Turn repeatedly clicked screenshots, cards, icons, or feature blocks into real links.
- Add a “which plan is right for me?” explainer when pricing sessions show repeated comparison-table backtracking.
- Move proof, demos, compatibility notes, refund/trust details, or FAQs above the point where users typically abandon.
- Add contextual product/demo/pricing links to high-intent docs that currently dead-end after answering the support question.
- Create a bug ticket when recordings show a JavaScript error, broken form, non-responsive CTA, or layout issue on a conversion path.

## Bad recommendations

- “Improve UX” without page/session evidence.
- Broad redesigns based on a handful of recordings.
- Treating Clarity as long-term trend reporting.
- Pulling generic traffic dashboards when the goal is conversion improvement.
- Ignoring mobile/desktop differences.
- Mixing search-console, web-analytics, and Clarity semantics as if they measure the same thing.

## Verification checklist

Before finalizing the report, confirm:

- [ ] The date range is explicit.
- [ ] The page group is close to revenue, signup, lead, onboarding, or support-deflection value.
- [ ] Clarity request count stayed within the planned budget.
- [ ] Findings are clustered into patterns, not raw session dumps.
- [ ] Each recommendation has evidence, owner, priority, and acceptance criteria.
- [ ] Caveats mention sample size and API/window limits.

## Post-change measurement

After fixes ship, rerun a focused Clarity review within the supported lookback window and compare:

- dead/rage/quickback signals on changed pages
- scroll depth to key CTAs or proof sections
- onward clicks from docs/content/demo pages to product, pricing, signup, or checkout
- form/CTA completion behavior
- JavaScript errors and performance issues on the changed path

Use GA4 or the primary analytics platform for conversion-rate validation, and use Clarity to explain the observed behavior change.
