#!/usr/bin/env python3
"""Render the FooGallery topical authority map HTML report from the JSON."""
import json
import html

with open('/home/claude/foogallery-map/topical-authority-map-wordpress-image-galleries-2026-05-20.json') as f:
    m = json.load(f)

# Build helper indexes
pages_by_id = {}
for c in m['clusters']:
    for p in c['pages']:
        pages_by_id[p['id']] = p

pillars_by_id = {p['id']: p for p in m['pillars']}

# Page count for sizing
total_pages = sum(len(c['pages']) for c in m['clusters'])

def esc(s):
    return html.escape(str(s)) if s is not None else ''

def status_badge(status):
    if status == 'exists':
        return f'<span class="badge badge-exists">exists</span>'
    if status == 'expand':
        return f'<span class="badge badge-expand">expand</span>'
    if status == 'new':
        return f'<span class="badge badge-new">new</span>'
    return f'<span class="badge">{esc(status)}</span>'

def priority_badge(p):
    if p == 'P1':
        return '<span class="badge badge-p1">P1</span>'
    if p == 'P2':
        return '<span class="badge badge-p2">P2</span>'
    if p == 'P3':
        return '<span class="badge badge-p3">P3</span>'
    return f'<span class="badge">{esc(p)}</span>'

def llm_badge(v):
    return f'<span class="badge badge-llm-{esc(v)}">{esc(v)}</span>'

# Counts for summary
p1_count = sum(1 for p in pages_by_id.values() if p['priority'] == 'P1')
p2_count = sum(1 for p in pages_by_id.values() if p['priority'] == 'P2')
p3_count = sum(1 for p in pages_by_id.values() if p['priority'] == 'P3')
expand_count = sum(1 for p in pages_by_id.values() if p['status'] == 'expand')
new_count = sum(1 for p in pages_by_id.values() if p['status'] == 'new')
exists_count = sum(1 for p in pages_by_id.values() if p['status'] == 'exists')
high_llm = sum(1 for p in pages_by_id.values() if p['llm_citation_potential'] == 'high')

# Build clusters HTML
clusters_html_parts = []
for c in m['clusters']:
    rows = []
    for p in c['pages']:
        title_html = esc(p['title'])
        if p.get('url'):
            title_html = f'<a href="{esc(p["url"])}" class="text-indigo-600 hover:underline">{title_html}</a>'
        target_query = esc(p.get('target_query', ''))
        rows.append(f'''
            <tr>
              <td class="py-3 pr-3 font-medium align-top">{title_html}<div class="text-xs text-slate-500 mt-1">{esc(p.get('notes',''))}</div></td>
              <td class="py-3 pr-3 align-top">{status_badge(p['status'])}</td>
              <td class="py-3 pr-3 align-top text-slate-700">{esc(p.get('type',''))}</td>
              <td class="py-3 pr-3 align-top text-slate-700">{esc(p.get('intent',''))}</td>
              <td class="py-3 pr-3 align-top">{priority_badge(p['priority'])}</td>
              <td class="py-3 pr-3 align-top">{llm_badge(p['llm_citation_potential'])}</td>
              <td class="py-3 align-top text-slate-600"><code class="text-xs">{target_query}</code></td>
            </tr>''')
    open_attr = 'open' if c['id'] == 'cluster-1' else ''
    clusters_html_parts.append(f'''
    <details {open_attr} class="mb-4 bg-white rounded-lg border border-slate-200">
      <summary class="cursor-pointer p-4 font-semibold text-slate-900 hover:bg-slate-50">
        {esc(c['theme'])} <span class="text-sm font-normal text-slate-500">({len(c['pages'])} pages)</span>
      </summary>
      <div class="overflow-x-auto px-4 pb-4">
        <table class="w-full text-sm">
          <thead class="text-xs text-slate-500 uppercase border-b border-slate-200">
            <tr>
              <th class="text-left py-2 pr-3">Title &amp; Rationale</th>
              <th class="text-left py-2 pr-3">Status</th>
              <th class="text-left py-2 pr-3">Type</th>
              <th class="text-left py-2 pr-3">Intent</th>
              <th class="text-left py-2 pr-3">Priority</th>
              <th class="text-left py-2 pr-3">LLM</th>
              <th class="text-left py-2">Target Query</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            {''.join(rows)}
          </tbody>
        </table>
      </div>
    </details>''')

