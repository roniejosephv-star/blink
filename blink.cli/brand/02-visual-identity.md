# Tinkr — Visual Identity

> What Tinkr looks like. The colors, the type, the mark, the motion, the rules.
> This is the document the CLI, the Tauri shell, the docs site, and the marketing site all read from.

---

## 1. What "Tinkr" evokes

Three readings of the name. We pick one as the primary; the others are present in the brand but not as the headline.

### Direction A — The LED (primary)

The first thing every hardware developer ever made was a tinkring LED. It's the universal "hello world" of embedded. The name Tinkr is the moment the user first sees their code do something physical.

This is the primary reading because it ties the product to a real moment in the user's history, not a metaphor about speed. Every time a user runs `tinkr project deploy` and the LED on their board starts tinkring, the brand is literally describing what just happened.

**How it shows up in the brand:**
- The wordmark "i" dot is a filled circle (the LED)
- The accent color is a warm amber (the LED on a fresh Arduino)
- The "tinkring" animation is a real animation, not a metaphor — a 1 Hz pulse on the LED mark
- The KB entry for a working "tinkr the LED" project is the canonical example in every plugin

### Direction B — The tinkr of an eye (secondary)

Iteration speed. Tight feedback loops. The agent is fast, the deploy is fast, the recovery from a typo is fast. The product respects the user's time.

**How it shows up in the brand:**
- Motion is fast (150–300ms) and never blocks
- Error recovery is "fix and retry" without a reload
- The CLI banner is one line — no splash screen
- The tagline ("the hardware IDE that ships") echoes this

### Direction C — The flicker of a state (latent)

On / off. Build / deploy. Working / broken. The state model in hardware is binary. The product is opinionated about states — a device is connected, a flash is in progress, a port is missing.

**How it shows up in the brand:**
- The status indicator is a binary dot (green/grey), not a spinner
- The deploy progress bar is a hard fill, not a smooth animation
- The plugin maturity is `stable | beta | experimental | deprecated` — no "in active development"
- The CLI uses ✓ and ✗, not "Success!" and "Error occurred"

### What we don't use

- Eye / vision / "see the future" — too mystical, doesn't fit the engineer voice
- Photography / "capture the moment" — wrong metaphor for a CLI tool
- Speed / "faster than the rest" — every tool claims this

---

## 2. Logo concept

The mark is built from two elements: a **wordmark** and a **symbol**. They can be used alone or together. The mark works at 16 px (favicon) and at 1024 px (hero).

### 2.1 The circuit mark (v7, primary)

**The Tinkr mark is a PCB trace network, not letters.** For a hardware IDE, the mark should *be* a real piece of PCB — bright cyan traces with chamfered corners, hollow pin circles at the trace ends, filled junction nodes at intersections, and dynamic data packets flowing along Bezier-curve motion paths through the lines.

**Structure (17 traces + 24 pins + 12 junctions + 10 dynamic nodes + 1 center LED):**

```
   ┌──────────────────────┐
   │ ○───●───○            │
   │  ╲     │     ╱       │
   │   ╲    │    ╱        │
   │    ╲   │   ╱         │
   │ ○─●─●─◉─●─●─○        │  ← center LED (amber)
   │    ╱   │   ╲         │
   │   ╱    │    ╲        │
   │  ╱     │     ╲       │
   │ ○───●───○            │
   └──────────────────────┘

   17 visible traces    ← PCB routing, 45° chamfered corners
   24 hollow pin circles  (○) ← trace termination points
   12 filled junctions  (●)   ← trace intersection points
   10 dynamic nodes     (●)   ← data packets flowing along curved paths
    1 center LED        (◉)   ← amber, the brand heart
    1 halo              (◯)   ← amber glow around the LED
```

**Colors:**
- Traces: cyan `#5EEAD4` with 1.4px stroke + cyan-glow drop-shadow
- Hollow pins: cyan, 1px stroke, 0.95 opacity, cyan-glow
- Filled junctions: cyan, 0.95 opacity, cyan-glow
- Dynamic nodes: cyan (most) + amber `#FB923C` (a few for variety) with strong drop-shadow
- Center LED: amber `#FB923C` with 3px drop-shadow + amber halo ring
- Background: radial gradient `#0A1628` → `#020409` (the PCB substrate)

