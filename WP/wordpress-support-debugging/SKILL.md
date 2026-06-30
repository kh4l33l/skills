---
name: wordpress-support-debugging
description: Evidence-led workflow for debugging WordPress plugin support issues. Use when a user asks an agent to reproduce a WordPress support ticket, choose a local or cloud WordPress runtime, collect proof, test a fix or workaround, prepare a pull request or snippet, and draft a support reply.
---

# WordPress Support Issue Debugging

This skill helps an agent turn a WordPress plugin support ticket into **evidence + next action**.

Use it when the user asks to:

- investigate or reproduce a WordPress support issue;
- choose between local WordPress debugging tools;
- install plugins/themes/content into a test site;
- test a plugin code change or compatibility workaround;
- decide whether a fix deserves a pull request;
- draft a copy/paste support ticket response.

## Outcome

The agent should produce:

1. A justified tool/runtime choice.
2. A reproducible or clearly blocked reproduction attempt.
3. Evidence: logs, screenshots, WP-CLI output, DOM/console/network observations, or database checks.
4. A likely root cause.
5. A tested fix, workaround, pull request, or snippet recommendation.
6. A concise draft support reply.
7. Cleanup status for any local/cloud test sites created.

## Tool selection policy

Choose the lightest tool that can answer the question, but escalate when fidelity or sharing matters.

Before running tools, write a short decision note:

```text
Repro tool: Cove
Reason: needs MariaDB + PHP logs + editable plugin working copy.
Escalation: InstaWP if local repro fails or a shareable URL is needed.
```

### Use Cove as the default local repro environment

Use **Cove** first when the issue needs a normal local WordPress stack:

- database behavior matters;
- plugin compatibility is unclear;
- PHP errors/logs are needed;
- email/form behavior matters;
- HTTPS, callbacks, redirects, mixed content, or admin URLs matter;
- plugin code needs to be mounted, edited, and re-tested locally;
- the issue should be reproducible through browser automation and WP-CLI.

Cove is useful because it provides Caddy, FrankenPHP, MariaDB, Mailpit, WP-CLI, local HTTPS, logs, and one-time admin login without Docker.

Typical commands:

```bash
cove add <issue-slug>
cove login <issue-slug>
cove path <issue-slug>
cove url <issue-slug>
cove db list
cove log <issue-slug>
cove log <issue-slug> -f
cove db backup
cove delete <issue-slug> --force
```

Use deterministic site names, e.g. `plugin-12345`, `gallery-polylang`, `form-email-debug`.

If the environment has an automated cleanup registry, register every local support-debugging site immediately after creation with the tool, site name, path, creation timestamp, ticket URL, and notes. Cleanup should only delete explicitly registered support sites, never guessed project directories.

### Use WP Playground CLI for fast smoke tests

Use **WP Playground CLI** when:

- a quick clean install is enough;
- the issue is likely frontend/admin rendering;
- SQLite/WASM differences are acceptable;
- a Blueprint can capture the setup;
- the task is a cheap first pass before a higher-fidelity local or cloud repro.

Typical commands:

```bash
npx @wp-playground/cli@latest start --skip-browser
npx @wp-playground/cli@latest start --wp=6.8 --php=8.3 --skip-browser
npx @wp-playground/cli@latest server --mount=.:/wordpress/wp-content/plugins/<plugin-slug>
npx @wp-playground/cli@latest server --blueprint=./blueprint.json
```

Do **not** close an issue as unreproducible based only on Playground. SQLite/WASM can differ materially from normal WordPress hosting.

### Use InstaWP CLI for cloud/fidelity escalation

Use **InstaWP CLI** when:

- local tools cannot reproduce but the report looks credible;
- a shareable repro is needed;
- cloud hosting behavior, remote logs, or a more production-like setup matters;
- a support/customer/stakeholder needs to inspect the site;
- plugin install/update flows need realistic testing;
- snapshots/rollback are useful before risky steps.

Typical commands:

```bash
instawp create --name <issue-slug> --php 8.3 --json
instawp plugin install <site> ./my-plugin.zip --activate
instawp plugin install <site> ./my-plugin/ --activate
instawp wp <site> plugin list --api
instawp wp <site> option get siteurl --api
instawp sql <site> "SELECT option_value FROM wp_options WHERE option_name='siteurl'"
instawp logs <site> --php --nginx --lines 200
instawp versions create <site> --name "before-debug"
instawp sites delete <site> --force
```

Never create paid or long-lived resources without permission. Report created site IDs/URLs and cleanup status.

### Use WP Codebox for agent-safe artifact experiments

Use **WP Codebox** when available and the task benefits from a disposable agent/runtime boundary:

- risky or untrusted patches;
- recipe-based repros;
- artifact bundles, diffs, screenshots, logs, or replay packages;
- parallel/fanout experiments;
- browser assertions, performance observations, or query diagnostics.

Treat WP Codebox as optional unless it is already installed and verified. If unavailable, do not block the investigation; use Cove or InstaWP.

### Use Studio CLI only when specifically helpful

Use **Studio CLI** when the user wants Studio-managed sites, WordPress.com/Pressable sync, or Studio preview sites. It is not the default for automated support debugging.

## Debugging workflow

### 1. Capture the ticket facts

Extract and record:

- ticket URL/source;
- plugin/product and version if known;
- WordPress, PHP, browser, theme, and conflicting plugins if reported;
- exact symptoms;
- expected vs actual result;
- reproduction steps;
- screenshots/logs/errors;
- urgency or user impact;
- what is unknown.

