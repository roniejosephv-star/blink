# Mockups — Summary & Open Questions

> This file records the **top design decisions** and **constraints discovered** while building the 5 mockups. It is the handoff to the brand spec author and to anyone reviewing these mockups before implementation. Pair it with `README.md` (the design rules) and the individual HTML files.

---

## 1. Top design decisions

### 1.1 A consistent Tinkr visual identity (since the brand spec doesn't exist yet)

The brand spec is being produced in parallel. To keep the mockups from drifting, a self-contained identity was established inline in all 5 files. If the brand spec lands with different tokens, swap the values in the `<style>` block of each file — the structure and content are independent of the spec.

| Token | Value | Use |
|---|---|---|
| Wordmark | `tinkr` (lowercase, Space Grotesk) | Logo treatment across all surfaces |
| Mark | A 1-bit LED: small cyan square inside a soft cyan halo | The "i" in `tinkr` — the dot is the LED |
| Primary | `#22D3EE` (dark) / `#0891B2` (light) | Brand color, "the LED is on" |
| Accent (LED-off) | `#F59E0B` | Warning, paid, attention |
| Success | `#10B981` | Verify, online, "verified" |
| Error | `#EF4444` | Destructive, errors, error-type entries |
| Info | `#60A5FA` | Secondary info, story-type entries |
| Accent (pattern) | `#C084FC` | Pattern-type entries, accent |
| Dark bg | `#0B1120` (deep blue-black, "LED-off display") | Default |
| Light bg | `#FAFAFA` | Docs default, marketplace opt-in |
| Display font | Space Grotesk | Headings, hero, wordmark |
| Body font | Inter | UI, paragraphs, tables |
| Mono font | JetBrains Mono | Code, terminal, paths, JSON/YAML |

**Rationale:** "Tinkr" = the on/off of an LED. Cyan is the on-state, amber is the off-state. The dark background is a screen with the LED off. This single metaphor drives the whole visual language.

### 1.2 The 3 personas are served by different surfaces, not different products

| Persona | Primary surface | Why |
|---|---|---|
| Hobbyist | CLI (`01`) | Works out of the box. No chrome. |
| Educator | Tauri shell (`02`) | Chat panel teaches; one-click "save as recipe" builds the corpus. |
| Embedded engineer | KB viewer (`05`) + shell (`02`) | They look up quirks and deploy from a single IDE. |

All three install the same `tinkr` CLI. The Tauri shell and the marketplace are layers on top, not separate products.

### 1.3 The 4 free plugins are the foundation of the marketplace

Locked decision: "4 free plugin projects per user + 4 free sim projects per user." The marketplace hero in `03` is built around this. The featured row is exactly the 4 free plugins (`tinkr-esp32`, `tinkr-rp2040`, `tinkr-nrf52`, `tinkr-micropython-runtime`). Everything else is opt-in paid or free from a third-party creator.

### 1.4 "Stays true to contributions" is a contract, not a footer

The 3-clause contract in `03` is its own section, above the footer, not buried. The 3 clauses:

1. **You own your plugin.** Source lives in your GitHub repo, MIT or your choice.
2. **70% of every sale is yours.** Tinkr takes 30% for registry, payment, and curation. Monthly payouts, no minimum.
3. **You control your code.** No AI rewrites, no silent updates, works offline, deletion within 24h.

This is what makes the marketplace feel like a community surface, not a rent-extraction surface.

### 1.5 The capture layer is a status-bar citizen, not a popup

Per `capture_layer.md` §3.1, the capture badge lives in the 28-px status bar of the Tauri shell. It pulses when a trigger fires. The 5 trigger types (`recipe` / `fix` / `chip` / `pattern` / `publish`) are always visible as chips so the user learns the vocabulary by seeing it. The same animation, the same period (1.6s), is used in the CLI output and the Tauri shell.

### 1.6 Errors teach, not intimidate

`01-cli-output.html` §8 shows an I²C scan that returns `ETIMEDOUT`. The error is followed by a "kb suggestion" block: 2 results from the community knowledge base, with relevance scores, and a one-line `tinkr knowledge fix <id>` command the user can copy-paste. The same pattern is used in the KB viewer's entry detail ("fix_steps" + "verify_steps"). Errors are a learning surface, not a dead end.

### 1.7 Light mode is the default for docs, not for the CLI

Docs (`04`) default to light. Most engineers read docs in bright environments. CLI (`01`) is always dark — it lives inside a terminal emulator. Tauri shell, marketplace, and KB all default to dark with a light-mode toggle. The same color semantics are used in all modes; only luminance changes.

---

## 2. Constraints discovered

### 2.1 The brand spec doesn't exist yet (a parallel agent is producing it)
**Impact:** Color tokens, font choices, and the logo mark are inline in these mockups. When the spec lands, do a token-swap, not a layout rework. **Action:** If the spec changes the visual identity significantly, the most affected file is `01-cli-output.html` (every color is named). The other 4 mockups use CSS custom properties (`--cyan`, `--amber`, etc.) and a `text-cyan` / `text-amber` Tailwind alias scheme, so a token swap is straightforward.

