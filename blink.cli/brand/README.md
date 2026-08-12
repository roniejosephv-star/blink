# Tinkr — Brand

> The complete brand specification for Tinkr. The single source of truth for what Tinkr looks and feels like, for the next 5 years.

This directory is the brand spec. Every surface — CLI, Tauri shell, marketplace, docs site, KB viewer, plugin registry, marketing site — reads from here. The MIT-licensed core of Tinkr is open source, and so is the brand. Fork it. Adapt it. Ship a plugin that follows it.

---

## What's in this directory

| File | What it covers | Audience |
|---|---|---|
| **[`01-positioning.md`](01-positioning.md)** | Name, tagline, positioning, personas, archetype, competitive landscape, brand promise, voice & tone, origin story, 5-year horizon | Founders, marketing, anyone writing copy |
| **[`02-visual-identity.md`](02-visual-identity.md)** | Name analysis, logo concept, color palette (hex + 256-color + 16-color ANSI), typography, iconography, visual style, motion, accessibility | Designers, front-end engineers, CLI authors |
| **[`03-design-tokens.json`](03-design-tokens.json)** | Style-Dictionary-compatible token file. 12 categories, 100+ tokens, light + dark variants. Consumed by every surface | Design system engineers, tooling |
| **[`04-component-library.md`](04-component-library.md)** | The 12 essential components (button, input, card, modal, toast, badge, table, tabs, nav, code block, status indicator, empty state) with HTML + Tailwind | Front-end engineers, designers |
| **[`05-applications.md`](05-applications.md)** | How the brand applies to each of 8 surfaces: CLI, Tauri shell, marketplace, docs site, KB viewer, plugin registry, marketing site, first-run | Everyone shipping a Tinkr surface |
| **[`SUMMARY.md`](SUMMARY.md)** | The top 5 brand decisions, with the reasoning | Anyone new to the brand, in 5 minutes |

---

## Brand at a glance

Five bullets. The whole brand in one breath.

- **Tinkr is the open-source hardware IDE that ships.** A small CLI, a plugin ecosystem, and an agent that reads your project. MIT-licensed core. Git-based registry. The project repo is the memory.
- **The voice is engineer-to-engineer.** Direct, technical, dry. No marketing speak. No "we empower you to ship." We ship. You ship. The community ships.
- **The visual style is modern minimalism, dark by default.** Inter for UI, JetBrains Mono for code. Cyan (`#5EEAD4`) for primary, amber (`#FB923C`) for the "ship it" accent. 1 px borders, no drop shadows, no glassmorphism, no neon.
- **The mark is a square frame with a center dot.** The frame is the project. The dot is the LED. In the wordmark, the "i" in "tinkr" is the LED — a filled circle in amber, no stem. The dot tinkrs at 1 Hz in the brand animation (suppressed under reduced motion).
- **The hard rules are non-negotiable.** CLI is a first-class surface. Light and dark are equal. No marketing speak in product copy. WCAG 2.1 AA is the floor. The accent is amber. Inter and JetBrains Mono only. Line icons, no emoji. Open source by default.

---

## Quick reference

### The logo

- **Wordmark**: `tinkr` in lowercase Inter, the "i" replaced by a filled amber circle.
- **Symbol mark**: a 24×24 square with a 6×6 filled circle centered.
- **Full ASCII**:
  ```
   ●  tinkr
  ```
- **Favicon (16×16)**: the symbol mark only, solid block with a center punched-out square.
- **SVG source**: `assets/logo.svg` (to be drawn from this spec — the `02-visual-identity.md` §2 has the full design intent).

### The colors

| Role | Hex | Used for |
|---|---|---|
| Primary | `#5EEAD4` | Wordmark on dark, links, focus rings, brand emphasis |
| Accent / CTA | `#FB923C` | Primary buttons, the LED dot, "ship it" emphasis |
| Secondary | `#A78BFA` | Agent surface, KB entries, AI-related elements |
| Status success | `#22C55E` | Deployed, validated, connected |
| Status warning | `#F59E0B` | Beta, deprecation, slow ops |
| Status error | `#EF4444` | Failures, blocking errors |
| Status info | `#3B82F6` | Informational, some links |
| Surface dark | `#0A0A0B` | Default background (dark mode default) |
| Surface light | `#FAFAFA` | Default background (light mode) |
| Text dark | `#FAFAFA` | Body text on dark |
| Text light | `#0A0A0B` | Body text on light |

Full palette in `02-visual-identity.md` §3 and `03-design-tokens.json`.

### The fonts