Separate **user-reported facts** from **verified evidence**.

### 2. Set up an isolated WordPress

Use a unique site/workdir. Avoid contaminating existing project/customer sites.

Install only the minimum plugins/themes/content needed to reproduce. Add complexity one variable at a time.

For code work:

- use a clean Git branch;
- make the smallest safe patch;
- run relevant tests/lints/builds where available;
- never deploy, tag, publish, or release without explicit approval.

### 3. Reproduce with evidence

Collect at least one of:

- browser screenshot/snapshot;
- console/network errors;
- PHP/debug log excerpt;
- WP-CLI command output;
- database observation;
- before/after rendered HTML or DOM;
- exact minimal reproduction steps.

If reproduction fails, document exactly what was tried and why the result is inconclusive.

### 4. Diagnose root cause

Prefer evidence over assumptions:

- inspect plugin code paths involved;
- inspect hooks, filters, templates, assets, and REST/AJAX endpoints;
- compare active plugin/theme state;
- test with a default theme if a theme conflict is suspected;
- deactivate unrelated plugins where safe;
- check JavaScript event binding and final DOM for frontend issues;
- check PHP logs for warnings/fatals;
- check database/options/meta when state is involved.

For compatibility issues, prove whether the plugin is at fault, third-party behavior changed, or the user's setup needs configuration.

### 5. Test possible fixes/workarounds

Choose the smallest effective fix:

- **Core plugin fix** when many users can hit it, it is not site-specific, and it improves robustness without breaking backward compatibility.
- **`functions.php` / Code Snippets workaround** when it is site-specific, temporary, risky for core, or depends on a third-party plugin/theme behavior.
- **Support/configuration reply** when the behavior is expected or caused by setup.
- **Needs more info** when key environment/repro facts are missing.

Always test the fix/workaround in the repro environment before recommending it, unless blocked. Label untested snippets clearly.

### 6. Create a pull request if worthwhile

When a plugin code change is justified:

1. Work in a branch.
2. Make the minimal patch.
3. Run relevant tests/lints/builds if available.
4. Re-run the repro to verify.
5. Open a pull request only if the change is useful, safe, and scoped.
6. Keep the PR body public-safe: no private customer details, credentials, local paths, or irrelevant internal context.
7. Include reproduction evidence, fix summary, test results, and risk notes.

### 7. Prepare a snippet when a PR is not appropriate

If a snippet is the right answer, provide:

- filename suggestion, e.g. `plugin-compatibility-workaround.php`;
- code block suitable for `functions.php` or the Code Snippets plugin;
- activation/removal notes;
- compatibility/risk notes;
- tested environment and limitations.

Keep snippets narrowly scoped, repeat-safe, and defensive. Avoid exposing private paths, tokens, internal URLs, or customer data.

### 8. Draft the support reply

The reply should be copy/paste-ready:

- acknowledge the issue;
- state what was reproduced or what is still missing;
- provide clear steps, workaround, or fix status;
- ask for specific missing info if needed;
- avoid overpromising release timelines;
- do not mention private/internal tooling unless useful;
- do not blame the customer or third-party plugin unnecessarily.

## Output format

```markdown
## Support debugging result: <short title>

### Classification
- Confirmed bug | Likely bug not reproduced | Compatibility issue | Configuration/support | Needs more info | Feature request | Duplicate/known issue

### Tool choice
- Used: <Cove / Playground CLI / InstaWP / WP Codebox / Studio>
- Reason:
- Escalation needed: yes/no

### Evidence
- Reproduction status:
- Environment:
- Key logs/screenshots/commands:
- What could not be verified:

### Root cause / likely cause
<concise explanation with evidence>

### Recommended action
- PR: <yes/no + link if created>
- Snippet/workaround: <yes/no + code if applicable>
- Support-only reply: <yes/no>

### Tested fix/workaround
<what changed and how it was verified>

### Draft ticket reply
<copy/paste response>

### Cleanup
- Local/cloud sites created:
- Cleanup status:
```

## Classification guide

- **Confirmed bug:** reproduced and evidence points to plugin code defect.
- **Likely bug but not reproduced:** credible report/code inspection suggests bug, but environment or data is missing.
- **Compatibility issue:** interaction with another plugin/theme/service; provide workaround or hardening path.
- **Configuration/support:** expected behavior or incorrect setup; give steps.
- **Needs more info:** exact steps/environment/data unavailable.
- **Feature request:** product does not currently support requested behavior.
- **Duplicate/known issue:** link to known issue/PR if public-safe.

## Verification checklist

Before finalizing:

- [ ] Tool choice is stated and justified.
- [ ] Repro environment is isolated and named.
- [ ] Evidence is attached or quoted.
- [ ] User-reported facts are separated from verified facts.
- [ ] Fix/workaround was tested, or limitations are stated.
- [ ] PR/snippet recommendation is scoped and safe.
- [ ] Draft support reply is copy/paste-ready.
- [ ] Local/cloud cleanup status is reported.

## Pitfalls

- Do not rely only on Playground for final conclusions when DB/runtime fidelity matters.
- Do not leave cloud resources running without reporting cleanup.
- Do not mutate production/customer sites.
- Do not publish plugin releases without explicit approval.
- Do not create broad snippets that affect unrelated pages/components.
- Do not claim a PR fixes the customer issue until the repro has been re-run successfully or the limitation is disclosed.
- Do not post replies automatically unless explicitly instructed; draft replies for review by default.
