# Tinkr — UI Mockups (15 surfaces)

> Reference mockups for the v1.0 CLI output, the v1.5+ Tauri surfaces, and the v1.0 Agentic Orchestrator (the "Mavis equivalent" with the Tinkr wordmark). These are the visual targets the CLI and Tauri implementations should match. They are static HTML, self-contained, and serve as a single source of design truth.

**One sentence per mockup:**

| # | File | What it is |
|---|---|---|
| 01 | [`01-cli-output.html`](./01-cli-output.html) | A simulated terminal session: first run, `init`, `plugin add`, `device scan`, `project deploy`, `repl`, `knowledge contribute`, an error with a KB fix, and a light-mode preview. The v1.0 product surface. |
| 02 | [`02-tauri-shell.html`](./02-tauri-shell.html) | The v1.5 desktop IDE: three-pane layout (devices / editor / agent chat), a 28-px status bar with the capture badge, and the 5 trigger types surfaced as chips. |
| 03 | [`03-marketplace.html`](./03-marketplace.html) | The v1.5 plugin marketplace: hero, 4 free featured plugins, full grid, plugin detail page, pricing bundles, the 3-clause "stays true to contributions" contract, and the creator program. |
| 04 | [`04-docs-site.html`](./04-docs-site.html) | The docs site (docs.tinkr.build/): three-column layout (tree / rendered / on-page TOC), search, version selector, "what's new in v0.5" banner. |
| 05 | [`05-kb-viewer.html`](./05-kb-viewer.html) | The knowledge base viewer (kb.tinkr.build/): semantic search, category filters, results with score + verification badge, full entry detail with YAML source, related entries, contribute CTA. |
| 06 | [`06-device-manager.html`](./06-device-manager.html) | The v1.5 device manager: 4+ detected devices in a card list (mix of online / offline / error), per-card plugin-compatibility strip, slide-out details panel with chip ID / KB entries / firmware, empty-state illustration, and a "Mock devices for testing" footer link. |
| 07 | [`07-repl-monitor.html`](./07-repl-monitor.html) | The v1.5 REPL + serial plotter surface: black-bg REPL with ANSI colors + tab-completion + highlighted traceback on the left, 3-trace inline-SVG plotter with readouts (current / min / max / mean) on the right, capture-to-KB bottom strip. |
| 08 | [`08-kb-editor.html`](./08-kb-editor.html) | The KB author surface: a 60/40 split — form on the left (title, chips/boards multiselect, difficulty, est. time, tags, rich-text description, ordered step editor with code blocks + verifications) and a live preview on the right that mirrors the KB viewer. 3-stage flow: draft → review → published. |
| 09 | [`09-plugin-dev-kit.html`](./09-plugin-dev-kit.html) | The plugin author's workspace: VS Code-style three-pane (file tree / tabbed editor / build & test). Tabbed editor for `tinkr.plugin.toml`, `cli/tinkr_weather_deploy.py`, and `knowledge/chips/esp32.json`. Build panel shows validate (8/8), tests (6/6 green), and a live "install" progress bar; the amber "Submit to marketplace" CTA is gated until manifest valid + all tests pass + pushed to fork. |
| 10 | [`10-project-explorer.html`](./10-project-explorer.html) | The v1.5 project explorer: first-run welcome banner ("tinker on."), a 3-col grid of project cards (Recent / Examples / Templates) with target chips, status pills, plugin lists, and Git-sync indicators; toolbar with filter pills + Clone-from-GitHub + amber "New project" CTA; first-run-only right rail with quick stats, a "Sync to cloud" card, and keyboard shortcuts. |
| 11 | [`11-settings-account.html`](./11-settings-account.html) | The v1.5 settings hub: shell sidebar (empty, no project open) + a 200-px settings nav (Account active) + the Account section with five cards (Profile / Plan / Connected accounts / Security / Danger zone) + a 300-px right rail with the last 5 logins, last 3 plan changes, last device, and a "Request export" card. Tone is calm, dense, scannable. |
| 12 | [`12-agentic-orchestrator.html`](./12-agentic-orchestrator.html) | **The v1.0 Agentic Orchestrator — the "Mavis equivalent" for Tinkr.** Three-column layout: sidebar (Project / Progress / Deliverables / Agent team), chat center (with Thought expansion, inline terminal commands, the t●nkr wordmark as the working indicator), right panel (model selector, reasoning toggles, run metrics). See `architecture/agentic_orchestrator.md` for the full design rationale. |
| 13 | [`13-wordmark-animations.html`](./13-wordmark-animations.html) | The 11 animation states of the t●nkr wordmark: idle, thinking, reading, writing, searching, flashing, compiling, done, error, waiting, ship. Pure CSS, no JS, no Lottie. The mark is the agent's face. |
| 14 | [`14-thought-expansion.html`](./14-thought-expansion.html) | The Thought expansion — the observability deep view. The agent's reasoning becomes a timeline of 5 step types (READ / THINK / DECIDE / ACT / REPORT), each with a colored node, badge, title, body, and inline diff. The user can review every action before approving. Solves the "what is the agent doing?" problem. |
| 15 | [`15-action-report.html`](./15-action-report.html) | The Action Report — the per-action review surface. After a Thought finishes, the user gets a 5-tab report (Changes / Brand & docs / KB entries / Decisions / Raw log) with per-file diffs, brand-deck update prompts, decision approval, and a sticky action bar at the bottom. The "update the brand deck and necessary documents" surface. |