**Why a PCB trace network (v7):** the visible trace network IS the design — the bright cyan lines look like a real chip's routing, the hollow pin circles mark the I/O points, the filled junctions mark the bridges between systems, and the dynamic nodes are the data flowing through. The 10 dynamic nodes travel along **Bezier-curve motion paths** (never straight lines) so the motion feels organic, like data packets bouncing through a real network. The 11 operational states (see §3) all use the same mark — only node count, color, and speed change.

**The mark's shape is fixed. Only the nodes flow.** This is the brand's "instrument-like" DNA made visible — like a logic analyzer watching signals on a real PCB.

**The 5 hard rules of the v7 mark:**

1. **No straight lines for node motion.** Dynamic nodes travel along Bezier-curve offset-paths (`Q` and `T` commands), never `L` (line). Motion must feel organic.
2. **45° chamfered corners on all traces.** No 90° Manhattan routing. Traces use 3-point turns (`L a b L a+3 b-3 L a+3 c`) like real PCB layout, not right angles.
3. **Hollow circles at every trace end.** Pins are stroked, not filled. They're the I/O pads, not nodes.
4. **Filled circles at every trace crossing.** Junctions are filled, not hollow. They're the bridges, not endpoints.
5. **Amber center LED + halo.** The only amber element by default. Everything else is cyan. The center is the brand heart, and it pulses.

**Sizes:**
- **Favicon (16×16)**: 5-7 traces only, no pins, no junctions. The center LED is the anchor.
- **App icon (32×32, 64×64)**: full structure minus the faintest traces. 8-10 pins visible.
- **UI mark (24×24 to 64×64)**: full structure. The standard size for in-app use. Static (no dynamic nodes at <32px).
- **Hero (96×96 to 256×256)**: full structure with 10 dynamic nodes + strongest glow filter. The signature mark.
- **Marketing (≥256×256)**: full structure with refined spacing + amber glow effect.

**In monochrome contexts:** all cyan elements become white, all amber elements become a slightly darker gray. The mark reads as a PCB trace network, no color distinction.

### 2.2 The wordmark (text only)

**`tinkr`** in lowercase JetBrains Mono, weight 500. Used alongside the circuit mark in dense contexts (chat headers, document titles, install commands, breadcrumbs). The text wordmark is **always** paired with the circuit mark when used as a logo lockup.

```
Light surface:   tinkr       ←  ink-black text
Dark surface:    tinkr       ←  light-gray text
```

The text wordmark is **NOT the primary mark**. The circuit is. The text is for type, not for logos.

### 2.3 The symbol mark (legacy, use sparingly)

A simple square frame with a center dot. Used only where the circuit mark is too complex (16×16 favicon, some compact contexts).

```
┌────────┐
│   ●    │       ←  the symbol mark
│        │
└────────┘
```

**Recommended:** use the circuit mark instead, even at 16×16. The simplified circuit (4 corner nodes + center, X traces only) reads as a Tinkr mark at favicon size.

### 2.4 The combined lockup (circuit + wordmark)

Default lockup — circuit on the left, wordmark on the right, 12 px gap:

```
   ◉  tinkr
   │
   └── the circuit, the wordmark
```

Stacked lockup (for narrow surfaces, social profile pictures, app icons):

```
    ◉
   tinkr
```

The circuit alone is the most common form. The circuit + wordmark is for the docs site header, the Tauri shell title bar, and marketing site headers.

### 2.3 The combined lockup

Default lockup — symbol on the left, wordmark on the right, 8 px gap:

```
●─── tinkr
│
└─ the symbol, the wordmark
```

Stacked lockup (for narrow surfaces, social profile pictures, app icons):

```
   ●
 tinkr
```

The wordmark alone is the most common form. The symbol alone is reserved for app icons, favicons, and 1×1 surfaces. The combined lockup is for the docs site header, the Tauri shell title bar, and marketing site headers.

### 2.4 The full CLI banner (for `tinkr` on first run)

The full banner is the wordmark + the version + a single one-liner. Designed to fit in 80 columns of a terminal.

```
   _  _       _      
  | | (_) ___| | __  
  | | | |/ __| |/ /  
  | |___| (__|   <   
  |_____|\___|_|\_\  v0.3.0

  The hardware IDE that ships.
```

The wordmark is rendered in cyan; the version number is dim; the tagline is in the default terminal color. (The actual SVG / figlet file lives in `tinkr.cli/cli/banner.txt` and is generated from the source — this is the visual specification, not the final asset.)

