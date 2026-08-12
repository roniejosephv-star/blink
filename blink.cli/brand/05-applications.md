# Tinkr — Applications

> How the brand shows up on every surface Tinkr ships. The CLI is a first-class surface. The Tauri shell is a view on the CLI. The web surfaces are views on the project. The first-run experience is the brand's handshake with a new user.

---

## 1. CLI output (terminal)

The CLI is the test surface. Every brand decision is verified in 80 columns of monospace before it touches a GUI. The terminal is where the brand proves it can ship.

### 1.1 The prompt

```
$ tinkr
```

Plain, no decoration. No `(base)`, no `~/projects/foo`, no ANSI color. The prompt is the user's prompt — Tinkr does not own it.

Inside an interactive REPL:

```
>>>
```

Three chevrons, dimmed, with a tinkring block cursor. The chevrons are JetBrains Mono. Nothing else. The user is in control; Tinkr is the session.

### 1.2 The banner

On every CLI invocation that does significant work, the first line is the banner. It's a one-liner — not a splash screen, not an ASCII logo, not a six-line figlet.

```
tinkr 0.3.0 · the hardware IDE that ships
```

The first word is in `brand-primary` (cyan). The version is dim. The tagline is in the default terminal color. That's it. The banner never changes between commands. It's recognizable in scrollback without being a billboard.

The figlet ASCII art (the larger banner) ships as an opt-in for the first-run experience only (`tinkr welcome`):

```
   _  _       _
  | | (_) ___| | __
  | | | |/ __| |/ /
  | |___| (__|   <
  |_____|\___|_|\_\  v0.3.0

  The hardware IDE that ships.

  → Run `tinkr init` to start a project.
  → Run `tinkr plugin search` to see available plugins.
  → Run `tinkr doctor` to check your setup.
```

Generated at build time from a `figlet.txt` file with the `colossal` font, in `brand-primary`. It's never auto-printed on every command — that would be spam.

### 1.3 Status indicators

Three states, three symbols. No spinners for completion. No "Loading…" with no progress.

| Symbol | Color | Meaning |
|---|---|---|
| `✓` | `status-success` | success, completed, ok |
| `✗` | `status-error` | failure, error, blocked |
| `⚠` | `status-warning` | warning, beta, deprecated |
| `→` | `brand-primary` | next step, the next thing to do |
| `·` | `text-tertiary` | info, sub-step, detail |
| `?` | `text-secondary` | question, prompt for input |

Every status line starts with one of these. No line of CLI output is ambiguous about its outcome.

Examples:

```
$ tinkr plugin add tinkr-esp32
✓ Resolved tinkr-esp32@1.2.3 from registry
✓ Downloaded to .tinkr/plugins/tinkr-esp32/
✓ Linked 12 CLI tools to .tinkr/bin/
✓ Added to tinkr.toml [plugins]
✓ Locked in .tinkr/lock.toml
✓ Plugin tests passed (5/5)

Installed tinkr-esp32@1.2.3.
→ Run `tinkr device scan` to see your connected ESP32.
```

```
$ tinkr project deploy
· Connecting to esp32s3-left on /dev/cu.usbserial-1410
✓ Connected (ESP32-S3, MicroPython v1.24.1)
· Uploading main.py (1.2 KB) ━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01
✓ Uploaded
· Soft-rebooting
✓ Deployed
· LED is tinkring

Deploy complete in 4.2s.
```

```
$ tinkr device scan
✗ No devices found.

  Check the USB cable and that no other terminal has the port open.
  Run `tinkr doctor` to check your setup.
```

### 1.4 Tables

Tables use Unicode box-drawing for borders. Columns are aligned with the user's terminal width. Numbers are right-aligned and use the terminal's default font (no need for tabular-nums; the terminal does this).

