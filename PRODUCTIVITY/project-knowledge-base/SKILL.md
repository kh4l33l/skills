---
name: project-knowledge-base
description: >
  Maintain an OKF-inspired, Markdown-first project knowledge base that acts as a durable second brain for humans and agents. Use when creating, auditing, updating, summarizing, or operationalizing project folders; keeping portfolio indexes current; turning loose notes into durable project context; or running scheduled maintenance/standup routines over a project documentation tree.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Project Knowledge Base

## Overview

This skill defines a generic, OKF-inspired documentation system for project portfolios.

It is designed for a root folder such as:

```text
~/projects
```

or any equivalent workspace-specific project directory.

It borrows the useful parts of Open Knowledge Foundation / knowledge-catalog style organization:

- Markdown-first knowledge bundles.
- YAML frontmatter for machine-readable metadata.
- `index.md` for orientation and navigation.
- `log.md` for chronological history.
- Cross-links between related docs.
- Diffable, agent-readable project state.

It adds operating metadata agents need to make decisions:

- Project status.
- Priority.
- Owner.
- Business, customer, operational, or strategic impact.
- Stage.
- Next action.
- Review cadence.
- Blockers and decisions needed.

The goal is not beautiful documentation. The goal is **fast operational clarity**: what exists, why it matters, what state it is in, what the next action is, and whether it deserves attention.

## Why This Works As A Second Brain

A project knowledge base works well as a second brain for agents because it gives them a stable, inspectable memory layer outside any single chat session.

Good agents need durable context. Chat history is fragmented, hard to search reliably, and full of transient discussion. A Markdown project tree gives every agent a shared working memory with clear rules:

- **State is explicit.** Status, priority, owner, next action, blockers, and review dates are readable without reconstructing old conversations.
- **Knowledge is durable.** Decisions, rationale, links, research, specs, and context survive model resets and handoffs.
- **It is diffable.** Git history shows exactly what changed, when, and why.
- **It is tool-agnostic.** Any agent, editor, script, or human can read and update Markdown.
- **It supports portfolio-level judgment.** Consistent metadata lets agents summarize all active, parked, idea, and archived work.
- **It lowers coordination cost.** Specialist agents can pick up a task from the docs, write back evidence, and leave the portfolio in a better state.
- **It creates continuity.** The next agent does not need to ask “where were we?” if the project has a current `index.md`, `status.md`, and `log.md`.

The system is intentionally lightweight. Small ideas stay one-page. Major projects can grow into structured knowledge bases. This prevents documentation from becoming a tax while still preserving the context that matters.

## Self-Maintaining And Self-Improving Model

This system is self-maintaining when agents treat the project tree as both input and output:

1. **Read before acting.** Agents inspect project docs before making claims or starting work.
2. **Write back durable changes.** After meaningful progress, agents update status, decisions, links, logs, task docs, and indexes.
3. **Use metadata for audits.** Scheduled jobs can detect stale `last_reviewed` dates, missing next actions, broken links, empty placeholders, and active projects without owners.
4. **Queue unknowns instead of guessing.** If an agent cannot confidently infer a repo, owner, status, or decision, it writes the question to `unknowns.md` or a project `## Open questions` section.
5. **Prune low-value structure.** Empty templates and placeholder docs are deleted or merged into `index.md`.
6. **Improve the system from usage.** When repeated friction appears, agents update this skill, templates, or operating docs so future agents do better.
7. **Commit changes.** Git turns the knowledge base into an auditable operating system rather than a loose note folder.

The flywheel is:

```text
Project docs -> agent work -> verified evidence -> durable doc update -> portfolio audit -> better next action
```

## When To Use

Use this skill when the user asks to:

- Create a new project folder.
- Normalize or audit an existing project folder.
- Manage a project documentation root as the source of truth.
- Summarize active, parked, idea, or archived projects.
- Add or update project status, context, roadmap, decisions, logs, tasks, research, links, or references.
- Convert loose notes into project documentation.
- Decide whether a small idea needs a tiny project record or a larger knowledge base.
- Build or refresh a project index or portfolio overview.
- Audit stale projects and recommend park, kill, advance, or clarify decisions.
- Run recurring project maintenance or standup jobs.

