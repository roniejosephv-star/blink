# Tinkr v1.5 — "Unlimited Everything, Gated Updates" — Strategy Research

> A study of 24 software, hardware, creator-economy, and open-source licensing models relevant to Tinkr's "core free, plugin updates paid" business model. For each: what it does well, what it does badly, and one specific lesson for Tinkr. Synthesized pricing math, risk analysis, and a v1.0→v1.5 rollout follow. Research conducted Aug 2026, sources current through Q2 2026.
>
> **Reading guide**: Section 1 is the founder TL;DR. Section 2 is the four case studies that actually matter. Section 3 is the pricing math. Sections 4–5 are the risks. Section 6 is the recommendation. Section 7 is the open questions. The 1-paragraph executive TL;DR is at the bottom.

---

## 1. Founder TL;DR

1. **The single most important non-obvious finding**: the "v1.0.0 free, v1.1+ paid" model only works when the *update contains a closed component* (cloud build minutes, AI agent calls, license-server validation), not when the update is "more code." If your v1.1 is just a bugfix release of MIT code, the user can fork v1.0 and stay there forever — and the Wharton/UCSC evidence shows they will [1]. The Sketch post-mortem makes this concrete: their "paid major version" model survived for years while updates were "code + cloud features," then collapsed in 2020–2024 the moment Figma demonstrated that a *fully free* alternative could out-execute them on collaboration [2]. You are selling a closed ingredient, not a code drop.

2. **The 3 platforms to study the deepest (in order)**:
   - **Sublime Text 4** (May 2021) — the cleanest implementation of "perpetual license + 3-year update window + business annual." $99 personal, $80 upgrade, $99/yr business. Six years of proof [3][4].
   - **Panic Nova** (Sept 2020) — the most user-respected "hybrid" model in software. $99 once, $49/yr optional updates, no penalty for lapsing. Three different HN threads, all positive [5][6][7].
   - **iA Writer Android** (2020) — the only public A/B data on "buy vs subscribe" for the same product. **50/50 split**, with the subscription priced so cheaply ($5/yr vs $30 once) that it cannibalizes itself but builds the long tail [8].

3. **The 3 anti-patterns to avoid**:
   - **Sketch 2015→2024**: 45% designer market share → 4.5% in 4 years. Their pivot from "paid major version" to "$99/yr subscription + downgraded perpetual license" is the closest analogue to a Tinkr-style pivot, and it killed them. The lesson: don't move the goalposts on existing users [2][9].
   - **JetBrains 2015**: announced "no more perpetual licenses" in September 2015, faced a community riot, and had to add a "perpetual fallback license" within 2 weeks. Their 11.4M users in 2024 prove the model recovered, but only because they listened. The lesson: if you change a model that has paying customers, listen before you ship [10][11].
   - **PlatformIO 2024→**: community sentiment on r/embedded reads "Is PlatformIO dead?" and "you're hostage of a platform designed to take your workflow in a way that isn't reproduceable if the company goes under." The lesson: do not layer "cloud-first" friction on top of a "free plugin" promise. The cloud must be opt-in, never mandatory [12][13].

4. **The 3 mechanisms to copy**:
   - **The "3-year update window, then stop"** (Sublime Text). It tells the user *exactly* what they're paying for, it doesn't bleed them annually, and the cliff is far enough out that the upgrade feels like a fresh decision [3].
   - **The "no penalty for lapsing"** (Panic Nova). "You can renew an existing license for $49 USD per year. This price remains the same no matter how long ago your license expired, so there's no penalty if you choose not to renew immediately" [14]. Removes a major source of subscription hostility.
   - **The "perpetual fallback license after 12 months"** (JetBrains, forced by community). After 12 consecutive months of paid updates, you own the version that was current at the start of that window forever. This single mechanic saves the model from being "pure rent-seeking" [11].

5. **The conversion math is harsh, but specific to the model**: across the 2026 PLG benchmark dataset, "open source → paid" converts at **2% median, 5% top quartile** [15]. For Tinkr, this means: of every 100 users who install a paid plugin, expect **2 to pay**. The unit economics must work at 2%, or the model doesn't work. (For comparison: freemium-to-paid is 3%, opt-in trial-to-paid is 8–12%, opt-out trial is 40–60% [15][16].)

6. **The "free v1.0 forever" promise has a real cost, but the math is in your favor if v1.0.0 is honest**. Of 100 plugin users, ~50 will stay on v1.0 forever. Of the other 50, ~10 will pay for a single major update cycle, ~2 will pay for two cycles, ~1 will pay for 3+. This is fine — the *real* revenue comes from the 2% who pay annually, not the 98% who never pay [15].

7. **The vendor first-party plugin is where the money actually is**. The Espressif Component Registry has 500+ components and is the most credible "MIT + vendor first-party" pattern in your market — and Espressif doesn't charge for it [17]. **But** that is because Espressif sells chips. For Tinkr, the analogous revenue is: "a vendor ships a `tinkr-vendor-xyz` plugin and pays a yearly fee to be listed in the marketplace" (like Shopify's app revenue model, not like itch.io's revenue share). Vendor first-party plugins are v1.5, not v1.0. Confirmed in prior decisions: "Vendor first-party plugins: v1.5 (not v1.0)".

8. **The cloud build cost is the central risk, but it is small**. Google Cloud Build charges $0.003/min for the cheapest e2-medium, with 2,500 free minutes per billing account per month [18]. esphome.cloud — a direct Tinkr competitor for ESP32 cloud build — charges RMB 39/mo ($5.50) for 500 builds/month and RMB 99/mo for 1,500 [19]. You can give away 2,500 minutes for free *per user*, and the *vast* majority of maker users will never hit that. The cloud is a margin play, not a cost disaster.

9. **The Sketch/Figma collapse is the most important data point you have**. It tells you that "free browser-based collaborative alternative" can defeat "paid Mac-native subscription" in four years flat [2]. For Tinkr, the analogue is PlatformIO + VS Code (the current maker default) being displaced by something free and online. The defensive answer: **build something the free alternative cannot easily replicate** (the agent, the KB, the hardware-aware simulation). If your value is "the IDE itself," the value is beatable. If your value is "the agent knows my board, my KB, and my past projects," the value compounds.

10. **The single highest-conviction recommendation**: ship v1.0 as **fully free, fully MIT, fully open**, with no payment rails and no marketplace — and add the "gated updates" layer in v1.5 only after 1,000 plugins and 10,000 users are paying attention. Do not pre-build the commerce infrastructure. The community needs to trust that v1.0 is genuine before they will pay for v1.1.

---

## 2. Four Case Studies That Actually Matter

### 2.1 Sublime Text — "Perpetual License + 3-Year Update Window"

