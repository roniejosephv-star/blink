# Tinkr Agentic Orchestrator — Design Spec

> The Tinkr agentic orchestrator is the desktop app's primary surface. It's the "Mavis equivalent" for Tinkr — minimal, smart, agentic, observable. This spec is the architect's view: why the design is the way it is, what Mavis patterns we kept, what we changed, and how the observability problem gets solved.

---

## 0. Design DNA

This surface is built on 6 design principles — the brand's "calm + technical + cognitive + information-dense + local-first + instrument-like" DNA, paired with the **PREMIUM PRODUCT DESIGN MODE** rules (no AI-slop patterns: no purple/blue gradients, no glassmorphism, no excessive rounded cards, no giant hero sections, no decorative gradients, no meaningless dashboard metrics).

- **Calm** — no harsh flashes, no rapid motion, no loud colors. Restrained palette. Motion is purposeful, never decorative.
- **Technical** — looks like real test equipment (oscilloscope, logic analyzer, multimeter). PCB-style circuit mark, mono fonts, dot-grid backgrounds.
- **Cognitive** — shows what's happening. Not decoration, communication. The circuit's current direction = the agent's state.
- **Information-dense** — every pixel tells you something. No big empty hero sections. No decorative gradients. No card grids without purpose.
- **Local-first** — feels self-contained, doesn't depend on a network. The data is in the UI itself, not fetched from a "personalization API."
- **Instrument-like** — like a piece of test equipment, not a consumer app. Has readouts, has signals, has measurements.

**The test:** would a senior product designer at Linear, Notion, Figma, Stripe, Raycast, or Arc actually ship this? If not, refine.

---

## 1. Why this exists

The Tinkr v1.0 vision is a hardware IDE with an embedded agent. The agent is not a chatbot — it's the operator's co-pilot that:

1. Audits the project (state on disk, skills connected, decisions made, gaps to fix)
2. Plans the work (RICE-prioritized, aligned with the 8-week plan and `decisions.md`)
3. Executes (scaffolds plugins, generates specs, runs the KB author, commits)
4. Reports (every step visible, every change reviewable, every decision is an A-number)
5. Learns (every fix becomes a KB entry, every decision becomes an A-number)

The Mavis/MiniMax Code product already does (1)–(5) for general code. Tinkr's orchestrator is the same shape, but:
- **Specialized for hardware** — flashing, REPL, plugin manifests, KB facts about chips
- **Open-source by default** — every action is auditable, every change reviewable, every decision is an A-number
- **Project-as-memory** — the agent's context is the user's repo (decisions.md, brand spec, KB sample, plugins), not a session
- **Brand-consistent** — the **Tinkr circuit mark** is the agent's face; different operations get different current flows through the circuit

This spec defines the surface that makes those four differences visible.

---

## 2. The Mavis → Tinkr mapping

I studied the Mavis UI (screenshots, Aug 13 2026) to identify the patterns. Here's the mapping:

| Mavis pattern | Tinkr equivalent | What changes |
|---|---|---|
| Welcome dialog with "What's New" | Same, but with Tinkr feature callouts | Tinkr color tokens, Tinkr copy |
| Sidebar: Environmental Info, Progress, Deliverables, Agent team | Same 4 cards, same chevron interaction | Project card shows git branch + connected device; Deliverables shows the project-as-memory folders |
| Deliverables: file tree of `architecture/`, `brand/`, `knowledge-sample/`, `mockups/`, `blink-esp32/` | Same folders, but `blink-esp32/` → `tinkr-esp32/` (A12 rename) | `tinkr-` prefix, amber dot on the active item |
| Chat: "Thought 1 time(s) >" expandable | Same pattern, deeper expansion (see §5) | Adds the timeline view with READ/THINK/DECIDE/ACT/REPORT step types |
| Chat: Terminal command inline | Same, but with Tinkr CLI commands (`tinkr agent "..."`, `tinkr kb query ...`) | Tinkr cyan, JetBrains Mono, expandable output |
| Mavis logo as working indicator | **The Tinkr circuit mark with 11 animation states** (see §4) | The mark is a CIRCUIT, not letters. Current flows in 11 different patterns. |
| Status bar: brain + "Thinking" + model selector + send | Same layout, brand tokens | "Thinking" → uses violet, model selector shows `tinkr-pro / tinkr-mini / tinkr-micro` |
| Model selector: MiniMax-M3 / M2.7 / M2.7-highspeed + Thinking toggle | `tinkr-pro / tinkr-mini / tinkr-micro` + Deep thinking toggle | Tinkr naming follows the project vocabulary |
| Tab bar: Browser / Review / zsh / View File | Same — useful for inspecting the project as the agent works | Tinkr cyan active state |
| Review / diff viewer | Same — but for the per-action report (see §6) | Tinkr file/folder colors, brand typography |

