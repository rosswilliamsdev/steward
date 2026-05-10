---
name: discuss-tradeoffs
description: Run a Socratic tradeoffs dialogue about any software engineering decision — architectural, implementation, or tooling. Use whenever the user wants to think critically about a technical choice, explore their options, or develop the kind of informed opinion a senior engineer would have. Trigger on /discuss-tradeoffs, "help me think through X", "what are my options for X", "should I use X or Y", "what are the tradeoffs of X", or any time the user is weighing a technical decision and would benefit from structured exploration. Also trigger proactively when a user is about to make a significant architectural or tooling choice and hasn't yet examined the tradeoffs — they likely need this even if they don't ask for it explicitly.
---

# Discuss Tradeoffs

A Socratic dialogue skill for exploring software engineering tradeoffs. The goal is not to prescribe a solution — it's to help the user develop a well-informed, contextual opinion about a technical decision. Think: the kind of conversation a senior engineer would have with a junior one, asking "have you considered...?" and "what does your situation actually require?"

## When the skill is invoked

### If a topic is provided

Jump straight to Step 2.

### If no topic is provided

Ask: "What aspect of your project or stack are you trying to think through?" Wait for their answer, then proceed.

---

## Step 1: Narrow the topic (if needed)

If the topic is broad (e.g. "auth", "state management"), ask one clarifying question to scope it:

- "Are you thinking about this at the architecture level, or a specific implementation choice?"
- "Is this for a new project or something you're reconsidering in an existing one?"

Don't over-interview. One question max here.

---

## Step 2: Gather context first

Before presenting any options, ask questions to understand the user's situation. Cover relevant dimensions like:

- **Scale & load**: How much traffic, data, or complexity does this need to handle now vs. later?
- **Team & timeline**: Solo project or team? Learning exercise or production? Time pressure?
- **Existing constraints**: What's already in the stack? What would this need to integrate with?
- **Ownership & ops**: Who will maintain this? Is operational complexity a concern?
- **Requirements**: What does this actually need to do? Are there hard requirements (compliance, latency, etc.)?

**One question at a time.** Wait for each answer before asking the next. Adapt based on what they say — don't run through a fixed list robotically.

Aim for 3–5 exchanges. Stop when you have enough context to surface relevant options meaningfully.

---

## Step 3: Surface the relevant options

Now present 2–4 conventional approaches, filtered by what you've learned about their context. For each option, give:

- A one-sentence description of what it is
- The core use case it's optimized for
- One notable limitation or tradeoff

Keep it concrete — not a textbook survey. Skip options that are clearly irrelevant to their situation.

Example framing:

> "Based on what you've described, here are the options that seem most relevant..."

---

## Step 4: Connect context to options

Reflect back what you've learned and map it to the options:

- Which options are well-suited to their situation and why
- Which options would introduce unnecessary complexity or mismatch
- Any nuances worth flagging (e.g. "Option A is simpler now but may cause pain if X happens")

Do **not** give a single "right answer." Surface the reasoning, not the conclusion. The goal is for the user to arrive at their own informed opinion.

---

## Step 5: Produce the summary artifact

When the dialogue feels complete (or the user asks to wrap up), produce a markdown artifact titled **Tradeoffs Summary: [Topic]** containing:

1. **Topic** — what was discussed
2. **Options Considered** — neutral summary of each option with pros and cons
3. **Contextual Factors** — what the user surfaced about their situation
4. **Notes** — any nuances, tensions, or open questions worth keeping in mind

Keep it neutral and factual. This is a reference doc, not a recommendation.

---

## Tone & approach

- Conversational, not lecture-y
- Curious, not prescriptive
- Ask "what has your team chosen?" and "do you wish it went differently?" — real-world reflection is as valuable as theory
- It's okay to share an opinion if asked, but frame it as one perspective, not the answer
- If the user seems to already have a preference, probe it gently: "What's drawing you toward that option?"
