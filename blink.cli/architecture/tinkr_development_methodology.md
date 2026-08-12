# Tinkr Development Methodology

> The dynamic system that wires the Tinkr skill ecosystem together. This is the master workflow that maps "what am I trying to do" → "which skills to invoke in what order." It's not a static checklist — it's a router that the AI agent (Mavis/MiniMax) uses to pick the right skill at the right time. The methodology is a living document: the executable form lives in the `tinkr-workflow` skill; this doc is the long-form explanation.

---

## 1. The product development lifecycle

Every Tinkr task falls into one of 5 phases, mapped against 3 axes (Product, Project, Monetization). The skill set differs by phase.

```
                Product              Project              Monetization
                -------              -------              ------------
Discovery  →    deep-research        tinkr-decision-      tinkr-pricing-
                tinkr-trademark-     recorder             strategist
                check                                    (validate market)

Design     →    tinkr-spec-writer    tinkr-week-planner   tinkr-pricing-
                tinkr-mockup-                            strategist
                author                                    (design tier)
                ui-ux-pro-max
                ui-ux-designer

Build      →    tinkr-plugin-author  tinkr-test-author    tinkr-stripe-
                init                 tinkr-spec-check     integration
                                     code-review

Ship       →    tinkr-mockup-        tinkr-changelog-     tinkr-launch-
                author (update)      writer               checklist
                                     tinkr-launch-        tinkr-conversion-
                                     checklist            funnel

Grow       →    tinkr-roadmap        tinkr-week-planner   tinkr-pricing-
                tinkr-mockup-        xlsx                 strategist
                author (marketing)                       tinkr-stripe-
                                                         integration
                                                         tinkr-conversion-
                                                         funnel
                                                         tinkr-partner-pitch
```

### Phase 1: Discovery (research, market, user)

**Goal:** Understand the user, the market, the technology.

| Task | Axis | Skill |
|---|---|---|
| Research a topic (competitor, market, technology) | Product | `deep-research` |
| Check if a proposed name is trademark-safe | Product | `tinkr-trademark-check` |
| Validate pricing for a new market | Monetization | `tinkr-pricing-strategist` (validate market) |
| Capture a decision as an A-number | Project | `tinkr-decision-recorder` (fires immediately) |
| Check existing Mavis skills before adding a new one | Meta | `skill-creator` |
| Read a GitHub / blog / paper for evidence | Discovery | `web_fetch`, `web_search` |

### Phase 2: Design (spec, brand, mockup)

**Goal:** Lock what we're building before we build it.

| Task | Axis | Skill |
|---|---|---|
| Draft a spec section from a discussion | Product | `tinkr-spec-writer` |
| Design a new Tauri surface following the brand | Product | `tinkr-mockup-author` |
| Design a UI element, color palette, or component | Product | `ui-ux-pro-max` + `ui-ux-designer` |
| Plan the week (Monday check-in) | Project | `tinkr-week-planner` |
| Design a pricing tier | Monetization | `tinkr-pricing-strategist` |
| Generate a marketing page or docs site | Product | `visual-page` |
| Create a pitch deck or partner PDF | Monetization | `pptx` + `pdf` |
| Write a long-form doc (white paper, RFC) | Product | `docx` |

### Phase 3: Build (code, plugin, test)

**Goal:** Ship working, tested, spec-compliant code.

| Task | Axis | Skill |
|---|---|---|
| Scaffold a new plugin from scratch | Product | `tinkr-plugin-author` |
| Generate tests for a new feature | Project | `tinkr-test-author` |
| Pre-commit / pre-PR review | Project | `tinkr-spec-check` + `code-review` |
| Implement a Tauri shell surface | Product | `ui-ux-pro-max` + `tinkr-mockup-author` |
| Design an AI agent prompt (BYO key model) | Product | `llm-call` (for testing) |
| Run a single LLM call against a provider | Product | `llm-call` |
| Bootstrap a new repo in `tinkr-org/` | Project | `init` |
| Wire up Stripe Connect (v1.5) | Monetization | `tinkr-stripe-integration` |

### Phase 4: Ship (release, document, announce)

**Goal:** Get the work into users' hands.

