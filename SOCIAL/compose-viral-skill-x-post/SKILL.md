---
name: compose-viral-skill-x-post
description: Use this skill whenever the user wants to turn an AI skill, prompt, workflow, agent setup, automation, pipeline, or tool into a high-engagement X/Twitter post or thread. Trigger on requests like "write an X post about my skill", "turn this workflow into a tweet thread", "help me share this prompt on Twitter", "make this go viral", "draft a launch post for my agent", "promote my automation on X", or any time the user has built something AI-related and wants to announce, showcase, or distribute it to an audience. Also use when the user asks for a hook, a thread breakdown, an infographic prompt for a post, or a CTA for sharing skill-style content. Covers hooks, breakdowns, infographic prompts, CTAs, timing, and anti-hype checks for AI, indie-hacking, productivity, and monetization audiences.
metadata:
  author: bradvin
  version: "2.1"
  created: "2026-05-28"
  updated: "2026-06-02"
---

# Compose Viral Skill X Post

Turn any AI skill, workflow, prompt system, multi-agent setup, pipeline, or tool into an X/Twitter post or thread engineered for bookmarks, reposts, replies, and follows. The goal is education + authority + asset distribution — not hype. This skill produces the actual post copy (ready to paste), an optional infographic generation prompt, and a CTA, plus the strategic choices behind them.

## What makes these posts work

People save and share posts that hand them a reusable mental model or tool they can test immediately. Four levers drive that:

- **Specificity** — concrete labels, real numbers, named components. "5 buyer personas" beats "a persona framework."
- **Front-loaded value** — the payoff is obvious in sentence one; the strongest 1-2 breakdown items come before any drop-off point.
- **A scannable visual** — a good infographic communicates the framework without reading the caption, which is what earns bookmarks.
- **Credibility over hype** — qualified, testable claims ("Tested in my workflow; results vary") build the trust that converts to follows and newsletter signups. Over-claiming invites reply-guys and destroys reputation.

Bookmarks, reply quality, and DM volume are better success signals than raw likes — they indicate intent, not vanity.

Audience fit matters. This skill works best for tool-hungry niches like AI workflows, automation, content creation, sales, productivity, and monetization. For abstract, entertainment-only, or purely opinion content, narrow the promise and do not force a giveaway or framework angle.

## Before you write: gather the inputs

Pull these from the conversation if they're already there. For most items, if they're missing, make a reasonable assumption and note it rather than interrogating the user. **Proof is the one exception — never invent it.**

