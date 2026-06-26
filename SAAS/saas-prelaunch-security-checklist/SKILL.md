---
name: saas-prelaunch-security-checklist
description: "Use before launching, dogfooding, beta-testing, or onboarding real users to an AI-built or conventional SaaS app; produces a practical security/privacy readiness gate for SaaS pre-launch."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [saas, security, prelaunch, privacy, compliance, ai-built-apps, owasp, checklist]
    created_by: agent
---

# SaaS Pre-launch Security Checklist

Use this skill whenever Brad asks to launch, dogfood, beta test, onboard users, expose a SaaS app publicly, or review an AI-built app before real-user usage.

The goal is not enterprise compliance theater. The goal is to prevent obvious legal/security failures before real customer data, API spend, or FooPlugins reputation is at risk.

## Default stance

- Treat any app with real users, auth, payments, analytics, uploaded content, or customer data as security-sensitive.
- Prefer a lightweight launch gate over a long audit.
- Do not approve production launch if critical items are unknown or unverified.
- For FooPlugins/AgentArmy projects, protect customer trust, data, billing/API costs, and Brad's focus.

## Output format

Return a concise readiness report:

```markdown
## SaaS pre-launch security gate
Status: PASS / PASS WITH CONDITIONS / BLOCKED

### Critical blockers
- ...

### Required before real users
- ...

### Recommended soon after launch
- ...

### Evidence checked
- ...

### Unknowns / assumptions
- ...
```

Use `BLOCKED` if privacy/data handling, auth isolation, secrets exposure, server-side validation, or rate limits are materially unknown for an app touching real users.

## Checklist

### 1. Legal/privacy baseline

Verify:

- A privacy policy exists and matches actual data collection.
- Terms of service exist if users create accounts, upload content, pay, or rely on outputs.
- The app owner knows where user data lives: database, auth provider, logs, analytics, email tools, AI providers, object storage, backups.
- Data retention/deletion expectations are clear enough for beta users.
- GDPR/CCPA exposure is considered if collecting personal data from EU/California users.

Minimum acceptable pre-beta answer:

- What personal data is collected?
- Where is it stored?
- Which third parties receive it?
- How can a user request deletion/export?

### 2. Authentication and authorization

Verify failure paths, not just happy paths:

- Wrong password repeatedly.
- Password reset for nonexistent email.
- Verification link clicked twice.
- Signup with existing email.
- Expired/invalid session token.
- Logged-out user attempts protected routes/API calls.
- User A attempts to access User B's records by changing IDs.
- Role changes, org membership, team switching, or tenant switching behave correctly.

For WorkOS-style auth:

- Callback URLs are restricted.
- Session validation happens server-side.
- Organization/tenant membership is checked for every tenant-scoped action.

### 3. Row-level/tenant data isolation

For Supabase/Postgres:

- Row Level Security is enabled on tenant/user-scoped tables.
- Policies exist for select/insert/update/delete.
- Anonymous and authenticated roles cannot read unrelated rows.

For Convex/serverless backends:

- Every query/mutation/action validates identity and tenant/org access server-side.
- Client-provided IDs are treated as untrusted.
- List endpoints are scoped by authenticated user/org.

Manual test:

- Create two users/orgs.
- Capture one valid request.
- Change user/org/resource IDs.
- Confirm cross-tenant reads/writes fail.

### 4. Server-side validation

Client-side validation is only UX. Verify server-side validation for:

- Form inputs.
- API route body/query/path params.
- File uploads.
- Webhooks.
- AI prompt inputs if they affect cost, data access, or downstream actions.
- Payment/subscription changes.

Reject malformed input safely. Do not rely on hidden fields, disabled buttons, frontend route guards, or TypeScript types alone.

### 5. Secrets and sensitive data exposure

Check for leaks in:

- Frontend bundles and public env vars.
- API responses returning excessive fields.
- Logs containing tokens, API keys, cookies, OAuth codes, PII, prompts with customer data, or payment details.
- Error tracking tools.
- Build output and source maps.
- Git history if the project has moved fast with AI assistance.

Rules:

- Browser-visible API keys are public. Move real secrets server-side or proxy through controlled endpoints.
- `.env` values must not be exposed through frontend config unless intentionally public.
- Never log raw secrets or full auth/session payloads.

Useful prompts for a coding agent:

```text
Review this app for credential or sensitive data leaks in frontend code, API routes, server actions, logs, source maps, and build output. List exact files/routes and required fixes.
```

### 6. OWASP/security baseline

Run a pragmatic OWASP-style review focused on:

- Broken access control.
- Injection: SQL/NoSQL/command/template injection.
- XSS and unsafe HTML rendering.
- CSRF where cookie-based auth is used.
- SSRF if fetching user-supplied URLs.
- Insecure direct object references.
- Insecure file upload and content-type handling.
- Dependency vulnerabilities.
- Open redirects.
- Misconfigured CORS.

Useful prompts for a coding agent:

```text
Review this app against OWASP Top 10 risks. Prioritize exploitable issues before theoretical concerns. Return blockers, exact locations, and minimal fixes.
```

### 7. Security headers and browser posture

Verify reasonable defaults:

- HTTPS only in production.
- `Strict-Transport-Security` if the domain is stable.
- `Content-Security-Policy` or at least a plan for it.
- `X-Frame-Options` or `frame-ancestors`.
- `X-Content-Type-Options: nosniff`.
- `Referrer-Policy`.
- Secure, HttpOnly, SameSite cookies where applicable.

Useful prompt:

```text
Review my app as a security specialist and check security headers, cookie flags, CORS, and baseline browser security posture. Give deploy-blocking issues first.
```

### 8. Rate limits, abuse controls, and cost protection

Required before public/beta use if endpoints hit paid resources:

- Rate limits on auth, public forms, AI calls, email sends, scraping, file uploads, and paid API calls.
- Per-user/org quota controls where relevant.
- Server-side enforcement, not frontend-only throttling.
- Clear behavior when limits are hit.
- Alerts or visibility for abnormal usage/cost spikes.

For AI-heavy apps:

- Cap tokens/requests per user/org/day.
- Avoid unbounded loops/retries.
- Log enough metadata to investigate abuse without storing sensitive prompts unnecessarily.

### 9. Bot and public-form protection

For public forms/endpoints:

- Add Cloudflare Turnstile or equivalent CAPTCHA where appropriate.
- Lock CORS to intended domains.
- Validate origin/referer when useful, but do not treat it as sole security.
- Add spam/abuse handling for contact forms, signup, trial creation, newsletter, waitlist, and webhooks.

### 10. Error handling and observability

Verify:

- User-facing errors are generic and safe.
- Server logs contain enough detail for debugging without leaking secrets/PII.
- Expected failure paths are monitored.
- Alerting exists for auth failures, webhook failures, payment failures, API quota spikes, and 5xx errors where relevant.

Bad:

- `SELECT * FROM users failed: ...` shown to users.
- Raw stack traces exposed in production.
- Full request bodies with secrets stored in logs.

Good:

- Generic user error.
- Structured server-side log with request ID, route, user/org ID where safe, and sanitized error.

### 11. Dependency and supply-chain sanity

Before launch:

- Run the package manager's audit command where practical.
- Remove unused experimental packages.
- Check obvious abandoned/high-risk dependencies.
- Ensure lockfiles are committed.
- Confirm CI/test/build runs from a clean checkout.

For WordPress/plugin-adjacent SaaS integrations:

- Validate webhook signatures.
- Treat WordPress-originated payloads as untrusted.
- Avoid storing unnecessary WordPress admin credentials or tokens.

## Recommended tool workflow

When reviewing an actual repo:

1. Inspect stack and entry points.
2. Run tests/build/lint if available.
3. Search for secrets and frontend env exposure.
4. Review auth/session/tenant access checks.
5. Review API routes/server actions/functions.
6. Test or reason through failure paths.
7. Check headers/CORS/rate-limit configuration.
8. Produce PASS / PASS WITH CONDITIONS / BLOCKED with exact fixes.

If implementation is needed, use `systematic-debugging` for bugs and `test-driven-development` for fixes that can be tested.

## Severity guide

### Block launch

- Cross-tenant/user data access possible or unverified.
- Secrets/API keys exposed to frontend or logs.
- No server-side authorization on protected data/actions.
- No privacy/data handling story for real user data.
- No rate limits on paid/abusable endpoints.
- Raw errors/stack traces exposed in production.

### Required before broader rollout

- Weak CSP/security headers.
- Missing abuse alerts.
- Incomplete failure-path tests.
- Dependency audit not run.
- Data retention/deletion unclear.

### Can usually wait briefly

- Polished policy wording.
- Full formal threat model.
- Advanced anomaly detection.
- Perfect CSP if a pragmatic baseline exists and no obvious XSS surface is present.

## Notes for Brad/FooPlugins projects

For AgentArmy or other SaaS side projects, the minimum pre-dogfood gate is:

- Privacy/data map.
- WorkOS/auth failure-path checks.
- Tenant isolation checks.
- Server-side validation.
- Secrets/log review.
- Rate limits on AI/API endpoints.
- CORS/security headers baseline.
- Generic production errors.

Keep it lightweight, but do not skip it. Shipping fast is fine; shipping naked is not.