### 2.5 Clear space and minimum size

- **Clear space** around the mark: at least the height of the "b" in the wordmark, on all sides.
- **Minimum size**: 16 px height for the symbol alone; 80 px wide for the wordmark alone.
- **Never**: rotate the mark, stretch it, recolor the dot, add a drop shadow, put it on a busy background.

---

## 3. Color palette

The palette is built for the terminal first, the GUI second. Every color exists in 24-bit (true color), 256-color, and 16-color fallbacks. Light and dark mode are both first-class.

### 3.1 Brand colors

| Role | Token | Hex (24-bit) | 256-color | 16-color | Notes |
|---|---|---|---|---|---|
| **Primary** | `brand-primary` | `#5EEAD4` | 51 (cyan) / 48 | 6 (cyan) / bold 6 | "Circuit cyan." Used for headings, links, the wordmark on dark, brand emphasis. |
| **Primary dim** | `brand-primary-dim` | `#0D9488` | 30 (teal) | 2 (green) | Pressed / active states, dim text. |
| **Accent / CTA** | `brand-accent` | `#FB923C` | 215 (light orange) / 208 | 3 (yellow) | "LED amber." The "ship it" color. Used for primary CTAs, the LED dot in the mark, success-adjacent emphasis. |
| **Accent dim** | `brand-accent-dim` | `#EA580C` | 166 (dark orange) | 1 (red) | Pressed / active states for the accent. |
| **Secondary** | `brand-secondary` | `#A78BFA` | 141 (light purple) | 5 (magenta) | "Code violet." Used for the agent surface, KB entries, AI-related elements. Separates the human-built (cyan) from the agent-built (violet). |
| **Secondary dim** | `brand-secondary-dim` | `#7C3AED` | 93 (dark purple) | 5 (magenta) | Pressed / active states for the secondary. |

### 3.2 Surface colors — dark mode (default)

| Role | Token | Hex | Notes |
|---|---|---|---|
| **Background base** | `surface-bg-dark` | `#0A0A0B` | Near-black. The default canvas. |
| **Background raised** | `surface-raised-dark` | `#111113` | Cards, panels, raised surfaces (+1 from base). |
| **Background sunken** | `surface-sunken-dark` | `#050506` | Code blocks, terminal panes, recessed surfaces (−1 from base). |
| **Border subtle** | `border-subtle-dark` | `#1F1F23` | Hairlines, separators. 1 px. |
| **Border default** | `border-default-dark` | `#27272A` | Card borders, input borders. 1 px. |
| **Border strong** | `border-strong-dark` | `#3F3F46` | Hover borders, focus borders. 1 px. |
| **Text primary** | `text-primary-dark` | `#FAFAFA` | Body text, headings. 16.4:1 contrast on bg-base. |
| **Text secondary** | `text-secondary-dark` | `#A1A1AA` | Captions, helper text. 7.0:1 contrast on bg-base. |
| **Text tertiary** | `text-tertiary-dark` | `#71717A` | Disabled text, placeholders. 4.6:1 contrast on bg-base. |
| **Text inverse** | `text-inverse-dark` | `#0A0A0B` | Text on light surfaces (buttons on amber). |

### 3.3 Surface colors — light mode

| Role | Token | Hex | Notes |
|---|---|---|---|
| **Background base** | `surface-bg-light` | `#FAFAFA` | Off-white. Slightly warmer than pure white. |
| **Background raised** | `surface-raised-light` | `#FFFFFF` | Cards, panels, raised surfaces. |
| **Background sunken** | `surface-sunken-light` | `#F4F4F5` | Code blocks, terminal panes, recessed surfaces. |
| **Border subtle** | `border-subtle-light` | `#F4F4F5` | Hairlines, separators. 1 px. |
| **Border default** | `border-default-light` | `#E4E4E7` | Card borders, input borders. 1 px. |
| **Border strong** | `border-strong-light` | `#A1A1AA` | Hover borders, focus borders. 1 px. |
| **Text primary** | `text-primary-light` | `#0A0A0B` | Body text, headings. 18.7:1 contrast on bg-base. |
| **Text secondary** | `text-secondary-light` | `#52525B` | Captions, helper text. 7.5:1 contrast on bg-base. |
| **Text tertiary** | `text-tertiary-light` | `#71717A` | Disabled text, placeholders. 4.8:1 contrast on bg-base. |
| **Text inverse** | `text-inverse-light` | `#FAFAFA` | Text on dark surfaces (buttons on cyan). |

