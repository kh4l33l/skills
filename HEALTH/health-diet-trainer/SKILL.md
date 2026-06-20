---
name: health-diet-trainer
description: >
  Plan easy high-protein, lower-carb/lower-fat family meals, track suggested and selected meals, and learn preferences over time from weekly feedback.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Health / Diet Trainer

## Overview

Use this skill when a user wants a practical trainer-style nutrition assistant for weekly meal planning and lightweight preference tracking.

The skill helps an agent:

1. Suggest simple high-protein, lower-carb/lower-fat meals for a full week.
2. Keep meal prep realistic and family-friendly.
3. Track meals already suggested so the plan does not become repetitive.
4. Record meals the household actually chose or cooked.
5. Learn liked/disliked meals, ingredients, cuisines, and effort constraints from user feedback.
6. Reuse liked meals occasionally without over-rotating them.

This is a meal-planning workflow, not medical advice.

## When To Use

Use this skill when the user asks to:

- Act as a gym trainer, nutrition coach, or diet accountability assistant.
- Create weekly meal ideas for a following week.
- Plan high-protein, low-carb, low-fat, easy dinners.
- Keep ingredient lists short.
- Track meals suggested over time.
- Record Sunday feedback about meals actually chosen or cooked.
- Remember meals the user or family likes/dislikes.
- Build a recurring weekly meal-planning email or scheduled digest.

Do **not** use this skill for diagnosis, treatment, eating-disorder support, medical nutrition therapy, or precise clinical macros unless the user is working with a qualified clinician and provides explicit targets.

## Core Meal Constraints

Default constraints for weekly plans:

- Cover Monday through Sunday.
- Suggest 7 dinner ideas unless the user asks for a different number.
- Keep meals easy: target 45 minutes or less active prep/cook time.
- Prioritize high protein.
- Keep carbs and fats relatively low.
- Use short ingredient lists: ideally 6-10 core ingredients, excluding pantry basics such as salt, pepper, dried herbs, spices, vinegar, stock cubes, and low-calorie cooking spray.
- Prefer repeatable household meals over novelty.
- Avoid deep frying, pastry, cream-heavy sauces, cheese-heavy recipes, and large pasta/rice bases unless the user asks for them.
- Favor lean cooking methods: grill, oven, air fryer, poach, steam, stir-fry with minimal oil, or sheet-pan cooking.

## Required Tracking Files

Maintain these files alongside the skill:

- `references/meal-preferences.md` — durable likes, dislikes, household constraints, ingredient preferences, cuisine preferences, budget/effort notes.
- `references/suggested-meals-log.md` — meal ideas suggested by send date and target week.
- `references/selected-meals-log.md` — meals the user says were actually chosen/cooked, with basic recipes and feedback.

Always read all three files before generating a weekly plan.

## Weekly Meal Plan Workflow

1. **Confirm date range**
   - Determine the next Monday-Sunday range from the current date.
   - If the user gives a specific week, use that instead.

2. **Read history**
   - Read `meal-preferences.md` for durable likes/dislikes and constraints.
   - Read `suggested-meals-log.md` to avoid excessive recent repetition.
   - Read `selected-meals-log.md` to learn what was actually chosen and what recipes worked.

3. **Build the plan**
   - Choose 7 meals that fit the constraints.
   - Include liked meals occasionally if present, especially when they match the current goals.
   - Avoid repeating the same meal too frequently unless the user explicitly wants repetition.
   - Keep the shopping list practical by reusing proteins, vegetables, or sauces across the week where helpful.

4. **Write the output**
   Each meal should include:
   - Day and meal name.
   - Why it fits the goal.
   - Prep/cook time estimate.
   - Short ingredient list.
   - Basic recipe steps.
   - Optional simple side or swap.

5. **After successful delivery**
   - Update `suggested-meals-log.md` with the target week, send date, and meal names.
   - Do not update the log if delivery failed.

## Weekly Email Format

Use this structure for scheduled weekly emails:

Subject:

```text
Meal ideas for next week (Mon DD MMM - Sun DD MMM)
```

Body:

```text
Hi [Name],

Here are 7 easy high-protein, lower-carb/lower-fat family meal ideas for next week.

1. Monday — Meal name
   Why: ...
   Time: ...
   Ingredients: ...
   Basic recipe: ...

2. Tuesday — Meal name
   Why: ...
   Time: ...
   Ingredients: ...
   Basic recipe: ...

...

Shopping shortcuts:
- ...
- ...

Reply on Sunday with what you actually picked/cooked and any changes. I’ll keep learning what works for the family.
```

Keep the tone practical, concise, and coach-like. Avoid guilt, moralizing, or overcomplicated nutrition language.

## Sunday Feedback Workflow

When the user provides the meals they actually chose/cooked:

1. Update `references/selected-meals-log.md` with:
   - Week/date.
   - Meal names.
   - Basic recipes or modifications provided by the user.
   - Notes about what worked or failed.

2. Update `references/meal-preferences.md` when feedback indicates durable preferences:
   - Liked meals.
   - Disliked meals.
   - Ingredients to avoid.
   - Meals that were too much effort.
   - Meals that were kid-friendly/family-friendly.
   - Helpful equipment, budget, or shopping constraints.

3. Keep preference entries compact and dated.

## Practical Defaults

Good protein staples:

- Chicken breast or trimmed chicken thigh.
- Turkey mince.
- Lean beef mince.
- Pork tenderloin or lean pork steaks.
- White fish.
- Salmon in moderation.
- Prawns/shrimp.
- Eggs or egg whites.
- Greek yogurt or cottage cheese.
- Tofu or tempeh if accepted.

Good lower-carb sides:

- Broccoli.
- Green beans.
- Courgette/zucchini.
- Salad.
- Cabbage slaw.
- Cauliflower rice or mash.
- Stir-fry vegetables.
- Roasted non-starchy vegetables.

Good flavor patterns:

- Lemon and herb.
- Peri-peri.
- Greek-style yogurt and herbs.
- Light fajita/taco seasoning.
- BBQ spice rub without sugary sauce.
- Teriyaki-light using reduced sugar sauce or soy/ginger/garlic.
- Tomato, chilli, and herbs.
- Burger bowls without buns.

## Safety And Boundaries

- Do not claim to treat medical conditions.
- Do not prescribe very low-calorie, extreme, or restrictive diets.
- If the user asks for medical advice, medication/diet interactions, diabetes/kidney/heart-disease nutrition, pregnancy nutrition, eating disorder support, or symptoms, recommend consulting a qualified healthcare professional.
- Do not store sensitive health metrics unless the user explicitly asks for that tracking and the environment is appropriate for private data.