**The patterns are preserved. The brand is Tinkr. The agent is the operator's co-pilot, not a generic chatbot.**

---

## 3. The brand mark — letters are out, circuit is in

The original brand spec called for `t●nkr` — 5 letters with a filled-amber dot for the "i." That was a fine wordmark, but it was *typography*. For a **hardware IDE**, the mark should be **a circuit** — and after 6 iterations (v1 letters → v2 5-node circuit → v3 dense PCB → v4 dynamic nodes → v5 organic Bezier paths → v6 visible traces → v7 PCB 45° + curved motion), the mark landed on the v7 trace network.

**The Tinkr v7 circuit mark:**

- **17+ visible traces** — bright cyan PCB routing with 45° chamfered corners (real chip layout, never Manhattan)
- **24 hollow pin circles** at trace ends — the I/O pads (stroked, not filled)
- **12 filled junction nodes** at trace crossings — the bridges between systems
- **10 dynamic data-packet nodes** flowing along **Bezier-curve motion paths** (never straight lines) — the operational signal
- **1 amber center LED** with halo — the brand heart, the only amber element by default
- **A radial-gradient PCB substrate background** — the dark `#050810` → `#0A1628` glow under the network

The trace network is fixed in shape. What changes between states is the **node flow** — which nodes are visible, what color they are, how fast they move, what Bezier path they follow.

**Why a PCB trace network (v7):**
- It's the literal visual metaphor for a hardware product — a real chip's routing
- The hollow pins (I/O) and filled junctions (bridges) encode information that letters never could
- The 10 dynamic nodes show **directional motion** through the lines, like a logic analyzer watching signals
- It looks like real test equipment — like an oscilloscope, a logic analyzer, a multimeter — not a logo
- The traces are VISIBLE (v7) so the network itself is the design, not just a frame for the nodes

**The text "tinkr"** still exists as a wordmark in mono font for use in dense layouts (chat headers, document titles, install commands). But the **primary visual mark is the circuit trace network.**

The implementations are in `brand/mockups/13-wordmark-animations.html` (the 11 states grid) and `brand/02-visual-identity.md` (the formal spec).

---

## 4. The 11 circuit states — operational signals

| # | State | What happens in the v7 circuit | When |
|---|---|---|---|
| 1 | **idle** | All 10 nodes flow along curved Bezier paths (3.6s, smooth). Cyan + amber mix. Center LED pulses 1Hz. | Default — agent is ready |
| 2 | **thinking** | All 10 nodes flow faster (2.2s, bouncy `cubic-bezier(0.34, 1.56, 0.64, 1)`). Center pulses 2Hz. | Model is reasoning |
| 3 | **reading** | Only the left-side nodes (1, 3, 4, 5, 7) flow at 2.4s. Right side dormant. Signal arriving from the left. | File read in progress |
| 4 | **writing** | Only the right-side nodes (2, 3, 4, 6, 10) flow at 2.4s. Left dormant. Output emanating to the right. | Streaming response |
| 5 | **searching** | All 10 nodes flow fast (1.8s). Full network sweep. The agent is alive everywhere. | KB / plugin / web search |
| 6 | **flashing** | All nodes + traces + pins turn amber. Center strobes amber↔cyan at 0.3s. The shipping moment. | Firmware is flashing |
| 7 | **compiling** | All 10 nodes with staggered delays (0.3s apart). Sequential activation along the network. | Build in progress |
| 8 | **done** | All nodes + traces + pins turn green. Bouncy 1.6x pop on the center LED. One-shot, then settles. | Task complete |
| 9 | **error** | All nodes + traces + pins turn red. Bouncy `cubic-bezier(0.68, -0.55, 0.27, 1.55)`. Center pulses on the error frame. | Action failed |
| 10 | **waiting** | Only 3 nodes flow, very slowly (6s). Everything dims to 60% opacity. Awaiting the human. | Awaiting user input |
| 11 | **ship** | All nodes + traces + pins turn bright amber. Bouncy. Center LED flashes 2x then settles into a glow. | Hardware deployed — closed ingredient |

**Why this matters for observability:**
- **Direction = operation.** Which nodes are flowing tells you what the agent is doing (left-only = reading, right-only = writing, all-fast = searching).
- **Color = status.** Cyan = working, amber = flashing/ship, green = done, red = error, dim = waiting, white = idle.
- **Speed = urgency.** 3.6s = idle, 2.2s = thinking, 1.8s = searching, 1.4s = error, 1.2s = flashing/ship, 6s = waiting.
- **Spread = scope.** All-10-pulse = full reasoning. 5-pulse = directional. 3-pulse = passive. Single LED = local action.

The user can read the mark at a glance, like a logic analyzer trace on a real PCB. No need to look at the text.

