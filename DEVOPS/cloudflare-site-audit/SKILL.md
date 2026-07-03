---
name: cloudflare-site-audit
description: >
  Audit a Cloudflare-hosted website from the command line and produce an evidence-led report covering DNS/proxying,
  crawler access, HTTPS/TLS, caching, security posture, Cloudflare bot policies, and prioritized next steps.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [cloudflare, devops, audit, security, performance, seo, bot-management, cli]
---

# Cloudflare Site Audit

Use this skill when a user asks to audit a site behind Cloudflare, check Cloudflare hosting best practices, verify SEO crawler access, review Cloudflare security/performance posture, or produce a practical next-step report from CLI/API evidence.

The goal is not a generic best-practices essay. The goal is a short, actionable audit with proof, risk levels, and simple remediation steps.

## Default stance

- Treat this as **read-only** unless the user explicitly approves a specific Cloudflare change.
- Prefer command output and API responses over assumptions.
- If a setting cannot be verified by CLI/API, mark it as **Unknown from CLI** and give the exact dashboard path to check.
- Do not recommend risky global changes such as HSTS preload or “Cache Everything” without explaining rollout risks and exclusions.

## Inputs

Ask for or infer:

- Domain, for example `example.com`.
- Important paths to check, for example `/`, `/pricing`, `/blog/`, `/docs/`, `/checkout`.
- Whether authenticated Cloudflare API checks are allowed.
- If API checks are allowed, whether a safe read-only token is available.

If no paths are given, check `/` plus any obvious money or content paths the user provides later.

## Safe read-only Cloudflare token setup

Use a **custom API token**, not the global API key. Relevant Cloudflare docs:

- Create API token: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/
- API token permissions: https://developers.cloudflare.com/fundamentals/api/reference/permissions/

Dashboard setup:

1. Cloudflare dashboard → **My Profile → API Tokens → Create Token → Custom token**.
2. Name it clearly, for example `Read-only Cloudflare Site Audit - <domain>`.
3. Add **Read** permissions only:
   - `Zone → Zone → Read` — resolves the zone.
   - `Zone → Zone Settings → Read` — reads SSL, HTTPS, cache, TLS, and security-level settings.
   - `Zone → DNS → Read` — reads DNS records and proxied status.
   - `Zone → Bot Management → Read` — reads bot-management data where the plan/API exposes it.
   - `Zone → Zone WAF → Read`, `Zone → Account Rulesets → Read`, or `Account → Account Rulesets → Read` where available and relevant.
4. Zone resources: **Include → Specific zone → <domain>**. Avoid all-zone access unless intentionally auditing multiple zones.
5. Optional hardening:
   - Add an IP address filter if the audit host has a stable outbound IP.
   - Add a short expiration date for one-off audits.
6. Create the token, copy it once, and verify it:

```bash
# Store the token in an environment variable for the current shell only.
export CLOUDFLARE_API_TOKEN='paste-token-here'

# Verify it without printing the token.
curl -fsS -H "Authorization: Bearer <token-value-from-env>" \
  https://api.cloudflare.com/client/v4/user/tokens/verify | jq .
```

Expected: `"success": true` and token status `active`.

Safety rules:

- Never use `Edit`, `Write`, `Cache Purge`, `DNS Write`, `Workers Edit`, `API Tokens Edit`, or account-level write permissions for this audit.
- Do not paste tokens into chat, issue trackers, commits, logs, or reports.
- If a read permission is unavailable in the plan/UI, omit it and mark the related audit area as **Unknown from CLI**.

## Key Cloudflare bot-policy SEO risk

Cloudflare's AI bot policies classify AI-related crawlers by behavior:

- **Search**: crawlers that collect or index content to answer questions later.
- **Agent**: automated activity acting on a person's behalf.
- **Training**: crawlers taking content to train or fine-tune models, including mixed-purpose crawlers used for both Training and Search.