---

## The design DNA (Aug 13, 2026)

The mockups follow the brand's core DNA: **calm + technical + cognitive + information-dense + local-first + instrument-like**. Plus the **PREMIUM PRODUCT DESIGN MODE** rules (no AI-slop patterns: no purple/blue gradients, no glassmorphism, no excessive rounded cards, no giant hero sections, no decorative gradients, no meaningless dashboard metrics).

The test: would a senior product designer at Linear, Notion, Figma, Stripe, Raycast, or Arc ship this?

## The 5 design rules every mockup follows

These are the rules that make all 15 mockups unmistakably the same product. They are non-negotiable for any future surface (landing page, blog, video, etc.).

1. **The Tinkr mark is a circuit, not letters (v7, Aug 13).** A **visible PCB trace network** — 17+ bright cyan traces with 45° chamfered corners (real PCB routing, never Manhattan), 24 hollow pin circles at the trace ends (the I/O pads), 12 filled junction nodes at the intersections (the bridges), 10 dynamic data-packet nodes flowing along Bezier-curve motion paths through the lines, and 1 amber center LED with halo (the brand heart). The trace network is fixed in shape — only the nodes flow, the color shifts, and the speed changes across 11 operational states. The text wordmark `tinkr` (JetBrains Mono) is for dense contexts (chat headers, breadcrumbs, install commands) — paired with the circuit mark. See `brand/02-visual-identity.md §2.1` and `brand/mockups/13-wordmark-animations.html` for the full spec and the 11 states.

2. **Semantic colors are universal.**
   - **Cyan** (`#5EEAD4` dark / `#0D9488` light) = brand, info, identity, the dormant circuit nodes
   - **Amber** (`#FB923C`) = the LED, working state, primary CTA, the "ship it" color
   - **Green** (`#22C55E`) = success, verified, online, "done" state
   - **Red** (`#EF4444`) = error, destructive
   - **Blue** (`#3B82F6`) = secondary info, READ step type
   - **Violet** (`#A78BFA`) = THINK step type, agent reasoning
   - **Slate** (`#0A0A0B` → `#111113` → `#1C1C1F`) = the only neutral scale
   
   No decorative colors. Every color means something. The same color is used for the same meaning across CLI, shell, marketplace, docs, KB, and agent.

3. **Dark mode is the default; light is opt-in.** The CLI is always dark. The Tauri shell, marketplace, docs, and KB all default to dark with a light-mode toggle. The toggle is in the top nav on web surfaces and the title bar in the Tauri shell.

4. **Type system is Inter + JetBrains Mono.**
   - **Body / UI** (Inter) = paragraphs, UI text, table data, headings
   - **Mono** (JetBrains Mono) = code, terminal, JSON/YAML, paths, IDs, the text wordmark, all data
   - **Display** = Inter at 600/700 weight (no separate display font — keep it simple)
   
   This is the only font stack. No system-ui fallbacks beyond the standard `ui-monospace, monospace` chain. **Space Grotesk was used in v1; the v2 mark drops it** to reduce visual noise and lean into the instrument-like DNA.