clusters_html = '\n'.join(clusters_html_parts)

# Quick wins list
def page_label(pid):
    if pid.startswith('pillar'):
        return esc(pillars_by_id[pid]['title'])
    p = pages_by_id.get(pid)
    return esc(p['title']) if p else pid

quick_wins_html = '\n'.join(f'<li>{page_label(pid)}</li>' for pid in m['action_plan']['quick_wins'])
medium_term_html = '\n'.join(f'<li>{page_label(pid)}</li>' for pid in m['action_plan']['medium_term'])
strategic_html = '\n'.join(f'<li>{page_label(pid)}</li>' for pid in m['action_plan']['strategic'])

# Internal linking rules
linking_rules = '\n'.join(f'<li>{esc(r)}</li>' for r in m['internal_linking']['rules'])
linking_rows = '\n'.join(f'''<tr>
              <td class="py-3 pr-3 text-slate-600 align-top">{page_label(r["from"])}</td>
              <td class="py-3 pr-3 text-slate-600 align-top">{page_label(r["to"])}</td>
              <td class="py-3 align-top text-slate-700">{esc(r["anchor_guidance"])}</td>
            </tr>''' for r in m['internal_linking']['specific_recommendations'])

# LLM citation list — collect every page with high LLM potential
high_llm_pages = [p for p in pages_by_id.values() if p['llm_citation_potential'] == 'high']
llm_list = '\n'.join(f'<li><strong>{esc(p["title"])}</strong> ({esc(p["type"])}) — {esc(p["notes"][:200])}...</li>' for p in high_llm_pages[:10])

# Data sources
sources_present = set(m['meta']['data_sources'])
def source_line(key, label, fallback_text=''):
    if key in sources_present:
        return f'<li>✓ <strong>{label}</strong></li>'
    return f'<li>✗ <strong>{label}</strong> — {fallback_text}</li>'

sources_html = f'''
        {source_line('gsc', 'Google Search Console', 'not used')}
        {source_line('ga4', 'GA4', 'property ID not provided — engagement data missing; map relies on GSC click data as the conversion proxy')}
        {source_line('dataforseo', 'DataForSEO', 'not used')}
        {source_line('page_scrape', 'Live page scraping', 'web_fetch permission restricts to user-provided URLs; page structure inferred from URL paths and GSC data')}
'''