### 3.4 Status colors

Identical hex in light and dark mode; only the surface they sit on changes.

| Role | Token | Hex | 256-color | Notes |
|---|---|---|---|---|
| **Success** | `status-success` | `#22C55E` | 42 | Deployed, validated, connected. |
| **Success dim** | `status-success-dim` | `#15803D` | 22 | Success on hover / pressed. |
| **Success surface** | `status-success-surface` | `#052E16` / `#F0FDF4` | — | Success badges / toasts (dark / light). |
| **Warning** | `status-warning` | `#F59E0B` | 214 | Beta features, deprecation notices, slow operations. |
| **Warning dim** | `status-warning-dim` | `#B45309` | 130 | Warning on hover / pressed. |
| **Warning surface** | `status-warning-surface` | `#451A03` / `#FFFBEB` | — | Warning badges / toasts. |
| **Error** | `status-error` | `#EF4444` | 196 | Failures, blocking errors, destructive actions. |
| **Error dim** | `status-error-dim` | `#B91C1C` | 124 | Error on hover / pressed. |
| **Error surface** | `status-error-surface` | `#450A0A` / `#FEF2F2` | — | Error badges / toasts. |
| **Info** | `status-info` | `#3B82F6` | 33 | Informational messages, links in some contexts. |
| **Info dim** | `status-info-dim` | `#1D4ED8` | 21 | Info on hover / pressed. |
| **Info surface** | `status-info-surface` | `#172554` / `#EFF6FF` | — | Info badges / toasts. |

### 3.5 Terminal RGB tuples (for the CLI)

The CLI uses Rich's color spec format. Here is the full mapping for the Python source.

```python
# tinkr/cli/style.py — terminal colors

# 24-bit true color (preferred)
BRAND_CYAN     = "rgb(94,234,212)"     # #5EEAD4
BRAND_CYAN_DIM = "rgb(13,148,136)"     # #0D9488
BRAND_AMBER    = "rgb(251,146,60)"     # #FB923C
BRAND_AMBER_DIM= "rgb(234,88,12)"      # #EA580C
BRAND_VIOLET   = "rgb(167,139,250)"    # #A78BFA

STATUS_SUCCESS = "rgb(34,197,94)"      # #22C55E
STATUS_WARNING = "rgb(245,158,11)"     # #F59E0B
STATUS_ERROR   = "rgb(239,68,68)"      # #EF4444
STATUS_INFO    = "rgb(59,130,246)"     # #3B82F6

TEXT_PRIMARY   = "rgb(250,250,250)"    # #FAFAFA (dark mode)
TEXT_SECONDARY = "rgb(161,161,170)"    # #A1A1AA
TEXT_TERTIARY  = "rgb(113,113,122)"    # #71717A
TEXT_MUTED     = "rgb(63,63,70)"       # #3F3F46

# 256-color fallbacks (auto-selected by Rich if 24-bit not supported)
BRAND_CYAN_256     = "color(51)"   # cyan
BRAND_AMBER_256    = "color(215)"  # light orange
BRAND_VIOLET_256   = "color(141)"  # light purple
STATUS_SUCCESS_256 = "color(42)"   # green
STATUS_WARNING_256 = "color(214)"  # amber
STATUS_ERROR_256   = "color(196)"  # red
STATUS_INFO_256    = "color(33)"   # blue

# 16-color fallbacks (the universal baseline)
BRAND_CYAN_16      = "bright_cyan"
BRAND_AMBER_16     = "bright_yellow"
BRAND_VIOLET_16    = "bright_magenta"
STATUS_SUCCESS_16  = "bright_green"
STATUS_WARNING_16  = "bright_yellow"
STATUS_ERROR_16    = "bright_red"
STATUS_INFO_16     = "bright_blue"
```

The auto-detection ladder (from best to worst): 24-bit → 256-color → 16-color → default. Use Rich's `Console(force_terminal=False)` so the colors gracefully degrade to bold + italic in non-ANSI streams (CI logs, file captures).

### 3.6 Contrast verification (WCAG 2.1 AA)

The hard requirement is 4.5:1 for normal text, 3:1 for large text (18 px+ or 14 px bold), 3:1 for interactive elements against background.