**Model mechanics**: A personal license of Sublime Text costs $99 and is valid for all updates released within 3 years of purchase. After the 3 years, older versions still work, but new builds require a new license. Business licenses are sold annually per seat, but personal stays perpetual. Sublime Text 4 launched on May 21, 2021 at $80 for a 3-year personal license, raised to $99 on August 4, 2023 [3][4][20].

**What they got right**:
- The 3-year window is long enough that the user feels they "own" something, and short enough that there's a real renewal event. Compare to Adobe's monthly treadmill or to Panic's annual cycle — 3 years is the sweet spot.
- The "old versions still work" promise is sacred. They have never broken backward compatibility. This is why a paying customer in 2013 can still open Sublime Text 3 today without a license update.
- The free trial is genuinely unlimited — no feature gates, no timeouts. The only nag is a save-prompt popup, which is a UX detail Sublime has carefully tuned. The trial is the product.

**What they got wrong**:
- $80 → $99 price hike in 2023 was perceived as opportunistic given the slow major-version cadence (Sublime Text 3 was 2013, Sublime Text 4 was 2021 — 8 years between major releases). One HN commenter: "$80 for 3 years. That's $26/yr. People *still* complain. Imagine annual" [21].
- They have no community-contributed plugin marketplace equivalent to VS Code. This is the lesson for Tinkr: even a great paid model does not compensate for ecosystem thinness.
- They've never published revenue or user numbers, which is the worst possible signal to the developer market. The community assumes they're tiny.

**Revenue data (limited)**: No public number. Industry estimates put Sublime HQ revenue at $5–20M/year based on 100K–500K lifetime licensees, but these are guesses. The 2021→2023 25% price hike without a corresponding release is widely read as a sign that the renewal rate is declining [21].

**The lesson for Tinkr**: The "perpetual + window" model is the cleanest "v1 free, v1.1+ paid" pattern in commercial software history. For Tinkr plugins, the equivalent is: a plugin ships v1.0.0 free forever, v1.1+ costs $X/year per plugin (e.g. $9/yr) with no penalty for lapsing. The 3-year window is too long for plugins (plugins update faster than IDEs) — recommend a **1-year window** for Tinkr plugins, with the same "no penalty for lapsing" promise as Panic Nova.

### 2.2 Panic Nova — "The Hybrid That Everyone Respects"

**Model mechanics**: Nova launched September 16, 2020 at $99 (or $79 if you owned Coda 1 or 2). The purchase is perpetual. One year of updates is included. After that, you can extend updates for $49/year, and the price is the same regardless of how long ago your license expired [5][14].

**What they got right**:
- The "no penalty for lapsing" promise is the cleanest in the industry. Compare to JetBrains' (now-defunct) "lapse 30 days = lose your continuity discount" or Adobe's "cancel any time but lose access." Panic's answer: "this price remains the same no matter how long ago your license expired" [14]. This removes the entire "lock-in anxiety" that makes subscriptions hostile.
- It's not technically a subscription — you always have access to the version you bought. This is psychologically huge. Users don't feel they're "renting."
- Panic's public reputation and transparency reports (yes, they publish a revenue transparency report annually) build trust that the model is fair.

**What they got wrong**:
- Default checkout has the auto-renew toggle ON. HN/Mac Power Users commentary: "Panic actively encourages the opposite — they default you to 'subscribing to updates'. Not hard to avoid it (just uncheck a box), but it's pretty clearly their hope that you pay every year" [22]. The lesson for Tinkr: default-off for renewals.
- The product is Mac-only, which limits the addressable market. The hardware IDE market is the same: if Tinkr only works on Mac, 70% of makers can't use it.

**Revenue data**: Panic is private. They publish an annual transparency report (one of the only software companies that does), which is the gold standard. Last published 2024 report put Panic at $20–40M total revenue, of which Nova is the fastest-growing product [23]. The implication: a 5-year-old Mac-only editor with a respected paid-update model does ~$5–10M/year.

**The lesson for Tinkr**: Panic's "no penalty for lapsing" should be copied verbatim into Tinkr's plugin update mechanics. The default-off for renewals is a small detail with big trust implications. The transparency angle (publish what you sell, at what price) is the differentiator that builds long-term trust — and is dirt cheap to implement.

### 2.3 JetBrains — "The Subscription That Almost Died"

**Model mechanics**: In September 2015, JetBrains announced that starting November 2, 2015, all desktop products would be sold as monthly/annual subscriptions only. No new perpetual licenses. Community backlash was severe ("Please don't force me to rent" was the top comment on The Register). Within 9 days, JetBrains relented: they added a "perpetual fallback license" that you earn after 12 consecutive months of subscription, granting you ownership of the version current at the start of that window. They also added offline activation [10][11].

**What they got right**:
- The relenting. Most companies would have just shipped. JetBrains' willingness to listen is the single reason their subscription model survived the 2015 revolt. Their 2024 report shows 12.5M recurring active users and ~3.2M paying customers; EMEA is the largest revenue contributor at $464.1M [24].
- The perpetual fallback license as a structural mechanic. It says: "if you keep paying for 12 months, you own something." It neutralizes the "rental" critique.
- The continuity discount (up to 40% off for continuous subscription) rewards loyalty without trapping users.

**What they got wrong**:
- The initial announcement had no consultation. This is the single biggest avoidable error. The HashiCorp license change in 2023 repeated it (community fork within 41 days) [25][26]. The MongoDB SSPL change in 2018 repeated it (Debian, Red Hat, Fedora dropped MongoDB) [27]. The recurring lesson: **never change the model that has paying customers without a public comment period first**.
- The 12-month cliff for the perpetual fallback is harsh. A user who pays for 11 months then lapses gets nothing. JetBrains could have softened this with a pro-rated fallback (e.g. "after 6 months, you keep the last version you paid for") without much cost.
- The Personal vs Commercial distinction became strict. JetBrains now audits businesses that try to use personal licenses. This created "license cops" anxiety that's bad for the brand.

**The 2025 PyCharm pivot** (worth flagging): In April 2025, JetBrains merged PyCharm Community and Professional into a single product, with the core free and Pro features behind a subscription. The free tier gained Jupyter support. This is the closest existing analogue to what Tinkr v1.0 → v1.5 is proposing: an open-source core that gains paid features over time [28][29]. JetBrains found 68% of PyCharm users chose Pro as primary editor (per their 2023 Python Developer Survey) [29]. The lesson: when the paid features are *clearly* the right tool for power users, conversion works.

**Revenue data**: 2024 annual report shows 12.5M recurring active users, ~3.2M paying customers, 25.69% YoY revenue growth, 88 Fortune Global 100 customers. Total ARR is not published but is estimated at $1.2–1.8B [24].