1. **What the skill does** — the one-line job and the core mechanism (why it's repeatable/unique).
2. **Components** — the 4-9 parts, steps, or agents. Each should ideally have a single responsibility. If the source material is fuzzy, first extract 3-5 core elements, then expand or consolidate only when the structure is clear.
3. **Proof (do not fabricate).** A real metric is the single strongest hook ingredient — revenue, time saved, before/after CTR, output volume, etc. First check whether the conversation, the user's earlier messages, attached files, or prior data already contain one. If you find evidence, use it. If you do NOT find a real metric, do not invent one and do not silently fall back to a vague outcome claim — **stop and ask the user for the actual number** before writing the post (e.g. "Do you have a real result for this — revenue, hours saved, a before/after? That makes the hook far stronger. If you'd rather not share a number, I'll write an outcome-based hook instead."). Only after the user declines or confirms there's no metric do you proceed with a qualified, outcome-based hook and no numbers. A made-up metric is the fastest way to get the post ratio'd and destroy the author's credibility, so this is worth one quick question.
4. **The asset** — what you'll actually give away (prompt file, JSON, skill files, Notion doc). The CTA must match something deliverable.
5. **Format** — single post vs. thread (see below).
6. **Audience** — AI builders, indie hackers, productivity, sales/marketing. Tone shifts slightly per audience.

For everything except proof, if the user hasn't said, default to: single post with infographic, indie-hacker/AI-builder audience, outcome-based hook — and note your assumptions. Proof always requires real evidence or an explicit user answer; never assume a number.

## Single post vs. thread

- **Single post + image** — default. Best when the skill has ≤5 components or the visual carries the framework. Highest completion rate.
- **Thread** — use for complex skills (>5 components) or when each step needs room. Risk: drop-off after tweet 3-5. Mitigate by front-loading the hook + the 1-2 strongest breakdown items in the first three tweets; never bury the best part at tweet 7.

## Writing the post

Build the post in this order. The full copy-paste template lives in `references/templates.md` — read it when you're ready to assemble the final draft.

1. **Hook (1 sentence).** Lead with the payoff. Strongest pattern when a real metric exists: "This is probably the [skill] that's directly made me the most money / saved me the most time / produced my highest-quality output." If you don't have a real metric yet, ask for one before writing (see "gather the inputs" → Proof) — a true number is the highest-leverage thing in the whole post. Only if the user has no metric or declines to share do you fall back to a dramatic-but-true claim, a contrarian angle, or "I built [X] that does [Y] while I sleep." Offer 2-3 hook variations so the user can A/B test — early engagement (first ~30 min) tells you which lands.

2. **What it is + mechanism (1-2 sentences).** Plain language. What's the magic, and why does it repeat?

3. **The breakdown (4-9 items).** Numbered or bulleted. Give every item a vivid, memorable label ("The Skeptic," "Dopamine Trigger Agent") + one line + a short parenthetical. Memorable labels are what make a framework quotable. For technical skills, keep one responsibility per item and note edge cases or verification steps where it adds credibility.

4. **How it works (3-5 steps).** The process flow: inputs → tools/secret sauce → output.

5. **What you get.** Quote or bullet a sample output. Add proof here if available.

6. **Use it for (4-7 cases).** Concrete scenarios so readers picture immediate value.

7. **CTA.** Match it to the real asset. Two reliable forms: "Full breakdown + the free [asset] below" (link/thread) or "Comment '[KEYWORD]' + like/repost/follow and I'll DM it." The comment-keyword form drives replies, which boost reach. If the goal is retention, add a newsletter or community CTA after the immediate asset CTA, not instead of it.

## The infographic

The visual is the single biggest virality lever — prioritize it. This skill doesn't generate the image directly; it generates a *prompt* you feed to an image model. Read `references/infographic-prompt.md` for the meta-prompt and fill-in instructions. The pattern: bold title → central mockup → 4-9 labeled components with arrows pointing inward → a bottom "What You Get / Output" panel. Keep it readable on mobile; for highly technical skills, abstract the icons; for pipelines, use flowchart arrows.

## Anti-hype check (run before delivering)

These are the failure modes that get posts ratio'd or quietly ignored. Verify every one:

- Every metric in the post is real — pulled from evidence or supplied by the user. None are invented, estimated, or guessed. If a number was needed and the user hadn't given one, you asked rather than filling it in.
- The hook's payoff is true and obvious in sentence one.
- The breakdown has 4-9 labeled parts, each with one clear job.
- Technical claims are scoped and caveated. For technical skills, include edge cases, verification loops, or what was actually tested.
- A beginner can tell what to do first. If the setup needs prerequisites, name them plainly.
- If it's a thread, the strongest value is in tweets 1-3.
- The infographic reads clearly on a phone and shows input → process → output.
- The CTA promises only an asset that actually exists and can be delivered.
- Only tested skills are shared. Over-delivering on a giveaway builds reputation; under-delivering destroys it.

## Timing

Treat any generic "post at 9am" advice as a hypothesis, not a rule. The real answer is the account's own X Analytics. If there's no account history yet, test weekday mornings in the audience's local timezone and track first-hour replies, bookmarks, reposts, and profile clicks to find the account's window. Consistency in schedule builds audience habit.

## Output format

Deliver, in this order: (1) 2-3 hook variations, (2) the full assembled post or thread, ready to paste, (3) the filled-in infographic generation prompt, (4) a one-line note on which assumptions you made and what the user should A/B test. Keep it copy-paste-ready — minimize commentary the user has to wade through.