| Pairing | Ratio | Pass? |
|---|---|---|
| `text-primary-dark` on `surface-bg-dark` | 18.6 : 1 | AAA |
| `text-secondary-dark` on `surface-bg-dark` | 7.0 : 1 | AAA |
| `text-tertiary-dark` on `surface-bg-dark` | 4.6 : 1 | AA |
| `text-primary-light` on `surface-bg-light` | 18.7 : 1 | AAA |
| `text-secondary-light` on `surface-bg-light` | 7.5 : 1 | AAA |
| `text-tertiary-light` on `surface-bg-light` | 4.8 : 1 | AA |
| `brand-primary` on `surface-bg-dark` | 12.6 : 1 | AAA — primary text on dark |
| `brand-primary` on `surface-bg-light` | 1.6 : 1 | **Fail** — primary is for accents on light, never body text |
| `brand-accent` on `surface-bg-dark` | 8.2 : 1 | AAA — accent on dark CTA text |
| `brand-accent` on `text-inverse-light` | 4.6 : 1 | AA — accent button label on amber itself |
| `status-success` on `surface-bg-dark` | 6.8 : 1 | AA — for status text |
| `status-error` on `surface-bg-dark` | 4.9 : 1 | AA — for status text |

Rule: **primary cyan is for accents on light surfaces (links, focus rings, the wordmark on light, small marks). It is never body text on light.** The text-primary color does that job. Cyan is a high-saturation color and only carries 4.5:1 on dark surfaces.

---

## 4. Typography

Three families. All Google Fonts. All open source. All with system fallbacks.

### 4.1 The trio

| Role | Family | Weights | Usage |
|---|---|---|---|
| **Heading + UI** | Inter (variable) | 400, 500, 600, 700 | All UI text, headings, body, labels, buttons. Default for everything except code. |
| **Body** | Inter (variable) | 400, 500 | Same family as headings. Smaller sizes, regular weight. |
| **Monospace** | JetBrains Mono (variable) | 400, 500, 600 | Code blocks, terminal output, the CLI, the REPL, plugin manifests, chip DBs, KB entries, any data with structure. |

We pick Inter because it is the dev-tool default for good reason (legible at small sizes, excellent in UI, broad weight range, ships as a variable font). We pick JetBrains Mono because it has ligatures for common operators (`->`, `!=`, `>=`), excellent in terminals, and pairs visually with Inter.

### 4.2 Google Fonts import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap"
  rel="stylesheet">
```

For the Tauri shell and the docs site, the font is loaded from Google Fonts at first paint. For the CLI, there is no font — the terminal font is the user's choice. We do not bundle fonts.

### 4.3 Fallback chain

```css
/* Inter fallback */
font-family: 'Inter', system-ui, -apple-system, TinkrMacSystemFont, 'Segoe UI',
             Roboto, 'Helvetica Neue', Arial, sans-serif;

/* JetBrains Mono fallback */
font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco,
             Consolas, 'Liberation Mono', 'Courier New', monospace;
```

The fallbacks are picked so a missing Google Font still looks intentional — system UI on macOS, Segoe UI on Windows, Roboto on Linux, etc. The terminal fallback is the user's terminal font (menlo on macOS, Consolas on Windows, Liberation Mono on Linux).

### 4.4 Type scale

Modular scale at 1.125 (major second). Line-heights are 1.2 for headings, 1.5 for body, 1.4 for UI labels.

| Token | Size (px) | Line-height | Weight | Usage |
|---|---|---|---|---|
| `text-display` | 48 | 56 (1.17) | 700 | Hero headlines on marketing site only. |
| `text-h1` | 36 | 44 (1.22) | 700 | Page titles. |
| `text-h2` | 30 | 38 (1.27) | 600 | Section headings. |
| `text-h3` | 24 | 32 (1.33) | 600 | Subsection headings, card titles. |
| `text-h4` | 20 | 28 (1.4) | 600 | Small headings, panel titles. |
| `text-body-lg` | 18 | 28 (1.55) | 400 | Lead paragraphs, intro text. |
| `text-body` | 16 | 24 (1.5) | 400 | Default body text. |
| `text-body-sm` | 14 | 20 (1.43) | 400 | Captions, secondary text, table cells. |
| `text-caption` | 12 | 16 (1.33) | 500 | Eyebrow labels, badges, tags. |
| `text-code` | 14 | 20 (1.43) | 400 | Code in prose (JetBrains Mono). |
| `text-code-block` | 13 | 20 (1.54) | 400 | Code blocks (JetBrains Mono). |
| `text-terminal` | 14 | 20 (1.43) | 400 | Terminal output (JetBrains Mono). |

### 4.5 Rules

- Body text is always left-aligned. Never justified.
- Headings are sentence case. ("The plugin ecosystem" not "The Plugin Ecosystem".)
- Numbers in tables and code are tabular. Use `font-variant-numeric: tabular-nums` in any tabular context.
- Never use a font weight below 400 in the UI — light weights fail contrast at small sizes.
- Tracked-out uppercase is reserved for `text-caption` (eyebrow labels) and never used for anything else.

---

## 5. Iconography

### 5.1 Style

**Line icons only.** 1.5 px stroke, 24×24 grid, rounded line caps and joins. No filled icons in the UI. No duotone in the UI. (Filled is reserved for badges and status dots; duotone is reserved for marketing illustrations.)

The icon set is **Lucide** (https://lucide.dev). It is open source, MIT-licensed, pixel-consistent, the standard for dev tools, and has every icon we need plus the ones we don't yet need.

We do not draw custom icons unless Lucide is missing one. The threshold for a custom icon is "Lucide has nothing semantically equivalent."

### 5.2 Icon grid

```
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │  ←  24px grid
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

       ◯     ←  stroke ends 1 px from the edge (live area 22x22)
       │
   1.5 px stroke
   rounded caps and joins