Do **not** use this for:

- Source-code repository conventions unless the repo is also being documented in the project knowledge base.
- Long-form research synthesis only; do the research first, then save durable findings into this format.
- Temporary task lists that will go stale within days unless they affect a real project status, decision, or handoff.

## Operating Principles

1. **The project root is the source of truth.** If a project matters, it should have at least one folder and a useful `index.md`.
2. **No placeholder files.** Do not create or keep files that only store structure, empty templates, generic cadence text, or boilerplate.
3. **Small projects stay small.** Do not create a large documentation tree for a half-formed idea.
4. **Large projects get structure.** If a project has multiple owners, repos, decisions, research, roadmaps, or recurring work, split docs into focused files.
5. **Every active project must have a next action.** If there is no next action, the project is parked, archived, or not yet real.
6. **Documentation must not become procrastination.** Prefer a useful 70% project record over a perfect taxonomy.
7. **Use metadata for agent parsing.** YAML frontmatter should be consistent enough that agents can inventory projects quickly.
8. **Separate durable knowledge from transient chatter.** Stable decisions, links, context, and status belong in project docs. Daily noise does not.
9. **Label assumptions.** If state is inferred from files, say so.
10. **Optimize for handoff.** A new agent should be able to read the project folder and know what to do next.

## Root Layout

Recommended root structure:

```text
projects/
  index.md
  log.md
  unknowns.md
  unlinked.md

  active/
    index.md
    <project-slug>/

  parked/
    index.md
    <project-slug>/

  ideas/
    index.md
    <project-slug>/

  archived/
    index.md
    <project-slug>/

  shared/
    index.md
```

### Bucket Meanings

| Bucket | Meaning | Attention rule |
|---|---|---|
| `active/` | Real projects with current work or decisions needed | Must have next action and last review date |
| `parked/` | Worth keeping, not currently being worked | Must state why parked and what would reactivate it |
| `ideas/` | Early concepts, sketches, opportunities | Keep lightweight; avoid premature planning |
| `archived/` | Done, dead, or no longer relevant | Preserve only useful history |
| `shared/` | Cross-project references, templates, operating docs | Keep generic and reusable |

## Project Size Tiers

### Tier 1 — Tiny Idea / Micro Project

Use for quick concepts, one-off tools, or early opportunities with little current commitment.

```text
projects/ideas/<project-slug>/
  index.md
```

`index.md` should include only useful known information:

- What it is.
- Why it might matter.
- Status.
- Next action, reactivation condition, or kill condition if known.
- Links, if any.

### Tier 2 — Normal Project

Use for most active initiatives. Start with `index.md`; add sibling files only when the content is substantial enough to justify separation.

```text
projects/active/<project-slug>/
  index.md
  status.md       # optional: only if status has real operational detail
  context.md      # optional: only if background/constraints are substantial
  decisions.md    # optional: only if durable decisions exist
  links.md        # optional: only if real links exist
  log.md          # optional: only if there are durable chronological updates
  tasks/          # optional: only if meaningful task docs exist
```

### Tier 3 — Major Project / Knowledge Base

Use for major products, complex initiatives, or projects with research, multiple workstreams, or many docs.

```text
projects/active/<project-slug>/
  index.md
  status.md
  context.md
  roadmap.md
  decisions.md
  log.md
  links.md

  tasks/
    index.md
    <task-slug>.md

  research/
    index.md
    <research-slug>.md

  specs/
    index.md
    <spec-slug>.md

  references/
    index.md
    <reference-slug>.md

  assets/
```

Do not create every directory by default. Add sections as the project earns them.

## Naming Conventions

- Folders: lowercase slugs, hyphenated where useful.
- Files: lowercase Markdown names, e.g. `status.md`, `decisions.md`, `customer-research.md`.
- Prefer `index.md` over `README.md` for navigation.
- Prefer `log.md` for chronological updates.
- Avoid spaces and date prefixes except for dated research snapshots or reports.