5. **Density follows context.**
   - **CLI** — maximum density, monospace, line-by-line
   - **Tauri shell** — high density, three panes, 28-px status bar
   - **Marketplace** — medium density, generous hero, card-based
   - **Docs** — long-form reading, light default, three-column
   - **KB viewer** — search-first, result list dense, detail view generous
   - **Device manager** — medium-high density, card list with plugin-compat strip, slide-out details panel
   - **REPL monitor** — high density, REPL is a tool, plotter is a tool, capture strip is the only "frame" chrome
   - **KB author** — split-density: 60/40 form/preview, both scrollable, draft chip is amber accent
   - **Plugin dev kit** — VS Code density, tabs + line numbers + bottom info bar, build panel is collapsible on the right
   - **Agentic orchestrator (v1.0+, mockups 12–15)** — three-column, dot-grid background, mono for all data (counts, IDs, paths, statuses), the circuit mark for all working-state indicators. Every pixel tells you something.

---

## How to use this (for the implementer)

### 1. For the CLI author (v1.0)
- Open `01-cli-output.html` in a browser. The colors, spacing, and stage format are the contract for the `rich` / `textual` styling in the Python CLI.
- The "stages" pattern (`[1/5] resolving · done 0.2s`) is the canonical progress format. Use it everywhere; don't reinvent per command.
- Errors always end with a "kb suggestion" block — the suggestion must be one CLI command the user can copy-paste.
- Light mode is `BLINK_THEME=light` for v0.7+. See the bottom of mockup 01 for the spec.

### 2. For the Tauri shell author (v1.5)
- The three-pane layout in `02-tauri-shell.html` is fixed: left = devices, center = editor, right = agent chat. No top toolbar.
- The status bar is 28 px. It's the home of: git branch, current device, test count, capture badge, MCP status, cursor position. Nothing else.
- The capture badge pulses when there's a suggestion. Clicking opens a side panel — never a modal. The 5 trigger types (`recipe` / `fix` / `chip` / `pattern` / `publish`) are always visible as chips so the vocabulary is learned by seeing it.
- Window chrome is native (close/min/max on macOS, etc.) — don't draw your own.

### 3. For the marketplace author (v1.5)
- The hero is "Hardware plugins, made by the community." Not "Buy a plugin." The marketplace is a discovery surface.
- The 4 free plugins (`tinkr-esp32`, `tinkr-rp2040`, `tinkr-nrf52`, `tinkr-micropython-runtime`) get the "free" badge and live in the featured row. They are the foundation.
- Pricing is in two bundles (Maker $49 / Pro $99) + per-plugin ($9–$29), never as a gate. The 3-clause "stays true to contributions" contract is its own section, above the footer.
- The creator program and vendor partnership are CTAs in their own section. Both link out to a real form.

### 4. For the docs author (v1.0+)
- Three-column layout: doc tree (left) / rendered markdown (center) / on-page TOC (right). Light mode default.
- The "what's new" banner is one row, dismissible, with a "last 2 days ago" freshness stamp. No modals.
- Search is `⌘K` and combines docs + KB + changelog.
- Version selector is in the top nav. Latest gets a green "latest" badge.
- Every code block uses the syntax colors defined here. No other palette.

### 5. For the KB viewer author (v1.0+)
- Search bar is the entire hero. Results show a relevance score (0–1) — color-coded (green ≥ 0.8, amber 0.5–0.8, red < 0.5).
- Entry types are color-coded chips: `error` (red), `fact` (cyan), `pattern` (magenta), `recipe` (amber), `story` (blue). Same chips as the capture layer.
- "Verified" is a green check, not a gate. 5+ independent confirmations get it.
- The entry detail shows full YAML source (with syntax highlighting) + rendered view + JSON + related entries + history. The "copy / fork / open in editor" actions are always visible.
- The contribute CTA is the same form as the capture layer's status-bar badge. One flow, one review pane.

### 6. For the device manager author (v1.5)
- The device list is a card list, not a table. Each card carries: board-specific SVG, name + chip + port, status badge, last-seen, action cluster (Connect / Flash / REPL / ⋯), and a plugin-compatibility strip at the bottom.
- "Scan for devices" is the *only* amber element on the surface — the "ship it" color, reserved for the moment the user commits to a hardware workflow. Everything else stays in the cyan / violet / status semantic palette.
- Status color is never alone. A red badge + the word "Error" + a ✕ icon. WCAG 2.1 AA floor.
- The details panel is a slide-out from the right (380 px), not a modal. Click another card to swap context without losing the panel.
- "Mock devices for testing" is a first-class footer link. The 4 free plugin projects + the demo flow must be cheap to enter.
- The empty state is illustrated (inline SVG of an unplugged board + cable) + one CTA. Hardware is physical — show the absence physically.

