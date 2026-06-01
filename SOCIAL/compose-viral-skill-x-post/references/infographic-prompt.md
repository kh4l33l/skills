# Infographic Prompt Generator

The visual is the biggest virality lever — a good infographic makes the framework obvious without reading the caption, which is what earns bookmarks. This skill produces a *prompt* for an image model, not the image itself.

## How to use

1. Fill in every bracket below with the skill's specifics.
2. Either feed the completed meta-prompt to an LLM to generate a polished image prompt, OR (faster) fill it in yourself and hand the user the final image prompt directly.
3. The user pastes the final prompt into their image model and attaches the result to the post.

## Meta-prompt (fill in the brackets)

```
You are a world-class infographic designer specializing in clean, minimalist tech illustrations for social media (X/Twitter). Your style uses simple line-art, a blue/white/gray palette, high contrast, modern sans-serif typography, and subtle tech motifs (grids, dots, arrows) for a professional yet approachable feel. Aspect ratio optimized for X posts (square 1:1 or 16:9 landscape — specify in the prompt).

Generate a single, highly detailed, ready-to-copy prompt for an image generation AI. The infographic must illustrate this skill:

Skill Name: [exact skill name, e.g. "Buyer Persona Objection Synthesizer"]

Central Element: [the main mockup — e.g. "a large central rectangle showing a sample landing page with placeholder text and buttons"]

Surrounding Components: [N] labeled sections arranged around the center in boxes/circles with icons and arrows pointing inward:
1. [Label 1] — [1-sentence description]
2. [Label 2] — [1-sentence description]
... ([N] total, matching the post's breakdown)

Bottom Section: a distinct panel titled "What You Get" showing [describe sample output visually — e.g. "a clean bulleted list of objections, fixes, and conversion recommendations with highlighted key phrases"]

Overall Layout: bold title at top "[Skill Name] Framework". Clean white background, light blue accents. Add subtle "Input → Process → Output" labels if they fit the flow. Must be scannable in seconds and readable on a phone.

Output ONLY the final image generation prompt — no preamble, no explanation.
```

## Edge cases

- **Highly technical skill:** simplify icons to abstract symbols; don't try to render real code.
- **Multi-step pipeline:** use flowchart arrows left-to-right or top-to-bottom rather than a radial layout.
- **Mobile clarity:** always sanity-check that labels are legible at phone size — fewer, larger labels beat many tiny ones.
- **Component count:** the infographic's labeled sections should match the post's breakdown count so the visual and copy reinforce each other.