## Standard Frontmatter

Every major project doc should start with YAML frontmatter.

Base fields:

```yaml
---
okf_version: "0.1"
type: Project
title: Project Name
description: One-line description.
resource: null
tags: [tag-one, tag-two]
timestamp: 2026-06-20T09:00:00+00:00
---
```

Operating fields:

```yaml
project: project-slug
status: active | parked | idea | archived
priority: P0 | P1 | P2 | P3 | P4
owner: Owner Name
impact: direct | indirect | none | unknown
stage: idea | validation | planning | build | launched | maintenance | parked | archived
last_reviewed: 2026-06-20
next_review: 2026-06-27
```

### Status Meanings

| Status | Meaning |
|---|---|
| `active` | Current attention or execution |
| `parked` | Intentionally paused; may resume later |
| `idea` | Captured concept, not committed |
| `archived` | Done, dead, or no longer operational |

### Priority Meanings

| Priority | Meaning |
|---|---|
| `P0` | Critical to revenue, customer trust, operations, or delivery now |
| `P1` | Important and near-term |
| `P2` | Useful but not urgent |
| `P3` | Low priority / optional |
| `P4` | Keep only as reference or maybe someday |

### Impact Meanings

| Value | Meaning |
|---|---|
| `direct` | Directly affects revenue, users, customers, delivery, support, operations, or strategic goals |
| `indirect` | Improves leverage, tooling, knowledge, or capabilities that may help later |
| `none` | Personal, experimental, or reference-only project with no clear operational link |
| `unknown` | Not yet assessed |

## Core Files

### `index.md` — Project Home

Purpose: quick orientation and navigation.

Recommended content:

```markdown
---
okf_version: "0.1"
type: Project
title: Project Name
description: One-line description.
tags: [project, example]
project: project-slug
status: active
priority: P1
owner: Owner Name
impact: direct
stage: build
last_reviewed: 2026-06-20
next_review: 2026-06-27
timestamp: 2026-06-20T09:00:00+00:00
---

# Project Name

One or two paragraphs explaining what this project is and why it matters.

## Current focus

- Short bullet list of current focus areas.

## Next action

- One concrete next action.

## Navigation

- [Status](status.md) — current state, next action, blockers.
- [Context](context.md) — background, users, constraints.
- [Roadmap](roadmap.md) — milestones and planned work.
- [Decisions](decisions.md) — durable decisions.
- [Log](log.md) — chronological updates.
- [Links](links.md) — repos, docs, analytics, dashboards, domains.
- [Tasks](tasks/) — active and archived task notes.
- [Research](research/) — customer, market, SEO, analytics, or technical research.
```

### `status.md` — Operational State

This is the most important file for active projects.

```markdown
---
type: Project Status
title: Project Status
description: Current status, priority, owner, next action, and blockers.
tags: [status]
project: project-slug
status: active
priority: P1
owner: Owner Name
impact: direct
stage: build
last_reviewed: 2026-06-20
next_review: 2026-06-27
timestamp: 2026-06-20T09:00:00+00:00
---

# Status

## Current state

Active.

## Why this matters

Explain why the project deserves attention.

## Next action

One concrete next action. If there are multiple, list the top 1-3 only.

## Blockers

- Blocker or `None known`.

## Decisions needed

- Decision or `None known`.

## Active tasks

- [Task title](tasks/task-slug.md)
```

Rules:

- Active projects must have `Next action`.
- If `Next action` is blank, recommend parking or archiving.
- `last_reviewed` should update whenever the project state is materially reviewed.

### `context.md` — Background And Constraints

Use for durable project understanding:

```markdown
---
type: Project Context
title: Project Context
description: Background, users, goals, constraints, and non-goals.
tags: [context]
project: project-slug
timestamp: 2026-06-20T09:00:00+00:00
---

# Context

## Problem / opportunity

## Target users / customers

## Goals

## Non-goals

## Constraints

## Key assumptions
```

### `roadmap.md` — Milestones

Use only when a project has meaningful phases or deliverables.