| Task | Axis | Skill |
|---|---|---|
| Generate a CHANGELOG entry | Project | `tinkr-changelog-writer` |
| Write release notes for a version | Project | `tinkr-changelog-writer` + `tinkr-decision-recorder` |
| Pre-launch go/no-go check | All | `tinkr-launch-checklist` |
| File a bug or document a fix in the KB | Product | `tinkr-kb-author` |
| Update the docs site | Product | `visual-page` + the existing docs site spec |
| Update the marketing site | Product | `visual-page` + `tinkr-mockup-author` (for new sections) |
| Plan the week's work | Project | `tinkr-week-planner` |
| Track the 8-week v1.0 plan | Project | `xlsx` (operational tracking, not a skill) |
| Post-launch funnel analysis | Monetization | `tinkr-conversion-funnel` |

### Phase 5: Grow (market, monetize, partner)

**Goal:** Turn the work into a business.

| Task | Axis | Skill |
|---|---|---|
| Generate a vendor cold email (Espressif, Wemos, etc.) | Monetization | `tinkr-partner-pitch` |
| Design a pricing tier or validate the existing one | Monetization | `tinkr-pricing-strategist` |
| Wire up Stripe Connect for marketplace | Monetization | `tinkr-stripe-integration` |
| Design the free → paid funnel | Monetization | `tinkr-conversion-funnel` |
| Prioritize the backlog with RICE | Product | `tinkr-roadmap` |
| Update the partner pipeline tracker | Project | `xlsx` |
| Design a sponsorship pitch (Maker Bundle, Pro Bundle) | Monetization | `tinkr-partner-pitch` (with a sponsorship angle) |
| Generate a marketplace listing for a new plugin | Monetization | (uses `tinkr-plugin-author` + spec writer, not a dedicated skill yet) |

---

## 2. The dynamic routing — how the AI agent picks skills

When the user says "I want to add support for the RP2040," the AI agent should:

1. **Identify the phase**: this is a **Build** task (new plugin) + a small **Discovery** task (verify chip support) + a small **Ship** task (mockup if new surface) + a small **Grow** task (marketplace listing).
2. **Identify the axis**: Product (new chip support) + Project (new code, new tests) + Monetization (marketplace listing).
3. **Run the right skills in order:**
   - `tinkr-workflow` (the orchestrator) confirms the chain
   - `deep-research` (verify RP2040 + MicroPython support, current user base)
   - `tinkr-roadmap` (RICE it — likely Next bucket, ~700 score)
   - `tinkr-decision-recorder` (record the "we will add RP2040 in v1.5" decision as A16 or higher)
   - `tinkr-plugin-author` (scaffold plugins/tinkr-rp2040/)
   - `tinkr-spec-check` (before commit)
   - `tinkr-test-author` (generate tests for the scaffold)
   - `tinkr-kb-author` (write 2 facts + 1 recipe + 1 error for the RP2040)
   - `tinkr-mockup-author` (if there's a new Tauri surface)
   - `tinkr-changelog-writer` (generate the next CHANGELOG entry)
4. **Chain outputs:** the plugin scaffold's output is the test author's input. The mockup's output is the Tauri shell's input. The decision record is referenced by every downstream doc.

When the user says "Espressif didn't reply to the cold email," the AI agent should:

1. **Identify the phase**: this is **Grow** (partner outreach).
2. **Identify the axis**: Monetization (partnership) + Product (vendor integration).
3. **Run the right skills in order:**
   - `tinkr-workflow` (confirms chain)
   - `tinkr-partner-pitch` (draft a follow-up with a new angle — same skill, different parameters)
   - `xlsx` (update the partner pipeline)
   - `tinkr-decision-recorder` (if we decide to abandon Espressif and try Wemos first)

When the user says "I learned that the ESP32-S3 USB-CDC requires a different boot mode," the AI agent should:

1. **Identify the phase**: this is **Grow** (KB entry) + a small **Discovery** (research the chip behavior).
2. **Identify the axis**: Product (KB is the moat) + Project (documented finding).
3. **Run the right skills in order:**
   - `web_search` or `deep-research` to verify the boot mode behavior
   - `tinkr-kb-author` to write the error/fact entry
   - `tinkr-plugin-author` (if needed) to update `plugins/tinkr-esp32/knowledge/chips/esp32s3.json`
   - `tinkr-changelog-writer` to mention the new KB entry in the next release
   - `tinkr-decision-recorder` if the finding changes how the plugin works

When the user says "I'm cutting v0.3.0 on Friday — am I ready?", the AI agent should:

1. **Identify the phase**: **Ship** (release).
2. **Identify the axis**: Project (release process) + Product (what's in the release).
3. **Run the right skills in order:**
   - `tinkr-launch-checklist` (run the v0.X.Y patch release checks)
   - `tinkr-spec-check` (final pre-commit hygiene)
   - `tinkr-changelog-writer` (generate the CHANGELOG entry)
   - `tinkr-decision-recorder` (if any decisions emerged during the cycle)

When the user says "I want to add a paid plugin marketplace. Should it be in v1.0 or v1.5?", the AI agent should:

1. **Identify the phase**: **Discovery** (validate the decision) + **Design** (the plan) + **Grow** (the strategy).
2. **Identify the axis**: Monetization (this is *entirely* monetization).
3. **Run the right skills in order:**
   - `tinkr-workflow` (confirms chain)
   - `deep-research` (re-validate the gated-updates research)
   - `tinkr-pricing-strategist` (validate the 4-tier pricing model)
   - `tinkr-decision-recorder` (record the "marketplace in v1.5, not v1.0" decision if not already locked — it is, A2/A10)
   - `tinkr-roadmap` (place in v1.5 with RICE scoring — should be very high)
   - `tinkr-stripe-integration` (start the design now, ship in v1.5)

---

## 3. The 7 golden rules of the methodology

### Rule 1: Spec before code

Every build task starts with a spec draft. `tinkr-spec-writer` or `tinkr-spec-check` runs first. No exceptions.

### Rule 2: Test with the user, not for the user

The KB is the moat (A15). Every debugging session that finds a non-obvious thing feeds the KB via `tinkr-kb-author`. No exceptions.

### Rule 3: Decisions are recorded immediately

If a discussion produces a decision, `tinkr-decision-recorder` fires before the conversation continues. The `decisions.md` is the single source of truth. No exceptions.

### Rule 4: Brand is consistent across all surfaces

Every new mockup, doc, page, or surface goes through `tinkr-mockup-author` or the existing brand spec. The cyan is `#5EEAD4`, the amber is `#FB923C`, the wordmark is `t●nkr`. No exceptions.

### Rule 5: Monetization is designed, not bolted on

The free → Pro → Managed Token pipeline is the conversion path. Every feature is positioned in this pipeline: is it free? Pro? Bundled? Pay-per-use? The answer is in the spec before the build, via `tinkr-pricing-strategist`. No exceptions.

### Rule 6: Phase and axis always identified

Before running any skill chain, the AI agent identifies the phase (Discovery/Design/Build/Ship/Grow) and the axis (Product/Project/Monetization). The `tinkr-workflow` skill enforces this. No exceptions.

### Rule 7: The orchestrator is the entry point

For any non-trivial or ambiguous task, `tinkr-workflow` runs first to confirm the chain. Single-skill tasks (e.g. "write a CHANGELOG") skip the orchestrator and go directly to the relevant skill. The orchestrator is a router, not a gate.

---

## 4. The skill inventory (full, current as of Aug 13 2026)

### Tinkr-specific (17 total — was 5, now 17)

#### Product development (5)

| Skill | ID | Purpose |
|---|---|---|
| `tinkr-spec-writer` | 14 | Draft a spec section from a discussion |
| `tinkr-mockup-author` | 13 | New Tauri surface mockups that match brand |
| `tinkr-trademark-check` | 4 | USPTO / EUIPO / WIPO / common-law check |
| `tinkr-pricing-strategist` | 15 | Design or validate a pricing tier (also Monetization) |
| `tinkr-roadmap` | 19 | Prioritize the backlog with RICE, place in v1.0/v1.5/v2.0+ |

#### Project development (6)

| Skill | ID | Purpose |
|---|---|---|
| `tinkr-decision-recorder` | 9 | Captures decisions as work happens |
| `tinkr-changelog-writer` | 10 | Generates release notes from git history |
| `tinkr-week-planner` | 11 | Plans the week given a goal |
| `tinkr-test-author` | 12 | Generates tests for new CLI commands |
| `tinkr-spec-check` | 7 | 7-check pre-commit validator |
| `tinkr-plugin-author` | 6 | Scaffold a new Tinkr plugin |

#### Monetization (5)

| Skill | ID | Purpose |
|---|---|---|
| `tinkr-pricing-strategist` | 15 | (also Product) Design / validate a pricing tier |
| `tinkr-stripe-integration` | 16 | Wire up Stripe Connect (v1.5 marketplace) |
| `tinkr-conversion-funnel` | 17 | Design / analyze the free → paid funnel |
| `tinkr-launch-checklist` | 18 | Pre-launch go/no-go (per A9 ship signal) |
| `tinkr-partner-pitch` | 5 | Vendor cold email (Espressif, Wemos, M5Stack) |

#### Meta + cross-axis (2)

| Skill | ID | Purpose |
|---|---|---|
| `tinkr-workflow` | 20 | The master orchestrator. Routes any task → skills. |
| `tinkr-kb-author` | 8 | KB entry generator (recipe, fact, error, pattern). Used across all axes. |

### Mavis built-ins used by Tinkr (19 total)

| Skill | Phase / Axis | Purpose |
|---|---|---|
| `code-review` | Build / Project | Pre-commit review |
| `init` | Build / Project | Bootstrap a new repo in tinkr-org/ |
| `plan-mode` | All | Plan before big features |
| `llm-call` | Build / Product | Test AI agent prompts |
| `skill-creator` | All | Build new skills |
| `skill-refiner` | All | Refine an existing skill with evidence |
| `deep-research` | Discovery / Product | Market / competitor / technology research |
| `ui-ux-pro-max` | Design / Product | Design intelligence (50+ styles, 97 color palettes) |
| `ui-ux-designer` | Design / Product | Design tokens, components, accessibility audit |
| `visual-page` | Design / Product | Marketing pages, docs site (NOT Tauri surfaces) |
| `pptx` | Grow / Monetization | Partner decks |
| `pdf` | Grow / Monetization | White papers, partner one-pagers |
| `docx` | Design / Product | Long-form docs (white papers, RFCs) |
| `xlsx` | Project | 8-week plan tracker, partner pipeline |
| `web_search` | Discovery | Verify a fact, find recent info |
| `web_fetch` | Discovery | Read a URL for evidence |
| `image_synthesize` | Design / Product | Marketing visuals (not Tauri surfaces) |
| `plugin-creator` | Build | Create MiniMax plugins (different from Tinkr plugins) |
| `create-agent` | All | Create a new Mavis agent (not a Tinkr user) |

### User-installed (3)

| Skill | Phase / Axis | Purpose |
|---|---|---|
| `tinkr-kb-author` | (Tinkr-specific, see above) | |
| `ui-ux-pro-max` | (Mavis user-installed copy) | |
| `ui-ux-designer` | (Mavis user-installed copy) | |
| `code-review` | (Mavis user-installed copy) | |

### Total active skill count: **37** (17 Tinkr + 19 Mavis built-ins + 3 user-installed, with 3 overlap = 36 unique + workflow orchestrator = 37)

---

## 5. The 3-axis matrix (Product × Project × Monetization)

This is the *second* way to slice the skill inventory. The phase is *what stage of work*; the axis is *what kind of work*.

| Axis | Question it answers | Skills |
|---|---|---|
| **Product** | "What are we building and why?" | `tinkr-spec-writer`, `tinkr-mockup-author`, `tinkr-trademark-check`, `tinkr-pricing-strategist`, `tinkr-roadmap`, `tinkr-plugin-author`, `tinkr-kb-author`, `ui-ux-pro-max`, `ui-ux-designer`, `visual-page`, `image_synthesize`, `docx`, `llm-call` |
| **Project** | "How do we build it well?" | `tinkr-decision-recorder`, `tinkr-changelog-writer`, `tinkr-week-planner`, `tinkr-test-author`, `tinkr-spec-check`, `tinkr-plugin-author` (scaffold), `code-review`, `init`, `plan-mode`, `xlsx`, `tinkr-launch-checklist` |
| **Monetization** | "How does it make money?" | `tinkr-pricing-strategist`, `tinkr-stripe-integration`, `tinkr-conversion-funnel`, `tinkr-launch-checklist`, `tinkr-partner-pitch`, `tinkr-roadmap`, `pptx`, `pdf` |

**The overlap is intentional.** `tinkr-pricing-strategist` is both Product (designing a tier) and Monetization (the tier itself). `tinkr-launch-checklist` is both Project (release process) and Monetization (verifying commerce). The axis tells you *why* you're using the skill, not *which* skill.

---

## 6. The daily / weekly / monthly rhythm

### Daily (during v1.0 build)

- 1 feature → `tinkr-spec-check` → commit
- 1 KB entry → `tinkr-kb-author` → commit
- 1 decision (if any) → `tinkr-decision-recorder` → update `decisions.md`
- 1 commit message → `tinkr-changelog-writer` (auto-generated)

### Weekly

- Monday: `tinkr-week-planner` for the week
- Friday: `tinkr-changelog-writer` for the week's changes
- Friday: review `decisions.md` for any new A-entries
- Friday: review the partner pipeline (`xlsx`)

### Monthly

- First Monday: review the 8-week plan via `tinkr-roadmap`
- Mid-month: review the monetization funnel (`tinkr-conversion-funnel`)
- End of month: review the KB growth, see which chips are most active
- Pre-launch month: `tinkr-launch-checklist` for the v-cut

---

## 7. The routing examples (concrete, end-to-end)

### Example 1: "Add support for the nRF52"

```
1. tinkr-workflow (orchestrator confirms chain)
2. deep-research (verify nRF52 chip families, MicroPython support, current users)
3. tinkr-roadmap (RICE it — probably 533, place in v1.5+)
4. tinkr-decision-recorder (record the "we will add nRF52 in v1.5" decision as A16 or higher)
5. tinkr-plugin-author (scaffold plugins/tinkr-nrf52/)
6. tinkr-test-author (generate tests for the scaffold)
7. tinkr-kb-author (author 2 facts + 1 recipe + 1 error for the nRF52)
8. tinkr-mockup-author (if there's a new Tauri surface)
9. tinkr-changelog-writer (generate CHANGELOG entry)
```

### Example 2: "Espressif didn't reply to my cold email"

```
1. tinkr-workflow (orchestrator confirms chain)
2. tinkr-partner-pitch (draft a follow-up with a new angle — same skill, different parameters)
3. (optional) deep-research (find Espressif's recent priorities — Matter, RISC-V, ESP32-C6)
4. xlsx (update the partner pipeline)
5. tinkr-decision-recorder (if we decide to abandon Espressif and try Wemos first)
```

### Example 3: "I just learned that the ESP32-C3 has a different flash address than the ESP32"

```
1. tinkr-workflow (orchestrator confirms chain)
2. web_search or tinkr-kb-author (verify the finding)
3. tinkr-kb-author (write a fact entry)
4. tinkr-plugin-author (if needed) to update plugins/tinkr-esp32/knowledge/chips/esp32c3.json
5. tinkr-changelog-writer (mention in the next release)
6. tinkr-decision-recorder (record the decision if it changes how the plugin detects the chip)
```

### Example 4: "I want to know what to do this week"

```
1. tinkr-workflow (orchestrator confirms chain)
2. tinkr-week-planner (given decisions.md, the 8-week plan, and recent commits, suggest 3-5 priorities)
3. (optional) tinkr-roadmap (for any feature that needs deeper prioritization)
4. (optional) plan-mode (for any feature that needs a deeper plan)
```

### Example 5: "I want to add a paid plugin marketplace. Should it be in v1.0 or v1.5?"

```
1. tinkr-workflow (orchestrator confirms chain)
2. deep-research (re-validate the gated-updates research)
3. tinkr-pricing-strategist (validate the 4-tier pricing model)
4. tinkr-decision-recorder (record the "marketplace in v1.5, not v1.0" decision if not already locked — it is, A2/A10)
5. tinkr-roadmap (place in v1.5 with RICE scoring — should be very high)
6. tinkr-stripe-integration (start the design now, ship in v1.5)
```

### Example 6: "I'm cutting v0.3.0 on Friday — am I ready?"

```
1. tinkr-workflow (orchestrator confirms chain)
2. tinkr-launch-checklist (run the v0.X.Y patch release checks)
3. tinkr-spec-check (final pre-commit hygiene)
4. tinkr-changelog-writer (generate the CHANGELOG entry)
5. tinkr-decision-recorder (if any decisions emerged during the cycle)
```

### Example 7: "I'm stuck. Help."

```
1. tinkr-workflow (orchestrator confirms chain)
2. tinkr-week-planner (where am I in the week?)
3. tinkr-roadmap (where am I in the release?)
4. plan-mode (if the user needs a structured brainstorm before any Tinkr skill)
5. (fallback) ask the user for context — what specifically are they stuck on?
```

---

## 8. The methodology is dynamic, not static

This document is a snapshot. As the project grows:

- New skills get added to the inventory (Section 4)
- The phase × axis matrix updates (Section 1, Section 5)
- The golden rules get refined (Section 3)
- The routing examples get more specific (Section 7)

**The dynamic part:** the AI agent (Mavis/MiniMax) reads the user's task, identifies the phase AND the axis, picks the right skill(s), and chains them. The agent also reads the user's context (what they're working on, what decisions are recent) to make smarter picks.

**How to update this doc:**

1. When a new Tinkr skill is added, append it to Section 4 and update Section 5 if it adds a new axis.
2. When a new standard chain emerges, append it to Section 7.
3. When the golden rules need a new principle, edit Section 3.
4. When the phase matrix needs a new row, edit Section 1.

**The doc is the long-form; `tinkr-workflow` SKILL.md is the executable.** Both stay in sync.

---

## 9. The user-facing summary

How you, the user (Ronie), use this:

1. **For any Tinkr task**, the AI agent (Mavis) reads this doc + the `tinkr-workflow` skill, identifies phase + axis, and proposes a chain.
2. **For specific questions** ("how should I price X?"), the agent invokes the relevant skill directly: `tinkr-pricing-strategist`.
3. **For stuck moments** ("what should I do this week?"), the agent invokes `tinkr-week-planner` first, then `tinkr-roadmap`, then falls back to asking.
4. **For launches**, the agent invokes `tinkr-launch-checklist` first — never announce without it.
5. **For monetization questions**, the agent invokes `tinkr-pricing-strategist` and `tinkr-conversion-funnel` together — they are two sides of the same coin.

The methodology is the rails. The skills are the engines. The AI agent is the conductor. The user is the audience — and the only one who can say "ship it" or "wait."

---

## Appendix A: The 8-week v1.0 plan → skill mapping

For each week of the build, the primary skills are:

| Week | Focus | Primary skills |
|---|---|---|
| 1 | Packaging refactor | `tinkr-spec-check`, `tinkr-test-author`, `tinkr-decision-recorder` |
| 2 | HAL + device abstraction | `tinkr-spec-writer`, `tinkr-plugin-author`, `tinkr-test-author` |
| 3 | Project deploy | `tinkr-spec-writer`, `tinkr-test-author`, `tinkr-kb-author` |
| 4 | REPL / monitor / plot | `tinkr-mockup-author`, `tinkr-test-author` |
| 5 | Tauri shell + MCP server | `tinkr-mockup-author`, `ui-ux-pro-max`, `tinkr-spec-writer` |
| 6 | AI agent (read-only + capture) | `tinkr-spec-writer`, `tinkr-kb-author`, `llm-call` |
| 7 | VS Code ext + TUI + CI + packaging | `tinkr-spec-check`, `tinkr-test-author`, `tinkr-changelog-writer` |
| 8 | Polish + public launch | `tinkr-launch-checklist`, `tinkr-changelog-writer`, `tinkr-partner-pitch` |

---

## Appendix B: The v1.5 marketplace workstream → skill mapping

| Workstream | Primary skills |
|---|---|
| Stripe Connect integration | `tinkr-stripe-integration`, `tinkr-pricing-strategist`, `tinkr-decision-recorder` |
| Plugin marketplace UI | `tinkr-mockup-author`, `ui-ux-pro-max`, `tinkr-spec-writer` |
| Managed AI tokens (MiniMax) | `tinkr-spec-writer`, `tinkr-decision-recorder`, `llm-call`, `tinkr-pricing-strategist` |
| Vendor first-party plugins (Espressif, Wemos) | `tinkr-partner-pitch`, `tinkr-plugin-author`, `tinkr-decision-recorder` |
| Conversion funnel | `tinkr-conversion-funnel`, `tinkr-pricing-strategist` |
| Marketplace launch | `tinkr-launch-checklist` (v1.5 mode), `tinkr-stripe-integration` (final test) |

---

## Appendix C: How to add a new Tinkr skill

1. Identify the gap: is there a workflow that recurs 3+ times without a skill? Add one.
2. Use the existing Tinkr skills as templates — they all follow the same structure (frontmatter, "When to use", step-by-step, anti-patterns, related skills, TL;DR).
3. Write the SKILL.md to `~/.minimax/skills/tinkr-<name>/SKILL.md`.
4. Register it in `~/.minimax/skill-hub.json` with a new ID, `source_type: 3`, `creator_info: {user_id: "local"}`.
5. Update Section 4 of this doc.
6. If it adds a new axis or phase, update Section 1 and Section 5.
7. If it creates a new standard chain, add to Section 7.
8. Commit the SKILL.md and the methodology update in the same commit.

The full Tinkr skill ecosystem should be self-documenting: this doc + the skill files + the decisions log form the complete picture of how Tinkr is built.