### 2.2 Tailwind via CDN, not a build step
**Impact:** The mockups are reference art, not production. They should open in any browser without `npm install`. The production Tauri shell will use the same Tailwind config with a real build pipeline. The CSS is inlined (a `<style>` block per file) so the mockups are self-contained.

### 2.3 The `kb` filter category names must match the entry type names
**Impact:** The KB viewer in `05` uses `error` / `fact` / `pattern` / `recipe` / `story` as filter chips. The capture layer in `01` and `02` uses `recipe` / `fix` / `chip` / `pattern` / `publish` as trigger types. **These are not the same vocabulary.** The KB stores generic types (`error`, `fact`); the capture layer produces specific subtypes (`fix` for the error type, `chip` for the fact type, etc.). The mapping should be documented in the brand spec or in the `capture_layer.md` §5 trigger logic. **Open question #1.**

### 2.4 The "verified" badge in the KB has no formal definition
**Impact:** The mockup uses "verified = 5+ independent confirmations" as a rule of thumb. This is not specified in any architecture doc. **Open question #2.**

### 2.5 The KB viewer's entry detail shows the YAML source by default
**Impact:** The KB is open data, and showing the YAML is a trust signal (no schema hidden in a database). But this assumes the user knows YAML. For educators and hobbyists, the "rendered" view is the friendlier default. The mockup makes YAML the default and rendered a tab. **Open question #3** — should YAML be the default in v1.0, or should the rendered view be the default with YAML as a tab?

### 2.6 The marketplace needs an actual storefront
**Impact:** The mockup shows a "Pay $19" button but the actual payment flow is out of scope for v1.5's first cut. **Open question #4** — does the marketplace launch with the "Pay $19" buttons live, or with all plugins free for the first 3 months while the creator program matures?

### 2.7 The Tauri shell is large (3 panes + 28-px status bar) and may not fit on a 13" laptop
**Impact:** At 1280×800, the right chat panel is cramped. The status bar is OK. **Open question #5** — should the right chat panel be a docked sidebar that can be hidden (⌘J) by default, or is the IDE always 3-pane? (The mockup shows the always-3-pane state, with the chat visible.)

### 2.8 The "What's new" banner is dismissible but not remembered
**Impact:** The mockup has a single row banner with an `✕` button. The mockup doesn't show what happens after dismissal. **Open question #6** — should the dismissal persist in `localStorage`, or should it always show on the first visit of a session? The brand spec should pick a default.

---

## 3. What this set of mockups is good for

- **Layout review.** All 5 surfaces use the same design system, the same logo, the same color semantics. Reviewers can see whether the visual language is consistent.
- **Copy review.** Every line of text is real, not lorem ipsum. The CLI error message, the chat conversation, the KB entry body, the marketplace plugin description — all of it is plausible content the product will ship with.
- **Information architecture review.** The KB viewer's filter set, the marketplace's pricing tiers, the docs site's tree, the Tauri shell's status bar items — all of these are decisions that should be reviewed before they go to code.
- **Brand handoff.** When the brand spec lands, this is the canonical set of surfaces to validate the spec against. If the spec's tokens don't translate cleanly into these mockups, that's a signal the spec needs more work.

## 4. What this set of mockups is NOT good for

- **Pixel-perfect specs.** The mockups are Tailwind-driven and the spacing is approximate. Figma specs are needed for true pixel fidelity.
- **Interaction design.** The mockups show static states. Hover, focus, drag, modal-open, command palette — none of this is in scope. The Tauri shell mockup shows the default state; the rest of the states (open chat, focused tab, palette open) are in the implementer's hands.
- **Empty / loading / error states for the marketplace and KB.** The mockups show the "happy path" — 1 query, 1 result set, 1 entry detail. Empty results, 0-found queries, 500 errors, offline mode — all to be added.
- **Mobile.** The docs site and marketplace are designed to work at 768px (tablet). The Tauri shell is desktop-only by spec. The CLI is desktop-only. The KB viewer's mobile state is a follow-up.

---

## 5. Open questions for the brand spec author

1. **What is the wordmark treatment?** The mockup uses lowercase `display` (Space Grotesk). Should the wordmark be a custom-cut logotype? If yes, these mockups need updated wordmark assets.
2. **What is the mark?** The mockup uses a 1-bit LED metaphor (a small cyan square inside a soft halo). Does the brand spec agree, or does it prefer a different mark (a circuit symbol, a stylized "B", etc.)?
3. **Are the semantic colors locked?** The mockup uses cyan/green/amber/red/blue/magenta as the semantic palette. The brand spec may want a different palette (e.g., cyan/orange/red only).
4. **What is the official light-mode primary?** The mockup uses `#0891B2` (cyan-600) for light-mode primary. The spec may want a different value, especially if the spec's dark-mode primary is not `#22D3EE`.
5. **Is the marketplace pricing model correct?** The mockup shows one-time payments only. The spec may want subscriptions, freemium tiers, or both. (Locked decision so far: one-time, lifetime, 70% to creator.)

---

**Status:** 5 mockups + README + SUMMARY delivered. Ready for brand spec handoff and implementer review.