All animations are pure CSS (no Lottie, no GIFs, no JS animation libraries). The dynamic nodes use `offset-path` with Bezier-curve motion paths (`Q` and `T` commands) to flow along the visible traces organically — never straight lines.

---

## 5. The Thought expansion — observability solved

The "Thought 1 time(s) >" in the main chat is the entry point. When the user clicks it, the timeline expands. This is the **observability layer** — the agent's reasoning is not a black box.

### 5 step types

Each step in the timeline has a type, indicated by a colored node and badge:

- **READ** (blue) — file read or KB query. Shows the command, the result.
- **THINK** (violet) — model reasoning. Shows the summary, no raw tokens.
- **DECIDE** (amber) — a branch the user can override. Shows the decision options.
- **ACT** (cyan) — file change, command run, external call. Shows the diff.
- **REPORT** (green) — generated artifact the user reviews. Shows the artifact summary.

The timeline is a vertical line with circular nodes. Each step has a number, a type badge, a title, and a body. The body can be expanded for details (mockup 14 shows the inline diff).

### Why this solves observability

- **No "what is the agent doing?"** — every step is visible, with a type and a status
- **No "where did this change come from?"** — every ACT step has a diff
- **No "why did the agent pick this?"** — every DECIDE step has the options shown
- **No "is it still working?"** — the active step has the working animation (state 2, 4, 5, 6, or 7)
- **No "is the work right?"** — the REPORT step is the summary, the user reviews before approving

The user can also click any step to expand it inline (mockup 14 shows the ACT step with a diff preview).

---

## 6. The action report — review every change

After a "Thought" finishes, the user gets the **action report** (mockup 15). This is the "can go and review the report for each actions" surface.

### 5 tabs

1. **Changes** — the file diffs, one row per file. Each row has an approve/reject button. Default: approve.
2. **Brand & docs** — the brand deck, README, and other doc surfaces that the change affects. Approving here updates those docs in the same commit.
3. **KB entries** — any new KB entries the agent created. Edit before approving.
4. **Decisions** — any new A-numbers the agent wants to record. Approve, reject, or edit.
5. **Raw log** — the full tool-call log, for debugging.

### The "update the brand deck" moment

The user explicitly asked: "update the band deck and necessary documents." The **Brand & docs** tab is the answer. When the agent's change affects a doc surface, it shows up in this tab with a "will update on approve" indicator. The user can:

- See which docs will change
- Approve the doc update in one click
- Edit the proposed doc change inline before approving
- Open the doc in the repo for the full context

This is the "trust the community" principle (A6) in practice: every doc change is reviewable, never silent.

### The bottom action bar

A sticky action bar at the bottom shows: progress (`1 of 5 approved`), pending decisions, and the two final actions: "Pause — let me review" or "Approve all". No surprising commits, no silent updates.

---

## 7. The right panel — model + reasoning + run metrics

The right panel has 3 cards:

1. **Model** — `tinkr-pro` (deep), `tinkr-mini` (default), `tinkr-micro` (fast). Selecting changes the next turn's model.
2. **Reasoning** — three toggles: "Deep thinking" (more tokens, more reasoning), "Show commands" (inline terminal display), "Auto-report" (auto-open the action report after each turn).
3. **This run** — per-turn metrics: turns, tools called, files read, decisions, cost. Updates in real time.

The model selector and toggles are persistent (per-user), not per-turn. The "This run" metrics reset each turn.

---

## 8. The Deliverables panel — project-as-memory, made visible

The sidebar's "Deliverables" card is the user's project tree. This is the project-as-memory model (per the architecture spec) made visible in the UI.

Each folder in the tree maps to a part of the user's project:

| Folder | What it is | Tinkr's role |
|---|---|---|
| `architecture/` | 14 design docs + decisions + methodology | The "what we're building" surface |
| `brand/` | 6 brand docs + 15 mockups | The "what it looks like" surface |
| `knowledge-sample/` | KB facts, errors, recipes, patterns, schemas | The "what we know" surface |
| `mockups/` | All Tauri surface mockups | The "what's shipping" surface |
| `tinkr-esp32/` (was `blink-esp32/`) | First plugin, 19 files | The "proof it works" surface |

The Deliverables panel is the entry point for the agent's "audit the project" command. Clicking any file opens it in the right pane (via the View File tab).

---

## 9. The 8 hard brand rules + PREMIUM PRODUCT DESIGN MODE

