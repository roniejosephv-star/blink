# Tinkr — Positioning

> The voice, the audience, the place in the market, and the line we will not cross.
> This is the document the rest of the brand builds on.

---

## 1. Product name

**Tinkr.**

Single word, no tagline baked in, no product suffix. The name does the work.

Why "Tinkr":

- **It's the maker verb that pre-dates "maker culture" by a century.** To tinker is to make, fix, experiment, and learn by building. Hardware developers tinker. The product is named for the user, not the product.
- **The "kr" spelling is fanciful and trademark-strong.** Tinker is a common English word with hundreds of existing uses; Tinkr is a made-up mark with no major class 9/42 holder. Tinkercad (Autodesk) is the closest existing product — a kids' circuit simulator at a completely different price point and audience. No collision.
- **It's five letters, one syllable.** Fits a CLI command (`tinkr`), a domain, a tab title, a favicon, a sentence. The shortest possible interaction with the brand.
- **It's pronounceable in any language.** /ˈtɪŋkər/. No diacritics, no awkward sounds.
- **The mark is a circuit, not a wordmark.** For a hardware IDE, the brand mark IS a small piece of PCB — a **visible trace network** (v7, Aug 13) with 17+ bright cyan traces using 45° chamfered corners (real PCB routing, never Manhattan), 24 hollow pin circles at the trace ends (the I/O pads), 12 filled junction nodes at the intersections (the bridges), and 10 dynamic data-packet nodes flowing along Bezier-curve motion paths through the lines. The mark can show **operational state** in 11 different animations, one for each state (idle, thinking, reading, writing, searching, flashing, compiling, done, error, waiting, ship). The trace network is fixed in shape — only the nodes flow, the color shifts, and the speed changes. This is the brand's "instrument-like" DNA made visible — like a logic analyzer watching signals on a real chip. See `brand/02-visual-identity.md §2.1` for the full spec and `brand/mockups/13-wordmark-animations.html` for the 11 states in action.

We use it lowercase in product surfaces (`tinkr`, `tinkr-esp32`, `tinkr.build`) and sentence-case in prose ("Tinkr ships the CLI, the plugins do the work"). The CLI command is `tinkr`. The PyPI / npm package is `tinkr-cli` (the bare `tinkr` name is taken on those registries by an unrelated AI observability tool). The GitHub org is `tinkr-org/`.

---

## 2. Tagline

**LOCKED (Aug 12, 2026): "Tinker on."**

The tagline is two words, imperative, persona-broad, and works as a hero line, a footer, a CLI banner, a button label, and a manifesto. It's an action statement aimed at the user: tinker, with whatever tool you have. Tinkr is the tool.

### Why this one (Ronie's reasoning, recorded)