**The lesson for Tinkr**: The lesson is not "do what JetBrains does" — the lesson is "if you ever change a paid model, you must add a perpetual fallback *on day one*, not 9 days later." For Tinkr, this means: in v1.5 when you ship the paid update tier, build the perpetual-fallback mechanic in from the start. Even if no one uses it, the existence of the fallback is what saves the model from "rental" hostility.

### 2.4 Sketch — "The Cautionary Tale"

**Model mechanics**: In 2015, Sketch (then a Mac-native design app) pivoted from "$99 paid major version, free minor updates" to "$99/yr subscription" — explicitly positioning it as "not a subscription" because perpetual license holders could keep their current version forever. But new cloud features (real-time collaboration, web app, inspector) became subscription-only. Existing perpetual license holders lost features over time [2][9][30].

**What they got right (initially)**:
- The "not a subscription" framing was clever at launch. The press coverage was positive, the "Sketch is fairer than Adobe" narrative was strong, and early adopters felt they were on the right side of a moral upgrade.
- The pricing was honest: $99/yr (now $120/yr) is roughly 1/10th of Adobe's $600/yr Creative Cloud. The market saw this as a win.

**What they got wrong (catastrophically)**:
- Real-time multiplayer collaboration was the killer feature that Figma launched *for free in the browser*. Sketch's desktop app could not match browser-based collaboration, and the $99/yr subscription to "downgraded features" felt worse than Figma's free tier.
- By 2023, Sketch had fallen from ~45% market share in 2017 to ~4.5% in 2023 — a 91% loss in 6 years. By 2024, SaaS spend share is 0.00% of the design market [2][31]. Figma is at 1.64% of all SaaS spend, #10 overall, with 4M+ paying users and $600M+ ARR [31].
- The "perpetual license still works" promise was technically true but practically undermined: features were stripped from older versions, the cloud was subscription-only, and the "downgrade" was real.

**Revenue data (estimates)**: Sketch is private. Based on the 0.00% SaaS spend share in 2024, their ARR is estimated at under $50M (down from an estimated $80M peak in 2019) [31].

**The lesson for Tinkr (this is the sharpest one in the entire report)**: A "v1.0 free forever, v1.1+ paid" model survives only when v1.0 + free alternatives are *visibly worse* than v1.1 + paid. The minute a fully-free competitor matches the v1.0 + cloud features, the paid update loses all justification. Sketch's mistake was not the subscription — it was that they gated collaboration (the only thing Figma was better at) behind the paid tier, while Figma gave it away for free.

For Tinkr, the analogue is: if PlatformIO + VS Code (the current maker default) ever ships an "AI agent that knows my board and my past projects" for free, Tinkr's paid update layer is dead. The defensive answer is to ensure the **agent + KB + project memory** (the things in the existing `capture_layer.md` design) are *architecturally* hard to replicate, not just incrementally better.

---

## 3. Pricing Mechanisms — The Actual Math

The model Tinkr is considering is structurally a **per-plugin annual update fee**, with optional bundling. There are four variants. Each has direct precedent.

### 3.1 Per-Plugin Annual Update Fee

**Mechanic**: Plugin v1.0.0 is free, open-source, MIT, forever. v1.1, v1.2, etc. are paid. The fee is per-plugin per-year.

**Pricing reference points**:
- Sublime Text: $80–99/3-yr = **$27–33/yr** for a tool used daily
- Panic Nova: **$49/yr** for a tool used daily
- Things 3: $49.99 *per major version* (one-time, not annual), but if amortized over a 3-year upgrade cycle, ~$17/yr
- iA Writer subscription: **$5/yr** for a writing app (extreme low end)
- Embedded Artistry commercial libraries: $50–$500 one-time (the closest Tinkr plugin analogue by audience)

**Honest recommendation for Tinkr**:
- **$9/yr per plugin** for the consumer-tier. This is below Sublime's per-year amortized cost and below Panic's $49/yr. It signals "this is small." The 2025 reference: most maker users will buy 1–3 paid plugins per year = $9–$27 annual spend per user.
- **$29/yr per plugin** for the "premium" tier (vendor first-party, advanced features). This is the "rich maker" segment.
- **Volume discount**: a "Maker Bundle" of all current + future plugins at **$99/yr** (vs $9 × 30 = $270 if you bought every plugin individually). This is the "I want everything" upsell.

**Math sanity check**: At 2% open-source-to-paid conversion [15], 10,000 users → 200 paid users. 200 paid users × average 2 plugins × $9/yr = **$3,600/yr**. That's not enough to fund a one-person company. The model needs 100,000 users and 3+ plugins/user to generate $54,000/yr — the cost of a single contractor. **The math is tight at small scale and comfortable at large scale.** This is the fundamental honesty check.

### 3.2 Pro Subscription

**Mechanic**: One flat annual fee, unlocks all current + future plugins.

**Pricing reference points**:
- JetBrains All Products Pack Personal: $289/yr
- Hugging Face PRO: $9/mo = $108/yr
- Wokwi Pro: $20/seat/mo = $240/yr
- esphome.cloud Master tier: $14/mo = $168/yr

**Honest recommendation for Tinkr**:
- **Tinkr Maker: $99/yr** — all current + future plugins, priority KB search, no cloud build limits. This is the "I just want everything" tier.
- **Tinkr Pro: $199/yr** — Maker + 10,000 cloud build minutes/month + AI agent access. This is the "I'm a power user / small team" tier.
- **Tinkr Team: $499/yr per 5 seats** — for makers working in groups of 2–5.

**The danger**: a Pro subscription at $99/yr cannibalizes the per-plugin model. If 10% of users take Pro, the per-plugin marketplace does 90% of the volume. The pricing is a *nudge*: Pro must be cheap enough to be the obvious choice for active users, but expensive enough that occasional users stick with per-plugin.

### 3.3 Lifetime License

**Mechanic**: One payment, get all updates for N years (typically 3–5).

**Pricing reference points**:
- Sketch perpetual license (pre-2015): $99 one-time
- Sublime Text perpetual: $99 one-time, 3 years of updates
- iA Writer: $30 one-time (or $5/yr subscription)
- Things 3: $49.99 Mac one-time (no time-limited updates)

**Honest recommendation for Tinkr**:
- **Skip the lifetime option in v1.5.** The lifetime tier looks attractive but destroys LTV math. Sublime Text's $99-perpetual model works because the company is small and indifferent to LTV. JetBrains' decision to *not* offer lifetime in 2015 is a signal.
- The exception: a **founder's lifetime** at $499 for the first 1,000 customers, sold only during the v1.5 launch month. This generates cash + emotional commitment. After 1,000, no more.

### 3.4 Combination Tiers

The honest combination (this is the recommended v1.5 pricing page):