```
$ tinkr plugin list
┌──────────────────────────┬─────────┬───────────┬─────────┬──────────────────────┐
│ Name                     │ Version │ Maturity  │ Devices │ Capabilities         │
├──────────────────────────┼─────────┼───────────┼─────────┼──────────────────────┤
│ tinkr-esp32              │ 1.2.3   │ stable    │ 2/3     │ flash, repl, fs, …   │
│ tinkr-rp2040             │ 0.8.0   │ beta      │ 0/1     │ flash, repl, fs      │
│ tinkr-sniffer            │ 0.1.2   │ exp.      │ -       │ serial-monitor       │
└──────────────────────────┴─────────┴───────────┴─────────┴──────────────────────┘
```

Column headers are in `text-secondary`. Cell text is in `text-primary`. The maturity column uses the badge color (`status-success` / `status-warning` / `status-info` / `status-error`).

Long values truncate with `…` (single character, the Unicode horizontal ellipsis). Empty cells show `-`.

### 1.5 Spinners and progress

Two spinner styles:

- **Dots** for short, indeterminate operations (1–3 s): `⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏`. Cycles at 80 ms per frame. Spinner color: `brand-primary`.
- **Bar** for long, determinate operations (flash, upload): `━━━━━━━ 100% 0:00:04`. Bar color: `brand-primary`. Background: `text-tertiary` (dimmed). Numbers are right-aligned in `text-secondary`.

The spinner label is on the same line, left of the spinner:

```
· Uploading main.py (1.2 KB) ━━━━━━━━━━━━━━ 100% 0:00:01
```

On success, the spinner is replaced by `✓`. On error, by `✗`. The progress event becomes a status line — no separate "done" state.

In non-TTY contexts (CI logs, file capture, `tinkr > out.log`), spinners are stripped to just the final status line. Progress bars show the final percentage. No ANSI in the file output. The `--json` flag forces NDJSON on stdout regardless of TTY.

### 1.6 Error messages

Error messages are three lines, always:

1. **What went wrong** — one line, the failure, in `status-error`.
2. **Why** — one line, the likely cause, in `text-primary`.
3. **What to do** — one line, the next step, in `brand-primary`, with the command to run.

```
✗ Couldn't open /dev/cu.usbserial-1410.
  Port is busy — another process has it open (`screen`, `minicom`, the Arduino IDE).
  → Close the other process, then run `tinkr device scan`.
```

```
✗ Plugin tinkr-esp32 failed to install.
  Missing dependency: esptool>=5.2 (found 4.7).
  → Run `pip install 'esptool>=5.2'` then `tinkr plugin add tinkr-esp32`.
```

```
✗ Flash failed at 23%.
  esptool reported: "Failed to connect to ESP32: Timed out waiting for packet header."
  → Hold down the BOOT button on the device, then run `tinkr project flash`.
```

Error codes are the same ones the plugin manifest uses (`PORT_NOT_FOUND`, `FLASH_FAILED`, `IMPORT_MISSING`, `OSError_ETIMEDOUT`). The CLI prints the code in the JSON output for programmatic consumers; the human gets the three-line format.

### 1.7 Interactive prompts

When Tinkr needs user input (confirming a destructive op, picking a device, picking a plugin version), it uses an inline prompt:

```
? Erase flash on esp32s3-left? (yes/no) [no]:
```

The `?` is in `text-secondary`. The question is in `text-primary`. The default value is in `text-tertiary` and bracketed. The user's typing appears after the colon, in the default terminal color.

For choices, use the arrow-key picker:

```
? Which port is the ESP32 on?
  ❯ /dev/cu.usbserial-1410   (ESP32-S3)
    /dev/cu.usbmodem14101    (RP2040 Pico)
    /dev/cu.usbserial-1420   (unknown)

  ↑/↓ to move · enter to select
```

The selected option has a `❯` marker in `brand-primary`. The list is in `text-primary`. The hint is in `text-tertiary`.

Both styles respect `--yes` / `--no` flags for scripting. Both write the answer to stdout (the same NDJSON stream the rest of the CLI uses, with `type: "user_response"`).

### 1.8 ANSI / no-ANSI

The CLI auto-detects TTY. If stdout is not a TTY (file, pipe, `> out.log`), ANSI codes are stripped. The `--color=always|never|auto` flag overrides.