```markdown
---
type: Roadmap
title: Project Roadmap
description: Milestones, phases, and planned sequencing.
tags: [roadmap]
project: project-slug
timestamp: 2026-06-20T09:00:00+00:00
---

# Roadmap

## Now

## Next

## Later

## Not planned
```

### `decisions.md` — Durable Decisions

Use for decisions future humans or agents will need to remember.

```markdown
---
type: Decisions Log
title: Project Decisions
description: Durable decisions and rationale.
tags: [decisions]
project: project-slug
timestamp: 2026-06-20T09:00:00+00:00
---

# Decisions

## 2026-06-20 — Decision title

**Decision:** What was decided.

**Rationale:** Why.

**Alternatives considered:** What was rejected.

**Implications:** What changes because of this.
```

### `log.md` — Chronological Updates

Use for short, factual update history.

```markdown
---
type: Project Log
title: Project Log
description: Chronological project updates.
tags: [log]
project: project-slug
timestamp: 2026-06-20T09:00:00+00:00
---

# Log

## 2026-06-20

- Reviewed project status.
- Updated next action.
- Added link to latest report.
```

Avoid dumping entire chat transcripts into `log.md`. Summarize only durable changes.

### `links.md` — Canonical Links

Use for URLs, repos, dashboards, docs, channels, domains, and external references.

```markdown
---
type: Links
title: Project Links
description: Canonical links and resources.
tags: [links]
project: project-slug
timestamp: 2026-06-20T09:00:00+00:00
---

# Links

## Repositories

- [Repo name](https://github.com/...)

## Dashboards

- [Dashboard title](...)

## Docs / references

- [Document title](...)
```

## Agent Write-Back Contract

A project knowledge base only works as a second brain if every agent writes back durable outcomes. After meaningful work, agents must update the project docs with only durable facts:

- What changed.
- Evidence link: PR, issue, commit, report, dashboard, support ticket, research source, execution card, or artifact.
- Decision made or decision needed.
- Updated next action.
- Blocker, if any.
- Where follow-up execution lives: task doc, issue, card, project file, or external artifact.

Suggested role boundaries:

- **Operator / PM agents** own portfolio hygiene, prioritization, status, synthesis, and execution orchestration.
- **SEO / growth agents** write durable search, analytics, content, and growth findings into `research/`, `tasks/`, project `index.md`, or `status.md`.
- **Development agents** write durable repo, PR, build, test, release, and technical-design outcomes into `log.md`, `tasks/`, `links.md`, `decisions.md`, or `status.md`.
- **Research agents** write durable customer, market, competitor, and technical due-diligence findings into `research/` and link implications back to `status.md` or `tasks/`.

Do not write chat transcripts, temporary scratch notes, or unverified claims. If evidence is missing, record the unknown instead of converting an assumption into project state.

## Task Files

Use task files for meaningful work items that need context, acceptance criteria, or history. Do not create a file for every tiny todo.

```markdown
---
type: Task
title: Task title
description: One-line outcome.
tags: [task]
project: project-slug
status: todo
priority: P1
owner: Owner Name
created: 2026-06-20
updated: 2026-06-20
due: null
---

# Task title

## Outcome

What success looks like.

## Context

Relevant background.

## Acceptance criteria

- Criterion 1.
- Criterion 2.

## Notes

- Links to reports, PRs, issues, support tickets, or decisions.
```

Task statuses:

```yaml
status: todo | doing | blocked | done | cancelled
```

## Research Files

Use research files for customer discovery, competitor notes, market research, technical due diligence, analytics summaries, or source-grounded findings.

```markdown
---
type: Research
title: Research Title
description: One-line summary of what this research answers.
tags: [research]
project: project-slug
source: web | customer | support | analytics | internal | mixed
created: 2026-06-20
updated: 2026-06-20
---

# Research Title

## Question

What question does this answer?

## Findings

## Evidence

## Implications

## Recommended actions
```

## Portfolio Indexes

Each bucket should have an `index.md` that lists projects and their state.

Example `active/index.md`:

```markdown
---
type: Project Index
title: Active Projects
description: Active projects currently requiring attention.
tags: [projects, active]
timestamp: 2026-06-20T09:00:00+00:00
---

# Active Projects

| Project | Priority | Owner | Impact | Next action | Last reviewed |
|---|---:|---|---|---|---|
| [Project Name](project-slug/) | P1 | Owner Name | direct | Decide launch scope | 2026-06-20 |
```

Root `projects/index.md` should link to each bucket and summarize the portfolio:

```markdown
# Projects

Source-of-truth project documentation.

## Buckets

- [Active](active/) — projects with current work or decisions needed.
- [Parked](parked/) — intentionally paused projects.
- [Ideas](ideas/) — early concepts.
- [Archived](archived/) — done/dead historical projects.
- [Shared](shared/) — templates and cross-project references.

## Operating rule

Active projects must have a current `status.md` or `index.md` with a concrete next action.
```

## Creating A New Project

1. Identify the project root directory.
2. Decide bucket: `active`, `parked`, `ideas`, or `archived`.
3. Pick a stable lowercase slug.
4. Choose size tier:
   - Tiny: `index.md` only, optional `log.md`.
   - Normal: `index.md`, plus optional `status.md`, `context.md`, `decisions.md`, `log.md`, and `links.md` only when needed.
   - Major: add `roadmap.md`, `tasks/`, `research/`, `specs/`, `references/`, and `assets/` as needed.
5. Create minimum useful docs.
6. Add the project to the bucket `index.md`.
7. If active, ensure the docs have a next action, priority, owner, blockers, and last reviewed date.
8. If execution needs to be delegated, create a meaningful task/spec doc before creating external task cards or issues. Link any created execution items back to the source doc.

## Auditing Projects

When asked to summarize projects:

1. Inspect the project root directly.
2. Prefer `index.md` and `status.md` for current state.
3. If missing, infer only from filenames and docs, and label inference clearly.
4. Report projects by bucket and priority.
5. Identify stale active projects:
   - Missing `status.md` or current status section.
   - No next action.
   - Old `last_reviewed`.
   - No clear owner.
   - No clear impact.
6. Recommend one of:
   - Keep active.
   - Move to parked.
   - Move to ideas.
   - Archive.
   - Needs human decision.

## Updating Existing Projects

When updating docs:

- Preserve useful existing content.
- Do not overwrite history unless cleaning obvious duplication.
- Add missing frontmatter when safe.
- Update `last_reviewed` only when you actually reviewed the project state.
- Prefer merging useful small docs into `index.md` over keeping many tiny files.
- Delete files/folders that only contain placeholders, generic cadence, or empty structure.
- Keep separate files only when they contain substantial information worth maintaining separately.
- If moving buckets, update bucket indexes.
- Run link, frontmatter, and stale-project checks where practical.

## Bulk Cleanup / Reorganization Workflow

For broad cleanups, do all of the following:

1. Check version control status before changes so pre-existing repo state is visible.
2. Create a timestamped backup before moving large numbers of files if the tree is not already cleanly versioned.
3. Move projects into `active/`, `parked/`, `ideas/`, `archived/`, or `shared/` using an operational review lens.
4. Rename paths to lowercase/kebab-case where safe.
5. Consolidate legacy files without data loss, then delete the source file when appropriate:
   - `README.md` → `index.md`.
   - `CONTEXT.md` / `context.md` → merge into `index.md` unless substantial enough to remain separate.
   - `DECISIONS.md` / `decisions.md` → keep only if real durable decisions exist.
   - `LINKS.md` / `REPOS.md` → merge real links into `index.md` or a meaningful `links.md`.
   - `TODO.md` / `tasks/index.md` → keep only if meaningful task context exists.
   - `WEEKLY.md` / `log.md` → keep only if it records real durable events.
   - `NOTES.md` / `notes.md` → merge useful notes into `index.md`; delete scratchpad shells.
   - `AGENT.md` / `agent.md` → merge genuinely useful operating notes into `index.md`; delete generic agent scaffolding.