```

### 5.3 Naming

`<context>-<noun>` in kebab-case. The set is namespaced by context.

| Context | Examples |
|---|---|
| `device-*` | `device-chip`, `device-plug`, `device-unplug`, `device-usb` |
| `action-*` | `action-flash`, `action-deploy`, `action-monitor`, `action-repl` |
| `nav-*` | `nav-home`, `nav-plugins`, `nav-devices`, `nav-kb`, `nav-docs` |
| `status-*` | `status-online`, `status-offline`, `status-syncing`, `status-error` |
| `ui-*` | `ui-chevron-down`, `ui-close`, `ui-search`, `ui-filter`, `ui-copy` |
| `kb-*` | `kb-fact`, `kb-recipe`, `kb-error`, `kb-pattern`, `kb-story` |

The file is `<name>.svg` in the icon set, and the React/Vue component is `<Icon name="device-chip" />`.

### 5.4 Color

Icons inherit `currentColor`. They pick up the parent's text color. Default is `text-primary` on the current surface. On hover, they shift to `brand-primary` for interactive icons, or stay the same for static icons.

The "tinkring" status indicator is a `status-online` icon with a 1 Hz opacity animation (0.5 → 1.0 → 0.5). All other icons are static.

### 5.5 No emojis

The brand explicitly does not use emoji as UI icons. The reasoning:

- Emoji render differently on every OS (Apple, Google, Microsoft, Twitter all have their own sets).
- Emoji are not accessible by default (screen readers read them with regional names).
- Emoji are visual noise in a precision tool.

The exceptions are:

- The README badges on GitHub (the `shields.io` style) — those are images, not emoji.
- The CLI prompt that uses Unicode box-drawing characters for the table layout — those are typographic primitives, not emoji.
- The user-contributed content on community channels (Discord, forum) — users can use emoji, the brand does not.

---

## 6. Visual style

**Modern Minimalism, dark mode default, with one warm accent.**

The visual style of Tinkr is the visual style of the tools the people we admire build. Specifically:

- **Linear** for the dark surface, the restrained palette, the one accent color, the lack of drop shadows.
- **Vercel** for the typography, the geometric grid, the precision of the spacing scale.
- **Raycast** for the terminal-aware details, the focused single-purpose surfaces.
- **Warp** for the opinionated CLI behavior, the speed of motion, the lack of splash screens.
- **Cursor** for the inline-clarity of the editor, the no-fluff voice of the UI copy.

### 6.1 The principles

1. **Restrained.** One primary color, one accent, one secondary. Status colors only for status. The rest of the palette is grey-scale.
2. **Sharp.** 1 px borders. Hairline separators. No drop shadows. No glows (except the focus ring).
3. **Spacious.** 8 px base spacing unit. Generous padding inside cards. 64 px section padding on marketing surfaces.
4. **Honest.** The UI is what it is. No skeuomorphism. No fake depth. The information is the design.
5. **Dark by default.** Dark mode is not a theme — it is the surface. Light mode is the alternative.

### 6.2 What we are not

- **Neo-brutalism.** No heavy borders, no raw colors, no intentionally rough typography. Engineers want a precision tool, not a manifesto.
- **Glassmorphism.** No `backdrop-blur`, no translucent layers, no gradient meshes. The tool should look the same on a 5-year-old ThinkPad as on a new MacBook.
- **Bento grid.** Reserved for marketing landing pages, not product UI. The product UI is linear and list-based.
- **Aurora / gradient mesh.** The product is not an AI consumer app. The agent is a CLI surface, not a hero animation.
- **3D / skeuomorphic.** The product does not pretend the UI is a physical device. The device is on the desk, plugged in via USB. The UI is a window into it.

### 6.3 What we borrow from the cited tools

| From | What | Why |
|---|---|---|
| Linear | Dark surface, one accent, dense info layouts | Engineers work in dark mode. The UI is information-dense, not decoration-dense. |
| Vercel | Typography, spacing scale, the lack of ornament | The tool gets out of the way. The user's code is the visual focus. |
| Raycast | The launcher metaphor, the speed of motion, the focused single-purpose surfaces | The CLI is a launcher. Every command is a focused action. |
| Warp | The terminal-aware design, the block-based output, the inline error recovery | The CLI is a first-class surface, not a legacy fallback. |
| Cursor | The project-wide context, the inline suggestion pattern, the no-fluff voice | The agent reads the project. The agent suggests inline. The voice is direct. |

### 6.4 The one deviation

The accent color is amber (`#FB923C`), not the typical SaaS purple or blue. The amber is the "LED" — it ties the brand to the hardware metaphor. It is the color of the LED on every Arduino, ESP32 dev board, and Raspberry Pi Pico the user has ever owned.