### 7. For the REPL monitor author (v1.5)
- REPL and plotter share the screen side-by-side. The two panes share state — a typed expression becomes a plot trace in one click.
- The REPL inherits the sunken surface (`#050506` per brand spec) — the only place in the shell darker than the canvas. This is the chip's screen, not the IDE's chrome.
- ANSI colors render as styled `<span>`s. The 8-color subset is identical to the Python CLI palette: cyan prompt, amber for highlighted errors / current line, violet for builtins, green for echoed input, red for tracebacks, yellow for soft warnings, grey for comments, white for output.
- Error tracebacks highlight the offending line in amber (not just red text) — VS Code / PyCharm convention. The line number, the source line, and the caret all read as a unit.
- Tab completion is a first-class surface, not a tooltip. It teaches the user the chip's API by showing the available attributes.
- The plotter is a chart, not a widget. Inline SVG, no chart library. 60-second rolling window, 2–3 traces, smooth line interpolation, light axis ticks, no grid clutter.
- Pause / Record / Export CSV. Three real engineering-tool verbs, not "share to Twitter" nonsense.
- "Capture to KB" is a bottom-strip action, visually identical to the status-bar capture badge in `02-tauri-shell.html`. It captures the entire REPL transcript + plotted values + device + plugin version as a single KB entry. One click, one review, done.

### 8. For the KB author surface (v1.0+)
- The screen is a 60 / 40 split — form on the left, a faithful render of the KB viewer on the right. The author and the reader share the exact same surface. "Stays true to contributions."
- Entry type is a segmented control (recipe / fact / error / pattern) in the top bar, not a dropdown. The vocabulary is learned by being seen.
- The 3-stage footer — `save as draft` → `save + submit for review` → `save + publish` (amber "ship it" CTA) — is the publication flow. "Publish" requires the pre-publish checklist to be green.
- The description is a rich text editor (contenteditable), not a textarea. Minimal toolbar: bold, italic, code, link, list, H2, H3.
- Steps are the unit of reuse. Each step has description + code block + verification. Code blocks use the same Shiki-class markup as the KB viewer (`.shiki` + `.tk-kw` / `.tk-fn` / `.tk-st` / `.tk-nu` / `.tk-cm`).
- The live preview pane is sticky-header, shows the search-result card AND the entry detail, and the publication-flow chip. As you type, the preview updates. (The mockup shows a fully-filled example; the real-time behavior is the implementation.)

### 9. For the plugin dev kit (v1.5)
- VS Code feel with Tinkr chrome. Three panes: file tree (220 px) / tabbed editor / build & test (360 px). No top toolbar.
- The manifest (`tinkr.plugin.toml`) is a first-class tab and lives at the front of the tab strip. The "●" on the active tab in the tree means "this is the file you have open"; the amber dot on each tab means "this file has unsaved edits." Different signals, different glyphs.
- Each tab has a close (×) button, revealed on hover, per editor muscle memory.
- The build panel is a co-pilot, not a log dump. Three sections (validate / tests / build & install) collapse to a summary line and expand to the full output. The "Submit to marketplace" CTA is amber, gated until manifest valid + all tests pass + pushed to fork.
- The bottom info bar (28 px, same as the Tauri shell status bar) carries plugin name, version, branch, last commit hash, dirty-file count, and build status. Nothing else.
- Code blocks use the shared CSS-only highlighter. TOML sections (`.tk-tk-section`) are amber to match the manifest's identity. JSON keys are cyan.

### 10. For the project explorer author (v1.5)
- The screen is the home base — first-run welcome AND every "no project open" state. Same layout both times; the welcome card is the only thing that collapses.
- Project cards are the unit. Name + last-touched + target chip + status pill (green Built / amber Modified / slate Not built) + plugin chips + sync state. Hover actions (Open / Clone / Delete) fade in, never on by default.
- Sections are lexical, not folders: Recent (5 most recent) → Examples (marketplace starters, dashed border, "Clone to start") → Templates (curated by Tinkr). The user does not organize; Tinkr organizes.
- The right rail is first-run only. The "Sync to cloud" card is cyan (brand product, not vendor plug) and lives in the welcome state. Once dismissed, the explorer goes full-width and tool-like.
- Amber is reserved for the "New project" CTA and the "Modified" pill. Everything else is cyan or slate. Violet never appears here — that color is for the agent surface.