| Rule | How this design applies it |
|---|---|
| 1. **CLI is first-class surface** | Every screen has a CLI equivalent in the footer. The chat is a thin UI over `tinkr agent "..."` — the same Tinkr CLI that runs headless. |
| 2. **Light + dark equal** | Every mockup has a `data-theme="light"` toggle. Default is dark (per A2/visual-identity). |
| 3. **No marketing speak** | Copy is lowercase, direct, present tense. No "Welcome to the future of hardware!" |
| 4. **WCAG 2.1 AA floor** | All text passes 4.5:1 on both themes. Cyan is never body text on light. |
| 5. **Accent is amber** | The LED dot, the primary CTA, the focus ring — all `#FB923C`. Cyan is for headings/links. |
| 6. **Inter + JetBrains only** | All UI in Inter, all code in JetBrains Mono. No other fonts loaded. |
| 7. **Line icons no emoji** | All icons are inline SVG (Lucide-style). No 🚀🔥💡 anywhere. |
| 8. **Open source by default** | Every surface has an "open in repo" link. Every change is a git commit. Every decision is an A-number. |

**Plus the "PREMIUM PRODUCT DESIGN MODE" additions** (Aug 13 brand update):
- **No AI-slop patterns** — no purple/blue gradients, no glassmorphism, no excessive rounded cards
- **Calm + technical + cognitive + information-dense + local-first + instrument-like** — the design DNA
- **No decorative elements** — every component serves a user purpose
- **Senior product designer test** — would a designer at Linear, Notion, Figma, Stripe, Raycast, or Arc ship this?
- **Subtle dot-grid backgrounds** for the "instrument-like" feel
- **Mono fonts for data** (counts, IDs, paths, statuses)
- **Flat surfaces with thin borders** (no decorative shadows)
- **Asymmetric layouts where appropriate** (e.g., the 5-tab Action Report with the right rail summary)

---

## 10. Implementation plan

### v1.0 (this is a v1.0 surface)

- Tauri shell with the 3-column layout (sidebar / chat / right panel)
- Tinkr circuit mark in 11 states (CSS keyframes, see mockup 13)
- Chat interface with Thought expansion (mockup 14)
- Action report with 5 tabs (mockup 15)
- Deliverables panel (file tree, mockup 12)
- Model selector + reasoning toggles + run metrics
- `tinkr agent "..."` CLI command as the headless equivalent

### v1.5 (with marketplace + Stripe)

- Plugin marketplace integrates with the right panel ("Agent team" card shows installed plugins)
- Managed AI tokens (A13) wired to the model selector
- Cloud sync status in the right panel
- Creator dashboard reuses the Action Report pattern (the creator sees the same review surface for their plugin's updates)

### v2.0 (with simulator + teams)

- Sim state in the right panel (a "Sim" card shows the current Wokwi session)
- Team workspaces in the Deliverables panel (multi-user folders)
- Shared action reports (the whole team can review and approve)

---

## 11. The 4 mockups

| # | File | What it shows |
|---|---|---|
| 12 | `brand/mockups/12-agentic-orchestrator.html` | The main view — sidebar, chat, right panel |
| 13 | `brand/mockups/13-wordmark-animations.html` | The 11 circuit animation states (the new v2 mark) |
| 14 | `brand/mockups/14-thought-expansion.html` | The Thought expansion — the observability timeline |
| 15 | `brand/mockups/15-action-report.html` | The Action Report — the per-action review surface |

All 4 are brand-compliant (8 hard rules + design DNA), standalone HTML files, and match the existing 11 mockups in style.

---

## 12. Open questions (for the user)

These came up while designing. Need decisions before v1.0 implementation:

1. **Model names**: `tinkr-pro / tinkr-mini / tinkr-micro` — confirm or rename?
2. **Default model in v1.0**: which one is on by default? (Recommend: `tinkr-mini`)
3. **BYO key in v1.0**: how does the user supply their own key? (A13 — Anthropic / Gemini / MiniMax, env var or settings panel)
4. **Auto-report on/off default**: should the action report auto-open after every turn, or only on demand?
5. **Decision override UX**: when the agent hits a DECIDE step, should the chat pause for the user?
6. **Circuit mark everywhere?** — the circuit mark is the primary visual, but in some dense contexts (e.g., chat header breadcrumbs) the text wordmark `tinkr` is more readable. Confirm both are acceptable.

---

## 13. Related

- `brand/01-positioning.md` — the Tinkr positioning
- `brand/02-visual-identity.md` — the circuit mark v2 (updated Aug 13), colors, type, motion
- `brand/03-design-tokens.json` — the 152 design tokens
- `brand/04-component-library.md` — the 12 component specs
- `architecture/decisions.md` — A1-A18, the locked decisions
- `architecture/tinkr_development_methodology.md` — how the agentic orchestrator is built
- `architecture/v1_week1_packaging_refactor.md` — the Week 1 build plan

The agentic orchestrator is the user-visible expression of everything in the architecture. Every spec doc, every decision, every KB entry feeds into the chat. The Tinkr agent knows the project because the project is its memory.
