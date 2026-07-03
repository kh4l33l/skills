#!/usr/bin/env python3
"""Read-only Cloudflare site audit helper.

Usage:
  python3 cloudflare_site_audit.py example.com --urls / /pricing --api

Requires: curl. Optional: dig/nslookup, openssl. Uses CLOUDFLARE_API_TOKEN or CF_API_TOKEN for API mode.
"""
import argparse, json, os, re, shutil, subprocess, sys, urllib.parse, urllib.request
from datetime import datetime, timezone


def sh(cmd, timeout=25):
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 999, "", str(e)


def curl_headers(url, ua=None, follow=True):
    cmd = ["curl", "-sS", "-I", "--connect-timeout", "10", "--max-time", "25"]
    if follow:
        cmd += ["-L", "--max-redirs", "5"]
    if ua:
        cmd += ["-A", ua]
    cmd.append(url)
    rc, out, err = sh(cmd)
    blocks = [b for b in re.split(r"\r?\n\r?\n", out) if b.strip()]
    final = blocks[-1] if blocks else out
    first = blocks[0] if blocks else out
    return {"cmd": " ".join(cmd), "rc": rc, "out": out, "err": err, "final": final, "first": first}


def curl_body(url, max_chars=5000):
    cmd = ["curl", "-sS", "-L", "--max-redirs", "5", "--connect-timeout", "10", "--max-time", "25", url]
    rc, out, err = sh(cmd)
    return {"cmd": " ".join(cmd), "rc": rc, "out": out[:max_chars], "err": err}


def status_code(header_text):
    m = re.findall(r"^HTTP/\S+\s+(\d+)", header_text, re.M)
    return int(m[-1]) if m else None


def header_value(header_text, name):
    m = re.findall(rf"^{re.escape(name)}:\s*(.*)$", header_text, re.I | re.M)
    return m[-1].strip() if m else ""


def dns(domain, rtype):
    if shutil.which("dig"):
        cmd = ["dig", "+short", rtype, domain]
    elif shutil.which("nslookup"):
        cmd = ["nslookup", "-type=" + rtype, domain]
    else:
        return {"cmd": "dig/nslookup missing", "rc": 127, "out": "", "err": "No DNS CLI found"}
    rc, out, err = sh(cmd)
    return {"cmd": " ".join(cmd), "rc": rc, "out": out, "err": err}


def api_get(path, token):
    url = "https://api.cloudflare.com/client/v4" + path
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "errors": [str(e)], "result": None}


def add(findings, severity, area, evidence, why, next_step):
    findings.append({"severity": severity, "area": area, "evidence": evidence, "why": why, "next": next_step})