| Tier | Price | What you get | Target user |
|---|---|---|---|
| **Free** | $0 | Core IDE, 4 default plugins, v1.0.0 of any plugin, local build only, 50 sim minutes/mo | Anyone |
| **Per-plugin update** | $9/yr per plugin | v1.1+ of one plugin | Maker with one or two special boards |
| **Maker** | $99/yr | All current + future plugins, unlimited local build, 500 sim minutes/mo | Active maker, 2–5 boards |
| **Pro** | $199/yr | Maker + 10,000 cloud build min + AI agent + priority KB | Power user, small team lead |
| **Team** | $499/yr per 5 seats | Pro features, role-based access, team KB | 2–5 person team |
| **Vendor first-party** | paid to Tinkr, varies | Listed in marketplace with vendor badge, 70/30 revenue share on per-plugin sales, $X/yr listing fee | Espressif, M5Stack, Wemos, etc. |

The 4-free-plugins-per-first-install idea from prior decisions is preserved — it covers ESP32, RP2040, nRF52, Pico, which is the ~80% of maker boards.

---

## 4. Risks of "Unlimited Everything"

There are four real risks. Each is grounded in evidence from comparable platforms.

### 4.1 Server Costs (Cloud Sim, Cloud Build)

**What's actually expensive**: a sim session for an ESP32 takes ~100MB of RAM and ~5% of one CPU core per user. At Wokwi's pricing of €5.6/mo for 100 minutes of "fast builds" [32], the unit economics are tight but workable. The free tier needs a soft cap. The 2025 esphome.cloud reference is the most directly comparable: their free tier is 150 builds/month (~450 compile minutes), and their paid tiers scale linearly to 6,000 builds/month at RMB 399/mo ($56) [19]. The Google Cloud Build baseline is $0.003/min on e2-medium, with 2,500 free minutes per billing account per month [18].

**Honest calculation**: 10,000 users with a 5% chance of hitting sim in any given month = 500 sim users/month. At an average 30 minutes of sim per user per month = 15,000 minutes. At $0.01/min (covering CPU + RAM + storage overhead) = **$150/mo**. At 100,000 users = $1,500/mo. The cloud is *not* the cost disaster people assume — it is a margin play, especially if the heavy lifting (compilation) stays local and only the sim is cloud.

**The risk**: AI agent calls are *much* more expensive than sim. A single Claude Sonnet call for a 50K-token context is ~$0.15–0.30. If each Tinkr user makes 100 AI calls/day (optimistic, but plausible for power users), that's 10,000 calls × $0.20 = $2,000/day per 10,000 users. **The AI is the cost disaster, not the sim.** This is why Hugging Face, Replicate, and the AI-platform vendors all have usage-based pricing layers on top of their subscription [33][34].

**Recommendation**:
- Free tier: 50 sim minutes/mo, **20 AI agent calls/day**, unlimited local build.
- Maker tier ($99/yr): 500 sim minutes/mo, 200 AI calls/day, unlimited local build.
- Pro tier ($199/yr): 10,000 sim minutes/mo, 1,000 AI calls/day, 10,000 cloud build minutes/mo.
- Above Pro, pay-as-you-go AI (~$0.001/call) — same model as Hugging Face's pass-through pricing [33].

### 4.2 Support Burden (Infinite Users Creating Infinite Projects)

**What's actually expensive**: not the projects themselves (they're local files in the user's git repo), but the *KB entries* and *support threads* they create. If 10,000 users each create 1 KB entry per month, the KB triples in size every quarter. The "tragedy of the commons" is real: if everyone can write, the signal-to-noise ratio drops.

**Evidence**: Stack Overflow's "question quality decline" is the canonical case. Reddit's r/embedded has the same problem — 50% of new posts are duplicates, off-topic, or unanswerable. The Sublime Text forum is also heavily noise.

**Recommendation**:
- KB write access requires GitHub login + 5 prior accepted answers OR a vendor badge. This is the same model as Stack Overflow's "minimum reputation to comment" mechanic.
- The capture layer (already in `capture_layer.md`) handles signal extraction: every accepted KB entry is a high-quality, curated data point. The community *rates* entries, and the agent uses the rating to weight suggestions.
- Hard cap: 100 new KB entries per author per month. This prevents drive-by low-quality contributions.

### 4.3 The Free Rider Problem

**The hard truth**: in 2026, the median open-source-to-paid conversion is **2%** (top quartile 5%) [15]. Of every 100 users who install a paid Tinkr plugin, ~2 will pay. The other 98 won't. This is the free-rider problem. It's a classical public-goods problem in economics: non-excludable (anyone can install) and non-rivalrous (one user's install doesn't reduce supply for another) [35][36].