- **Shortest possible statement of the value prop.** Two words. "Tinker" is the verb. "On" is the commitment. "Tinker on" reads as both an imperative ("start tinkering") and a permission ("you're allowed to tinker"). Either reading works.
- **Imperative, not descriptive.** A tagline that says "we are X" is a brochure. A tagline that says "do X" is a call. "Tinker on." tells the user what the product is for without describing the product.
- **Persona-broad.** Mira tinkers on weekend prototypes. Devansh tinkers with curricula. Sara tinkers with production firmware. They all tinker. The tagline doesn't segment.
- **Pairs with the text wordmark.** The circuit mark + the text `tinkr` (in JetBrains Mono) form the lockup. The circuit is the brand; the text is the type. Together with `tinker on`, the brand reads: "tinkr — tinker on." Two lines, three syllables, done.
- **The "on" is intentionally open.** "On" can mean "start" (begin tinkering) or "ongoing" (keep tinkering, don't stop). The tagline covers the first project and the hundredth. It's a habit, not a moment.
- **No trademark risk.** "Tinker on" is a generic English phrase. Zero conflict.

### Trademark history (compressed — every tagline revision in one place)

| Date | Tagline | Why it changed |
|---|---|---|
| Aug 12 morning | "The hardware IDE that ships." | Engineer-first, persona-narrow. Rejected in the first round. |
| Aug 12 morning | "Tinker on." | Memorable, but trademark-flagged (HIT/Mattel owns "Bob the Builder"). |
| Aug 12 afternoon | "Tinker on." | Replaced the "tinker on" line. Two-word imperative. Pairs with the (then-current) name "Tinkr." |
| Aug 12 evening | "Tinker on" → **"Tinker on."** (locked) | Trademark question fully closed. |
| Aug 12 night | "Tinker on." → **"Tinker on."** (locked) | Name changed from "Tinkr" to "Tinkr." The verb form pairs with the new name. |

### Why not these (kept for reference, not for launch)

- **"The hardware IDE that ships."** — engineer-first, persona-narrow.
- **"Tinker on."** — memorable but trademark-flagged.
- **"Be the builder of things."** — safe but verbose.
- **"Tinker on."** — was the locked tagline for "Tinkr." Replaced when the name changed.
- **"Cursor for Edge Devices."** — one-liner for investor pitches, not the public tagline.
- **"Ship firmware in the tinkr of an eye."** — plays on the (former) name. Cute but stale.
- **"Hardware dev, without the friction."** — persona-broad but dull.

Rule of thumb: if the tagline needs an explanation, it's the wrong tagline. "Tinker on." needs none.

---

## 3. Positioning statement

> **For** hardware developers working on ESP32, RP2040, nRF52, and friends,
> **who** are tired of tools that either treat them like beginners or treat them like enterprise customers,
> **Tinkr** is an open-source hardware IDE built around a small CLI, a plugin ecosystem, and a project repo that acts as the memory.
> **Unlike** Thonny (too simple), PlatformIO (too heavy), or Wokwi (no real hardware), Tinkr treats the project as the source of truth and the community as the engine — so the user owns their work, the plugins stay small, and the agent gets smarter as the community grows.

One paragraph. One sentence if you take the bones out:

> Tinkr is the open-source hardware IDE that puts your project at the center — a small CLI, a plugin ecosystem, and an agent that learns from what you and the community ship.

---

## 4. Target personas

Three personas, one product. Each gets a name, a job, a frustration, and a thing they love about the tool. The brand talks to all three; the product serves all three through the same HAL.

### 4.1 Mira — the hobbyist

- **Background:** Software engineer by day, weekend maker. First project with an ESP32 was a WiFi-connected plant-watering reminder. Has soldered once, broke the joint, ordered a new one.
- **Goal:** Get a working prototype on the desk by Sunday evening. Doesn't care about the cleanest firmware, cares about "it works and my partner thinks it's cool."
- **Frustration:** Every IDE either assumes she's never seen a terminal or assumes she's written a kernel driver. Thonny is friendly but stops where the real work starts. PlatformIO is fast but the docs read like a legal disclaimer.
- **What she values in a tool:** "Just works." Clear errors. A REPL she can paste into. Examples she can clone and run. The feeling that the tool respects her time.
- **What she hates:** Required logins for the 80% case. Marketing splash screens. Tooltips that explain what a button is instead of letting her click it.
- **What Tinkr does for Mira:** `tinkr init` to start, `tinkr plugin add tinkr-esp32` to get her chip, `tinkr project deploy` to ship her code. Five commands, no login required. The friendly path is the default path.

### 4.2 Devansh — the educator

- **Background:** Teaches an "Intro to Embedded Systems" elective to second-year CS students. Has 30 students per cohort, each with a $15 ESP32 dev board and a syllabus.
- **Goal:** Get every student to a working "tinkr the LED" project by week 2, a working sensor-reading project by week 6, and a working capstone by week 12. Reproducibility matters more than elegance.
- **Frustration:** "Works on my machine" is his recurring nightmare. Every year, two students have a different USB driver, three have a different board revision, and one has somehow installed Python 2.7. Grading projects that don't run is a tax he pays every semester.
- **What he values in a tool:** Predictable behavior. Identical project setup across machines. A way to ship a known-good starting template that every student clones. The ability to inspect what a student did without being a detective.
- **What he hates:** Tools that silently update themselves between classes. Floating versions. "Just run this curl-pipe-bash one-liner." Hidden state.
- **What Tinkr does for Devansh:** `tinkr.toml` is a curriculum artifact — every student starts from the same template, every project is reproducible, the lockfile pins every plugin version. The project is the documentation. He can `git clone` a student's repo, run `tinkr install`, and grade what they built, not their toolchain.

### 4.3 Sara — the embedded engineer

- **Background:** Twelve years writing firmware for industrial sensors. C/C++ for the production code, MicroPython for the bring-up scripts and the test rigs. Owns the hardware. Owns the bugs.
- **Goal:** Bring up a new sensor module on a known board, get a working driver skeleton in an afternoon, hand it off to firmware team. She doesn't want a wizard; she wants a screwdriver and a clear manual.
- **Frustration:** Tools that hide the protocol. Tools that re-implement the same chip-datasheet lookup in a way she can't audit. Tools that "simplify" the serial monitor until she can't see the raw bytes. Tools that won't let her write a custom plugin and have the rest of the system pick it up.
- **What she values in a tool:** Precision. Raw access. CLI that doesn't lie. Open file formats. The ability to drop down a layer when the abstraction is wrong. Documentation that links to the chip datasheet, not "for more information see our blog."
- **What she hates:** Black boxes. "AI magic" with no audit trail. Locked-down file formats. Vendor SDKs that "just work" until they don't. UIs that put a friendly face on a broken abstraction.

---

## 5. The line we will not cross

(The same eight hard rules from the v1 brand spec apply. Tagline, name, and visual identity have all changed since the rules were first written, but the rules themselves have not. They are reproduced in `02-visual-identity.md` and remain in force.)

The brand test for any new surface, feature, or asset:

1. **Does it pass the engineer-aloud test?** ("Would an engineer read this aloud to another engineer?")
2. **Does it work in both light and dark?** If not, it doesn't ship.
3. **Does it work in the terminal?** If it doesn't work in 80 columns of monospace, the GUI version doesn't ship either.
4. **Does it break one of the 8 hard rules?** If yes, the decision is wrong, not the rule.

These four questions are the test. The spec is the record. The mark is the design system.