This is the one place Tinkr is opinionated about color. Everything else follows from the standard dev-tool playbook. The amber is the brand's signature.

---

## 7. Motion principles

Motion is fast, purposeful, and invisible. The user should never wait for an animation; the animation should already be done by the time they noticed it started.

### 7.1 The timing scale

| Token | Duration | Easing | Usage |
|---|---|---|---|
| `motion-instant` | 0 ms | — | State changes that should not animate. |
| `motion-fast` | 150 ms | `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out) | Hovers, focus rings, small state changes. |
| `motion-base` | 200 ms | `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out) | Default for most transitions. |
| `motion-slow` | 300 ms | `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out) | Modal open/close, drawer slide, panel expand. |
| `motion-slower` | 450 ms | `cubic-bezier(0.4, 0, 0.6, 1)` (ease-in-out) | Page transitions, large layout shifts. |
| `motion-tinkr` | 1000 ms | `cubic-bezier(0.4, 0, 0.6, 1)` (ease-in-out) | The "tinkring" LED animation in the brand mark. |

### 7.2 Easing

The default easing is `cubic-bezier(0.4, 0, 0.2, 1)` (the Material "standard" curve). It is the dev-tool default, it is the Vercel default, it is the one engineers don't notice.

The "ease-in-out" curve is reserved for symmetric motions (open + close, expand + collapse). It is never used for one-way transitions.

### 7.3 What animates

- **Opacity** (hover, focus, active, disabled, toast in/out).
- **Color** (border, background, text — all on hover/focus).
- **Transform** (translate, scale — for drawers, modals, toasts).
- **Box-shadow** (focus rings, the single shadow we use).

### 7.4 What does NOT animate

- **Layout.** No grid reflows. No width/height transitions. No `top`/`left` for positioning.
- **Font size.** Headings and body text never change size on hover.
- **Number values** in tables, counters, etc. The number changes instantly.
- **Anything longer than 300 ms** in product UI. (The 450 ms "page transition" is reserved for marketing surfaces.)
- **The CLI output** — there is no motion in the terminal. The cursor tinkrs, the text appears, the prompt returns. That's it.

### 7.5 Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Reduced motion is the default for users who have set the OS preference. We respect it everywhere — even in the LED tinkr animation, which becomes a static dot.

### 7.6 The one branded animation

The LED tinkr in the brand mark: opacity oscillates 0.5 → 1.0 → 0.5 at 1 Hz, indefinitely, on the amber dot in the wordmark. It is the one place the brand breathes. It is suppressed under reduced motion.

---

## 8. Accessibility baseline

WCAG 2.1 AA is the floor. AAA where we can. The product is for engineers, many of whom have disabilities, all of whom will eventually have reduced vision, and all of whom deserve a tool that works without contortion.

### 8.1 Contrast

| Requirement | Ratio | Where |
|---|---|---|
| Normal text (< 18 px, < 14 px bold) | **4.5 : 1** | All body text, labels, captions. |
| Large text (≥ 18 px, ≥ 14 px bold) | **3 : 1** | Headings, large numerals, hero text. |
| Interactive elements | **3 : 1** | Buttons, links, form controls against background. |
| Focus ring | **3 : 1** | Visible against any surface it appears on. |
| Status color | **3 : 1** for the color itself + icon or text | Color is never the only indicator. |

Verified pairings in §3.6.

### 8.2 Focus states

Every interactive element has a visible focus state. The focus ring is:

- 2 px solid `brand-primary` (`#5EEAD4` on dark, `#0D9488` on light)
- 2 px offset from the element edge
- Always visible, never removed (no `outline: none` without a replacement)
- Same on keyboard and pointer focus
- Not animated (it appears instantly)