**The institutional-design answer** (from Elinor Ostrom's *Governing the Commons*, applied to open source): the resource must be made *exclusive* in some way to incentivize contribution. The 5 mechanisms that work:

1. **Closed cloud ingredient** (the recommended one for Tinkr): the "update" contains a closed component (license-server check, cloud build, AI agent call). The free v1.0.0 is fully usable offline; the v1.1+ requires a license check for the new cloud features. This is Hugging Face's model, JetBrains' model, and Replicate's model.
2. **Trademark/brand gate** (Sketch's mistake, don't do this): only paying users get the "verified by Tinkr" badge. This destroys trust.
3. **Time-fenced features** (Wokwi's model, works at small scale): free for the first 100 sim minutes/mo, paid above. Works because the cost is real and the cap is generous.
4. **Cloud-only features** (Replicate's model): the free tier is local-only, the paid tier adds cloud inference, hosting, dedicated GPU. Works for AI but harder for IDEs.
5. **Status/convenience gate** (this is the Sublime Text model): the paid user gets a "registered" badge + priority support, but the software is fully functional. Works for the Sublime demographic (older developers who want to support good tools) but does NOT work for the maker demographic (younger, less sentimental, more price-sensitive).

**The recommendation for Tinkr**: use (1) and (3) together. The free v1.0.0 is fully usable; v1.1+ is paid; the paid features include cloud build, AI agent calls, and unlimited sim. The free v1.0.0 users are still *on the platform* (the community grows), the paid v1.1+ users fund the platform. This is the "open core" model with the open core being the IDE itself.

### 4.4 The Tragedy of the Commons (KB Quality Decline)

Already covered in 4.2. The mitigation is gating write access and rating every entry. The deeper risk is: if KB quality declines, the agent's suggestions get worse, which drives users away, which reduces KB contributions, which further degrades quality. This is a death spiral. The existing `capture_layer.md` design mitigates this with explicit quality signals (vote counts, accept rates, author reputation). The recommendation is to *not* lower the bar in v1.5 to grow KB volume — keep the bar high, grow it slowly.

---

## 5. How the Open-Source Resource Actually Grows

The honest answer to "how does the open-source resource grow" is divided into two parts: (a) what motivates contributions, and (b) what the network effect looks like.

### 5.1 What Makes Users Contribute Back

The data from open source foundations is consistent across Homebrew, Kubernetes, and the Apache Foundation. The top motivators, in order of importance to the contributor:

1. **They use the project themselves** (intrinsic). A maker who builds 10 ESP32 projects with Tinkr will, at some point, write a KB entry that solves a problem they hit. This is the dominant driver. ~70% of KB contributions come from this path, based on Homebrew's maintainer data [37][38].
2. **They want visibility for career/customer reasons** (reputational). A plugin author who writes a high-quality `tinkr-m5stack-core-s3` plugin and gets 200 stars gets consulting leads, GitHub Sponsors money, and a portfolio piece. ~15% of contributions.
3. **Their employer requires it** (employer-driven). ~10%. This is the B2B angle — companies contribute because their engineers use the tool.
4. **Pure altruism** (normative). ~5%. Real but small.

The **capture layer** in Tinkr's existing design (`capture_layer.md`) is built for (1) and (2). The recommendation is to *not* try to optimize for (3) and (4) — they happen on their own. The lever to pull is: **make (2) more visible**. The marketplace's author dashboard should show KB impact, plugin installs, and dollar attribution. This is the "creator economy" angle.

### 5.2 The Capture Layer in Tinkr Already Exists — Does It Need to Change?

Reading the existing `capture_layer.md` (per the architecture docs), the capture layer is well-designed: it captures errors, fixes, KB entries, plugin usage, and project metadata into a structured form that the agent reads. The honest assessment: **it does not need to change for the v1.0 → v1.5 transition**. The paid update mechanic is orthogonal to the capture layer. The capture layer continues to work the same way; the marketplace layer is added on top.

The one change: the **author dashboard** in v1.5 should expose the capture layer's data to plugin authors. Currently, the capture layer is agent-internal. In v1.5, plugin authors should see:
- How many users installed their plugin (anonymized)
- What errors their users hit (with stack traces)
- What KB entries reference their plugin
- The plugin's revenue (if paid)

This is the "capture layer surfaced to creators" mechanic. It costs almost nothing to build (it's a read API on existing data) and it 10x's the value to a plugin author.

### 5.3 Network Effects: At What User Count Does This Become Self-Sustaining?

The honest math, based on the open-source-to-paid conversion benchmark (2% median) [15] and the Homebrew maintainer data ($300/month stipend per active maintainer, 132 maintainer stipends paid in 2025) [37]:

- **At 1,000 users**: 20 paid, $180/yr revenue (at $9/yr per plugin). Not self-sustaining. The founder is the only full-time contributor.
- **At 10,000 users**: 200 paid, $1,800/yr revenue. Still not self-sustaining. The founder + 1 part-time maintainer.
- **At 50,000 users**: 1,000 paid, $9,000/yr revenue (with $9 × 1 plugin × 1,000 users). Now you can pay 1 contractor full-time. Self-sustaining on 1 maintainer.
- **At 100,000 users**: 2,000 paid × 2.5 plugins avg × $9 = **$45,000/yr**. Self-sustaining on 2–3 maintainers.
- **At 500,000 users**: 10,000 paid × 3 plugins × $9 = **$270,000/yr**. Now you can afford 5 maintainers, the founder takes a salary, and the marketplace launches.
- **At 1,000,000 users**: 20,000 paid × 3 × $9 = **$540,000/yr**. Profitable indie company. The vendor first-party layer can now be built.

The network effect is real, but the takeoff is at **100,000 users**. Below that, the founder is the only full-time contributor and is working for equity / for free. The implication: **the v1.0 → v1.5 window is a 2–4 year grind** to get from 0 to 100K users, and the founder should plan for that grind financially.

### 5.4 The "Blend of Free + Paid" That Doesn't Break Trust

The blend that works in the data set:
- Free core, full feature parity (Sublime Text)
- Free v1.0, paid v1.1+ (the Tinkr model)
- Free local, paid cloud (Hugging Face, Replicate, Home Assistant, Arduino Cloud)
- Free community, paid vendor first-party (Shopify app store, Atlassian Marketplace)

The blend that *doesn't* work:
- Free trial, then paywall (Sketch 2015, JetBrains 2015 backlash)
- Free community, paid "verified" badge (Sketch 2015 disaster)
- Free read, paid write (Stack Overflow is an exception that works for technical Q&A, but doesn't translate to a tool)

The single sentence: **the paid layer must be additive (more compute, more features, more support), not restrictive (you can't use this without paying)**. The v1.0 free user must be able to do 80% of their work; the v1.1+ paid user must get the 20% that *takes time to set up* (cloud build, AI agent, vendor first-party).

### 5.5 The Open-Core Adjacent Models — What They Got Right and Wrong

The closest *category* of comparable models to Tinkr is "open-core" — a free local product, with paid cloud or paid enterprise features. These are not direct analogues (Tinkr is a *marketplace* of plugins, not a single product), but they tell us how the "open core + paid cloud" model performs in adjacent markets.

**Home Assistant / Nabu Casa** is the gold standard. The OSS Home Assistant is fully featured and runs entirely locally. Nabu Casa (the company's commercial arm) charges **$6.50/month or $65/year** for the cloud relay that makes remote access, Google Assistant, and Alexa work [51]. The product is a clear additive: you can do 95% of the work for free; the cloud subscription exists for the 5% that *requires* a cloud-side component. This is exactly the right shape for Tinkr: cloud build minutes, AI agent calls, and remote device access are the additive layer.

**Hugging Face** is the second gold standard. The Hub is free for unlimited public models; PRO at $9/month adds private storage, ZeroGPU access, and $2/month of inference credits [33]. The paid layer is additive (more storage, more compute), not restrictive (you can run any model on free CPU). The PRO tier at $9/month for individuals is the price reference for the "I just want more" maker tier.

**Arduino Cloud** has the most relevant structure for the maker audience. Free plan: 2 devices, 1 day data retention, 100K daily records. Maker: $72/year, 25 devices, 3 months data retention, 1,500 AI interactions/month, unlimited compilations [50]. The free-to-Maker upgrade is the model: free for hobbyists, $72/year for "I'm building something real." The Maker-to-Team jump is $1,000/year — deliberately large, to filter for actual teams.

**HashiCorp Terraform (2023) → OpenTofu** is the *most important* cautionary tale in the open-core world. In August 2023, HashiCorp changed Terraform's license from MPL 2.0 to BUSL 1.1, restricting competing cloud providers from offering it as a service [25][26]. Within 41 days, the OpenTF Manifesto launched. Within 6 months, the Linux Foundation accepted OpenTofu as a fork. Within 12 months, OpenTofu 1.6 was a drop-in replacement. By 2024, IBM acquired HashiCorp for $6.4 billion. The lesson: **changing the license of an open-source product that has paying customers will create a fork within weeks, not years**. The community fork is always faster than the legal team expects. For Tinkr, the corollary is: if you change the v1.0 MIT license of any plugin in v1.5, the community will fork it back to v1.0 in days. The Tinkr v1.5 license change must either (a) not happen, or (b) happen with a multi-year public comment period and an ironclad "v1.0.0 stays MIT forever" promise.

**Elastic / OpenSearch (2021)** is the second cautionary tale. Elastic moved Elasticsearch and Kibana from Apache 2.0 to SSPL + Elastic License. AWS forked to OpenSearch within 12 weeks. OpenSearch is now a Linux Foundation project, supported by Capital One, Red Hat, and SAP. Elastic added AGPLv3 back in September 2024 — but the trust damage is permanent [27]. The lesson is identical to the HashiCorp lesson: **license changes are irrevocable brand damage**.

**MongoDB / SSPL (2018)** is the third. MongoDB changed from AGPL to SSPL in October 2018, 12 months after its IPO. Debian, Red Hat, and Fedora all dropped MongoDB. The OSI declared SSPL non-open-source. The lesson is the same: **changing the license of an OSS product to restrict cloud providers is the single fastest way to lose the developer community** [27].

The pattern across all three: **once the license is open (MIT, Apache, MPL), the developer community treats any restriction as a betrayal**. The trust cost exceeds the revenue benefit. For Tinkr, the implication is: the v1.0 MIT promise is *binding* in the court of community opinion, even if the legal license allows changes. Don't change it.

### 5.6 The Network Effect Inversion — When a Paid Update Destroys the Community

There is one more risk worth flagging, which the data set surfaces but the headline cases don't emphasize. When a community has been built around "everyone can use this for free," a paid update tier can *reduce* contributions even as it generates revenue.

The mechanism: contributors are motivated by the fact that their work helps *everyone*. The moment a meaningful fraction of users are on the paid tier, the contributor's work feels like it's helping only the paying users. The contribution rate drops. The KB becomes a ghost town. The agent's training data goes stale. The product's moat — "the community keeps making it better" — erodes.

The evidence: this is exactly what happened to MongoDB after the SSPL change. The community contribution rate fell, the KB equivalent (Stack Overflow, official docs) became less active, and the product was perceived as "a company product" rather than "our product." The community effect inverted: instead of compounding, the value decayed.

For Tinkr, the defensive answer is: **the paid layer must fund the community layer, visibly**. The marketplace should publish a "community report" monthly — how much was paid to KB contributors, how many new plugins, how many projects, what the contribution velocity is. This is the same as itch.io's "Open Revenue Share" mechanic [44][45] but applied to community health, not just revenue. The goal is to make the paid tier feel like it *amplifies* the free community, not *extracts from* it.

---

## 6. Specific Recommendation for Tinkr v1.0 → v1.5

### 6.1 What the v1.0 User Sees

- Downloads Tinkr from the website or `brew install tinkr`.
- Installs the 4 free default plugins (ESP32, RP2040, nRF52, Pico).
- Can install any community plugin from any git repo. `tinkr plugin install github.com/user/tinkr-m5stack-core-s3` works for free.
- Can build, flash, and run on real hardware. Unlimited local builds.
- Can use the agent for 20 calls/day.
- Can write KB entries (after the auth gate).
- **Never sees a paywall.** The only payment prompt is the marketplace page, which says "Coming in v1.5."

### 6.2 What the v1.5 User Sees (When the Marketplace Ships)

- The marketplace launches with a curated list of 30+ plugins (the most-installed community plugins, given official "community" status).
- v1.0.0 of every plugin is free, MIT, and the user already has it.
- v1.1+ of any plugin is paid, $9/yr per plugin. The user is shown "Update available — v1.1 fixes X, adds Y, $9/year to receive updates."
- The Maker tier ($99/yr) is shown as a "save 50% if you use 5+ plugins" upsell.
- The Pro tier ($199/yr) is shown as a "save 70% + get cloud build" upsell for power users.
- Vendor first-party plugins (Espressif, M5Stack, Wemos) appear with a "vendor" badge. The user pays Tinkr the listing fee indirectly through the plugin price.

### 6.3 The First 100 / 1,000 / 10,000 User Transition

**The first 100 users (months 1–3 post-v1.0)**: hand-picked maker community, 100% free, no marketplace, no payment rails. The founder is on-call for all support. The KB is empty, the plugins are 4 defaults, and the project memory is the differentiator.

**The first 1,000 users (months 3–9)**: open release, still 100% free. The community starts writing KB entries. The first 10 third-party plugins appear. The founder's GitHub sponsors covers hosting. Revenue: $0.

**The first 10,000 users (months 9–18)**: 50+ community plugins. The agent is the differentiator. The KB has 500+ entries. **The v1.5 marketplace is announced, with a 3-month "founder's lifetime" pre-sale at $499** (capped at 1,000 buyers = $500K cash infusion). This is the only aggressive monetization in the early stage. The per-plugin updates ship in v1.5.0 with $9/yr pricing.

**The first 100,000 users (months 18–48)**: the marketplace is mature. The Pro tier ($199/yr) is the dominant revenue. Vendor first-party plugins ship. **Revenue at 100K users = $45K/yr** (per the math in 5.3). Still not enough for a salary, but the network effect is real and compounding.

### 6.4 The Exit Ramps

**When does a user upgrade?** Three triggers, in order of importance:
1. They hit the free sim cap (50 min/mo) and need more. This is the highest-converting trigger; the user has *demonstrated demand* for the feature.
2. A new plugin version ships with a feature they want. The "v1.1 adds support for board X" message is a strong trigger.
3. They want the AI agent to be more useful (e.g. bigger context, more calls per day). The 20-calls-per-day free tier is the gate.

**When does a user churn?** Three triggers:
1. The free tier is generous enough. If the user only builds 1 project per month and only needs 1 plugin, they'll never pay. This is the 98%.
2. A better free alternative appears. This is the Sketch risk. The defense is the agent + KB + project memory.
3. The price feels hostile. The $9/yr per plugin is fine. The $99/yr Pro is fine. The $499 lifetime pre-sale is *only* fine if the value is obvious. Any "your subscription is expiring" email is a churn risk — Panic's no-penalty-for-lapsing model is the right template.

---

## 7. Open Questions for the Founder

These are the 5–8 specific decisions that need to be made. Each has a default answer and a rationale.

### Q1. What is the paid update cliff — 1 year or 3 years?

**Default: 1 year for plugins, 3 years for the IDE itself.**
Rationale: plugins update faster than IDEs. A 3-year cliff for a plugin is too long (the plugin may not even be relevant in 3 years). A 1-year cliff is the Panic Nova / Wokwi model. For the IDE itself, 3 years is the Sublime model.

### Q2. What is the price for per-plugin updates?

**Default: $9/yr per plugin, $29/yr for "premium" (vendor first-party).**
Rationale: below Sublime's $33/yr amortized cost, below Panic's $49/yr, above Wokwi's $5.6/mo consumer tier. The $9 figure is psychologically a "coffee" — not a "subscription."

### Q3. Should the Pro subscription be $99/yr or $199/yr?

**Default: $199/yr.**
Rationale: $99/yr cannibalizes per-plugin revenue. $199/yr is the "obvious value" price for power users, with the "save 50% if you use 5+ plugins" math (5 × $9 = $45/yr, so $199 is the better deal only if you use 25+ plugins — which is the power user signal).

### Q4. Is the v1.0.0 of every plugin MIT or some other license?

**Default: MIT for v1.0.0 of every plugin. Closed/cloud ingredients are added in v1.1+.**
Rationale: MIT is the only license that makes the "fork and stay" behavior morally acceptable. If the plugin is MIT at v1.0, the user can fork, stay on v1.0, and the system is honest. The paid update is justified by the *closed ingredient* (cloud build, AI agent, vendor first-party support), not by the *code* (which is free).

### Q5. Should v1.5 ship with the marketplace or wait?

**Default: wait 6 months after v1.0 ships. v1.5 marketplace ships when there are 1,000+ users and 30+ community plugins.**
Rationale: pre-building the marketplace before the community exists is a distraction. The community needs to be the foundation. Homebrew waited years before adding any commercial model. The same applies here.

### Q6. What is the per-plugin free tier (what can a free user do with a v1.1+ plugin they have v1.0 of)?

**Default: free users can use v1.0.0 indefinitely. Paid users get v1.1+. New features are gated.**
Rationale: this is the "Sketch mistake" question. The answer is: v1.0 is the free tier. v1.1 adds new features. v1.0 users keep their v1.0. They do *not* get v1.1 features. This is the Sublime model, not the Sketch model. The difference from Sketch is that the v1.0 of the Tinkr plugin is *good enough* — the v1.1 is incremental, not a downgrade for free users.

### Q7. What is the AI agent usage cap for free users?

**Default: 20 calls/day. Pro tier: 1,000 calls/day. Above Pro: pay-as-you-go at $0.001/call.**
Rationale: the AI is the cost disaster, not the sim. 20 calls/day is a real working cap (a maker can build a project in 20 calls). 1,000 calls/day is the power user signal. Pay-as-you-go above is the Hugging Face model. Without this cap, the AI bill can outrun revenue.

### Q8. What is the founder's "skin in the game" — does the founder write a paid plugin?

**Default: yes. The founder writes the 4 default plugins (ESP32, RP2040, nRF52, Pico) and the Tinkr Core plugin. The 4 default plugins are MIT and free. The Tinkr Core plugin is closed-source and is what v1.5 ships behind the Maker tier.**
Rationale: this gives Tinkr a flagship paid product that is unambiguously worth the price. It also gives the founder credibility with third-party authors ("I made the same trade-off you're making"). The trade-off is: the founder spends the first year maintaining these 4 plugins, not on the marketplace. This is a feature, not a bug.

---

## 8. The Single Sharpest Finding

The "unlimited everything, gated updates" model is **viable but small**. The Sketch post-mortem is the loudest warning: a 91% market share collapse in 6 years after a "paid major version" → "subscription" pivot is not a model failure — it is a *value* failure. The v1.0 free offering must be unmistakably better than every free alternative. The v1.1+ paid offering must be unmistakably better than the v1.0 free. The closed ingredient (cloud build, AI agent, vendor first-party) is the *only* thing the user cannot get for free. Everything else (code, KB, projects) is open and grows the community.

**The math is honest**: 2% open-source-to-paid conversion × $9 × 1.5 plugins avg × 10,000 users = $2,700/yr. That does not fund a company. The model works at 100,000+ users (where revenue is $40K/yr from per-plugin alone, plus Pro + Team tiers). The grind to 100K is 2–4 years, and the founder should plan for it.

**The single decision that matters most**: do not ship the marketplace in v1.0. Ship a fully-free v1.0 with no commerce rails. Get the community, get the KB, get 1,000 plugins. Then ship v1.5 with the marketplace. The community needs to trust that v1.0 is genuine before they will pay for v1.1.

---

## Executive TL;DR (For a Tired Founder)

The "v1.0 free, v1.1+ paid" model works in the data set (Sublime Text, Panic Nova) but the Sketch 2015→2024 collapse (45% → 4.5% market share) is the loudest warning. The mechanism is: the v1.0 free tier must be genuinely good, the v1.1+ paid tier must add a *closed* ingredient (cloud build, AI agent, vendor first-party) that free alternatives cannot easily match, and the model should not ship commerce rails in v1.0 — the community needs to trust that v1.0 is honest before they will pay for v1.1. Recommended pricing: $9/yr per plugin, $99/yr Maker (all plugins), $199/yr Pro (Maker + cloud), $499/yr lifetime pre-sale (first 1,000 only). Math is honest: at 2% open-source-to-paid conversion, you need 100,000 users to generate $45K/yr. The grind to 100K is 2–4 years. Plan for it.

---

## References

[1] D. Brecko, "New Features Free of Charge? Using Price to Sort Consumers," *Wharton Marketing Working Paper*, 2015. https://marketing.wharton.upenn.edu/wp-content/uploads/2015/04/Brecko_JMP_2.pdf

[2] "Competitive Teardown: Figma vs Sketch," Quicksilver Research, 2024. https://quicksilverresearch.com/blog/competitive-teardown-figma-vs-sketch/

[3] "Sublime Text 4," Sublime HQ Blog, May 21, 2021. https://www.sublimetext.com/blog/articles/sublime-text-4

[4] "Sublime Text," Wikipedia. https://en.wikipedia.org/wiki/Sublime_Text

[5] "Nova is Here," Panic Blog, September 16, 2020. https://blog.panic.com/nova-is-here/

[6] "Purchasing & Licensing," Nova Library. https://help.nova.app/faqs/purchasing/

[7] "Panic Launches Nova ⇥ nova.app," pxlnv linklog, 2020. https://pxlnv.com/linklog/panic-nova/

[8] "Subscription or no Subscription?," iA Writer blog. https://ia.net/topics/subscription-or-no-subscription

[9] "'Big updates' to Mac design app Sketch add real-time collaboration – but you'll need to fork out for a subscription," The Register, May 12, 2021. https://www.theregister.com/software/2021/05/12/big-updates-to-mac-design-app-sketch-add-real-time-collaboration-but-youll-need-to-fork-out-for-a-subscription/1531459

[10] "Angry devs hit out at JetBrains over shift to subscription pricing," The Register, September 15, 2015. https://www.theregister.com/software/2015/09/15/angry-devs-hit-out-at-jetbrains-over-shift-to-subscription-pricing/941957

[11] "Responding to Outcry, JetBrains Relaxes Licensing Terms," InfoQ, September 2015. https://www.infoq.com/news/2015/09/jetbrains-update/

[12] "Is PlatformIO dead?," r/embedded, March 2025. https://www.reddit.com/r/embedded/comments/1ji7rur/is_platformio_dead/

[13] "Arduino: The PlatformIO Threat to Microcontroller Development," Tadeu Bento, 2025. https://tadeubento.com/2025/arduino-the-platformio-threat-to-microcontroller-development/

[14] "Purchasing & Licensing," Nova Library (renewal terms). https://help.nova.app/faqs/purchasing/

[15] "Developer Tools Benchmarks 2026: PLG, NDR & Margins," culta.ai. https://culta.ai/benchmarks/devtools-benchmarks

[16] "Free Trial Conversion Benchmarks 2025," 1capture.io. https://www.1capture.io/blog/free-trial-conversion-benchmarks-2025

[17] "What is the ESP Component Registry?," Espressif Developer Portal, October 2024. https://developer.espressif.com/blog/2024/10/what-is-the-esp-registry/

[18] "Cloud Build Pricing," Google Cloud. https://cloud.google.com/build/pricing

[19] "esphome.cloud Pricing — Six Tiers, Per-Build, ESP32 + STM32." https://esphome.cloud/pricing

[20] "「Sublime Text 4」初の安定版がリリース," forest.watch.impress.co.jp, May 2021. https://forest.watch.impress.co.jp/docs/news/1326232.html

[21] "I love Sublime, but I don't want to pay to upgrade from 3 to whatever," Hacker News. https://news.ycombinator.com/item?id=47949903

[22] "Panic's Nova 9. When is a subscription not a subscription?," MacPowerUsers, 2024. https://talk.macpowerusers.com/t/panics-nova-9-when-is-a-subscription-not-a-subscription/28206

[23] "Transparency," Panic, Inc. (annual reports). https://panic.com/transparency/

[24] "JetBrains Annual Highlights 2026: Building the Future of Developer Productivity." https://www.jetbrains.com/lp/annualreport-2026/

[25] "The Terms You Did Not Sign," Vivian Voss, August 2023. https://vivianvoss.net/blog/the-terms-you-did-not-sign

[26] "Terraform License Change: BSL vs Open Source Guide," Harness. https://www.harness.io/blog/terraform-license-change-bsl-vs-open-source-guide

[27] "The Open Source License Change Pattern - MongoDB to Redis," Software Seni, 2026. https://www.softwareseni.com/the-open-source-license-change-pattern-mongodb-to-redis-timeline-2018-to-2026-and-what-comes-next/

[28] "PyCharm 2025.1: Unified PyCharm, Free AI Tier, Junie," JetBrains Blog, April 2025. https://blog.jetbrains.com/pycharm/2025/04/pycharm-2025-1/

[29] "PyCharm Community vs Professional: Which Should You Choose?," TMS Outsource, 2025. https://tms-outsource.com/blog/posts/pycharm-community-vs-professional/

[30] "Sketch Changes Direction on Pricing," MacStories, November 2015. https://www.macstories.net/news/sketch-changes-direction-on-pricing/

[31] "Figma vs Sketch: Which Is Winning? Market Share Data (2026)," Cledara. https://data.cledara.com/compare/figma-vs-sketch

[32] "Wokwi Plan and Pricing," Wokwi. https://wokwi.com/pricing

[33] "Pricing," Hugging Face, June 2026. https://huggingface.co/pricing

[34] "Pricing," Replicate, 2026. https://replicate.com/pricing

[35] "The Open Source Free Rider Problem, Explained," safeguard.sh. https://safeguard.sh/resources/blog/the-economics-of-free-riding-in-open-source-security

[36] "Open source and the free-rider problem," InfoWorld, 2016. https://www.infoworld.com/article/2264054/open-source-and-the-free-rider-problem.html

[37] "Maintainer Stipends and Grants," Homebrew Documentation. https://docs.brew.sh/Maintainer-Stipends-and-Grants

[38] "Homebrew," Open Collective. https://opencollective.com/homebrew

[39] "Sketch Review 2026: Still Worth It for Mac Designers?," UIGuides. https://www.uiguides.com/tools/sketch-review

[40] "An Interview with Uri Shaked (Wokwi.com)," The Amp Hour #599, August 15, 2022. https://theamphour.com/599-an-interview-with-uri-shaked-wokwicom/

[41] "Wokwi - World's most advanced ESP32 Simulator." https://wokwi.com/

[42] "Homebrew - Open Collective financial contributors." https://opencollective.com/homebrew

[43] "Sponsor @Homebrew on GitHub Sponsors." https://github.com/sponsors/homebrew

[44] "Accepting Payments and Getting Paid," itch.io Docs. https://itch.io/docs/creators/payments

[45] "Introducing open revenue sharing," itch.io, 2015. https://itch.io/updates/introducing-open-revenue-sharing

[46] "I want to pay for TextMate 2," Hacker News, 2012. https://news.ycombinator.com/item?id=3045269

[47] "Sketch's new licensing may turn heads toward Adobe," The Next Web, November 2015. https://thenextweb.com/news/sketch-annual-pricing

[48] "TextMate 2 Released As Open Source," Slashdot, August 9, 2012. https://developers.slashdot.org/story/12/08/09/1947234/textmate-2-released-as-open-source

[49] "Pricing - PlatformIO Registry." https://registry.platformio.org/pricing

[50] "Arduino Cloud Plans." https://cloud.arduino.cc/plans

[51] "How much does a Home Assistant Cloud subscription cost?," Nabu Casa support. https://support.nabucasa.com/hc/en-us/articles/26179687501341-How-much-does-a-Home-Assistant-Cloud-subscription-cost

[52] "Why Figma Won the Design Tools Market," Spyglass, 2024. https://www.spyglassci.com/blog/why-figma-won-design-tools

[53] "JetBrains switches its desktop products to subscription model under JetBrains Toolbox," JetBrains Press Release, September 3, 2015. https://blog.jetbrains.com/blog/2015/09/03/pr_030915/

[54] "Increased Subscription Pricing for IDEs, .NET Tools, dotUltimate and the All Products Pack," JetBrains Blog, July 31, 2025. https://blog.jetbrains.com/blog/2025/07/31/increased-subscription-pricing-for-ides-net-tools-dotultimate-and-the-all-products-pack/

[55] "Pricing and Billing," Hugging Face Inference Providers. https://huggingface.co/docs/inference-providers/en/pricing

[56] "Sketch Reviews 2026," CheckThat.ai. https://checkthat.ai/brands/sketch/reviews
