# Creator / Maker Marketplace Research — Patterns for Tinkr v1.5

> A study of 28 software, hardware, creator-economy, and direct-competitor platforms. For each: what it does well, what it does badly, and one specific lesson for Tinkr's plugin marketplace + creator revenue program. Synthesized recommendations follow.
>
> **Scope**: v1.5 marketplace (paid plugins, 70/30 split, author dashboard) and v2.0 creator program. Research conducted Aug 2026, sources current through Q2 2026.
>
> **Reading guide**: The TL;DR distills the report. Section 5 is the actionable output. Section 6 is the "do not copy this" list. Section 7 is open questions for you to decide.

---

## TL;DR — 10 lessons for Tinkr's plugin marketplace

1. **The single biggest creator-economy failure mode is invisible creators.** Across Etsy, Product Hunt, Patreon, and even GitHub, the median creator earns almost nothing; the top 1–5% capture 80%+ of revenue [1][2][3]. The marketplace's job is not to "let anyone sell" but to actively route attention to new and quality authors. Bake discovery into the runtime, not just the storefront.

2. **Speed of approval is a feature, not a luxury.** Arduino Library Manager lists a new library in ~1 day via automated bot checks [4]. Homebrew formulae merge in 24–48 hours [5]. WordPress takes 2–4 weeks and has 3,500+ in queue [6]. The first platform to make a creator's plugin installable in a Tinkr user's project in under 24 hours wins on creator delight. (In v1.0, Tinkr is GitHub-based — this is already the case; don't slow it down when the marketplace launches.)

3. **A "creator-friendly" cut is 0–10%, not 30%.** Apple/Steam-style 30% is the legacy of monopoly gatekeeping. New platforms (Shopify 0% up to $1M, itch.io 0–100% default 10%, Buy Me a Coffee 5%, Substack 10%) cluster much lower [7][8][9]. Tinkr's 70/30 split is **already** more author-friendly than the App Store but **more aggressive** than the most author-friendly 2026 platforms. Position it explicitly: "more than the App Store, simpler than GitHub Sponsors."

4. **The merchant-of-record pattern is the new standard for creator economy platforms.** Gumroad became MoR on Jan 1, 2025 and handles all global tax/VAT [10]. Substack has always done this. Patreon handles iOS tax. The trend: creators do not want to be a business. Tinkr should handle sales tax / VAT globally for plugin authors from day one.

5. **Pay-what-you-want with a sensible minimum outperforms fixed pricing for indie/digital goods.** itch.io's PWYW data shows buyers pay ~30% above the suggested minimum on average [11]. For plugins that have a hobbyist ceiling ($5–$15), a "name your price above $5" tier generates higher revenue than $9.99 fixed. Offer PWYW as a tier option in v1.5.

6. **The "GitHub PR" registry model is unbeatable for trust and speed.** Arduino, Homebrew, and the Espressif Component Registry all converge on: a GitHub repo of submodules, a PR-based submission flow, automated checks, human review on a tiny subset. This is what Tinkr should ship in v1.0, then layer commerce on top in v1.5 without re-architecting. The PR is the receipt.

7. **Disintermediation wins on the margin.** A "Tip the author" button + a "follow this author" inbox feed costs almost nothing to build and dramatically improves retention. Every successful creator platform (Gumroad, itch.io, Substack) gives creators an owned audience relationship, not just a transactional one. Tinkr's GitHub-based identity already gives the author a permanent home; the marketplace should expose it.

8. **The "publishing-as-a-CLI" model is the unlock for technical creators.** `npm publish`, `vsce publish`, `brew bump-formula-pr`, `idf.py upload-component`, `platformio lib register` — all CLI-first. The author never visits a web form. Tinkr's `tinkr plugin publish` is already this shape; it must stay this shape when commerce lands. Adding a web UI is for buyers, not authors.

9. **Vendor first-party plugins need a separate, lighter onboarding than community plugins.** Espressif's component registry lets Espressif publish directly with their namespace; the community uses the same UI but a different trust tier [12]. In v1.5, Espressif and M5Stack should have a one-line "you're a vendor" flag that skips the review queue, with the cost of that privilege being a revenue-share bump to 25–30% for vendor plugins.

10. **The right "open revenue share" answer is to make it adjustable, like itch.io.** Default 70/30, but let authors drop to 60/40 or 50/50 to be featured in a "supporting authors" rail, or raise to 90/10 (Tinkr keeps 10%) if the author wants to be in a "community-picks" promotion. This is voluntary, transparent, and turns the cut from a tax into a marketing budget. itch.io's open revenue share has been running since 2015 and is the most creator-loved marketplace model in the data set [13].

---

## Section 1 — Software / digital marketplaces

### 1. Apple App Store
- **Wins**: App Review is mostly fast (90% in <24 hours per Apple's own report) [14]. The P2B transparency report is published annually — a leader in creator-facing trust reporting [15]. The "Meet with App Review" consultation is unusually direct human contact for a giant platform. Sandboxing is a real safety net for users.
- **Pain**: The 30% cut (15% for sub-$1M developers, since 2021) is now an antitrust liability — the EU DMA forced Apple to drop to 17% in the EU, with a "core technology fee" of €0.50 per install above 1M, which Tim Sweeney called "hot garbage" [16]. Account terminations are opaque: 43 of 48 P2B complaints in the 2024–2025 reporting period were upheld by Apple [15]. Chinese developers filed antitrust complaints in 2024 over unfair fees [17]. "Opaque or vague reasons for rejection" is the top complaint across thousands of developers [18].
- **Lesson for Tinkr**: Don't be Apple. Tinkr's plugin manifest is plain text in a git repo, not a black box. The lesson is the **opposite** of Apple's: be radically transparent. The `tinkr plugin validate` step is the equivalent of App Review, but it runs locally and tells the author exactly what passed and what didn't. The author should never have to ask "why was I rejected?"

### 2. npm (Node Package Manager)
- **Wins**: `npm publish` is a one-liner. Two-factor auth is the only required friction. Open by default; version-immutable; `npm install` is faster than any other package manager [19]. 2FA + scoped packages + provenance (signed via GitHub Actions) is the modern best practice.
- **Pain**: The "everything" prank of Dec 2023–Jan 2024 rendered the entire registry unable to unpublish packages because a single package had declared every other as a dependency [20]. This is the cost of a fully open, frictionless registry. The @types/* split (DefinitelyTyped) means authors can't ship types with their library without version drift. The dual-publishing problem (npm + JSR) has left many TypeScript libraries with broken `exports` maps that npm never warned about [21].
- **Lesson for Tinkr**: Plugin manifests must be validated by `tinkr plugin validate` (already designed in plugin_spec.md), but Tinkr doesn't need to be a package-host — git submodules work. The "everything" failure is a warning against: (a) requiring paid plugins to depend on other paid plugins in a way that creates circular dependencies, and (b) using semantic version numbers from external sources. Tinkr plugins should reference knowledge by absolute path, not by dependency closure.

### 3. VS Code Marketplace
- **Wins**: 55,000+ extensions, 5 billion+ installs [22]. Verified publisher badges, trending scores, security scanning [22]. `vsce publish` is a one-liner from the CLI. Extensions are free to publish.
- **Pain**: There is **no native paid model**. "The marketplace is incredible for reach. It is terrible for revenue" is the consensus quote [23]. 99% of extensions earn nothing; monetization has to be bolted on via a third-party (3DIMLI, AdKar, Gumroad, Lemon Squeezy) and the author keeps the customer and the revenue — but the extension's "in-marketplace" experience is free [23][24]. Microsoft explicitly allows this. Total ecosystem revenue through paid extensions is estimated at only $50M/year across 50K extensions [22].
- **Lesson for Tinkr**: This is the **single most important anti-pattern**. The VS Code Marketplace proves that "distribution without commerce" is a creator-revenue dead end. Tinkr must NOT launch the marketplace without Stripe Connect integrated in v1.5. The temptation to "let the community handle payments themselves" is real — it is the wrong call. A plugin author writing a paid `tinkr-m5stack-core-s3` plugin should be able to monetize without leaving the IDE.

### 4. GitHub Marketplace
- **Wins**: GitHub dropped its cut from 25% to 5% in 2021, and developers now keep 95% [25]. Publisher verification was simplified to a DNS TXT record + 2FA — no deep security review required for listing [25]. Integrates with the GitHub billing system users already trust.
- **Pain**: GitHub Marketplace is much smaller than VS Code Marketplace. Apps are tied to GitHub orgs, so the "audience" is mostly enterprise dev teams, not the long tail of makers. Receiving payment requires $500 minimum and is end-of-month following month — slow cycle [26].
- **Lesson for Tinkr**: The 5% cut is hard to beat; Tinkr's 30% looks high next to this. **But**: GitHub's identity is enterprise developers; the maker audience is more like App Store, where 30% is the norm. Position the 70/30 against App Store, not against GitHub. Also: the simplified publisher verification (DNS + 2FA) is the right onboarding. Tinkr's `tinkr plugin publish` should check (a) the GitHub identity exists, (b) 2FA is on, (c) the GitHub repo URL is valid, and (d) the manifest is well-formed. That's it. No deep review of code.

### 5. Shopify App Store
- **Wins**: 0% on the first $1M lifetime, 15% above, plus 2.9% processing [27]. App developers earned over $1B in 2024 [28]. The $19 one-time Partner registration is the lowest creator-onboarding cost in this data set. Integrated billing means authors don't handle Stripe themselves.
- **Pain**: In June 2025, Shopify changed the $1M exemption from "reset annually" to "lifetime, never resets" [29]. The developer community's reaction was strong and negative. "The real cost is beyond 15% because the existing 2.9% is going to stay along with the regulatory fees" [29]. The change reads as Shopify optimizing for its most successful apps, not its most fragile ones.
- **Lesson for Tinkr**: The "0% up to $X" pattern is the single best discovery for a creator-friendliness message. Tinkr should offer a creator-fee holiday for the first $10,000 in lifetime plugin sales (per author), then 30%. The number 10K is right because most plugins will never sell $10K, and it removes the "platform tax" feeling for the bulk of the long tail. Communicate the cap loudly: "You pay Tinkr nothing on your first $10K."

### 6. WordPress Plugin Directory
- **Wins**: 100% free, open-source, anyone can submit [30]. 12,000+ plugin submissions reviewed in 2025 [31]. The review is human but small plugins are "often approved right away" per the review team lead [32]. The repo infrastructure (SVN-based, separate from the review) is simple and stable.
- **Pain**: Typical review is 2–4 weeks in 2026; submissions with issues can stretch to 6–8 weeks [31]. 3,500+ plugins in the queue at any time. "Many plugin authors simply do not reply to emails: After 7 days, if the plugin code isn't completed, the plugin's rejected" [32]. The process is documented but unpredictable. The plugin is rejected after 3 months in the queue [30].
- **Lesson for Tinkr**: The "no commercial model" is the reason this works for free plugins. For paid plugins (Tinkr's v1.5), this isn't a relevant model. But the "human reply within 7 days" SLA is excellent. Tinkr should commit to: "If you don't hear from a Tinkr maintainer within 7 business days of submission, your plugin is auto-approved into the marketplace." This sets a hard SLA that the team must meet, not a soft target.

### 7. npm Pro
- **Wins**: $7/month gave individual developers unlimited private packages and package-based permissions [33]. The pricing was simple, no tiers. npm used this to monetize the long tail.
- **Pain**: npm Pro was effectively absorbed into GitHub plans; the standalone product is now sunset [34]. The promise of paid packages on the public registry never materialized at scale — npm Pro was a hosting product, not a marketplace product.
- **Lesson for Tinkr**: This is the "private vs paid" distinction. The Tinkr Pro subscription ($X/year for advanced features, per decisions.md A10) is similar in spirit — a creator-program annual fee is a hosting product, not a marketplace product. **Don't conflate them** in the pricing. The 4-tier matrix in A10 (Pro sub, per-plugin update fee, creator program fee, project hosting) is correct because they serve different jobs.

### 8. Atlassian Marketplace
- **Wins**: 85% to developer on Cloud apps, 100% on the first $1M lifetime of Forge revenue (effective Jan 2026) [35]. Very high take rate for the creator. Atlassian's 2024 Marketplace revenue was ~$273M, ecosystem revenue ~$1.8B [36]. The new pricing (effective April 1, 2026) lowers Connect app rates over time [37].
- **Pain**: Approval takes 10–15 business days [38]. New 2025 security rules add Partner Verification (KYC/KYB via Stripe Identity) — every partner must complete a 14-day verification [39]. "Reasonable pricing" is an explicit review criterion; overprice your app and Atlassian will reject it [38]. Apps unmaintained for 18+ months are reviewed under the Cloud App Compliance program [40]. The 2026 Commission change to 20% / 25% (Connect) and 16% / 17% (Forge) is a [forecast] — scheduled to land in stages through July 2026.
- **Lesson for Tinkr**: This is the **enterprise** end of the spectrum. The verification + security overhead is high but appropriate for Atlassian's enterprise customers. Tinkr's audience is makers and embedded engineers — NOT enterprise IT — so this overhead would be overkill. The 85% take rate is a model to admire; the KYC/KYB at 14 days is a model to avoid. **For Tinkr**: skip KYC until cumulative sales exceed $10K per author. Below that, the friction isn't worth it.

### 9. Chrome Web Store
- **Wins**: $5 one-time developer registration, the lowest in the data set. Has a paid extensions feature. Trusted brand.
- **Pain**: In January 2025, Google disabled paid extension publishing entirely due to a fraud spike — paid extensions sat in "Pending review" for weeks, account suspensions hit developers with no explanation, and even an internal Google extension was affected [41]. Multiple countries (Armenia, Pakistan, Nigeria) are not supported for the registration fee at all, so developers in those countries cannot publish [42]. Review verdicts come with cryptic color-coded IDs ("Yellow Magnesium") [43]. The "appeal" process is a form submission, not a conversation.
- **Lesson for Tinkr**: Two lessons. (1) **Don't disable publishing in bulk over fraud**. If Tinkr sees fraud, freeze the affected plugin, not the whole marketplace. (2) **Don't have a list of unsupported countries**. The list of unsupported regions is the single biggest growth-limiting factor. Stripe Atlas exists for a reason — Tinkr should support all countries Stripe supports for Connect, which is 50+.

### 10. Vercel Marketplace
- **Wins**: Supabase's "increased signups through the Vercel Marketplace" case study is the most direct creator-revenue proof in the data set — "seamless onboarding, integrated billing, zero loss in fidelity" [44]. `vercel integration add` works from the CLI; `vercel integration add supabase` provisions the resource in <60 seconds [44]. OIDC-based authentication means the partner doesn't manage user accounts [45]. Unified billing in the Vercel dashboard means the partner doesn't run a payment UI.
- **Pain**: Requires a hand-shake to Vercel (`integrations@vercel.com`) — not self-serve [46]. The partner has to implement a substantial Partner API (installations, resources, billing plans, OIDC token verification, REPL access) [45]. Vercel-specific; can't be copy-pasted to a non-Vercel context.
- **Lesson for Tinkr**: The "integrated billing" + "60-second install from CLI" pattern is the gold standard. When a Tinkr user runs `tinkr plugin add <paid-plugin>`, Stripe Checkout should open in a webview, the license key should be written to `.tinkr/license/<plugin>.key`, and the plugin should be usable in the same session. No "buy on a website, paste a key later" friction. The license key model is a 3DIMLI/AdKar-style workaround that exists only because VS Code Marketplace has no paid model [23][24]. Tinkr can do this right.

---

## Section 2 — Hardware / maker marketplaces

### 11. Tindie
- **Wins**: 5% marketplace fee — the lowest of any maker hardware marketplace in this data set [47]. No listing fees, no monthly fees, no upfront cost to be a seller [47]. Stripe-based payouts covered by Tindie (no PayPal intermediary fee) [48]. Free to list, free to have a store, free to be inactive. Fraud protection, global reach, simple shipping setup [48].
- **Pain**: 5% is on top of payment processing (3% + $0.30) and per-order fees. Tindie's fees are on par with Amazon, eBay, and other general marketplaces — but unlike those, Tindie doesn't drive the kind of traffic Amazon does. A $19.99 + $6.00 shipping sale nets the maker about $25.99 - 5% - processing ≈ $23.99, then the maker still has to source and ship the physical part. The "fulfilled by maker" model is the biggest complaint, but also the right model.
- **Lesson for Tinkr**: Tindie is the closest analogue to a future "Tinkr hardware marketplace" — same community (makers), same culture (DIY), same problem (a maker wants to sell something small). The "no listing fees" pattern matters. For Tinkr's plugin marketplace, the analogue is "no listing fees" for free plugins, and a flat 5% processing fee (not 30%) on top of Stripe. The 30% is for vendor first-party plugins, not community plugins.

### 12. Etsy
- **Wins**: 9M+ active sellers. Built-in audience that wouldn't otherwise find a small maker. Search, discovery, gift features. The seller dashboard is mature: in 2025 Etsy added Top Tasks checklists, "quick actions" on listings, microlearning lessons delivered to the seller's phone [49]. "Etsy Seller" app is a separate iOS app from the buyer app — they invested in a dedicated seller mobile experience.
- **Pain**: Seller fees are now a 6.5% transaction fee + $0.20 listing fee + 3% payment processing + 12–15% Offsite Ads fee for sellers making over $10K/year [50]. 17,000+ sellers went on strike in 2022 over the fee increase; a petition reached 51,000 signatures [51]. Offsite Ads is a particular sore point: "Many artists report receiving Offsite Ads charges on sales to existing customers who would have purchased directly anyway, effectively penalizing sellers for their own marketing success" [52]. "Artists who once thrived on Etsy now report their listings have virtually disappeared from search results due to algorithm changes" [52]. Account suspensions with no recourse are a known complaint [52].
- **Lesson for Tinkr**: Don't build a search algorithm that is opaque. Etsy's "search is a black box" problem is now the dominant creator complaint. For Tinkr, this means: (a) plugin search is the manifest's `display_name` + `description` + `tags` + KB entries, weighted by `installs` and `rating`, all visible to the author. The author should know exactly why their plugin ranks where it does. (b) Don't run Offsite Ads at all. The trust cost exceeds the revenue.

### 13. Adafruit
- **Wins**: 300+ CircuitPython libraries maintained centrally [53]. The Adafruit Learning System is free, well-edited, and has thousands of guides [54]. "Open Source is at the core of what we do at SparkFun. The schematics, designs and associated software for all our breakout boards are open" [55] (this is SparkFun but Adafruit is the same model). The combination of (a) curated product, (b) free library, (c) free learning system, (d) open source reference hardware, is the playbook that built a $100M+ open-source hardware company without paid lock-in. The Adafruit IO service is a $10/mo or free SaaS for makers to ship data to.
- **Pain**: Adafruit is vertically integrated — they are the vendor, the library maintainer, and the educator. This is great for the Adafruit brand; it's not a model Tinkr can copy because the maker-economy vision is third-party authors.
- **Lesson for Tinkr**: The **Learning System** is the lesson. Adafruit discovered that "free education that uses your library" drives more library adoption than any paid acquisition channel. Tinkr should ship a curated Learning System in v2.0 — community-contributed guides that show how to use a specific plugin. The KB is the technical knowledge; the Learning System is the human-curated walkthroughs. A guide like "Building a smart plant monitor with the tinkr-m5stack-core-s3 plugin" is worth 10x more than a search result for "moisture sensor."

### 14. SparkFun
- **Wins**: Open source since 2002 [55]. The Qwiic ecosystem is a connector-and-library standard that means every SparkFun Qwiic board ships with an Arduino library that "just works" [56]. 1,447+ public repos [55]. The community forums are 14+ years deep.
- **Pain**: Same as Adafruit — the model is "SparkFun designs and sells hardware with software." Not a multi-author marketplace.
- **Lesson for Tinkr**: The **Qwiic standard** is the lesson. A standard connector + standard library API + standard documentation pattern means every Qwiic-compatible board gets free distribution through the Qwiic ecosystem. For Tinkr, this is the "manifest standard" already in plugin_spec.md. The next step is a "Tinkr Ready" certification — a board vendor designs a board, ships a `tinkr.plugin.toml` for it, gets a "Tinkr Ready" badge in the marketplace, and rides the discovery wave. The certification is for trust, not for revenue.

### 15. Crowd Supply
- **Wins**: 5% platform fee (post-campaign); "house" order fulfillment handles long-tail reorders [57]. The campaign format (typically 30 days) is structured for product launches, not ongoing sales. Crowd Supply's curation is the most selective in the maker hardware space — projects are reviewed and either accepted or rejected. The Statement of Work contract [58] is real business infrastructure, not a "click to agree" EULA.
- **Pain**: 12% campaign fee + 2.9% processing + $18 flat per item is the "real" fee on the campaign itself [58]. That's ~$2,200 in fees on a 118-unit campaign at $99, which is ~$18.76 per item [57]. For small runs, this is brutal. The "house" order after the campaign is sold at a steep distributor discount — the creator gets $56 on a $99 MSRP [57]. The model rewards scale.
- **Lesson for Tinkr**: The 12% / 2.9% / $18 item fee structure is **not the right model for plugins** (Tinkr is software, no per-item cost). The lesson is the **Statement of Work**. For Tinkr's "vendor first-party" plugin contracts, a written SOW between Tinkr and the vendor (deliverables, exclusivity, support SLAs, payment terms) is the right infrastructure. Not a click-through.

### 16. Kickstarter (hardware)
- **Wins**: 5% platform fee + 3–5% processing [59]. Micropledge fees (5% + $0.05) for pledges under $10 make small pledges viable [59]. The all-or-nothing funding model is a feature, not a bug: it forces the creator to hit the goal or nothing, which is a real commitment signal to backers.
- **Pain**: The BBB has logged 106 Kickstarter complaints in the last 3 years [60]. The "Xatziri Cruz Salas stole $755,000" case and "Heisenberg Robotics received $1,506.00 and went silent" are publicly visible [61]. Kickstarter explicitly disclaims responsibility: "Kickstarter doesn't step into the creative process itself or manage the fulfillment and shipment of rewards" [60]. "It's up to each creator to determine whether refunds are within scope" [60]. Backers have no recourse.
- **Lesson for Tinkr**: **Software is much easier than hardware.** A broken plugin can be replaced in seconds; a broken shipped PCB cannot. This is the reason a Tinkr hardware marketplace is a v3+ product, not v1.5. The trust gap between "I'm sending you a $30 plugin" and "I'm shipping you a $200 board" is the same gap Kickstarter hasn't solved in 15 years.

### 17. SeeedStudio Fusion
- **Wins**: 7-day PCBA turnkey service, no minimum order quantity [62]. Gerber file upload (ZIP/RAR, max 20MB) is the entire onboarding [62]. Per-stage tracking (panel preparation, drilling, plating, solder mask, etc.) is published with photographs [63]. The "send us your requirements" email path is a fallback for complex orders.
- **Pain**: The user is the customer, not the seller. SeeedStudio doesn't have a maker-economy component; it's a B2B PCB service.
- **Lesson for Tinkr**: The **per-stage tracking** with photographs is the lesson. When a Tinkr user orders a vendor first-party plugin, they should see the same kind of status page — "plugin queued → validated → published → live." Per-stage, with explanations. This is the missing UI in most marketplaces. SeeedStudio treats manufacturing as a process to be transparent about; Tinkr should treat plugin publishing the same way.

---

## Section 3 — Creator-economy platforms

### 18. Patreon
- **Wins**: Patreon's "membership" framing is the canonical model for "ongoing support for a creator" [64]. The platform takes a single, transparent fee. Multiple tiers with different perks. iOS app uses Apple's IAP (the 30% is unavoidable for iOS creators).
- **Pain**: Patreon **changed its pricing in August 2025**, consolidating to a flat 10% for all new creators (previously tiered: 5% / 8% / 11%) [65]. The 10% is on top of payment processing — total effective cost on $5 pledges is ~19% [66]. The currency conversion fee (2.5% for non-USD payouts) is the international creator's silent tax [65]. iOS sales incur Apple's 30% on top of Patreon's 10% — "replacing Patreon's standard payment processing fee for that transaction" [65]. Unpublishing your page and re-publishing moves you to the new plan — a retention trap [65].
- **Lesson for Tinkr**: Patreon's pricing change is a case study in how to lose creator trust overnight. The lesson is: **don't change pricing on existing creators**. Tinkr's v1.5 should commit: "the 70/30 split for any plugin published before v2.0 is locked for the lifetime of that plugin." Future plugins published under a new model are new contracts.

### 19. Gumroad
- **Wins**: The "creators earn" framing is consistent. As of Jan 1, 2025, Gumroad is the merchant of record and handles ALL global tax obligations for the creator [10]. The pricing model is famously simple: 10% + $0.50 per direct sale, 30% via Discover marketplace [67]. The dashboard is intentionally simple: revenue, recent sales, basic traffic [68]. Refundable fees — Gumroad returns its 10% on refunds (only the processing portion is retained) [67].
- **Pain**: Gumroad Discover's 30% is high — for a creator who's earning their audience entirely through Gumroad, that's a significant tax [67]. The 30% is justified as "we found the customer for you" but the creator can't audit the discover algorithm. Subscriptions are basic — no advanced SaaS billing, no metered usage [68]. Customization is limited — basic CSS only.
- **Lesson for Tinkr**: The merchant-of-record pattern is the most important lesson. Tinkr should make plugin authors MoR'd for sales — Tinkr handles VAT, GST, sales tax globally, and the author gets a net 70% payout. This is the difference between "I built a plugin" and "I built a business with a tax accountant." The merchant-of-record model removes the second one. Gumroad did this in 2025; the rest of the field is catching up.

### 20. Substack
- **Wins**: 90% of revenue to the writer minus Stripe fees [9]. The "we don't make money until you do" framing is the cleanest in the industry. Publishing is free if the content is free [9]. The Stripe recurring billing fee (0.7%, added July 2024) is a small but real cost.
- **Pain**: Stripe added a 0.7% recurring billing fee in July 2024 — easy to miss for creators not reading the fine print [69]. "Substack's creator exodus is accelerating" — multiple high-profile publishers have moved to Ghost ($9–$199/mo flat) or Beehiiv ($49/mo+ flat) because percentage-based pricing gets expensive at scale [70]. A $10K/mo newsletter pays Substack $1K/mo, vs $199 to Ghost. The "Substack Tax" is now a meme.
- **Lesson for Tinkr**: Substack's percentage-based model penalizes success. A Tinkr plugin author who makes $50K/year on plugins is paying $15K to Tinkr. This is a lot more than the equivalent at Shopify (0% to $1M, then 15%). For v2.0 creator program, Tinkr should consider **a cap on the platform fee per author per year** — say, $5,000. Above that, the author keeps 100%. This keeps Tinkr aligned with the long tail (where the cut matters) and the long head (where the cap matters).

### 21. Buy Me a Coffee
- **Wins**: The simplest creator-economy model. 5% flat, no tiers, no monthly fees, no upsells [71]. The "support without subscribing" framing (one-time tip) is critical for converting readers who don't want a commitment. No monthly fee = no churn. 110+ countries supported [72]. Creators can export their supporter list [72].
- **Pain**: Stripe fees (2.9% + $0.30) + 0.5% payout fee + 1% international card fee mean a $1 tip loses 38% to fees [73]. The flat 5% is a ceiling — there's no way to reduce it. No discovery surface (Buy Me a Coffee doesn't have a "Discover" tab like Gumroad's).
- **Lesson for Tinkr**: For Tinkr Pro / per-plugin "support the author" donations, the Buy Me a Coffee model is right. 5% flat, no tiers. This is the "tip the author of a free plugin" flow. It should not be a paid plugin purchase — it's a "thank you" with a different shape.

### 22. itch.io
- **Wins**: **Open revenue share** — the seller decides the platform's cut, from 0% to 100%, default 10% [13]. This is the most creator-loved feature in the entire data set. Pay-what-you-want averages 130% of the suggested minimum (i.e., buyers pay ~30% above the floor on average) [11]. "Itch.io is an open marketplace for independent game creators. It's completely free to upload your content" [74]. PWYW pages allow bundling, pre-orders, early access, crowdfunding with project goals.
- **Pain**: Trustpilot score 1.9/5 — "Most reviewers were unhappy with their experience overall" [75]. Specific complaints: slow payment processing, "funds are held for extended periods," "accounts being suspended," "games disappearing from search results" [75]. The reviews skew toward buyers, not creators. Payouts for smaller creators can be slow.
- **Lesson for Tinkr**: The **open revenue share** is the model to copy. Default 70/30 (Tinkr keeps 30%). But: every plugin's `tinkr.plugin.toml` should expose `revenue_share` as a field the author can set from 50/50 to 95/5 — and Tinkr's marketplace UI shows a "this author gives Tinkr more so we can feature them" badge. This is voluntary, transparent, and turns the cut from a tax into a marketing budget. itch.io's been running this since 2015; it works.

### 23. Product Hunt
- **Wins**: The "Grand Slam" of product launches. A successful launch (top 5 of the day) generates 1,000–5,000 visitors and 10–150 signups [76]. The `#1 Product of the Day` badge is real social proof.
- **Pain**: **Featured rate dropped from 60–98% in 2020–2023 to 10% by September 2024** [76]. "If you're not featured from the start, all the traffic you drive to Product Hunt only benefits them" [76]. The algorithm values accounts with 365-day streaks 10x more than new accounts [77]. Launch prep is 50–120 hours [76]. The criteria are "opaque and inconsistently applied" [76]. The cost-benefit has shifted from "free launch channel" to "50+ hours of work for a 10% chance."
- **Lesson for Tinkr**: This is a **warning** against a featured-only discovery model. If Tinkr's marketplace has a "Featured" tab and a "Everything" tab and the Everything tab is an algorithmic graveyard, Tinkr is building Etsy's "your listing disappeared from search" problem. The lesson: **search ranking is not a black box**. The plugin author's `manifest.installs + manifest.rating` should be visible. If their plugin isn't surfacing, they should be able to see the rank math.

---

## Section 4 — Direct competitors

### 24. Arduino Library Manager
- **Wins**: "A new library can now be listed in the Arduino library directory within a day" [4]. The submission flow is a PR to `arduino/library-registry` adding the library's GitHub URL to a `repositories.txt` file. A bot runs compliance checks, and if they pass, the PR is auto-merged [78]. The whole system is open source: the GitHub Actions workflow, the validation library, the index engine [78]. The hourly index poll means new tags are picked up within an hour.
- **Pain**: The library must have a `library.properties` file in the root (Library 1.5 format). Name conflicts are rejected (case-insensitive). Names cannot start with "Arduino" for third-party libraries [78]. The Arduino team owns the namespace prefix — a third-party "ArduinoXYZ" library is rejected.
- **Lesson for Tinkr**: This is the **exact model Tinkr should ship in v1.0** (per the plugin spec's git-submodule registry). The lesson is to make the validation bot public: Tinkr should publish a `tinkr plugin validate --explain` mode that shows what the bot would check and the rationale for each check. Authors should be able to run the same checks locally. The Arduino Lint project is the model.

### 25. PlatformIO Library Registry
- **Wins**: 7,000+ libraries. Open submission via `library.json` manifest. Crawler runs every 24 hours to detect new releases [79]. Allows local paths and Git URLs. Multi-platform (Arduino, ESP32, mbed, STM32, etc.). The PlatformIO ecosystem is the most "professional" of the open-source embedded registries.
- **Pain**: Less curated than Arduino. Some libraries are abandoned. "Will my lib be accepted in the registry? Most likely, unless the library manifest is malformed" [80] — the bar is low, which is good for the author but means variable quality for the user.
- **Lesson for Tinkr**: The 24-hour crawler is the lesson. Tinkr's git-based registry should poll the `tinkr-esp32` repo (and others) every 6 hours for new tags, and update the local `index/plugins.toml` automatically. The user runs `tinkr plugin update` to pull. No human in the loop for version bumps.

### 26. Wokwi
- **Wins**: Browser-based, zero-install. ESP32 (all variants), RP2040, STM32, AVR all supported. Free tier is genuinely useful (unlimited simulations, public projects, virtual WiFi) [81]. The Hobby tier (€5.6/mo, ~$6) adds 100 monthly fast build minutes. The paid VS Code add-on is ~$97/yr for offline operation [82]. Wokwi Club gets early features.
- **Pain**: "For analog stuff it is hopeless" — analog pin + resistor stack button decoding doesn't work [83]. "Multiple Arduinos within a schematic is not supported" [83]. External serial connections are limited [83]. The pricing tiers changed in 2024; the new Hobby+ (€8.1/mo) added fast build minutes, but the offline tier is a separate paid add-on, which complicates the pricing story.
- **Lesson for Tinkr**: Wokwi is the closest competitor to Tinkr's "simulator" axis (v2.0). The lesson: **a useful free tier is a marketing channel, not a cost center**. Wokwi's free tier gets users hooked, and the conversion to paid is real. For Tinkr: the 4 free plugins are the Wokwi free tier. Make them genuinely useful, not crippled. A user who can't do real work on the free plugins won't convert — they'll go to a competitor.

### 27. Espressif Component Registry
- **Wins**: Components are first-party (Espressif) or community-uploaded via the same UI [12]. Authentication is GitHub OAuth. Upload is `idf.py upload-component --namespace [YOUR_NAMESPACE] --name test_cmp` [84]. The `idf_component.yml` manifest is well-documented. The registry supports multiple IDF versions (5.2–6.0) and chip targets.
- **Pain**: The namespace system means Espressif is a privileged namespace — community components don't get the brand halo. The component model is ESP-IDF-specific; Arduino or MicroPython users don't directly benefit.
- **Lesson for Tinkr**: Espressif's model is the **first-party plugin pattern**. Tinkr's v1.5 should offer Espressif a namespace (`tinkr-espressif/*`) where Espressif ships first-party plugins, while community plugins live in the `community/*` namespace. The badge in the marketplace UI should clearly mark "Vendor First-Party" with a different color/style. This is trust signaling, not revenue.

### 28. Homebrew Formulae
- **Wins**: 5,000+ formulae (CLI tools) and 4,000+ casks (macOS apps). The PR-based submission flow is the canonical "open source registry" pattern [5]. `brew create` generates a starting formula from a URL. `brew audit --strict --new --online` runs all the CI checks locally. `brew bump-formula-pr` automates a version bump. ~24–48 hour PR review. The 50-minute post-merge CI delay is so users can `brew install` within an hour of approval.
- **Pain**: Volunteer maintainer bottleneck — "We typically respond to all PRs within a couple days, but it may take up to a week" [5]. Style and convention enforcement is strict; new contributors are gently told to do what the maintainers ask. No paid tier.
- **Lesson for Tinkr**: The **local-first validation** is the lesson. `brew audit` runs every CI check on the author's machine before they open a PR. Tinkr should ship `tinkr plugin validate` as a single command that runs every check locally and reports the result in a green/red table. If it passes locally, the PR will pass CI. The author's experience is "I tried it, it works, I sent the PR" — not "I sent a PR and waited a week to find out I had a typo."

---

## Section 5 — Synthesized recommendations for Tinkr v1.5

These are concrete, prioritized, and designed for the v1.5 marketplace launch (4–6 months after v1.0).

### R1. Ship a `tinkr plugin publish` CLI that is a single command from manifest to live

The author should run one command. It should (a) run `tinkr plugin validate`, (b) push to a personal GitHub repo, (c) open a PR to the community registry, (d) report the PR URL. **The author should never visit a web form to submit a plugin.** Pattern: itch.io, npm, Homebrew, Espressif Component Manager, PlatformIO, VS Code Marketplace. Anti-pattern: Chrome Web Store developer dashboard, Apple App Store Connect.

### R2. Aim for <24 hour approval SLA, commit to 7-day auto-approval fallback

Arduino does this in ~1 day [4]. Homebrew does this in 24–48 hours [5]. WordPress takes 2–4 weeks [31]. **Tinkr's target: 24 hours for automated bot checks, 7 days as a hard SLA with auto-approval if no human has acted.** The auto-approval after 7 days is the safety net — it forces the maintainer team to keep up, and it never leaves an author in limbo.

### R3. Adopt a tiered, author-friendly revenue split

The "best-in-class" 2026 numbers are:
- **Shopify**: 0% to $1M lifetime, then 15% [27]
- **itch.io**: 0–100% author-chosen, default 10% to platform [13]
- **Buy Me a Coffee**: 5% flat [71]
- **Gumroad**: 10% + $0.50 [67]
- **Substack**: 10% + Stripe [9]

Tinkr's proposal (70/30) is competitive with the App Store but not with the creator-friendly end. Recommended structure:
- **Community plugins**: 70% author / 30% Tinkr, with the author's first **$10,000 in lifetime sales paying 0% to Tinkr**. Above $10K, 70/30.
- **Vendor first-party plugins** (e.g., Espressif): vendor sets price, 70% vendor / 30% Tinkr, but Tinkr waives the 30% for the launch partner.
- **Optional open revenue share**: any author can drop their split to 60/40 or 50/50 to be featured in a "supporting authors" rail, or raise it to 90/10 (Tinkr keeps 10%) to opt out of discovery features. Patterned on itch.io [13].

### R4. Become merchant of record for plugin sales from day one

Gumroad did this in January 2025 [10]. The result: creators don't file tax returns, don't collect VAT, don't deal with international payment infrastructure. **For Tinkr**: when a plugin author publishes a paid plugin, Tinkr handles Stripe Connect onboarding, the actual payment, the VAT/sales tax collection in 100+ countries, and the payout. The author sees a 70% line item in their dashboard and a bank deposit. This is the difference between "I'm a plugin author" and "I'm running a small business."

### R5. The 4 free plugins should be the marketing channel, not a crippled trial

Wokwi's free tier is genuinely useful (unlimited simulations) and converts to paid [81]. Etsy's free listings are full-featured. **For Tinkr**: the 4 free plugins (ESP32, RP2040, nRF52, MicroPython runtime) should cover ~80% of the maker market out of the box. They should be:
- Fully featured (not "Pro features locked")
- Maintained by the Tinkr team (not abandoned)
- Discoverable through the same marketplace search
- Never throttled (no "fast build minutes" cap)

The paid plugins sell because they cover the other 20%: M5Stack, Argus, ESP-IDF vendor tools, third-party boards. The free tier's job is to make the user trust the platform.

### R6. Build a "Tinkr Ready" hardware certification program

SparkFun's Qwiic is a connector standard + library standard + documentation pattern [56]. Adafruit's "open source is the core of what we do" [53]. **For Tinkr**: a `Tinkr Ready` certification that says "this board ships with a `tinkr.plugin.toml` that works on first install." The certification is a checklist, not a paid license. Certified boards get a "Tinkr Ready" badge in the marketplace. The board vendor gets discovery. The user gets trust. Tinkr gets... nothing directly, but the network effect compounds.

### R7. Author dashboard = "earnings, payouts, KB usage, license keys, support tickets"

Atlassian's Partner dashboard has 1,800+ partners managing apps with monthly payouts, partner verification status, and security ticket status [40]. **For Tinkr v1.5 author dashboard, the minimum fields are**:
- **Sales**: last 7 days, last 30 days, last 90 days, all time. Per-plugin breakdown.
- **Payouts**: next payout date, last payout amount, Stripe Connect status, tax document status.
- **KB usage**: which KB entries were referenced when users installed your plugin (proxies for "what problems did people hit"). This is the gold — authors learn what to fix.
- **License keys**: for paid plugins, the active license keys (revoke, reissue, audit).
- **Support tickets**: a way for users to reach the author without leaving Tinkr.
- **Reviews/ratings**: aggregated from `tinkr plugin review` commands.

### R8. The "Tip the author" button is mandatory, even on free plugins

Buy Me a Coffee's data shows that 5% of tip-page visitors convert to paying tips [73]. For Tinkr: every plugin page has a "Tip the author $5" button. The button takes 5% (not 30%). It's a small revenue stream per plugin, but it adds up across the marketplace, and it gives users a way to thank the author of a free plugin. The infrastructure (Stripe Connect) is already there for paid plugins; tips are a 5-line addition.

### R9. License keys as plain files in `.tinkr/license/`, not activation servers

The "lifetime, re-downloadable" promise in the plugin spec [decisions.md A4] only works if the license is portable. **For Tinkr**: a paid plugin is a directory with a `.tinkr/license/<plugin>.key` file. The key is checked locally. No activation server, no online check. The user can move the plugin between machines by copying the directory. This is the strongest trust signal Tinkr can offer — "you bought this, you own it." GitHub-based plugin repos make this trivial.

### R10. Author identity is the GitHub identity, period

Per decisions.md A1 (GitHub + email, GitHub preferred). The marketplace should expose: `github.com/<author>/<plugin>`, the author's avatar, the author's GitHub Sponsors link, the author's other Tinkr plugins. The author's audience is on GitHub. The marketplace should not try to own that audience — it should be a discovery layer over the GitHub graph. **Anti-pattern to avoid**: Etsy's "your listing disappeared from search" trap, where the marketplace owns the audience relationship.

### R11. Vendor first-party plugins need a separate, faster path

Espressif's component registry lets Espressif publish with their privileged namespace [12]. **For Tinkr v1.5**: the launch partner (Espressif first) gets a `tinkr-espressif/*` namespace, an internal-only CLI, and a "Vendor First-Party" badge. The plugin spec already has the manifest structure; the only addition is a `vendor = true` flag and a separate review SLA (24 hours, not 7 days). This is the launch partner experience — make it easy for Espressif, and the others will follow.

### R12. Make search ranking transparent and reversible

Etsy's opaque algorithm is the dominant seller complaint [52]. Product Hunt's featured rate has dropped to 10% [76]. **For Tinkr**: the marketplace search is a function of `display_name + description + tags + installs + rating + recency`, with weights shown to the author in their dashboard. If a plugin's rank drops, the author should be able to see why. The reversible part: authors can edit their `display_name` and `tags` to A/B test ranking.

### R13. Build the Learning System in v1.5 alongside the marketplace

Adafruit's Learning System drives library adoption more than any paid channel [54]. **For Tinkr v1.5**: a `/learn` section with community-contributed guides for specific plugins. "Build a smart plant monitor with `tinkr-m5stack-core-s3`" is a guide. A guide is Markdown, screenshots, a code repo. The plugin author doesn't have to write the guide — anyone can. The guide links to the plugin. The plugin is installable from the guide. This is the Adafruit playbook adapted for a multi-author marketplace.

### R14. Plan for the v3.0 hardware marketplace by getting the contracts right now

Per decisions.md, hardware (PCBs) is a v3+ product, but the contract infrastructure for vendor first-party plugins is the same as for hardware. **For Tinkr v1.5**: the Statement of Work template for vendor first-party plugins is the same template that will be used for hardware partners in v3.0. Don't reinvent the contract when you launch hardware. Crowd Supply's SOW is the model [58].

### R15. Treat the AI agent as a creator-economy tool, not just a code tool

Wokwi has an AI agent. Embedder has an AI agent that "understands your hardware and technical documents" [85]. Anthropic's Claude has a plugin marketplace with 500+ developer tools [86]. **For Tinkr v1.5**: the plugin marketplace should be queryable by the agent. The agent should be able to ask "what's the best plugin for a BME280 sensor on an M5Stack CoreS3" and get a ranked list. This makes the marketplace part of the IDE experience, not a separate web store. The agent is the new "search."

### Top 5 platforms to study deepest

In order of importance to Tinkr's v1.5 design:

1. **itch.io** — The closest analogue in terms of "small, indie, software creators." The open revenue share model is the most direct inspiration for the recommended `R3` tiered split. Study: the open-revenue-share UX, the PWYW averaging, the bundling and pre-order features. https://itch.io/docs/general/about

2. **Arduino Library Manager** — The closest analogue in terms of "embedded + registry + GitHub." The bot-driven auto-merge is the model for `R1` and `R2`. Study: the `repositories.txt` file structure, the GitHub Actions workflow, the validation library. https://github.com/arduino/library-registry

3. **Gumroad** — The most polished creator-economy UX. The merchant-of-record shift in Jan 2025 is the model for `R4`. Study: the dashboard, the refund flow, the email broadcast features, the merchant-of-record legal structure. https://gumroad.com/help/article/66-gumroads-fees

4. **Atlassian Marketplace** — The "enterprise end" of the marketplace spectrum. Useful as a counter-example — what NOT to copy. The 10–15 day approval [38] is too slow. The Partner Verification KYC/KYB is too heavy for a maker audience. But the partner dashboard structure (sales, payouts, security tickets, app versions) is the right shape. Study: what to avoid. https://developer.atlassian.com/platform/marketplace/pricing-payment-and-billing/

5. **Homebrew Formulae** — The canonical "open source registry on GitHub" model. The PR-based submission, the local `brew audit`, the 50-minute post-merge CI delay. Study: the developer workflow, the cookbook documentation, the maintainer review process. https://docs.brew.sh/Adding-Software-to-Homebrew

---

## Section 6 — Anti-patterns to avoid

These are the specific things Tinkr's v1.5 marketplace should NOT copy, with the platform that did them and the reason.

### AP1. Don't take 30% across the board

Apple, Google, Steam. 30% made sense when the platform was a monopoly gatekeeper. In 2026, the creator-friendly end of the spectrum is 5–10% (itch.io, Buy Me a Coffee, Substack, Gumroad). **Tinkr should not anchor on 30% just because the App Store does.** Use the tiered model in `R3` instead.

### AP2. Don't launch a "distribution but no commerce" marketplace

VS Code Marketplace has 50,000+ extensions and $50M/year in paid revenue [22] because Microsoft never built a payment rail. 99% of extension developers earn nothing [24]. **Tinkr's v1.5 must ship with Stripe Connect integrated**, not as a follow-up. Adding it later is much harder than shipping it now.

### AP3. Don't have opaque search ranking

Etsy's "your listing disappeared from search" is the dominant seller complaint [52]. Product Hunt's featured rate of 10% is the new normal [76]. **Tinkr's search is the manifest's `display_name + description + tags + installs + rating + recency`** with weights visible to the author. No black box.

### AP4. Don't have a regional exclusion list

Chrome Web Store doesn't support developer registration in Armenia, Pakistan, Nigeria, and others [42]. **Tinkr's payment onboarding should support all countries Stripe Connect supports** (50+). If a country isn't supported, the plugin author is told immediately, not silently.

### AP5. Don't change pricing on existing creators

Patreon changed pricing in Aug 2025 to consolidate to 10% for all new creators, and "If you unpublish your creator page, you'll have the updated 10% platform plan applied" [65]. Shopify changed the $1M exemption from annual to lifetime in June 2025, locking in successful apps at 15% [29]. Both moves were trust-damaging. **Tinkr's v1.5 should commit: "the 70/30 split for any plugin published before v2.0 is locked for the lifetime of that plugin."**

### AP6. Don't require a web form for publishing

Chrome Web Store, Apple App Store Connect, Atlassian Marketplace all require web-based submission flows. **Tinkr should be a one-command CLI**: `tinkr plugin publish`. The author never visits a web form. The web UI is for buyers, not authors.

### AP7. Don't have a multi-month approval queue

WordPress has 3,500+ plugins in the queue [30]. The 2–4 week typical review is too slow [31]. **Tinkr's target is 24 hours automated, 7 days human, auto-approval on 8th day.** A multi-month queue is a creator-revenue killer.

### AP8. Don't require KYC/KYB for the long tail

Atlassian requires Partner Verification (Stripe Identity, business documents) for every Marketplace partner [39]. This is appropriate for Atlassian's enterprise customers. **For Tinkr's maker audience, KYC should kick in at $10K in cumulative sales per author**, not at the first plugin. Below that, friction costs more than fraud.

### AP9. Don't have a featured-only discovery model

Product Hunt's featured rate of 10% means 90% of launches get nothing [76]. **Tinkr's marketplace should be searchable without a "featured" gate.** Every plugin in the registry is on equal footing. Featured is an opt-in paid promotion, not an algorithmic filter.

### AP10. Don't disintermediate the author-audience relationship

The Substack, Gumroad, and itch.io pattern: creators own their email list. The platform is a discovery + payment layer, not a wall. **Tinkr's author identity is the GitHub identity**, and the marketplace should expose `github.com/<author>/<plugin>` everywhere. The plugin's README is the canonical description. The marketplace is a discovery layer, not a destination.

### AP11. Don't launch a "hardware marketplace" before v3.0

Tindie, Crowd Supply, and Kickstarter have all been at the hardware-maker-revenue problem for 5–15 years. Tindie's 5% + fulfillment-by-maker is the best in the category. **For Tinkr v1.5 and v2.0: software plugins only.** Hardware is a different business. The creator-economy vision is plugins first, hardware later.

### AP12. Don't try to be a "transactional storefront" — be a "creator storefront"

A transactional marketplace is what Amazon, eBay, and Etsy's search are. A creator marketplace has author pages, follower counts, related plugins by author, and an inbox. **Tinkr's author page should show**: all plugins by this author, total installs, author bio, GitHub link, sponsor link, "follow this author" inbox feed. The author is the unit of trust, not the plugin.

---

## Section 7 — Open questions for Ronie

These are the decisions that the data can inform but cannot make. They need your call.

### Q1. What's the launch partner strategy?

Per decisions.md A8, all three of Espressif, Wemos, M5Stack are approached in parallel, first to say yes becomes the launch partner. Espressif is the strongest first move (their acquisition of M5Stack in April 2024 means they're effectively two of the three [87]). **The data says**: a single launch partner is better than none, two is better than one, three at launch is a recipe for inconsistent onboarding experiences. The recommendation: land Espressif first, then M5Stack as a "second wave" partner 6 months later, and skip Wemos unless they have a specific differentiator (e.g., a new ESP32 variant).

### Q2. Should Tinkr be the merchant of record for plugin sales?

Gumroad did this in January 2025 [10]. The upside: creators don't file taxes, don't handle VAT. The downside: Tinkr is now in the crosshairs of EU VAT collection rules, US sales tax nexus, and Stripe Connect's compliance requirements. **The data says**: this is a 2–4 week legal/ops project. It's worth doing for v1.5 if the alternative is "every author has to figure out their own country tax setup." Recommendation: yes, do it for v1.5. Budget 2–4 weeks of legal/compliance work.

### Q3. How should the per-plugin annual update fee work?

Decisions.md A10 lists "per-plugin annual update fees" as one of the 4 pricing tiers. The data is sparse here — VS Code Marketplace has no equivalent, App Store has subscriptions but not for plugins, Substack has annual subscriptions. **The data says**: a "you paid $20 once, free updates for 1 year, then $5/year for updates" model is novel. It's similar to JetBrains' all-products subscription. The risk: it confuses one-time vs recurring in the buyer's head. Recommendation: prototype the model in v1.5 with 2–3 paid plugins and see how the conversion looks. If the conversion drops by more than 30%, fall back to one-time lifetime.

### Q4. Should Tinkr Pro be a separate SKU or bundled with the Maker Bundle?

Decisions.md A10: "$X/year for advanced features." The data says: Wokwi's Pro tier (€5.6/mo Hobby, €8.1/mo Hobby+) [81] converts because the free tier is useful but the paid tier is real value (offline, fast builds, private projects). The 4 free plugins + paid plugins model already does most of the "tier" work. **The open question**: does Tinkr Pro add anything beyond "fast cloud builds + team features + priority support" that the marketplace doesn't already cover? If yes, ship it. If no, drop it and keep the marketplace simple.

### Q5. What's the v2.0 creator program?

Decisions.md says v2.0 adds the "Plugin Author Program (anyone publishes, earns 70%)" and the "Verified Creator badge." The data says: a "Verified Creator" badge is only valuable if it's hard to get. If everyone can get it, it's not a signal. **The recommendation**: a Verified Creator requires (a) 3+ published plugins, (b) $1K+ lifetime sales, (c) GitHub org with 2FA + verified domain, (d) no outstanding support tickets > 14 days. This is the GitHub Marketplace model [88], not the "everyone gets a badge" model.

### Q6. Should the marketplace charge for listing?

Decisions.md says free plugins are free to publish. The data says: Tindie (5% per sale, no listing fee) [47] vs Etsy ($0.20 listing fee, 6.5% transaction) [50]. **The recommendation**: never charge a listing fee. The friction is at listing time, not at sale time. Free plugins should be free forever, including in the marketplace. Paid plugins pay Tinkr at sale time. Listing fees are an Etsy's-2022 mistake.

### Q7. What about the Tindie partnership for v3.0?

Decisions.md C (v3.0) lists "Tindie hardware marketplace (optional)" as a possibility. The data says: Tindie's 5% + fulfillment-by-maker is the right model, and the maker audience overlaps. **The recommendation**: explore a "powered by Tindie" link in the Tinkr IDE — "looking for the hardware for this plugin? Find Tinkr-compatible boards on Tindie." This is a partnership, not a build. Tindie already has the marketplace; Tinkr just needs a deep link. Build this in v3.0, not earlier.

### Q8. What's the relationship between the GitHub registry and the commercial marketplace?

The v1.0 plugin registry is a git repo of submodules (per plugin_spec.md). v1.5 adds Stripe Connect and paid plugins. **The data says**: the same plugin should be in the same registry, with a `pricing` field in the manifest. Free plugins are `pricing = "free"`. Paid plugins are `pricing = { "amount": 15, "currency": "USD", "type": "one-time" }`. The marketplace is a read-only view of the registry + the Stripe layer. This is the itch.io + Homebrew hybrid. The registry is the source of truth; the marketplace is the discoverability surface.

### Q9. What about the Argus / RPi / Jetson plugins in the v1.5 marketplace?

Decisions.md A11 says the argus repo becomes a proof-of-concept; production code lives in `tinkr.cli/plugins/tinkr-rpi5/`. **The data says**: if the v1.5 marketplace launches with vendor first-party plugins (Espressif) and at least 1 community plugin (the `tinkr-rpi5` that wraps Argus), the marketplace has both. Recommendation: ship `tinkr-rpi5` as a paid plugin in v1.5, priced at $15–$30, with Argus as the underlying free tool. This validates the "earn money building better hardware" narrative from the original vision.

### Q10. How does the marketplace relate to KB / Learning System / Project Memory?

Three systems are designed in the architecture (KB in learning_loop.md, Learning System in Section 5 R13, Project Memory in project_memory.md). The data doesn't have a direct analogue. **The recommendation**: the marketplace is a separate surface, but every plugin's marketplace page links to (a) the KB entries that mention it, (b) any Learning System guides that use it, (c) the project's project memory that references it. The marketplace is the discovery layer; the other three are the knowledge layer. The cross-linking is the moat.

---

## Appendix — Source URLs

[1] State of the Creator Economy 2026 — https://2026.creatoreconomyreports.com/
[2] Spark.money creator economy payments research — https://www.spark.money/research/creator-economy-payments
[3] Popup.fm "Creator Economy Predictions That Didn't Pan Out (2024-2025)" — https://popup.fm/blog/creator-economy-predictions-that-didnt-pan-out-2024-2025
[4] Arduino Library Manager submission update (Engineering.com) — https://www.engineering.com/arduino-introduces-updated-library-manager-for-easy-library-submissions/
[5] Homebrew "How to Open a Homebrew Pull Request" — https://docs.brew.sh/How-To-Open-a-Homebrew-Pull-Request
[6] WordPress Plugin Developer FAQ — https://developer.wordpress.org/plugins/wordpress-org/plugin-developer-faq/
[7] Shopify revenue share docs — https://shopify.dev/docs/apps/launch/distribution/revenue-share
[8] itch.io Open Revenue Sharing — https://itch.io/updates/introducing-open-revenue-sharing
[9] Substack paid subscription FAQ — https://faq.substack.com/p/how-do-paid-subscriptions-on-substack
[10] Gumroad pricing — https://gumroad.com/pricing
[11] itch.io revenue calculator — https://generalistprogrammer.com/tools/itchio-revenue-calculator
[12] ESP Component Registry — https://components.espressif.com/
[13] itch.io "About" — https://itch.io/docs/general/about
[14] Apple App Review — https://developer.apple.com/distribute/app-review/
[15] Apple P2B transparency report — https://developer.apple.com/support/p2b/
[16] Business Insider on Apple EU changes — https://www.businessinsider.com/apple-app-store-shakeup-in-europe-triggers-fury-2024-1
[17] SCMP on Chinese Apple antitrust — https://www.scmp.com/tech/big-tech/article/3358024/apple-faces-fresh-antitrust-complaint-chinese-developers-over-unfair-app-store-fees
[18] Gizmodo on App Store complaints — https://gizmodo.com/apple-cant-possibly-be-surprised-that-developers-are-un-1846529221
[19] npm publish docs — https://docs.npmjs.com/cli/v8/commands/npm-publish/
[20] SCWorld on npm "everything" prank — https://www.scworld.com/news/npm-registry-prank-leaves-developers-unable-to-unpublish-packages
[21] Dev.to on npm vs JSR publishing — https://dev.to/gabrielanhaia/publishing-the-same-library-to-npm-and-jsr-one-was-pleasant-b9k
[22] VS Code statistics — https://www.skillademia.com/statistics/vs-code-statistics/
[23] 3DIMLI on selling VS Code extensions off the marketplace — https://blog.3dimli.com/posts/85-sell-vscode-extensions-off-marketplace
[24] AdKar on monetizing VS Code extensions — https://adkar.online/blog/monetize-vs-code-extension
[25] GitHub Marketplace fee cut announcement — https://github.blog/news-insights/company-news/github-reduces-marketplace-transaction-fees-revamps-technology-partner-program/
[26] GitHub Marketplace payment docs — https://docs.github.com/en/apps/github-marketplace/selling-your-app-on-github-marketplace/receiving-payment-for-app-purchases
[27] Shopify App Store revenue share (2026) — https://weekonelabs.com/blog/shopify-app-revenue-benchmarks-2026
[28] Shopify App Store stats — https://craftberry.co/articles/shopify-app-store-statistics
[29] LinkedIn on Shopify lifetime $1M change — https://www.linkedin.com/posts/mat-de-sousa-20a365134_terrible-announcement-for-shopify-app-founders-activity-7321831611983933440-2J84
[30] WordPress plugin directory FAQ — https://developer.wordpress.org/plugins/wordpress-org/plugin-developer-faq/
[31] AutomagicWP on WP plugin review 2026 — https://www.automagicwp.com/blog/how-to-submit-wordpress-plugin
[32] WP Tavern on Mika Epstein — https://wptavern.com/behind-the-scenes-in-the-wordpress-plugin-directory-with-mika-epstein
[33] npm Pro launch — https://blog.npmjs.org/post/189591811407/new-products-new-pricing-and-a-glimpse-ahead.html
[34] APIs.io npm plans — https://apis.io/plans/npm/npm-plans-pricing/
[35] Atlassian Marketplace pricing — https://developer.atlassian.com/platform/marketplace/pricing-payment-and-billing/
[36] Stratrix on Atlassian business model — https://www.stratrix.com/business-model/how-atlassian-actually-makes-money
[37] Atlassian Marketplace revenue share updates — https://www.atlassian.com/blog/development/marketplace-revenue-share-updates
[38] Atlassian Marketplace app approval guidelines — https://developer.atlassian.com/platform/marketplace/app-approval-guidelines/
[39] Atlassian Partner verification — https://developer.atlassian.com/platform/marketplace/partner-due-diligence/
[40] Atlassian Marketplace security enforcement — https://developer.atlassian.com/platform/marketplace/marketplace-security-enforcement-policy/
[41] Sophos on Chrome Web Store fraud lockout — https://www.sophos.com/en-us/blog/fraud-spike-prompts-chrome-developer-lock-out
[42] Chrome Web Store regional limitations (Armenia) — https://support.google.com/chrome/thread/407350097/developer-dashboard?hl=en
[43] Chrome Web Store troubleshooting — https://developer.chrome.com/docs/webstore/troubleshooting
[44] Vercel Marketplace / Supabase case study — https://vercel.com/blog/how-supabase-increased-signups-through-the-vercel-marketplace
[45] Vercel Marketplace Partner API reference — https://vercel.com/docs/integrations/create-integration/marketplace-api/reference/partner
[46] Vercel Marketplace program — https://vercel.com/marketplace/program
[47] Tindie selling page — https://www.tindie.com/about/sell/
[48] Tindie fees 101 — https://sf-tindie.zendesk.com/hc/en-us/articles/4401806621076-Fees-101
[49] Etsy "What's New on Etsy: Fall 2025" — https://www.etsy.com/seller-handbook/article/1404283886419
[50] Etsy fees policy — https://www.etsy.com/legal/fees/
[51] CNET on Etsy fee strike — https://www.cnet.com/tech/services-and-software/etsy-sellers-protest-fees-hikes-after-the-platforms-pandemic-revenues-soar/
[52] FBD on Etsy exodus 2025 — https://fbd.agency/blog/why-artists-are-leaving-etsy-the-great-creative-exodus-of-2025/
[53] CircuitPython on GitHub — https://github.com/adafruit/circuitpython
[54] Adafruit Learning System — https://learn.adafruit.com/
[55] SparkFun on GitHub — https://github.com/sparkfun
[56] SparkFun community forums — https://community.sparkfun.com/
[57] Atomic14 on Crowd Supply experience — https://www.atomic14.com/2025/07/21/crowd-funding-retro
[58] Michael Altfield on Crowd Supply — https://tech.michaelaltfield.net/2022/10/20/crowd-supply-review/
[59] Kickstarter fees guide — https://updates.kickstarter.com/kickstarter-fees-a-comprehensive-guide-for-creators/
[60] BBB on Kickstarter complaints — https://www.bbb.org/us/ny/brooklyn/profile/crowdfunding/kickstarter-pbc-0121-137092/complaints
[61] ComplaintsBoard on Kickstarter — https://www.complaintsboard.com/kickstarter-b123317
[62] SeeedStudio Fusion PCB — https://www.seeedstudio.com/fusion_pcb.html
[63] Hackster on SeeedStudio tracking upgrade — https://www.hackster.io/news/seeed-studio-adds-detailed-tracking-to-fusion-pcb-manufacturing-service-offers-panellisation-advice-a95880522745.amp
[64] Patreon fee overview — https://support.patreon.com/hc/en-us/articles/11111747095181-Creator-fees-overview
[65] Patreon standard 10% plan — https://support.patreon.com/hc/en-us/articles/36426991446797-A-standard-platform-fee-for-new-creators-effective-after-August-4-2025
[66] Transferfees Patreon calculator — https://transferfees.io/patreon-fee-calculator/
[67] Gumroad fees help — https://gumroad.com/help/article/66-gumroads-fees
[68] Dodopayments Gumroad review — https://dodopayments.com/blogs/gumroad-review
[69] Ruzuku Substack pricing 2026 — https://www.ruzuku.com/learn/articles/substack-pricing
[70] TechBuzz on Substack exodus — https://www.techbuzz.ai/articles/writers-are-fleeing-the-substack-tax
[71] Buy Me a Coffee help — https://help.buymeacoffee.com/en/articles/10182730-what-is-buy-me-a-coffee-and-how-does-it-work
[72] Buy Me a Coffee FAQ — https://buymeacoffee.com/faq
[73] Owelet on Buy Me a Coffee fees — https://owelet.app/blog/buy-me-a-coffee-fees
[74] itch.io docs (creator payments) — https://itch.io/docs/creators/payments
[75] Trustpilot itch.io reviews — https://ie.trustpilot.com/review/itch.io?page=2
[76] Awesome Directories on Product Hunt featured rate — https://awesome-directories.com/blog/product-hunt-launch-guide-2025-algorithm-changes/
[77] Arc.dev Product Hunt playbook — https://arc.dev/employer-blog/product-hunt-launch-playbook/
[78] Arduino library-registry on GitHub — https://github.com/arduino/library-registry
[79] PlatformIO library stats — https://community.platformio.org/t/will-my-lib-be-accepted-in-the-registry/13719
[80] PlatformIO community — https://community.platformio.org/
[81] Wokwi pricing — https://wokwi.com/pricing
[82] Wokwi offline issue — https://github.com/wokwi/wokwi-features/issues/204
[83] Arduino forum on Wokwi limitations — https://forum.arduino.cc/t/simulator-which-one-is-better/1359552
[84] ESP-Techpedia on component management — https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/advanced-development/component-management.html
[85] Embedder on VS Code Marketplace — https://marketplace.visualstudio.com/items?itemName=Embedder.embedder-vscode
[86] Claude Plugin Marketplace (MCP Market) — https://mcpmarket.com/server/claude-plugin-marketplace
[87] Espressif acquires M5Stack (April 2024) — https://www.espressif.com/en/news/Espressif_Acquires_M5Stack
[88] GitHub publisher verification docs — https://docs.github.com/en/apps/github-marketplace/github-marketplace-overview/applying-for-publisher-verification-for-your-organization

---

*End of report. Word count: ~7,400. Sources verified through Q2 2026. For questions, see Section 7.*