6. If a target file already exists, append useful old content under a clear heading rather than overwriting.
7. Verify every project has a useful `index.md`.
8. Verify optional sibling docs exist only when they contain meaningful project-specific information.
9. Run validation checks and commit the cleanup as a reviewable change.

## Repository Linking

When connecting project docs to source-code repositories:

- Every checked project folder should end with either a `## Repositories` section in `index.md` containing confident repo links, or a row in root `unlinked.md` asking for the canonical repo URL.
- Do not guess weak matches.
- Use local git remotes, repository CLI/API searches, existing docs, and naming evidence.
- When a human supplies URLs in `unlinked.md`, verify them where practical, update the project `index.md`, remove completed rows, and follow any status/bucket instructions in the Notes column.

## Suggested Cron Jobs

These jobs make the project knowledge base self-maintaining. Schedules are examples; adjust to the team's cadence and delivery channel.

### 1. Nightly Project Maintenance

**Schedule:** daily, off-hours.

**Prompt:**

```text
Load the project-knowledge-base skill. Inspect the configured project root. Maintain the project knowledge base without inventing facts.

Tasks:
1. Check version control status and current bucket folders before acting.
2. For new folders, initialize a useful `index.md` with minimal frontmatter and known context.
3. For moved folders, update bucket indexes, frontmatter status/stage, stale path references, and add a dated maintenance note.
4. For deleted folders, infer reason only from version control, notes, or nearby moves. If unclear, add an item to `unknowns.md`.
5. Read and action root `todo.md` maintenance instructions if present; remove or mark completed only after acting.
6. Ensure active projects have next actions, owners, priorities, and last reviewed dates.
7. Remove or merge placeholder-only files.
8. Commit completed documentation changes separately with a clear message.
9. Send a concise summary: changes made, unknowns, stale active projects, and decisions needed.
```

### 2. Daily Project Standup

**Schedule:** every workday morning.

**Prompt:**

```text
Load the project-knowledge-base skill. Review every folder under `active/` in the configured project root.

For each active project:
1. Read `index.md`, `status.md` if present, task docs, and recent log entries.
2. Check linked repositories or execution systems only when the project docs provide confident links.
3. Report movement, blockers, decisions needed, and the next action.
4. If the next action is unclear, create or update an open question instead of guessing.
5. Update project docs only for durable changes.
6. Commit documentation updates if any.

Send a concise standup summary grouped by priority.
```

### 3. Weekly Portfolio Review

**Schedule:** weekly.

**Prompt:**

```text
Load the project-knowledge-base skill. Produce a portfolio review for the configured project root.

Review active, parked, ideas, and archived indexes. Identify:
1. Active projects with stale reviews or no next action.
2. High-priority projects with blockers or missing owners.
3. Parked projects that have a clear reactivation trigger.
4. Ideas that should be promoted, killed, or left alone.
5. Projects that should be archived.
6. Documentation quality issues that reduce agent handoff reliability.

Update indexes and project docs where the correct change is evident. Put uncertain items in `unknowns.md`. Commit safe documentation changes. Send recommendations with trade-offs and a short action list.
```

### 4. Weekly Execution Handoff Sweep

**Schedule:** weekly or twice weekly if many agents are working.

**Prompt:**

```text
Load the project-knowledge-base skill. Inspect project task docs and linked execution items where links exist.

For completed work:
1. Verify evidence from the linked PR, issue, card, report, or artifact.
2. Reflect durable outcomes back into the relevant project docs.
3. Add decisions or log entries only when they preserve future-useful context.
4. Mark task docs done/cancelled/blocked where appropriate.

For blocked work:
1. Capture the blocker in the project status.
2. Add required human decisions to `unknowns.md` or the project open questions.

Commit documentation updates and send a concise sweep summary.
```

### 5. Monthly Knowledge Base Hygiene

**Schedule:** monthly.

**Prompt:**

```text
Load the project-knowledge-base skill. Run a hygiene audit over the configured project root.

Check for:
1. Broken internal links.
2. Missing or invalid YAML frontmatter on major docs.
3. Placeholder-only docs.
4. Duplicate project folders.
5. Inconsistent bucket/status combinations.
6. Active projects without next actions.
7. Old unknowns that can now be resolved.
8. Repeated friction that should become a template, skill update, or operating rule.

Fix safe issues, list uncertain issues, commit changes, and recommend improvements to this skill or local templates.
```