Cloudflare docs state that from **2026-09-15**, updated defaults for new domains block bots classified as Training or Agent on pages with ads, Search remains allowed, and mixed-purpose crawlers that combine Search and Training are blocked by configurations that block AI training, including the legacy “Block AI bots” option.

For SEO-critical sites, verify:

`Security → Settings → Configure AI bot policies → Training = Allow (do not block)`

Unless the site owner intentionally accepts the SEO trade-off of blocking mixed-purpose Search + Training crawlers.

Authoritative docs:

- https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/
- https://developers.cloudflare.com/bots/concepts/bot/

## Audit scope

### 1. Cloudflare presence and DNS proxying

Check:

- Nameservers and live response headers.
- `CF-RAY`, `Server: cloudflare`, and `cf-cache-status` response headers.
- A/AAAA/CNAME records for web-serving hostnames.
- Whether apex and `www` traffic are actually proxied.

Guidance:

- Web-serving A/AAAA/CNAME records should generally be proxied.
- Mail, TXT, verification, and non-web records should generally stay DNS-only.
- Do not rely on nameservers alone; partial/CNAME setups can still proxy through Cloudflare.

### 2. SEO crawler access

Check:

- `robots.txt` is reachable and parseable.
- Sitemap references are present where expected.
- Homepage and key URLs return healthy status codes for Googlebot, Bingbot, and Applebot user agents.
- Bot/WAF/AI policies do not challenge or block important crawlers.

Red flags:

- `403`, `429`, `503`, challenge pages, or captcha-like responses to major crawler user agents.
- AI Training policy set to block on an SEO-critical site without explicit business approval.
- Bot Fight Mode or WAF rules that create crawler false positives.

### 3. TLS and HTTPS

Check:

- HTTP redirects directly to HTTPS.
- SSL mode is not `Flexible`; prefer Full (strict) when origin certificates are valid.
- Always Use HTTPS is enabled where the whole site supports HTTPS.
- Minimum TLS version is at least 1.2.
- HSTS is enabled only after confirming HTTPS stability across required subdomains.

### 4. Caching and performance

Check:

- Static assets return cacheable headers and useful `cf-cache-status` after repeat requests.
- HTML cache behavior is intentional.
- Compression is enabled (`br`, `gzip`, or zstd where appropriate).
- Browser Cache TTL, Brotli, HTTP/3, and Early Hints where visible through API/settings.

For WordPress, ecommerce, dashboards, or logged-in apps, do **not** recommend global full-page caching unless bypasses are proven for admin, account, cart, checkout, login, preview, and cookie-specific paths.

### 5. Security posture

Check:

- Security Level is not left in Under Attack mode except during an active attack.
- WAF/rulesets exist and are not obviously overbroad.
- Response security headers are present where appropriate: `x-content-type-options`, `x-frame-options` or CSP frame policy, `referrer-policy`, and HSTS if safe.
- Cloudflare challenge behavior does not break APIs, forms, or crawler access.

### 6. Reliability and origin protection

Check:

- Origin IP exposure risk from DNS-only web records.
- Apex and `www` point to expected targets.
- No repeatable Cloudflare error pages or origin 5xx responses.
- Key URLs remain healthy after redirects.

## CLI helper workflow

If this skill includes `scripts/cloudflare_site_audit.py`, use it first:

```bash
python3 scripts/cloudflare_site_audit.py example.com --urls / /pricing /blog/
```

With authenticated API checks:

```bash
export CLOUDFLARE_API_TOKEN='paste-token-here'
python3 scripts/cloudflare_site_audit.py example.com --api --urls / /pricing /blog/
```

Required tools: `python3`, `curl`.

Useful extras: `dig` or `nslookup`, `openssl`, `jq`.

## Manual command checklist