```css
:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 2px;
  border-radius: inherit; /* match the element's radius */
}
```

### 8.3 Touch targets

- Minimum 44 × 44 px for any interactive element on touch devices.
- Minimum 8 px spacing between adjacent targets.
- The CLI is exempt (terminal input has no concept of touch targets).

### 8.4 Keyboard

Every action is reachable by keyboard. The keyboard map follows platform conventions:

- `Tab` / `Shift+Tab` — move focus forward / backward.
- `Enter` / `Space` — activate the focused control.
- `Esc` — close the current modal / drawer / popover.
- `Cmd/Ctrl+K` — global command palette (in the Tauri shell and the docs site).
- `↑` / `↓` — navigate lists and tables.
- `/` — focus the search field (in the docs site, the marketplace, the KB viewer).

### 8.5 Screen readers

- Every interactive element has an accessible name (via `aria-label`, visible label, or visible text).
- Every image has alt text (or `alt=""` if decorative).
- The status indicator (online / offline) has an `aria-live="polite"` region for state changes.
- The terminal output has `role="log"` and `aria-live="polite"`.
- Form fields have associated labels (via `<label for>` or `aria-labelledby`).
- Error messages are linked to the field via `aria-describedby`.

### 8.6 Color independence

Color is never the only indicator. The status dot has both a color AND an icon (or text label). The error state has both a red color AND an error icon AND the word "Error" or the specific code. The progress bar has both a fill color AND a percentage label.

### 8.7 Forms

- Every input has a visible label above it (never a placeholder as a label).
- Required fields are marked with `aria-required="true"` and a visible `*`.
- Errors appear below the field, in the error color, with a specific message and a link to fix.
- Disabled fields have `disabled` attribute (not just visual styling).

### 8.8 Motion

Reduced motion is respected globally (see §7.5). The brand tinkr animation is the only non-essential motion, and it is suppressed.

### 8.9 Language

The default language is `en`. Other languages are added by the community, with the same baseline. The CLI output and error messages are localized. Marketing copy is localized. The brand voice remains the same in all languages — direct, technical, no marketing speak.

---

## 9. The hard rules (non-negotiable)

These rules override any designer's preference. They are the brand's contract with its users.

1. **The CLI is a first-class surface.** Every brand decision is tested in the terminal first. If it doesn't work in 80 columns of monospace, it doesn't ship.
2. **Light and dark mode are equal.** Neither is a theme. Both are first-class. Every screen, every component, every state is verified in both.
3. **No marketing speak in product copy.** Error messages, CLI output, docs, the Tauri shell — none of it contains the words "empower," "unlock," "seamless," "revolutionary," or "delight."
4. **Accessibility is not a feature.** It is a baseline. WCAG 2.1 AA is the floor. We do not ship features that fail it.
5. **The accent color is amber.** Not blue, not purple, not green. The amber is the LED; the LED is the brand.
6. **Inter and JetBrains Mono only.** No proprietary fonts. No bundled fonts. Google Fonts + system fallbacks.
7. **Icons are line icons.** No filled icons in the UI. No emoji as UI icons. Ever.
8. **Open source by default.** The brand assets (logo, fonts, color tokens, the brand spec itself) are MIT-licensed. Anyone can use them to build a Tinkr plugin.

If a future decision breaks one of these rules, the decision is wrong.