## Execution System Integration

Use this pattern when project work needs durable multi-agent execution:

```text
Project task/spec -> execution queue -> worker outputs -> durable project update -> execution item archived/closed
```

Rules:

- The project knowledge base remains the source of truth for durable project context, status, decisions, research, and task specs.
- External execution systems are disposable queues for concrete work assigned to a person or agent.
- Do not duplicate strategy/status into execution cards. Cards should link to the project source path.
- Add a `## Handoff brief` section to meaningful task docs before creating cards/issues. Include: assignee, expected output, inputs, acceptance criteria, constraints, evidence required, and where to write the durable result.
- Add/update a `## Execution` section only after successful card/issue creation. Include returned ID/URL, assignee, status/date, and dependency notes.
- Use deterministic idempotency keys or unique source links where the execution system supports them to avoid duplicate cards.
- Scheduled sweeps should close the loop: inspect done/blocked/review items, verify evidence, reflect durable results into project docs, archive reflected done items only after the source docs are updated, and capture blocked/review-required items in project docs or `unknowns.md`.
- A done execution item is not operationally done until its durable outcome is reflected into the project knowledge base.
- Blocked execution items should update the relevant project `status.md`, task doc, or root `unknowns.md` with the blocker and decision needed.
- Research, growth, and development outputs should link back to the exact project files they updated.

## Operational Review Lens

When deciding what deserves attention, rank projects by:

1. Direct revenue, customer, user, or mission impact.
2. Trust, reliability, support, or delivery impact.
3. Founder, operator, or team leverage.
4. Strategic learning value.
5. Distribution advantage.
6. Maintenance burden.
7. Opportunity cost.

Be direct: if a project is interesting but distracts from higher-impact work, recommend parking it.

## Common Pitfalls

1. **Over-documenting tiny ideas.** A one-page idea is often enough.
2. **Creating placeholder docs.** Do not keep files that only contain headings, empty sections, generic cadence, placeholder links, or instructions to fill something in later.
3. **Leaving active projects without next actions.** Active means actionable.
4. **Treating OKF as a rigid spec.** Operating clarity is more important than strict conformance.
5. **Mixing transient todos into durable docs.** Only save tasks that need context, history, or handoff.
6. **Keeping `agent.md` / `AGENT.md` files as boilerplate.** Merge genuinely useful operating notes into `index.md`; delete generic scaffolding.
7. **Failing to update indexes.** If a folder moves or status changes, update the relevant `index.md`.
8. **Assuming project state without reading files.** Always inspect the folder before summarizing or changing state.
9. **Letting low-impact projects crowd out important work.** Use the impact and priority fields to force trade-offs.
10. **Writing back unverified claims.** If evidence is missing, record the unknown instead.

## Verification Checklist

After creating or updating project docs, verify:

- [ ] Project is in the right bucket.
- [ ] Folder and file names are lowercase/slugs.
- [ ] `index.md` exists and contains useful project summary/context.
- [ ] No project-level `agent.md` / `AGENT.md` files remain unless there is a strong local convention requiring them.
- [ ] No structure-only docs remain unless they contain meaningful project-specific information.
- [ ] Frontmatter includes `type`, `title`, `description`, `tags`, `project`, `status`, `priority`, `owner`, `impact`, `stage`, and dates where relevant.
- [ ] Bucket `index.md` is updated.
- [ ] Retained `log.md` records real durable changes, not generic cadence/template text.
- [ ] Any assumptions are labeled clearly.
- [ ] Recommendations are tied to impact, leverage, strategic learning, maintenance burden, and opportunity cost.
- [ ] Durable outcomes from execution cards, PRs, reports, or research have been reflected back into the relevant project docs.
- [ ] Unresolved questions are captured in root `unknowns.md` or a project `## Open questions` section instead of being guessed.
- [ ] If changes were made, version control diff is reviewed and committed.