The `NO_COLOR` environment variable (https://no-color.org) is respected. If `NO_COLOR` is set, ANSI is disabled regardless of TTY.

The `TERM=dumb` terminal type forces no-ANSI. The `TERM=xterm-256color` and `TERM=*-truecolor` types use the full 24-bit palette. Anything else falls back to 256-color, then 16-color.

---

## 2. Tauri desktop shell (v1.5)

A thin native window on top of the CLI. The Tauri shell is a view, not a different product.

### 2.1 Window chrome

- **Title bar**: native OS title bar. Title is `tinkr — <project>`. Icon is the Tinkr symbol mark (24×24 PNG/ICO).
- **Frame**: native. The shell is not frameless; we don't want to be a "Mac-app-pretending-to-be-iOS" app.
- **Traffic lights**: standard on macOS, standard on Windows, no special handling.
- **Minimum size**: 800 × 600. Below this, the shell forces fullscreen.
- **Default size**: 1280 × 800. Restored on relaunch.

The Tauri shell is dark by default. The OS title bar uses the system theme. We do not draw a custom title bar — Tauri 2's default looks correct, and a custom one would be a maintenance burden.

### 2.2 Menu bar

The native menu bar. The Tinkr menu is a single, focused set of items:

```
File
  New project           ⌘N
  Open project…         ⌘O
  ─
  Close project         ⌘W
  ─
  Quit tinkr            ⌘Q

Edit
  Undo                 ⌘Z
  Redo                 ⇧⌘Z
  ─
  Cut                  ⌘X
  Copy                 ⌘C
  Paste                ⌘V
  Select all           ⌘A
  ─
  Find                 ⌘F

View
  Toggle sidebar       ⌘\
  Toggle panel         ⌘;
  Toggle fullscreen    ^⌘F
  ─
  Command palette      ⌘K
  ─
  Toggle theme         ⌘⇧L

Project
  Scan devices         ⌘⇧S
  Open REPL            ⌘⇧R
  Deploy               ⌘⇧D
  Monitor              ⌘⇧M

Help
  Documentation        F1
  Knowledge base
  GitHub repository
  Report an issue
  About tinkr
```

Shortcuts follow platform conventions (Cmd on macOS, Ctrl elsewhere). No sub-menus in v1.5; the menu bar is intentionally flat.

### 2.3 Layout

The shell is a three-pane layout:

```
   ┌─ Title bar ───────────────────────────────────────┐
   ├─ Menu bar ────────────────────────────────────────┤
   ├─ Sidebar ──┬─ Main view ──────────────────────────┤
   │  (240px)   │                                       │
   │            │   [content per active tab]            │
   │  ▸ Project │                                       │
   │  ▸ Devices │                                       │
   │  ▸ Plugins │                                       │
   │  ▸ KB      │                                       │
   │            │                                       │
   ├─ Status bar ─────────────────────────────────────┤
   └──────────────────────────────────────────────────┘
```

The sidebar is the navigation (component 9). The main view is tab-based (component 8). The status bar is a single 24 px line at the bottom.

### 2.4 Status bar

A single 24 px line, `bg-surface-raised-dark`, top border `border-subtle-dark`. Five regions, left to right:

```
   [device: esp32s3-left ✓]   [branch: main]   [agent: idle]   …   [notifications: 0]   [build: 0/0]
```

- **Device** — the active device, with the status indicator (component 11). Click to switch.
- **Branch** — the current git branch. Click to open git tools.
- **Agent** — the agent state (`idle` / `thinking…` / `running tool: flash`). Click to open the agent panel.
- **Spacer** — flex-fill.
- **Notifications** — count of unread toasts. Click to open the notification center.
- **Build** — current build status (0/0, 1/0 errors, etc.). Click to open the build panel.

Each region is its own `<button>`. The whole bar is keyboard-navigable.

### 2.5 The agent panel

A right-side panel, 360 px wide, that slides in when the agent is invoked (`⌘K` for the command palette, or a chat-style trigger). The panel contains:

- The current conversation.
- The agent's current action (`Calling flash.esp32s3_left…`).
- A small list of which tools the agent has access to (collapsible).
- An input field at the bottom for the user's next message.

The panel uses `bg-surface-raised-dark`, a 1 px left border. The brand mark is in the panel header, dim, with the LED dot animating while the agent is thinking.

### 2.6 What the shell never does

- Splash screen with the logo. The window appears instantly, content loads.
- Onboarding modal that blocks the app. The first-run experience is a single banner across the top that the user can dismiss.
- Animated background, particle effects, or any "wow" transition.
- Custom title bar, custom traffic lights, custom window controls.
- A "loading…" overlay. The shell shows the current state. If the project is being scanned, it shows "Scanning…". If the agent is thinking, it shows "Thinking…".

---

## 3. Marketplace web UI (v1.5)

A web UI at `tinkr.build/marketplace`. Cards, search, filters, plugin detail pages.

### 3.1 Layout

- **Header**: 64 px, dark surface, contains the wordmark (left), the search bar (center, max-width 480 px), the auth menu (right).
- **Body**: 1280 px max-width, 24 px padding, two-column at lg+ (sidebar filters + grid).
- **Footer**: minimal, 64 px, links to docs / GitHub / Discord / Twitter.

### 3.2 The plugin grid

A 3-column grid at `lg`, 2-column at `md`, 1-column at `sm`. The card is component 3 (with header, badge, capabilities, version, install count, install button).

Sort options: Most installed, Recently updated, Recently published, Alphabetical.

Default view: 12 cards per page, pagination at the bottom.

### 3.3 Filters

A vertical filter sidebar, 240 px, sticky on scroll:

- **Maturity**: stable, beta, experimental, deprecated (checkboxes).
- **Chip family**: ESP32, RP2040, nRF52, Pico, SAMD, … (searchable).
- **Capabilities**: flash, repl, fs, plotter, gdb, ota (checkboxes).
- **License**: MIT, Apache-2.0, GPL-3.0, … (checkboxes).
- **Price**: Free, Paid, $1–10, $10–50, $50+ (radio).
- **Verified by Tinkr team**: only (toggle).

Filters apply on change. The result count is shown above the grid: "47 plugins · filtered from 312."

### 3.4 The plugin detail page

URL: `tinkr.build/marketplace/<plugin-name>`

Layout:

- **Hero band** (320 px): name, description, install button, version, maturity badge, install count, star count.
- **Tabs** (component 8): Overview, Tools, Knowledge, Versions, Reviews, Dependencies.
- **Overview tab**: long description (Markdown), the plugin's README, screenshots (if any), the maintainers.
- **Tools tab**: table of CLI tools, one row each. Columns: name, description, tier, requires device, requires port.
- **Knowledge tab**: list of files in the knowledge bundle, with file type icon, name, and size.
- **Versions tab**: version history, with semver bumps, dates, and "what changed" links.
- **Reviews tab**: 1–5 star reviews from users. Sorted by recent.
- **Dependencies tab**: required plugins, required Python packages, the Tinkr version range.

The "Install" button is sticky on the right side as the user scrolls.

### 3.5 Search

The search bar is in the header. It's a real-time search, debounced at 200 ms. Results appear in a dropdown as the user types:

- Top 5 plugin matches.
- Top 5 KB entry matches.
- Top 5 docs page matches.
- A "See all results" link.

`/` focuses the search bar. `Esc` clears it.

---

## 4. Docs site (tinkr.build/docs)

The docs site is content-first. It is the long-form reference for everything Tinkr does.

### 4.1 Layout

- **Header**: 64 px, dark surface, wordmark + version selector + search + GitHub link.
- **Sidebar** (left, 280 px): the docs hierarchy. Collapsible sections.
- **Main** (center, max-width 768 px for prose): the article.
- **Right sidebar** (240 px, on lg+): the table of contents for the current page.
- **Footer**: minimal, "Edit on GitHub" link, last-updated date, prev/next page links.

The content area is 768 px wide on a 1280 px viewport. The text is `text-body` (16 px / 1.5 line-height) with `text-h3` headings. Code blocks are component 10.

### 4.2 Typography

- **Body**: Inter 400, 16 px / 24 px line-height, `text-primary`.
- **Headings**: Inter 600/700, the type scale. Sentence case.
- **Code in prose**: JetBrains Mono 14 px, `bg-surface-sunken-{theme}`, padding 2 px 4 px, `radius-sm`.
- **Code blocks**: component 10, full width (within the main column).
- **Links**: `text-brand-primary`, underline on hover, never the default blue.
- **Lists**: `text-body`, hanging indent, 8 px between items.
- **Blockquotes**: 4 px left border in `brand-secondary`, italic, `text-secondary`.

### 4.3 The sidebar

A 280 px sidebar with the doc hierarchy. Sections are collapsible. The active page is highlighted with `bg-brand-primary/10` and `text-brand-primary`.

Each item in the sidebar is a real `<a>`. Keyboard navigation works (↑/↓ to move, Enter to follow, Space to collapse).

### 4.4 Search

A search modal (`⌘K` / `Ctrl+K`) that searches the entire docs site. Powered by a static index. Results are ranked by:

- Title match (weight 10).
- Heading match (weight 5).
- Body match (weight 1).
- Code match (weight 1).

Top 10 results, with the matching text highlighted. `Enter` follows the first result. `↑/↓` navigates.

### 4.5 Code samples

Every code sample in the docs is real and runnable. The "Copy" button in component 10 is always present. Long samples have a "Run in the playground" link (when the sample is a Tinkr CLI command, this opens a simulated terminal in the browser).

The code samples use the same syntax highlighting colors as the design system (component 10).

---

## 5. KB viewer (tinkr.build/kb)

A read-only view of the curated knowledge base. Search-first.

### 5.1 Layout

- **Header**: same as the docs site. Search is the primary action.
- **Body**: 1024 px max-width. Two states: search results (list of cards) and entry view (one card, expanded).

### 5.2 Entry cards

The KB has five entry types: `fact`, `error`, `pattern`, `recipe`, `story`. Each gets a card variant:

- **Fact** — small, dense, one-line summary + chips for `category` and `chips`.
- **Error** — medium, the error code, the summary, "what to do" steps in a numbered list.
- **Pattern** — large, the summary, the wiring diagram (image), the code skeleton.
- **Recipe** — large, the summary, the step list (numbered, with `run` shown as code).
- **Story** — long-form, the case study, the project, the outcome.

Each card has a type badge in the top-left:

- `fact` → `bg-status-info-surface-{theme}` / `text-status-info`
- `error` → `bg-status-error-surface-{theme}` / `text-status-error`
- `pattern` → `bg-status-success-surface-{theme}` / `text-status-success`
- `recipe` → `bg-brand-accent` / `text-text-inverse-dark`
- `story` → `bg-brand-secondary` / `text-text-inverse-dark`

### 5.3 Search

The KB search is a single search box. Real-time, debounced at 200 ms. Results grouped by type:

```
   Facts (12)
     • ESP32 I2C pins have no internal pull-ups
     • ESP32-S3 has 45 GPIO, 20 ADC channels
     …

   Errors (8)
     • OSError: [Errno 110] ETIMEDOUT on i2c.scan()
     …

   Recipes (3)
     • Flash MicroPython to a fresh ESP32 and deploy tinkr-led
     …

   Patterns (2)
     • ESP32 + BME280 over I2C
     …

   Stories (1)
     • Bringing up a BME280 on the kitchen sensor: a 30-minute adventure
     …
```

The grouping is collapsible. The default sort is by relevance, with a toggle for "most used" (telemetry, opt-in).

### 5.4 Cross-references

KB entries reference each other and reference datasheets, plugins, and chip DBs. These are real `<a>` tags in the rendered Markdown. The link style:

- Entry → entry: `text-brand-primary`, hover underline.
- Entry → datasheet (PDF): `text-text-secondary`, "PDF" badge, icon `file-text`.
- Entry → plugin: `text-brand-secondary`, plugin icon.
- Entry → chip DB: `text-text-primary`, chip icon.

Every cross-reference is a clickable link. No "see also" lists that are just text.

---

## 6. Plugin registry (`github.com/tinkr-registry/index`)

A git repo with submodules — one per plugin. The registry is open source, version-controlled, fork-able. The visual identity here is the GitHub README.

### 6.1 The top-level README

```markdown
# tinkr-registry

The official Tinkr plugin registry. Open-source. PR-based. Anyone can submit a plugin.

## Browse

- [Plugin index](plugins.toml)
- [Knowledge base](https://github.com/tinkr-knowledge/index)
- [Recipe library](https://github.com/tinkr-recipes/index)

## Submit

- Read the [submission guide](CONTRIBUTING.md)
- Run `tinkr plugin init` to scaffold a new plugin
- Open a PR adding your plugin to `plugins.toml`

## Stats

- 312 plugins · 1,247 tools · 5,438 knowledge files
- Updated 14 minutes ago
```

No hero image. No marketing. The README is the table of contents. The brand is the GitHub badge.

### 6.2 The plugin README

Every plugin repo follows the same README template. The template is part of the plugin spec.

```markdown
# tinkr-esp32

> ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6 support via esptool and minny.

![Status](https://img.shields.io/badge/status-stable-22C55E?style=flat-square)
![Version](https://img.shields.io/github/v/release/tinkr-esp32/tinkr-esp32?style=flat-square)
![License](https://img.shields.io/github/license/tinkr-esp32/tinkr-esp32?style=flat-square)
![Downloads](https://img.shields.io/badge/dynamic/json?style=flat-square&label=downloads&query=$.downloads&url=...)

## Install

`tinkr plugin add tinkr-esp32`

## Supported devices

- ESP32-DevKitC
- ESP32-S3-DevKitC-1
- M5Stack-CoreS3
- NodeMCU-32S

## Capabilities

- `flash` · `repl` · `filesystem` · `package_manager` · `serial_plotter`

## Documentation

- [Quickstart](docs/quickstart.md)
- [API reference](docs/api.md)
- [Knowledge bundle](knowledge/)

## License

MIT
```

### 6.3 Shields.io badge style

Every badge uses `style=flat-square` (matches the brand's flat aesthetic). The colors are the brand status colors:

| State | Hex (no leading #) |
|---|---|
| Stable | `22C55E` |
| Beta | `F59E0B` |
| Experimental | `3B82F6` |
| Deprecated | `EF4444` |

The label is `status` (lowercase), the value is the state (lowercase). The left-side color is always dark grey (`0A0A0B`) — Tinkr's surface color — so the badge is recognizable across all repos.

---

## 7. Marketing site / landing page (tinkr.build)

The marketing site is the one place the brand is allowed to be a little louder. Still direct. Still no fluff. But the typography is bigger, the spacing is more generous, and there is a hero.

### 7.1 The hero

```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │                                                              │
   │           The hardware IDE that ships.                       │
   │                                                              │
   │           A CLI, a plugin ecosystem, and an agent            │
   │           that reads your project.                           │
   │                                                              │
   │           [Get started]   [View on GitHub]                   │
   │                                                              │
   │                                                              │
   │     ┌────────────────────────────────────────────────────┐   │
   │     │  $ tinkr init                                      │   │
   │     │  ✓ Created tinkr.toml                              │   │
   │     │  $ tinkr plugin add tinkr-esp32                    │   │
   │     │  ✓ Installed tinkr-esp32@1.2.3                     │   │
   │     │  $ tinkr project deploy                            │   │
   │     │  ✓ Deployed. LED is tinkring.                      │   │
   │     └────────────────────────────────────────────────────┘   │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
```

The hero is text, not video. The "screenshot" is a real terminal session, captured in a screenshot, not a fake mockup. The headline is 48 px (display size), 1 line. The subhead is 18 px (body-lg), 2 lines. The CTAs are above the fold.

### 7.2 The features section

Three feature blocks, 3-column on `lg`, 1-column on `sm`. Each has:

- A 24 px icon in `brand-primary` (Lucide).
- A 1-line title.
- A 2-line description.

```
   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
   │  [chip icon]       │  │  [plugin icon]     │  │  [git icon]        │
   │                    │  │                    │  │                    │
   │  Project-as-memory │  │  Plugin ecosystem  │  │  Git-collaborative │
   │                    │  │                    │  │                    │
   │  Your project repo │  │  Hardware support  │  │  Every project is  │
   │  is the source of  │  │  is a git repo,    │  │  a git repo.       │
   │  truth. Tinkr      │  │  not a vendor SDK. │  │  Branch, review,   │
   │  reads it.         │  │  The community     │  │  ship.             │
   │                    │  │  grows the         │  │                    │
   │                    │  │  ecosystem.        │  │                    │
   └────────────────────┘  └────────────────────┘  └────────────────────┘
```

### 7.3 The "How it works" section

A 4-step horizontal flow, with arrows between steps. Each step is a card with a number, a title, a description, and a terminal command.

```
   1. Install          2. Add a plugin     3. Plug in         4. Deploy
   ──────────          ──────────          ──────────          ──────────
   $ pip install       $ tinkr plugin      Plug your          $ tinkr project
   tinkr-micropython   add tinkr-esp32     ESP32 in.          deploy

                        ↓                  ↓                  ↓

                        Run `tinkr         Run `tinkr         Watch the
                        device scan`.      repl`.             LED tinkr.
```

### 7.4 The "Who builds with Tinkr" section

A 3-column grid of personas. Each card is a 240×320 card with an avatar, a name, a quote (1–2 lines), and a use case (1 line).

```
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  [M]     │  │  [D]     │  │  [S]     │
   │  Mira    │  │  Devansh │  │  Sara    │
   │          │  │          │  │          │
   │  "I had  │  │  "Every  │  │  "I can  │
   │  my      │  │  student │  │  read    │
   │  kitchen │  │  on the  │  │  every   │
   │  sensor  │  │  same    │  │  line of │
   │  running │  │  page by │  │  the     │
   │  in an   │  │  week 2. │  │  driver  │
   │  hour."  │  │  That's  │  │  before  │
   │          │  │  the     │  │  I run   │
   │          │  │  win."   │  │  it."    │
   │          │  │          │  │          │
   │  Hobbyist│  │ Educator │  │ Engineer │
   └──────────┘  └──────────┘  └──────────┘
```

### 7.5 The pricing section

A simple, three-tier layout. Free, Maker Bundle, Pro Bundle. The Free tier is the IDE. The Maker Bundle is all plugins + 5 seats. The Pro Bundle is Maker + cloud build + priority support.

```
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │  Free      │  │  Maker     │  │  Pro       │
   │            │  │  Bundle    │  │  Bundle    │
   │  $0        │  │  $49       │  │  $199      │
   │            │  │  lifetime  │  │  lifetime  │
   │  ✓ CLI     │  │  ✓ Free    │  │  ✓ Maker   │
   │  ✓ 4 free  │  │  ✓ All     │  │  ✓ Cloud   │
   │    plugins │  │    plugins │  │    build   │
   │  ✓ Docs    │  │  ✓ All     │  │  ✓ Priority│
   │  ✓ KB      │  │    future  │  │    support │
   │            │  │    plugins │  │  ✓ 5 seats │
   │  [Get]     │  │  [Buy]     │  │  [Buy]     │
   └────────────┘  └────────────┘  └────────────┘
```

The "Free" column has the brand-accent CTA (amber). The "Maker" column is highlighted with a "Recommended" badge. The "Pro" column has a "For teams" badge.

### 7.6 The footer

```
   tinkr — the hardware IDE that ships.
   ┌──────────┬──────────┬──────────┬──────────┐
   │ Product  │ Docs     │ Community│ Legal    │
   │ CLI      │ Quickstart│ Discord │ Privacy  │
   │ Plugins  │ Plugin   │ Forum   │ Terms    │
   │ Marketplace│ spec   │ Twitter │ License  │
   │ Pricing  │ HAL      │ GitHub  │          │
   └──────────┴──────────┴──────────┴──────────┘

   © 2026 Tinkr. MIT licensed core.
```

### 7.7 What the marketing site never does

- A "trusted by" logo wall of companies that haven't used the product.
- A "features" page that's a list of 47 bullet points. Six features, each with substance.
- A "testimonials" page with stock photos. Quotes only, attributed by name and role.
- A "blog" with SEO-bait posts about "the future of embedded development."
- A "contact us for enterprise pricing" CTA. The pricing is on the page.
- A cookie banner that blocks the page. The cookie banner is at the bottom, dismissable, and remembers the choice for a year.

---

## 8. CLI welcome / first-run experience

The first thing a new user sees. The brand's handshake.

### 8.1 The trigger

`tinkr` with no arguments, run for the first time. The user has just installed Tinkr. They've typed `tinkr` and hit enter.

### 8.2 The output

```
   _  _       _
  | | (_) ___| | __
  | | | |/ __| |/ /
  | |___| (__|   <
  |_____|\___|_|\_\  v0.3.0

  The hardware IDE that ships.

  Welcome. Three commands to get started:

    1. mkdir kitchen-sensor && cd kitchen-sensor
    2. tinkr init
    3. tinkr plugin add tinkr-esp32

  → Run `tinkr doctor` to check your setup.
  → Run `tinkr help` to see all commands.
  → Visit https://tinkr.build for the full guide.

  v0.3.0 · MIT licensed · https://github.com/tinkr-core/tinkr
```

The ASCII art is in `brand-primary`. The "three commands" block is the meat — it's a real, runnable sequence. The links at the bottom are in `text-secondary`.

### 8.3 The follow-up

The first time the user runs `tinkr init`, they see:

```
✓ Created tinkr.toml
✓ Created .tinkr/
✓ Created .gitignore
✓ Created main.py (hello world — tinkrs the LED on GPIO 2)
✓ Created lib/
✓ Created tests/

Your project is ready.

  → Plug in your board, then `tinkr plugin search` to find support.
  → Already have a plugin? `tinkr plugin add <name>` to install it.
  → Run `tinkr project deploy` to flash and run.
```

The hello world is a real, runnable tinkr-the-LED program. It's the brand promise in code form. The user has shipped something in the first 60 seconds.

### 8.4 What the first-run experience never does

- A "let's set up your account" flow. Login is optional, for power features.
- A "subscribe to our newsletter" prompt. There's a link in the footer, not a modal.
- A "watch our 90-second intro video" CTA. The CLI is not the place for video.
- A "select your hardware" wizard. The user will plug in a board when they plug in a board.
- A "rate this experience" prompt. Not yet. Maybe at 30 days. Maybe never.

The first-run is fast, useful, and gets out of the way. The user came to ship, not to be onboarded.

---

## 9. Cross-surface consistency rules

The same data should look the same on every surface. The rules:

1. **A plugin name is `tinkr-<vendor>-<family>` everywhere.** CLI, Tauri, marketplace, docs, KB, registry, marketing.
2. **A device ID is `chip-side` or `chip-location`.** Same format in `tinkr.toml`, the CLI, the Tauri shell, the KB.
3. **A version is `MAJOR.MINOR.PATCH`** (SemVer). No `v` prefix in code, no `v` prefix in display. The CLI prints `1.2.3`, not `v1.2.3`. The docs say "1.2.3".
4. **A status is one of `stable | beta | experimental | deprecated`.** Same words, same colors, same badge, everywhere.
5. **An error code is the same everywhere.** `PORT_NOT_FOUND` in the CLI is `PORT_NOT_FOUND` in the KB, the docs, and the marketplace.
6. **A color is one of the 8 brand + 4 status colors.** No new colors are added without a token in `03-design-tokens.json`.
7. **A font is Inter or JetBrains Mono.** No other fonts, anywhere.

If a surface needs a new pattern, the pattern is added to this document, not invented locally.
