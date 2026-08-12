# Tinkr Decisions Log — Single Source of Truth

> All decisions made in the Aug 12, 2026 architecture session. This is the canonical record. Update this when a decision changes. The user_profile memory and the synthesis report are summaries; this is the full log.

---

## A. Locked Decisions (Aug 12, 2026 evening)

| # | Decision | Choice | Why |
|---|---|---|---|
| A1 | Auth at install | **GitHub + email both, GitHub preferred** | GitHub is the developer identity; email is the hobbyist identity. Both paths; GitHub unlocks power-user features. |
| A2 | Vendor first-party plugins | **v1.5 (not v1.0)** | v1.0 ships 4 free plugins only. Vendor partnerships (Espressif first) launch with the marketplace in v1.5. |
| A3 | Simulator | **v2.0** | Real hardware only for v1.0. Sim is v2.0. For v1.0, a "verify in Wokwi" deep-link is the bridge. |
| A4 | Free plugin projects per user | **4 free per user** | Plugin creators can ship 4 plugins free. After that, the 5th is paid. Aligns with the creator economy. |
| A5 | Free sim projects per user | **4 free per user (in v2.0)** | When sim ships, sim is free. Hardware deploy is always paid. |
| A6 | "Stays true to contributions" contract | **3-clause agreement, codified in marketplace terms** | Clause 1: contributor retains authorship/IP. Clause 2: Tinkr may broadcast updates, not modify. Clause 3: unmaintained plugins marked, not taken over. |
| A7 | Open-source from day one | **MIT-licensed core** | Trust requires openness. The "lifetime" pricing only works because plugins are git repos. |
| A8 | Launch partners (v1.5) | **Espressif + Wemos in parallel; M5Stack via Espressif.** | **⚠️ SUPERSEDED Aug 12 evening:** Espressif acquired M5Stack in April 2024. Two independent partner conversations with the parent and subsidiary looks uninformed. Lead with Espressif (covers ESP32 + M5Stack ecosystem), run Wemos in parallel. Wemos is the market-honesty backup — they're the most maker-friendly. **NOT** Adafruit (owns CircuitPython) or Raspberry Pi (Thonny relationship). |
| A9 | Ship signal for v1.0 | **100 installs + 5 plugins + 50 KB entries + <5 critical bugs + 2-min Loom demo** | Not "all features done" — "good enough that I'd tell my mom to use it." |
| A10 | Platform cost renewals | **All 4 tiers, integrated**: Tinkr Pro subscription + per-plugin annual update fees + creator program annual fee + project cloud hosting. Research similar creator / maker market implementations to design it. | Multi-axis pricing matches a multi-persona product. Research makes the onboarding smooth for creators and makers. |
| A11 | Argus integration | **Argus is a prototype repo. Develop it into Tinkr directly.** The `tinkr-rpi5` plugin absorbs the argus architecture. The argus repo becomes a reference / proof-of-concept; production code lives in `tinkr.cli/plugins/tinkr-rpi5/`. | Argus isn't a shipped product — it's a test repo. The real ship is the tinkr plugin. |
| A13 | AI features | **BYO API key in v1.0; managed tokens via MiniMax partnership in v1.5+** | Initial supported providers: Anthropic, Gemini, MiniMax. The free product has full AI capability from day 1 because the user pays the AI provider directly. Edge doesn't pay inference costs in v1.0. The MiniMax partnership (parent company of Mavis) enables a managed token plan in v1.5+ for users who don't want to manage their own key. This is the Continue.dev / Cline / Aider pattern: BYO key, closed ingredient for the paid tier, no artificial AI limits on the free tier. |
| A14 | Hardware deploy | **Paid (pay-per-flash OR bundled in Pro). NOT in v1.0 free tier.** | The "shipping" moment is the value-capture point. Real hardware deploy (esptool flash, network deploy) is the closed-ingredient feature. v1.0 ships with sim-only (v2.0 sim) and BYO-AI development. The first hardware deploy experience happens in the Pro subscription or via pay-per-flash. This captures value at the moment of "shipping to silicon" without gating features the free tier has always had. |
| A15 | Open-source resource model | **Unlimited KB / recipes / patterns / projects. The "open source" is the moat, not the catalog.** | The free tier allows unlimited contributions to the KB, unlimited project templates, unlimited recipe creation, unlimited plugin installation (subject to A4's 4-plugin-projects-per-user cap on authoring). Every user contributes, the platform gets smarter with updates (more KB entries → better AI suggestions → better diagnostics → more value). This is the "stays true to contributions" 3-clause contract (A6) in practice: contributor retains IP, the platform broadcasts updates, the project grows. |
| A16 | Primary domain | **`tinkr.build`** (selecting this; `tinkr.dev` rejected) | `.build` TLD matches the project-as-memory model and the verb-driven brand. `tinkr.dev` was registered by a third party (likely investor-parked) — not worth acquiring; pivot to `.build` instead. Primary use: marketing site at `tinkr.build/`, docs at `docs.tinkr.build/`, marketplace at `marketplace.tinkr.build/`, telemetry at `telemetry.tinkr.build/`. Email format: `user@tinkr.build`. Backup: `tinkr.sh` for the one-line install script (`curl -L tinkr.sh | sh`) if a separate install surface is wanted later. |
| A17 | Agentic Orchestrator UI | **The "Mavis equivalent" for Tinkr — modeled on the Mavis/MiniMax Code chat + sidebar + status pattern, re-skinned with the t●nkr wordmark, cyan/amber tokens, and the 8 hard brand rules. 4 new mockups shipped (12–15).** | The wordmark `t●nkr` is the agent's face — 11 animation states (idle, thinking, reading, writing, searching, flashing, compiling, done, error, waiting, ship) replace Mavis's single brain icon. The "Thought N time(s) >" pattern is expanded into a 5-step-type timeline (READ / THINK / DECIDE / ACT / REPORT) — the observability layer. After each Thought, an Action Report with 5 tabs (Changes / Brand & docs / KB / Decisions / Raw log) gives the user per-action review with an explicit "Brand & docs" surface for updating the brand deck and necessary documents. Headless CLI equivalent: `tinkr agent "..."`. Full design rationale at `architecture/agentic_orchestrator.md`. |
| A18 | Brand Mark v7 (PCB Trace Network) | **The Tinkr mark is a visible PCB trace network — 17+ bright cyan traces with 45° chamfered corners (real PCB routing, never Manhattan), 24 hollow pin circles at trace ends (the I/O pads), 12 filled junction nodes at intersections (the bridges), 10 dynamic data-packet nodes flowing along Bezier-curve motion paths (never straight lines), and 1 amber center LED with halo (the brand heart). The mark's shape is fixed; only the node flow, color, and speed change across 11 operational states.** | Iterated from v1 (letter wordmark `t●nkr`) through v6 (visible traces) to v7 (PCB 45° + curved motion paths). The PCB trace network makes the brand read as a real chip's routing — a logic analyzer watching signals — which matches the "instrument-like" design DNA. The 5 hard rules of v7: (1) no straight lines for node motion (Bezier only), (2) 45° chamfered corners on all traces, (3) hollow circles at every trace end, (4) filled circles at every crossing, (5) amber center LED + halo only. All 15 mockups updated to use the v7 mark. |
| A19 | v1.0 Implementation Plan (8 weeks) | **The 8-week v1.0 build is locked: Week 1 = pack & rename, Week 2 = 4 free plugins, Week 3 = 50 KB entries, Week 4 = project memory + capture layer, Week 5 = MCP server + headless AI, Week 6 = Tauri shell, Week 7 = brand v7 sweep + polish, Week 8 = 2-min Loom + ship.** | Lives at `architecture/implementation_plan.md`. Each week has a hard gate; the v1.0 ship signal is the A9 gates all green (100 installs + 5 plugins + 50 KB entries + <5 critical bugs + 2-min Loom). No v1.5 work begins until Week 8 ships. v1.5 backlog (Stripe, vendor first-party, tinkr-rpi5, managed AI tokens, hardware deploy) is queued for the Monday after ship. |
| A20 | Skill Ecosystem (24 Tinkr skills) | **The Tinkr skill ecosystem has 24 skills in `~/.minimax/skills/tinkr-*/` — 17 from the prior rounds (trademark, partner-pitch, plugin-author, spec-check, kb-author, decision-recorder, changelog-writer, week-planner, test-author, spec-writer, mockup-author, pricing-strategist, stripe-integration, conversion-funnel, launch-checklist, roadmap, workflow) + 7 new ones added in this turn (rename-sweep, packaging-refactor, cli-developer, kb-curator, tauri-builder, mockup-v7-migrator, v1-ship-runbook).** | The 7 new skills map 1:1 to the 8-week plan: rename-sweep + packaging-refactor = Week 1, plugin-author = Week 2, kb-curator = Week 3, cli-developer = Weeks 4-5, tauri-builder = Week 6, mockup-v7-migrator = Week 7, v1-ship-runbook = Week 8. `tinkr-workflow` is the conductor that routes between them. Skill registration: `~/.minimax/skill-hub.json` IDs 21-27. |
| A12 | Product name | **`Tinkr`** (revised from `Blink` on Aug 12 evening) | "Tinkr" — the maker verb with creative spelling. Fanciful in trademark terms; no class 9/42 holder. Pairs with "Tinker on." tagline. CLI command is `tinkr`; package is `tinkr-cli` (bare `tinkr` is taken on PyPI by an unrelated AI observability tool). GitHub org `tinkr-org/`. Wordmark `t●nkr` (amber dot replacing the "i"). |
| A12b | Tagline | **"Tinker on."** (revised from "Build it." on Aug 12 evening) | Two-word imperative. Persona-broad, pairs with `tinkr` wordmark. No trademark risk (entirely generic). The earlier "Be Bob the builder" was flagged for HIT/Mattel; the name change from Blink → Tinkr required a corresponding tagline update. |

---

## B. Pricing Model (in progress — see "Platform Cost Renewals" question)

### Confirmed tiers
- **4 free plugins** (bundled with the IDE, open-source): ESP32, RP2040, nRF52, MicroPython runtime
- **4 free sim projects per user** (v2.0)
- **4 free plugin projects per user** (creator side)
- **Paid plugins**: $5-$30 one-time, lifetime, re-downloadable
- **Maker Bundle**: $49 lifetime (all current + future plugins)
- **Pro Bundle**: $199 lifetime (all plugins + priority support + cloud features when they exist)
- **Team Bundle**: $499/year (5 seats + dedicated support)
- **Creator revenue split**: 70% author / 30% Tinkr (for paid plugins)
- **Vendor first-party**: vendor sets price, Tinkr takes 30%

### Open: "Platform cost renewals" — RESOLVED (A10)
**All 4 tiers, integrated.** The pricing model covers all four angles simultaneously:

| Tier | What it covers | How it works |
|---|---|---|
| **Tinkr Pro subscription** | $X/year for advanced features (CI builds, cloud sync, team features, priority support) | Stripe / Paddle recurring billing |
| **Per-plugin annual update fee** | Plugins are $5-$30 one-time for v1.0, but updates after the first year are paid | SaaS twist on lifetime; gives authors recurring revenue |
| **Creator program annual fee** | Plugin authors pay $Y/year to be in the curated marketplace | Filters spammers, funds curation team |
| **Project cloud hosting** | Local-first is default; cloud-synced projects cost $Z/year | Breaks pure local-first but is a clear SaaS tier |

**Plus**: research similar creator / maker market implementations (Patreon, Gumroad, Substack, Tindie, Etsy, Shopify, App Store, VS Code Marketplace, npm Pro, GitHub Sponsors) to design smooth onboarding for creators. Specifically: how do creators and makers connect to the market, get paid, find their audience? Use the lessons to make Tinkr's onboarding friendly.

### Open: Argus integration — RESOLVED (A11)
**Argus is a prototype repo, not a shipped product. Develop it into Tinkr directly.**

The `tinkr-rpi5` plugin absorbs the argus architecture:
- argus's `profiler.py` → `tinkr-rpi5`'s `profile` capability
- argus's `assess.py` → `tinkr-rpi5`'s `tier_assessment` capability
- argus's `optimizer.py` → `tinkr-rpi5`'s `generate_config` capability
- argus's `mcp/server.py` → `tinkr-rpi5`'s sub-MCP
- argus's `safety/` → tinkr's HAL safety model
- argus's `state/` → tinkr's project memory

The argus repo at `/Users/mindflow/Projects/Hackathon/Arm Create/argus` becomes a **reference / proof-of-concept**. The production code lives in `tinkr.cli/plugins/tinkr-rpi5/`. The argus README's `argus-pi4` MCP-over-SSH pattern is the template for the plugin's deployment flow.

**Migration plan**:
- Week 1 of `tinkr-rpi5` development: copy argus's `core/profiler.py` and `core/assess.py` into the plugin's `adapters/` and `cli/`. Adapt the entry points to match the Tinkr CLI contract.
- Week 2: rewrite the MCP server as a sub-MCP of the Tinkr MCP server. Same tools, but registered with `tool_prefix = "rpi5"`.
- Week 3: write the deploy flow (argus doesn't have one — that's new Tinkr work).
- Week 4: tests, KB entries, ship as v1.5 plugin.

---

## C. Product Model

### v1.0 (8 weeks) — open-source CLI
- CLI only (Tauri shell deferred)
- 4 free plugins (ESP32, RP2040, nRF52, MicroPython runtime)
- GitHub-based plugin discovery (no marketplace yet)
- GitHub + email auth (both, GitHub preferred)
- Agent (read-only of project memory + device state)
- Capture layer (local-only; v0.5 ships GitHub submission)
- 50 hand-curated KB entries (Tinkr team)
- Ship signal: see A9

### v1.5 (4-6 months later) — add marketplace
- `tinkr plugin marketplace` subcommand (search, buy, install)
- Stripe Connect / Paddle for payments
- Plugin Author Dashboard (sales, payouts, KB usage)
- 70/30 revenue split
- "Maker Bundle" and "Pro Bundle" upsells
- `tinkr-rpi5` plugin (wraps Argus)
- Vendor first-party plugin (`tinkr-espressif`)

### v2.0 (12 months later) — creator program
- Plugin Author Program (anyone publishes, earns 70%)
- Hardware Partner Program (vendors ship first-party)
- Optional: hardware marketplace (Tindie partnership)
- "Verified Creator" badge
- "blend of simulator + real hardware" (sim v2.0 shipped)
- `tinkr-jetson` and `tinkr-arm-mac` plugins

### v3.0 (18+ months) — agentic self-extension
- Constrained self-extension within plugins (the real Loop 2, in its proper form)
- AI agent that writes plugin tools with human review
- Tindie hardware marketplace (optional)
- Vendor Partner Program (expanded)

---

## D. Architecture (the 6 design docs)

| Doc | Purpose | Status |
|---|---|---|
| `tinkr_synthesis_report.md` | Top-level synthesis of the original plan | Done |
| `plugin_spec.md` | Plugin package spec (manifest, structure, build/publish) | Done |
| `hal_design.md` | HAL common layer (device, capability, adapter) | Done |
| `project_memory.md` | Project-as-memory design | Done |
| `learning_loop.md` | The 4 feedback channels + curated KB + release process | Done |
| `capture_layer.md` | The "just by building in it" capture system | Done |
| `product_analysis.md` | Honest analysis of the business model + 10 smart implementations | Done |
| `argus_integration.md` | How Tinkr wraps Argus for RPi / Jetson / Arm-Mac | Done (this update) |
| `decisions.md` | This file — the single source of truth | Done (this update) |

---

## E. Open Questions — RESOLVED (this update)

### E1. "Platform cost renewals" — RESOLVED (A10)
**All 4 tiers, integrated.** Multi-axis pricing matches a multi-persona product.

| Tier | What it covers | Mechanism |
|---|---|---|
| Tinkr Pro subscription | CI builds, cloud sync, team features, priority support | Stripe / Paddle recurring |
| Per-plugin annual update fee | Plugins $5-$30 one-time for v1.0; updates after year 1 are paid | SaaS twist on lifetime |
| Creator program annual fee | Plugin authors pay $Y/year to be in curated marketplace | Filters spammers, funds curation |
| Project cloud hosting | Local-first default; cloud-synced projects cost $Z/year | Breaks pure local-first but is a clear SaaS tier |

Plus: research spawned on creator/maker market implementations to design smooth onboarding.

### E2. Launch partner approach — RESOLVED (A8)
**Approach all three in parallel**: Espressif, Wemos, M5Stack. First to say yes becomes the launch partner.

### E3. Argus integration — RESOLVED (A11)
**Argus is a prototype, not a shipped product. Develop it INTO Tinkr directly.** The argus repo becomes a reference / proof-of-concept. Production code lives in `tinkr.cli/plugins/tinkr-rpi5/`. Migration is a 4-week absorption of argus's architecture.

### E4. Argus + Tinkr brand?
Argus is now a reference, not a co-product. No brand confusion.

### E5. Where to incorporate? — PENDING
Australia, Canada, UK, Singapore, US, Germany. Will dispatch a research agent when the brand work + creator research finishes.

### E6. New: Creator / Maker market research
- Spawned research agent to study Patreon, Gumroad, Substack, Tindie, Etsy, Shopify, App Store, VS Code Marketplace, npm Pro, GitHub Sponsors, Arduino Library Manager, etc.
- Goal: design smooth onboarding for Tinkr creators and makers
- Output: `architecture/creator_marketplace_research.md`

---

## F. What we built (artifacts on disk)

### Architecture (8 docs)
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/tinkr_synthesis_report.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/plugin_spec.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/hal_design.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/project_memory.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/learning_loop.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/capture_layer.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/product_analysis.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/argus_integration.md`
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/implementation_plan_review.md` (the original architect agent's review)
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/decisions.md` (this file)
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/rust_platform_design.md` (existing)

### Reference plugin
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/plugins/tinkr-esp32/` — the first plugin, 19 files, ~3000 LoC of real working code

### Knowledge sample
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/architecture/knowledge-sample/` — 2 facts, 2 errors, 1 pattern, 1 recipe, 3 JSON schemas, working query tool + capture demo

### Brand spec (in progress, 2 agents working)
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/brand/` — being created
- `/Users/mindflow/Projects/Tinkr/tinkr.cli/brand/mockups/` — being created

---

## G. Decision history (chronological)

| Time | Decision | Why |
|---|---|---|
| Aug 12 14:30 | Original 5-Loop plan (Tauri + React + AI self-growing) was the user-supplied input | The starting point |
| Aug 12 14:45 | Architect agent: plan ignores 5 load-bearing artifacts; should keep existing 12 Python tools | Save 3-4 weeks of work |
| Aug 12 15:00 | 4 deep-research agents dispatched: Tauri feasibility, AI tool registry, 3D sim, architect review | Evidence-based decisions |
| Aug 12 15:30 | User clarified: 3 personas, project-as-memory, lightweight, community plugin ecosystem, building factory | Sharper vision than the original 5-Loop plan |
| Aug 12 16:00 | Plugin spec, HAL design, project memory design shipped | The 3 new design docs |
| Aug 12 16:30 | Reference `tinkr-esp32` plugin shipped | First product, proves the spec |
| Aug 12 17:00 | User: "How does Tinkr get smarter?" | Knowledge accumulation design |
| Aug 12 17:30 | Learning loop design + KB sample + capture layer + product analysis | 4 more design docs |
| Aug 12 18:00 | User asked 10 questions; gave 4 answers, deferred 6, asked for honest pushback | Locked items 3, 4, 5, 6, 8, 9, 10 |
| Aug 12 18:15 | Pushed back on: 4 free projects interpretation, RPi/Jetson scope, "stays true" contract, launch partners | Honest critique |
| Aug 12 18:20 | User confirmed: 4 free projects interpretation, RPi/Jetson v1.5, "stays true" contract, Espressif + Wemos/M5Stack, asked for UI/UX work | Locked items |
| Aug 12 18:25 | Discovered argus (Ronie's existing RPi work) | Integrates perfectly |
| Aug 12 18:30 | 2 UI/UX agents dispatched in background | Brand spec + mockups |
| Aug 12 18:40 | UI/UX agents landed brand spec + 5 mockups | Brand is real; mockups have a #22D3EE vs #5EEAD4 color conflict |
| Aug 12 18:50 | Re-skinned 5 mockups to #5EEAD4; tagged with brand token reference | Mockups now match brand spec; design tokens drive both |
| Aug 12 18:55 | Tagline locked: "Tinker on" + trademark flag added | Persona-broad, trademark check queued |
| Aug 12 19:00 | Tagline revised: "Tinker on" → "Tinker on." | Trademark question closed; stronger two-word line; pairs with wordmark |
| Aug 12 19:00 | Launch-partner strategy revised: Espressif + Wemos in parallel, M5Stack via Espressif | Found Espressif acquired M5Stack April 2024; original "3 independent" plan was uninformed |
| Aug 12 19:05 | Incorporation research landed: 13K-word, 6-jurisdiction comparison | SG Pte Ltd = best tax; DE C-Corp = best VC; explicit India-founder notes (Mercury rejection, FEMA ODI, GIFT City no-go) |
| Aug 12 19:10 | UI scope locked: full Tauri app, 6 new mockups | Spawn 3 parallel agents: device/REPL, KB/plugin-dev, project/settings |
| Aug 12 19:20 | 3 UI agents completed: 6 new mockups on disk | All 11 mockups re-skinned to brand cyan; brand README updated |
| Aug 12 20:00 | Trademark + domain check on "Blink" | **CRITICAL FINDING:** Amazon owns "BLINK" in class 9/42 (security cameras). Forced rename. |
| Aug 12 20:30 | Considered "Edge" as replacement | Microsoft owns "Microsoft Edge"; "edge" is descriptively generic. Rejected. |
| Aug 12 21:00 | Considered "Block" as replacement | Block, Inc. (Jack Dorsey) owns the brand, 30+ live applications. Rejected. |
| Aug 12 21:30 | Considered "Faber" as replacement | Faber-Castell class 9/16 with active enforcement. Coexistence letter possible but expensive. Rejected for now. |
| Aug 12 22:00 | Considered "Flink" as replacement | Apache owns "FLINK" in class 9 EXACT match (Reg #5020107, 2016). Rejected. |
| Aug 12 23:00 | **Product name locked: "Tinkr"** | Fanciful, no major class 9/42 holder. Trademark + domain check passed. Tagline updated to "Tinker on." to pair. Brand sweeping all docs. |
| Aug 12 23:15 | **AI model locked:** BYO API key (Anthropic, Gemini, MiniMax) for v1.0; managed tokens via MiniMax partnership for v1.5+ | Continue.dev / Cline / Aider pattern. Free product has full AI from day 1. |
| Aug 12 23:20 | **Hardware deploy locked:** paid (pay-per-flash OR bundled in Pro); NOT in free tier | The "shipping" moment is the value-capture point. Closed-ingredient feature. |
| Aug 12 23:25 | **Open-source resource model locked:** unlimited KB / recipes / projects; the "open source" is the moat | The 4-plugin-projects cap (A4) is preserved as authored-plugin cap; everything else (KB, projects, recipes) is unlimited. |

---

## H. Open work

1. **Trademark filing for "Tinkr"** — file in class 9 + 42 in US, EU, UK before public launch. Cost: $1,500-$3,000 per class per jurisdiction. DIY via TEAS or hire a trademark attorney.
2. **Domain acquisition** — **`tinkr.build` is the primary domain (A16).** Register immediately via Cloudflare or Namecheap. ~$12/yr for the `.build` TLD. `tinkr.dev` was rejected (taken by third party, not worth acquiring — pivot to `.build`). Optional backup: `tinkr.sh` (~$15/yr) for the one-line install script if a separate install surface is wanted. Not pursuing: `tinkr.io` (taken, expensive to acquire), `tinkr.app` (Apple controls), `tinkr.run` / `tinkr.tools` (no brand fit).
3. **GitHub org creation** — `tinkr-org/` on GitHub. Repo structure: `tinkr-cli`, `tinkr-esp32`, `tinkr-rpi5`, `tinkr-kb`, `tinkr-knowledge`, `tinkr-docs` (the source repo for `docs.tinkr.build/`).
4. **PyPI + npm package registration** — `tinkr-cli` on PyPI, `@tinkr/cli` on npm. CLI command `tinkr` (one word, the user-facing entry point).
5. **v1.0 Week 1 packaging refactor** — split 12 flat tools into `tinkr.cli` core + `tinkr-esp32` plugin. Plan on disk at `architecture/v1_week1_packaging_refactor.md`. The plugin directory rename `blink-esp32/` → `tinkr-esp32/` happens in this refactor. ~11 hours of work, ~2 days for solo dev.
6. **Trademark check on "Tinker on."** — no risk (entirely generic English phrase), but file for the trademark as a combined mark to be safe.
7. **Final tagline / brand rationale cleanup** — `01-positioning.md` §2 already updated to lock "Tinker on." with full rationale. Done.