- **UI / heading / body**: Inter (variable, 400/500/600/700). Google Fonts: `Inter`.
- **Code / terminal / monospace**: JetBrains Mono (variable, 400/500/600). Google Fonts: `JetBrains+Mono`.
- **Fallback chain**: Inter → system-ui → -apple-system → TinkrMacSystemFont → Segoe UI → Roboto → sans-serif. JetBrains Mono → ui-monospace → SFMono-Regular → Menlo → Consolas → Liberation Mono → monospace.
- **Import**:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  ```

### The tagline

> **"The hardware IDE that ships."**

Used in the hero, the GitHub README, the CLI banner, the Twitter bio. Don't dilute it. Don't paraphrase it.

---

## Brand rules (the 8 non-negotiables)

These are the rules that override any designer's preference. They are the contract with the next 5 years of work.

1. **The CLI is a first-class surface.** Every brand decision is tested in the terminal first. If it doesn't work in 80 columns of monospace, it doesn't ship.
2. **Light and dark mode are equal.** Neither is a theme. Both are first-class. Every screen, every component, every state is verified in both.
3. **No marketing speak in product copy.** Error messages, CLI output, docs, the Tauri shell — none of it contains "empower," "unlock," "seamless," "revolutionary," or "delight."
4. **Accessibility is not a feature.** It is a baseline. WCAG 2.1 AA is the floor. We do not ship features that fail it.
5. **The accent color is amber.** Not blue, not purple, not green. The amber is the LED; the LED is the brand.
6. **Inter and JetBrains Mono only.** No proprietary fonts. No bundled fonts. Google Fonts + system fallbacks.
7. **Icons are line icons.** No filled icons in the UI. No emoji as UI icons. Ever.
8. **Open source by default.** The brand assets (logo, fonts, color tokens, this spec) are MIT-licensed. Anyone can use them to build a Tinkr plugin.

If a future decision breaks one of these rules, the decision is wrong.

---

## What is Tinkr?

Three lengths, for three audiences.

### The 1-sentence version

> Tinkr is the open-source hardware IDE that ships: a CLI, a plugin ecosystem, and an agent that reads your project.

### The 1-paragraph version

> Tinkr is the open-source hardware IDE for ESP32, RP2040, nRF52, and friends. It's a small `tinkr` CLI, a HAL that talks to any device the right way, and a plugin ecosystem where the community builds and shares hardware support. Your project repo is the memory — `tinkr.toml`, your firmware, the datasheets you reference, the chip DBs, the recipes you've saved. Tinkr reads it; it doesn't own it. The agent (Gemini, Claude, or local Ollama) reads the project, calls the HAL, and proposes changes you review. The CLI works for hobbyists on day one and embedded engineers on day 1,000. Same product, same HAL, same agent. The plugins are the only thing that changes.

### The 1-page version

> **The problem.** Hardware developers work with tools that are either too simple (Thonny, Wokwi) or too heavy (PlatformIO, Arduino IDE 2). The simple tools stop where the real work starts. The heavy tools hide the protocol, version-lock your libraries, and treat the user like a customer. The MicroPython niche is uncontested.
>
> **The product.** Tinkr is a CLI, a HAL, an MCP server, and a plugin ecosystem. The CLI is the test surface — `tinkr init`, `tinkr plugin add`, `tinkr device scan`, `tinkr project deploy`. The HAL is the common layer that lets one workflow talk to many devices. The MCP server is the agent surface. The plugin ecosystem is the moat — every chip family is a plugin, every plugin is a git repo, the registry is a PR-based open-source index.
>
> **The moat.** Twelve working CLI tools, refactored into the first plugin (`tinkr-esp32`). The architecture is open. The reference plugins are MIT. The registry is a git repo. The community grows the ecosystem; the agent gets smarter as the community grows. The project's git history is the safety net — the agent proposes, the user reviews, the user commits.
>
> **The personas.** Mira the hobbyist (works out of the box, five commands to a tinkring LED). Devansh the educator (every student on the same page, every project reproducible). Sara the embedded engineer (raw access, open formats, no hidden state, a HAL she can read in 30 seconds). One product, three workflows, the same HAL.
>
> **The business model.** v1.0 is the IDE — free, open-source, MIT. v1.5 adds the plugin marketplace (paid plugins, 70/30 split, vendor first-party). v2.0 adds the creator program (users earn money from plugin sales). v3.0+ is open. The core is always free.
>
> **The community.** The KB is the brain. Users contribute by building in Tinkr — the capture layer watches, pre-fills, asks the user to submit. The community is the loop. The agent consumes the loop.
>
> **The 5-year bet.** Hardware is a 100x bigger market than the IDEs that serve it. The plugin spec is the first serious open-source standard for hardware tool extension. The community grows with the project's use. Tinkr is the tool. The community is the engine.

---

## How to use this spec

- **Starting a new surface?** Read `01-positioning.md` (for the voice), then `02-visual-identity.md` (for the visuals), then `04-component-library.md` (for the components), then `05-applications.md` (for the surface-specific rules).
- **Adding a new component?** Propose the spec in `04-component-library.md`. Match the existing format. Get a review from the design system owner.
- **Adding a new token?** Add it to `03-design-tokens.json` with a complete description. Run `style-dictionary build` to regenerate every downstream asset.
- **Writing copy?** Read the voice & tone section in `01-positioning.md`. Run your draft through the "engineer reads it aloud" test. Cut every second adjective.
- **Reviewing a PR that touches brand assets?** Open the relevant file. Check the 8 hard rules. If the PR breaks a rule, request changes.
- **Updating the brand for a new product line?** Add a section, don't change the existing one. The 5-year horizon is the constraint.

---

## License

This brand specification is MIT-licensed. Use it. Fork it. Ship a Tinkr plugin that follows it. The brand is open because the product is open.

```
MIT License

Copyright (c) 2026 Tinkr Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```