### 11. For the settings author (v1.5)
- Settings is calm on purpose. The amber accent appears twice on the entire Account screen: the plan tier badge and the danger-zone icon. The "Upgrade" CTA stays cyan.
- Four-pane grid: shell project tree (empty, "no project open") + 200-px settings nav (Account highlighted) + main content (5 cards: Profile, Plan, Connected accounts, Security, Danger zone) + 300-px activity rail.
- The danger zone is a 1-px red border card, last in the page, single button. The confirmation modal is not drawn — the card copy mentions the 30-day soft-delete grace so the user is warned in advance.
- The plan card does double duty: it states the tier and shows the value prop in one line ("You're on Pro — CI builds, cloud sync, priority support."). The three small stat tiles (plugin projects / storage / CI minutes) are the "are you using it?" hook.
- The activity rail is forensic, not social. Last 5 logins, last 3 plan changes, last device. The blocked login from Singapore is in red — security is a feature, not a footnote.

---

## File layout

```
brand/mockups/
├── README.md             ← you are here
├── SUMMARY.md            ← top design decisions + open questions
├── 01-cli-output.html    ← CLI surface (v1.0)
├── 02-tauri-shell.html   ← Desktop IDE (v1.5)
├── 03-marketplace.html   ← Plugin marketplace (v1.5)
├── 04-docs-site.html     ← Documentation site (v1.0+)
├── 05-kb-viewer.html     ← Knowledge base viewer (v1.0+)
├── 06-device-manager.html ← Device manager (v1.5)
├── 07-repl-monitor.html  ← REPL + serial plotter (v1.5)
├── 08-kb-editor.html     ← KB author surface (v1.0+)
├── 09-plugin-dev-kit.html← Plugin dev kit (v1.5)
├── 10-project-explorer.html ← Project explorer (v1.5)
├── 11-settings-account.html ← Settings hub (v1.5)
├── 12-agentic-orchestrator.html ← Agentic Orchestrator (v1.0+, the "Mavis equivalent")
├── 13-wordmark-animations.html ← 11 wordmark animation states
├── 14-thought-expansion.html ← Thought expansion (observability deep view)
└── 15-action-report.html ← Action report (per-action review surface)
```

Each HTML file is self-contained: Tailwind via CDN, Google Fonts via `<link>`. Open in any browser. Toggle the theme button in the top right (where present) to switch dark/light. The CLI mockup is always dark with a small light preview at the bottom.

---

## Constraints discovered while building

1. **No brand spec existed yet.** A consistent Tinkr visual identity was established inline in these mockups (see `SUMMARY.md`). When the brand spec is finalized, every color, font, and radius in these mockups should be replaced by the spec's tokens. The structure, layout, and content are independent of the brand spec and should not change.
2. **Tailwind via CDN, not a build step.** This is intentional — the mockups are reference art, not production code. They should be openable in a browser without `npm install`. The production shells will use the same Tailwind config but with a real build pipeline.
3. **No JavaScript framework.** The only JS is the theme toggle (one line of `classList.toggle`). Everything else is HTML + Tailwind classes. This keeps the mockups portable and reviewable in a code review.
4. **The capture layer's status-bar badge is the only animated element.** The pulse on the badge in `02-tauri-shell.html` and the capture suggestion in `01-cli-output.html` are the same animation, with the same period (1.6s). Other surfaces are static.
5. **All copy is real.** No lorem ipsum. Every error message, code snippet, entry title, and chat line is plausible content the real product would ship with. This makes the mockups useful for copy review, not just layout review.

---

**Brand note:** The brand spec is being produced in parallel. These mockups use a consistent, self-contained Tinkr visual identity (cyan LED mark, Space Grotesk + Inter + JetBrains Mono, slate dark surfaces, semantic accents). When the spec lands, swap the token values in the `<style>` block of each file. The mockup structure, content, and tone do not depend on the spec.