```bash
DOMAIN=example.com

# DNS / proxy indicators
dig +short NS "$DOMAIN"
dig +short A "$DOMAIN"
dig +short CNAME "www.$DOMAIN"

# Redirects and live headers
curl -I --max-time 25 "http://$DOMAIN/"
curl -I -L --max-redirs 5 --max-time 25 "https://$DOMAIN/"

# SEO crawler access
curl -sS "https://$DOMAIN/robots.txt" | sed -n '1,80p'
curl -I -A 'Googlebot/2.1 (+http://www.google.com/bot.html)' "https://$DOMAIN/"
curl -I -A 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)' "https://$DOMAIN/"
curl -I -A 'Mozilla/5.0 Applebot/0.1' "https://$DOMAIN/"

# TLS certificate sanity
openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" -tls1_2 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

Authenticated Cloudflare API checks:

```bash
API=https://api.cloudflare.com/client/v4
# Set TOKEN from your read-only token environment variable without printing it.
TOKEN='<token-value-from-env>'
ZONE_ID=$(curl -fsS -H "Authorization: Bearer <token-value-from-env>" "$API/zones?name=$DOMAIN" | jq -r '.result[0].id')

curl -fsS -H "Authorization: Bearer <token-value-from-env>" "$API/zones/$ZONE_ID/settings" \
  | jq '.result[] | {id,value,editable}'

curl -fsS -H "Authorization: Bearer <token-value-from-env>" "$API/zones/$ZONE_ID/dns_records?per_page=100" \
  | jq '.result[] | {type,name,content,proxied}'

curl -fsS -H "Authorization: Bearer <token-value-from-env>" "$API/zones/$ZONE_ID/rulesets" \
  | jq '.result[] | {name,kind,phase,enabled}'

curl -fsS -H "Authorization: Bearer <token-value-from-env>" "$API/zones/$ZONE_ID/bot_management" | jq .
```

If an endpoint is unavailable for the token or plan, do not treat it as safe or unsafe. Mark it as **Unknown from CLI** and give the dashboard path.

## Severity scoring

Use these labels consistently:

- **Critical**: site unavailable, HTTPS broken, major crawlers blocked, likely deindexing/crawl failure, or exposed origin with active exploit risk.
- **High**: AI Training/mixed-purpose crawlers blocked on an SEO-critical site, Flexible SSL, Under Attack mode left on, key web records DNS-only, or cache rules that may cache private/cart/account pages.
- **Medium**: missing safe HTTPS redirects, weak cache/compression setup, missing security headers, poor robots/sitemap hygiene, or unknown account settings that should be verified.
- **Low**: documentation, observability, cleanup, and non-urgent hardening.

## Report format

Return Markdown in this shape:

```markdown
# Cloudflare Site Audit: <domain>

## Executive summary
- Overall risk: Critical/High/Medium/Low
- Biggest issue: ...
- Fastest win: ...
- Unknowns: ...

## Findings
| Severity | Area | Evidence | Why it matters | Next step |
|---|---|---|---|---|
| High | SEO bots | ... | ... | ... |

## Easy next steps
1. ...
2. ...
3. ...

## Verification commands run
```bash
...
```

## Raw notes / unknowns
- ...
```

Keep recommendations concrete. Prefer steps like “Dashboard → Security → Settings → Configure AI bot policies → Training = Allow (do not block)” over vague advice.

## Verification checklist

Before finalizing the audit, verify:

- [ ] The domain and checked paths are listed.
- [ ] Every major finding has evidence from command/API output or is clearly labeled as unknown.
- [ ] No Cloudflare token or secret appears in the report.
- [ ] Bot-policy SEO risk is checked or explicitly marked as unknown.
- [ ] Next steps are ordered by risk and ease.

## Pitfalls

- Do not assume `Server: cloudflare` means every hostname is proxied; check DNS/API records.
- Do not assume non-Cloudflare nameservers means no Cloudflare proxy; partial/CNAME setups exist.
- Do not recommend HSTS preload casually; it can lock users out if HTTPS is not stable everywhere.
- Do not recommend “Cache Everything” globally for WordPress, ecommerce, dashboards, or logged-in apps without proven bypass rules.
- Do not mutate Cloudflare configuration without explicit approval.
- Prefer Cloudflare docs Markdown (`index.md`) over scraping docs HTML when researching current behavior.