def sev_rank(s):
    return {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}.get(s, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", help="Domain, e.g. example.com")
    ap.add_argument("--urls", nargs="*", default=["/"], help="Paths or full URLs to check")
    ap.add_argument("--api", action="store_true", help="Use Cloudflare API if token is available")
    ap.add_argument("--token", default=os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CF_API_TOKEN"))
    args = ap.parse_args()
    domain = args.domain.replace("https://", "").replace("http://", "").strip("/")
    findings, commands, unknowns, evidence = [], [], [], {}

    if not shutil.which("curl"):
        print("ERROR: curl is required", file=sys.stderr); sys.exit(2)

    ns = dns(domain, "NS"); commands.append(ns["cmd"]); evidence["nameservers"] = ns["out"]
    if "cloudflare" not in ns["out"].lower():
        unknowns.append("Nameservers do not clearly show Cloudflare; this may be partial/CNAME setup. Live headers/API are stronger evidence for proxy status.")

    a = dns(domain, "A"); commands.append(a["cmd"]); evidence["a_records"] = a["out"]
    www = dns("www." + domain, "CNAME"); commands.append(www["cmd"]); evidence["www_cname"] = www["out"]

    http = curl_headers(f"http://{domain}/", follow=False); commands.append(http["cmd"])
    https = curl_headers(f"https://{domain}/"); commands.append(https["cmd"])
    evidence["http_headers"] = http["first"][:1200]
    evidence["https_headers"] = https["final"][:1200]
    hstatus, sstatus = status_code(http["first"]), status_code(https["final"])
    location = header_value(http["first"], "location")
    server = header_value(https["final"], "server")
    cfray = header_value(https["final"], "cf-ray")
    cf_cache = header_value(https["final"], "cf-cache-status")

    if hstatus not in (301, 302, 307, 308) or (location and not location.lower().startswith("https://")):
        add(findings, "High", "HTTPS redirect", f"HTTP status {hstatus}, location={location or 'missing'}", "HTTP should normally redirect directly to HTTPS to protect users and canonical URLs.", "Enable Always Use HTTPS or a single HTTPS redirect after confirming all paths support HTTPS.")
    if not sstatus or sstatus >= 400:
        add(findings, "Critical", "Availability", f"HTTPS status {sstatus}; error={https['err']}", "The audited HTTPS homepage is not returning a healthy response.", "Fix origin/Cloudflare errors before tuning performance or SEO settings.")
    if "cloudflare" not in server.lower() and not cfray:
        add(findings, "Medium", "Cloudflare proxy", f"server={server or 'missing'}, cf-ray={cfray or 'missing'}", "Live response does not clearly show Cloudflare proxying.", "Verify apex/www DNS records are orange-cloud proxied in Cloudflare.")
    if not cf_cache:
        add(findings, "Low", "Cache observability", "cf-cache-status header missing on homepage", "Without cache headers, it is harder to verify CDN behavior from CLI.", "Check whether the hostname is proxied and whether response headers are stripped upstream.")

    robots = curl_body(f"https://{domain}/robots.txt"); commands.append(robots["cmd"])
    evidence["robots_head"] = robots["out"][:1000]
    if robots["rc"] != 0 or "<html" in robots["out"].lower()[:300]:
        add(findings, "Medium", "SEO crawlability", "robots.txt did not return plain text", "Search engines expect robots.txt to be accessible and parseable.", "Serve a valid robots.txt and include Sitemap directives where useful.")

    for ua_name, ua in {
        "Googlebot": "Googlebot/2.1 (+http://www.google.com/bot.html)",
        "Bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "Applebot": "Mozilla/5.0 Applebot/0.1",
    }.items():
        chk = curl_headers(f"https://{domain}/", ua); commands.append(chk["cmd"])
        code = status_code(chk["final"])
        evidence[f"{ua_name}_status"] = str(code)
        if not code or code >= 400:
            add(findings, "Critical", "SEO bots", f"{ua_name} received HTTP {code}", "Blocking major crawlers can damage organic visibility.", f"Review WAF/Bot/AI bot policies and allow verified {ua_name} traffic.")
        elif code in (403, 429, 503):
            add(findings, "Critical", "SEO bots", f"{ua_name} received HTTP {code}", "Challenge/block responses can stop crawling.", f"Allow verified {ua_name} and inspect Cloudflare security events.")

    for path in args.urls:
        url = path if path.startswith("http") else f"https://{domain}{path if path.startswith('/') else '/' + path}"
        chk = curl_headers(url); commands.append(chk["cmd"])
        code = status_code(chk["final"]); cache = header_value(chk["final"], "cf-cache-status")
        evidence[f"url_{path}"] = f"status={code}, cf-cache-status={cache or 'missing'}"
        if not code or code >= 500:
            add(findings, "High", "URL health", f"{url} returned {code}", "Important URLs should be reachable before optimizing Cloudflare settings.", "Fix origin/route errors for this URL.")

    api_notes = []
    if args.api:
        if not args.token:
            unknowns.append("Cloudflare API requested but no CLOUDFLARE_API_TOKEN/CF_API_TOKEN or --token was provided.")
        else:
            z = api_get("/zones?name=" + urllib.parse.quote(domain), args.token)
            if not z.get("success") or not z.get("result"):
                unknowns.append("Could not resolve Cloudflare zone via API; token may lack Zone:Read or domain differs.")
            else:
                zone = z["result"][0]; zid = zone["id"]
                api_notes.append(f"Zone: {zone.get('name')} ({zid}), status={zone.get('status')}, plan={zone.get('plan',{}).get('name')}")
                settings = api_get(f"/zones/{zid}/settings", args.token).get("result") or []
                smap = {s.get("id"): s.get("value") for s in settings if isinstance(s, dict)}
                for key in ["ssl", "always_use_https", "automatic_https_rewrites", "min_tls_version", "brotli", "browser_cache_ttl", "security_level", "http3", "early_hints"]:
                    if key in smap: api_notes.append(f"{key}: {smap[key]}")
                if smap.get("ssl") == "flexible":
                    add(findings, "High", "TLS", "Cloudflare SSL mode is flexible", "Flexible SSL encrypts visitor-to-Cloudflare only and can cause redirect/security issues.", "Install/verify an origin certificate and switch to Full (strict).")
                if smap.get("always_use_https") == "off":
                    add(findings, "Medium", "HTTPS", "Always Use HTTPS is off", "HTTP traffic may remain available or rely on origin redirects.", "Enable Always Use HTTPS if all paths support HTTPS.")
                if str(smap.get("min_tls_version", "1.2")) < "1.2":
                    add(findings, "High", "TLS", f"Minimum TLS version is {smap.get('min_tls_version')}", "TLS 1.0/1.1 are obsolete and weaken security posture.", "Set Minimum TLS Version to 1.2 or higher.")
                if smap.get("brotli") == "off":
                    add(findings, "Medium", "Performance", "Brotli is off", "Compression improves transfer size for text assets.", "Enable Brotli unless a known compatibility issue exists.")
                if smap.get("security_level") == "under_attack":
                    add(findings, "High", "Security Level", "Security Level / Under Attack mode is active", "Under Attack mode can challenge legitimate users and APIs; it should be temporary.", "Disable after the attack window or scope challenges with configuration rules.")

                dns_records = api_get(f"/zones/{zid}/dns_records?per_page=100", args.token).get("result") or []
                for r in dns_records:
                    if r.get("type") in ("A", "AAAA", "CNAME") and r.get("name") in (domain, "www." + domain) and r.get("proxied") is False:
                        add(findings, "High", "DNS proxy", f"{r.get('type')} {r.get('name')} is DNS-only", "Web traffic bypasses Cloudflare protections/cache and may expose origin IP.", "Proxy web-serving apex/www records unless a specific integration requires DNS-only.")
                rulesets = api_get(f"/zones/{zid}/rulesets", args.token).get("result") or []
                api_notes.append(f"Rulesets visible: {len(rulesets)}")
                bot = api_get(f"/zones/{zid}/bot_management", args.token)
                if bot.get("success"):
                    btxt = json.dumps(bot.get("result"), sort_keys=True)
                    api_notes.append("Bot management endpoint returned data")
                    if re.search(r"training.*block|block.*training", btxt, re.I):
                        add(findings, "High", "AI bot policies", "API bot data appears to mention Training + block", "Blocking Training can also block mixed-purpose Search+Training crawlers under Cloudflare's 2026 AI bot policy behavior.", "Dashboard: Security → Settings → Configure AI bot policies → Training = Allow (do not block), unless deliberately trading SEO reach for AI-training blocking.")
                    else:
                        unknowns.append("AI bot Training policy was not clearly exposed/recognized in API output; verify in dashboard.")
                else:
                    unknowns.append("Bot management / AI bot policy endpoint unavailable to this token/plan; verify in dashboard.")
    else:
        unknowns.append("Cloudflare account settings not checked. Run with --api and a read token to inspect SSL, DNS proxying, WAF/rulesets, and bot settings.")
        unknowns.append("Manually verify Security → Settings → Configure AI bot policies → Training = Allow (do not block) for SEO-critical sites.")

    if not findings:
        add(findings, "Low", "Overall", "No major issue detected from available unauthenticated checks", "This does not prove Cloudflare dashboard settings are safe.", "Run authenticated API audit and manually verify AI bot policies.")

    top = max(findings, key=lambda f: sev_rank(f["severity"]))
    overall = top["severity"]
    fastest = next((f for f in findings if f["severity"] in ("Critical", "High")), findings[0])

    print(f"# Cloudflare Site Audit: {domain}\n")
    print("## Executive summary")
    print(f"- Overall risk: {overall}")
    print(f"- Biggest issue: {top['area']} — {top['evidence']}")
    print(f"- Fastest win: {fastest['next']}")
    print(f"- Unknowns: {len(unknowns)} (see Raw notes / unknowns)\n")
    print("## Findings")
    print("| Severity | Area | Evidence | Why it matters | Next step |")
    print("|---|---|---|---|---|")
    for f in sorted(findings, key=lambda x: -sev_rank(x["severity"])):
        esc = lambda s: str(s).replace("|", "\\|").replace("\n", "<br>")[:500]
        print(f"| {f['severity']} | {esc(f['area'])} | {esc(f['evidence'])} | {esc(f['why'])} | {esc(f['next'])} |")
    print("\n## Easy next steps")
    for i, f in enumerate(sorted(findings, key=lambda x: -sev_rank(x["severity"]))[:5], 1):
        print(f"{i}. **{f['area']}**: {f['next']}")
    print("\n## API/account notes")
    if api_notes:
        for n in api_notes: print(f"- {n}")
    else:
        print("- No authenticated Cloudflare API data collected.")
    print("\n## Verification commands run")
    print("```bash")
    for c in commands: print(c)
    print("```")
    print("\n## Raw notes / unknowns")
    for u in unknowns: print(f"- {u}")
    print(f"- Audit timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("- Selected evidence:")
    for k, v in evidence.items():
        print(f"  - {k}: {str(v).replace(chr(10), ' / ')[:700]}")

if __name__ == "__main__":
    main()