# Pillar block
pillar = m['pillars'][0]
pillar_html = f'''
    <div class="bg-white rounded-lg border-2 border-indigo-300 p-5 mb-6">
      <div class="text-xs font-semibold text-indigo-600 uppercase tracking-wide mb-1">Pillar</div>
      <h3 class="text-xl font-bold text-slate-900 mb-2">{esc(pillar['title'])}</h3>
      <div class="text-sm text-slate-600 mb-2">
        <a href="{esc(pillar['url'])}" class="text-indigo-600 hover:underline">{esc(pillar['url'])}</a>
        &nbsp;·&nbsp; {status_badge(pillar['status'])}
        &nbsp;·&nbsp; Goal: <strong>{esc(pillar['goal'])}</strong>
      </div>
      <p class="text-sm text-slate-700 mb-2"><strong>Rationale:</strong> {esc(pillar['rationale'])}</p>
      <div class="text-xs text-slate-500">Target keywords: {' · '.join(esc(k) for k in pillar['target_keywords'])}</div>
    </div>
'''

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Topical Authority Map — WordPress Image Galleries — fooplugins.com</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }}
  .badge-exists {{ background: #d1fae5; color: #065f46; }}
  .badge-expand {{ background: #fef3c7; color: #92400e; }}
  .badge-new {{ background: #dbeafe; color: #1e40af; }}
  .badge-p1 {{ background: #fee2e2; color: #991b1b; }}
  .badge-p2 {{ background: #fed7aa; color: #9a3412; }}
  .badge-p3 {{ background: #e0e7ff; color: #3730a3; }}
  .badge-llm-high {{ background: #ede9fe; color: #5b21b6; }}
  .badge-llm-medium {{ background: #f3f4f6; color: #4b5563; }}
  .badge-llm-low {{ background: #f9fafb; color: #6b7280; }}
  code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #f1f5f9; padding: 1px 4px; border-radius: 3px; }}
  @media print {{ body {{ font-size: 11pt; }} details {{ open: true; }} }}
</style>
</head>
<body class="bg-slate-50 text-slate-800">

<div class="max-w-6xl mx-auto px-6 py-10">

  <header class="mb-10 pb-6 border-b border-slate-200">
    <div class="text-sm text-slate-500 uppercase tracking-wide mb-2">Topical Authority Map</div>
    <h1 class="text-4xl font-bold text-slate-900 mb-3">{esc(m['meta']['topic'])}</h1>
    <div class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
      <div><span class="font-semibold">Site:</span> {esc(m['meta']['site'])}</div>
      <div><span class="font-semibold">Generated:</span> {esc(m['meta']['generated_at'])}</div>
      <div><span class="font-semibold">Goal:</span> {esc(m['meta']['goal'])} <span class="text-slate-400">(tilt: {esc(m['meta'].get('goal_tilt') or '—')})</span></div>
      <div><span class="font-semibold">Data confidence:</span> <span class="text-amber-700 font-semibold">{esc(m['meta']['data_confidence'].title())}</span></div>
    </div>
  </header>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Executive Summary</h2>
    <ul class="space-y-2 text-slate-700 list-disc list-inside">
      <li><strong>Single-pillar strategy:</strong> Expand <code>/foogallery-wordpress-gallery-plugin/</code> as the topical hub — it&apos;s already the #1 traffic page (1,758 clicks / 53k impressions in 90d) and the natural commercial conversion endpoint for every cluster.</li>
      <li><strong>Headline opportunity — selling photos online:</strong> <code>/how-to-sell-photos-online/</code> has 91k impressions but only 0.2% CTR at pos 13.6. DataForSEO confirms 1,900/mo on the head term — the highest-volume keyword in this map. Title was already updated April 1; continue the optimization push.</li>
      <li><strong>The hover-effects problem becomes a hover-effects opportunity:</strong> <code>/thumbnail-hover-effect/</code> is the second-highest impression page (98k impressions, 0.76% CTR) but the audience is mostly CSS developers, not WordPress users. Rewrite to serve both: CSS solutions up top (capture the SEO traffic), FooGallery&apos;s no-code hover settings as the commercial tie-back below. Add a new listicle (&quot;15 CSS hover effects&quot;) that does the same job at the next level.</li>
      <li><strong>Comparison + listicle pages dominate the high-LLM-citation set:</strong> The existing <code>/gallery-plugin-comparison-2026/</code> ranks at pos 6.1 with 34k impressions but converts terribly (0.55% CTR). Title rework + comparison table at the top + new vs-Envira and vs-NextGEN pages should compound into multi-page authority.</li>
      <li><strong>Map shape:</strong> 1 pillar, 6 clusters, {total_pages} supporting pages. {p1_count} P1 quick wins, {p2_count} P2 medium-term, {p3_count} P3 strategic. {expand_count} pages already exist (expand), {new_count} are new, {exists_count} stays as-is.</li>
    </ul>
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Data Sources Used</h2>
    <div class="bg-white rounded-lg border border-slate-200 p-5">
      <ul class="space-y-1 text-slate-700">{sources_html}</ul>
      <p class="mt-3 text-sm text-slate-600">
        <strong>Confidence: Medium.</strong> GSC and DataForSEO returned solid data. GA4 property ID was not provided in this session — without engagement metrics, the map uses GSC click data as the conversion proxy, which is a reasonable but partial substitute. Live page scraping was unavailable due to web_fetch URL restrictions; existing page structure was inferred from URL paths and the GSC top-pages list. Sharing your GA4 property ID would let me re-run this with engagement and conversion data factored in, which would sharpen the priority calls in particular.
      </p>
    </div>
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Core Topic &amp; Audience</h2>
    <div class="bg-white rounded-lg border border-slate-200 p-5 space-y-3">
      <div>
        <div class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-1">Definition</div>
        <p>{esc(m['core_topic']['definition'])}</p>
      </div>
      <div>
        <div class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-1">Audience</div>
        <p>{esc(m['core_topic']['audience'])}</p>
      </div>
    </div>
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">The Map</h2>
    {pillar_html}
    {clusters_html}
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Prioritized Action Plan</h2>
    <div class="grid md:grid-cols-3 gap-4">
      <div class="bg-red-50 border border-red-200 rounded-lg p-5">
        <h3 class="font-bold text-red-900 mb-3">Quick Wins (P1) — {len(m['action_plan']['quick_wins'])}</h3>
        <ol class="text-sm space-y-2 text-slate-700 list-decimal list-inside">{quick_wins_html}</ol>
      </div>
      <div class="bg-orange-50 border border-orange-200 rounded-lg p-5">
        <h3 class="font-bold text-orange-900 mb-3">Medium-Term (P2) — {len(m['action_plan']['medium_term'])}</h3>
        <ol class="text-sm space-y-2 text-slate-700 list-decimal list-inside">{medium_term_html}</ol>
      </div>
      <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-5">
        <h3 class="font-bold text-indigo-900 mb-3">Strategic (P3) — {len(m['action_plan']['strategic'])}</h3>
        <ol class="text-sm space-y-2 text-slate-700 list-decimal list-inside">{strategic_html}</ol>
      </div>
    </div>
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Internal Linking Recommendations</h2>
    <div class="bg-white rounded-lg border border-slate-200 p-5">
      <h3 class="font-semibold text-slate-900 mb-2">Rules</h3>
      <ul class="text-sm space-y-2 text-slate-700 list-disc list-inside mb-5">{linking_rules}</ul>
      <h3 class="font-semibold text-slate-900 mb-2">Specific Recommendations</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs text-slate-500 uppercase border-b border-slate-200">
            <tr>
              <th class="text-left py-2 pr-3">From</th>
              <th class="text-left py-2 pr-3">To</th>
              <th class="text-left py-2">Anchor Guidance</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">{linking_rows}</tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">LLM Citation &amp; AI Visibility Opportunities</h2>
    <div class="bg-violet-50 border border-violet-200 rounded-lg p-5">
      <p class="text-slate-700 mb-3">{high_llm} pages in this map carry <strong>high LLM citation potential</strong> — most likely to be quoted in ChatGPT, Perplexity, and Google AI Overview answers about WordPress galleries. Top candidates:</p>
      <ul class="text-sm space-y-2 text-slate-700 list-disc list-inside">{llm_list}</ul>
      <p class="text-sm text-slate-600 mt-4">Pair with structured data: <strong>HowTo</strong> schema on tutorial pages, <strong>FAQPage</strong> schema on the FAQ, <strong>Product</strong> schema on the FooGallery pillar, <strong>DefinedTerm</strong> on the definition page. AI Overview presence in the &quot;best wordpress gallery plugin&quot; SERP confirms this niche is actively being summarized by Google&apos;s AI — the listicle page is the highest-leverage citation target in the map.</p>
    </div>
  </section>

  <section class="mb-10">
    <h2 class="text-2xl font-bold text-slate-900 mb-4">Next Steps</h2>
    <ol class="space-y-2 text-slate-700 list-decimal list-inside">
      <li>Start with <strong>page-7</strong> (<code>/how-to-sell-photos-online/</code>) — biggest volume opportunity, already being ROI-tracked, momentum to maintain.</li>
      <li>Tackle <strong>page-1</strong> (gallery plugin comparison) and <strong>page-21</strong> (thumbnail hover effects) — both have massive impression counts but terrible CTR. Use the <code>seo-title-optimizer-v2</code> skill on both before doing content work.</li>
      <li>Build <strong>page-2 and page-3</strong> (vs Envira, vs NextGEN) — these intercept consideration traffic and have high LLM citation potential.</li>
      <li>Run <code>seo-change-roi-tracker</code> on every change made — this is exactly what that skill is for.</li>
      <li>Share your GA4 property ID and I&apos;ll regenerate the map with engagement-rate data layered in, which will likely promote a few P2s to P1 and demote any high-traffic-but-zero-engagement pages.</li>
      <li>Regenerate this map in 60–90 days as the SEO changes land and ranking data evolves.</li>
    </ol>
  </section>

  <footer class="text-xs text-slate-400 text-center pt-6 border-t border-slate-200">
    Generated by topical-authority-map-generator · Schema v{esc(m['schema_version'])} · {esc(m['meta']['generated_at'])}
  </footer>

</div>
</body>
</html>
'''

with open('/home/claude/foogallery-map/topical-authority-map-wordpress-image-galleries-2026-05-20.html', 'w') as f:
    f.write(html_doc)

print(f"Wrote HTML report ({len(html_doc):,} chars)")
print(f"Pages: {total_pages} (P1={p1_count}, P2={p2_count}, P3={p3_count})")
print(f"Status: expand={expand_count}, new={new_count}, exists={exists_count}")
print(f"High LLM citation potential: {high_llm}")
