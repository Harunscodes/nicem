# NiceM Document Plan v0.1

**Status:** Section-level content plan — sits between the canonical fact-set and the future language renderings
**Role:** Maps the 78 canonical facts onto the section structure of the eight NiceHome KB documents, fixes controlled terminology, and resolves ambiguity risks before any prose is written. The English, Dutch, and Turkish renderings will each be authored from this plan and the fact-set.
**Version:** kb-plan-v0.1.0 (not yet frozen)
**Source of truth:** `canonical-fact-set.md` (fs-v0.1.0) — the only source of policy content
**Depends on:** `canonical-fact-set.md`, `dataset-specification.md`
**Feeds into:** `language-rendering-plan.md`, `kb-rendering-en.md`, `kb-rendering-nl.md`, `kb-rendering-tr.md`, `intent-set.md`

---

## 1. Purpose

The document plan exists between the canonical fact-set and the language renderings for one reason: **three independent renderings cannot be parallel unless their structure is fixed in advance**. If the English, Dutch, and Turkish documents were each authored freely from the fact-set, they would diverge in section count, fact placement, and chunk boundaries — and any such divergence becomes a structural confound in language-matched retrieval. A fact that lives in section 2 of the English document but section 4 of the Turkish document will be retrieved differently for reasons that have nothing to do with token-tax or execution-tax.

The plan fixes, once, language-neutrally:
- which facts go in which document section
- the section headings (as language-neutral labels to be rendered identically in structure)
- the controlled terminology each rendering must use consistently
- the chunk boundaries that preserve complete policy conditions
- the explicit resolution of every ambiguity risk identified in the fact-set

After this plan is stable, authoring a rendering becomes a constrained translation-of-meaning task, not a free composition task. This protects the core experimental control: **the same canonical facts, in the same structure, retrieved as the same semantic units, across all three languages.**

This plan introduces no new policy content. Every fact placed here already exists in `canonical-fact-set.md`. The plan adds only structure.

---

## 2. Planning principles

**Structured fact-set remains canonical.** This plan organizes the fact-set; it does not amend it. If a structural need reveals a gap or contradiction in the fact-set, the fact-set is fixed first (with a version bump), and the plan follows.

**No English document is canonical.** The English rendering is one of three peers. This plan is written in English because the project is documented in English, but the plan's *labels and structure* are language-neutral specifications, not the English document itself.

**All language renderings must be based on this plan and the fact-set.** No rendering is authored by translating another rendering. Each of English, Dutch, and Turkish is built from (plan + fact-set).

**Section structure must be parallel across languages.** Every document has the same number of sections, in the same order, covering the same fact IDs, in all three languages. Headings are rendered per language but their structure and meaning are identical.

**Terminology must be controlled.** §3 fixes the canonical meaning of every key term. The per-language word choices are deferred to `language-rendering-plan.md`, but the *concept* each term denotes is fixed here, and a rendering must use one consistent term per concept throughout.

**Similar facts must be disambiguated.** Where two facts could be confused (the eight ambiguity risks), the plan places them so the distinction is visible and adds explicit disambiguation guidance.

**No new policy facts may be introduced in prose renderings.** A rendering may add connective language ("To return a device, follow these steps:") but may not add any policy claim not present in the fact-set. §8 makes this a quality gate.

**Ambiguity risks must be handled explicitly.** Every risk from the fact-set summary is assigned a control in §5 and reflected in the relevant document plan.

---

## 3. Global terminology decisions

The following terms have fixed canonical meanings. Per-language word choices are deferred to `language-rendering-plan.md`; this section fixes *what each term means* and the constraint that one term maps to one concept (and vice versa) within and across renderings.

| Canonical term | Fixed meaning | Terminology constraint |
|---|---|---|
| NiceHome Hub | The central device that manages all other NiceHome devices (F0101) | Product name; rendered identically across all languages (brand name not translated) |
| NiceHome Sensor | The device measuring temperature, humidity, motion (F0102) | Product name; not translated |
| NiceHome Plug | The smart outlet with remote switching and energy monitoring (F0103) | Product name; not translated |
| NiceHome Camera | The indoor camera with motion alerts and live view (F0104) | Product name; not translated |
| standard warranty | The 2-year-from-purchase coverage applying to all devices (F0201) | One term per language for "warranty"; do not alternate synonyms within a rendering |
| return window | The 30-day-from-purchase period for returns (F0301) | Must be distinct in wording from any "storage period"/"retention" term |
| cloud storage | The 30-day cloud video retention provided by the subscription (F0402) | Must be distinct in wording from "return window"; tied to subscription, not device |
| live view | Real-time Camera viewing; works without subscription but needs Hub online (F0104, F0403, F0110) | Distinct from "cloud storage"/"recording"; never implies stored video |
| soft reset | Restart of a device that keeps its settings (F0804) | Must be lexically distinct from "factory reset" and from "restart the Hub" |
| factory reset | Full erase of settings + unlink from account (F0805) | Must be lexically distinct from "soft reset" |
| pairing mode | Device state for connecting to the Hub, entered by a 5-second setup-button hold (F0607) | "Pairing" wording distinct from "reset"; 5-second hold never conflated with the 10-second reset hold |
| repair | Fixing a device (in- or out-of-warranty) (F0701, F0702) | Distinct from "replacement" |
| replacement | Providing a different device when repair is not possible/applicable (F0703) | Distinct from "repair"; may be new or refurbished (F0704) |
| refurbished replacement | A replacement device that is refurbished, not new (F0704, F0705) | "Refurbished" qualifier explicit; carries remainder-of-warranty-or-90-days floor |
| subscription plan | The Camera Plus Plan; cloud subscription requiring Camera + Hub (F0401, F0404) | Plan name "Camera Plus Plan" rendered consistently; not translated as a generic phrase |
| account recovery | The password-reset procedure via email link (F0801–F0803) | "Account/password recovery" distinct from "device reset" |

Additional fixed quantities (must render identically as values, not be recomputed):
- 2 years (warranty), 30 days (return window), 30 days (cloud storage), 14 days (trial), 5 to 7 business days (Standard shipping), 2 business days (Express shipping), 2 hours (order modification), 14 business days (refund processing), 10 business days (repair turnaround), 5 seconds (pairing hold), 10 seconds (Hub factory-reset hold), 90 days (refurbished warranty floor), 50 (not present — do not introduce).

---

## 4. Document-level plans

Each plan below covers: purpose, target reader, fact IDs covered, section headings (language-neutral labels), section-by-section fact mapping, ambiguity risks, terminology notes, facts that must not be confused, forbidden prose additions, and expected retrieval chunks.

The proposed chunking convention throughout: **one retrieval chunk per section**, so that a chunk carries a complete policy condition (or a complete ordered procedure) and a known set of fact IDs. Final chunk length is an open question (§10), but the chunk *boundary* is the section boundary.

---

### D01 — Product overview and device compatibility

- **Document purpose:** Introduce the four devices and state the compatibility/requirement rules between them and across generations.
- **Target reader:** A prospective or new user asking what each device does and what is required to use it.
- **Fact IDs covered:** F0101–F0110 (10 facts)
- **Proposed section headings:**
  1. Device overview
  2. Hub requirement and standalone capability
  3. Generation compatibility
  4. Live view availability
- **Section-by-section fact mapping:**
  - §1 Device overview → F0101 (Hub), F0102 (Sensor), F0103 (Plug), F0104 (Camera)
  - §2 Hub requirement and standalone capability → F0105 (Sensor needs Hub), F0106 (Camera needs Hub), F0107 (Plug: on/off without Hub, automation needs Hub)
  - §3 Generation compatibility → F0108 (Gen 2 devices need Gen 2 Hub), F0109 (Gen 2 Hub backward compatible)
  - §4 Live view availability → F0110 (no live view when Hub offline)
- **Ambiguity risks:** Live-view-vs-subscription confusion (F0110 here is about Hub-online; the subscription dependency lives in D04). The one-directional generation compatibility (F0108/F0109) must not collapse into "all Hubs support all devices."
- **Terminology notes:** Use "Hub required" consistently for F0105/F0106; for F0107 use the controlled split between "basic on/off" and "automation features."
- **Facts that must not be confused:** F0108 vs. F0109 (asymmetric compatibility); F0110 (Hub-online live view) vs. D04 F0403 (subscription-independent live view).
- **Forbidden prose additions:** No device-count limit (the "50 devices" fact was deliberately excluded); no technical specs (power, frequency); no roadmap/future products.
- **Expected retrieval chunks:** 4 chunks (one per section). Compatibility queries should retrieve §2 and/or §3; "what does X do" queries should retrieve §1.

---

### D02 — Warranty policy

- **Document purpose:** State warranty period, coverage, exclusions, the claim process, and the outcome of a confirmed claim.
- **Target reader:** A user whose device failed and wants to know whether and how it is covered.
- **Fact IDs covered:** F0201–F0209 (9 facts)
- **Proposed section headings:**
  1. Warranty period
  2. What is covered
  3. What is not covered
  4. Making a warranty claim
  5. Claim outcome
- **Section-by-section fact mapping:**
  - §1 Warranty period → F0201 (2 years from purchase, all devices)
  - §2 What is covered → F0202 (manufacturing defects, hardware failures under normal use)
  - §3 What is not covered → F0203 (accidental damage), F0204 (misuse/unauthorized modification)
  - §4 Making a warranty claim → F0205 (proof of purchase required), F0206 (step 1: contact support with serial), F0207 (step 2: claim reference + prepaid label), F0208 (step 3: ship with prepaid label)
  - §5 Claim outcome → F0209 (confirmed covered defect → free repair or replacement)
- **Ambiguity risks:** 2-year warranty vs. 30-day return window (D03) — these must read as separate timeframes. Proof of purchase (F0205) vs. serial number (F0206) are two distinct requirements.
- **Terminology notes:** "Prepaid label" (F0207) signals free in-warranty shipping; keep it lexically distinct from the customer-paid out-of-warranty shipping in D07 (F0706).
- **Facts that must not be confused:** Warranty period (2 years) vs. return window (30 days); covered-defect outcome (F0209) vs. repair policy details (D07).
- **Forbidden prose additions:** No specific claim-processing time (none is in the fact-set); no fee for in-warranty claims; no device-specific warranty variation.
- **Expected retrieval chunks:** 5 chunks. Coverage queries → §2/§3; "how do I claim" → §4 (one chunk holding the full ordered procedure).

---

### D03 — Return and refund policy

- **Document purpose:** State the return window, the refund conditions (unopened/opened/damaged), exclusions, refund mechanics, and the return process.
- **Target reader:** A user who bought a device and wants to return it.
- **Fact IDs covered:** F0301–F0311 (11 facts)
- **Proposed section headings:**
  1. Return window
  2. Refund by device condition
  3. Return exclusions
  4. Refund processing
  5. Return process
- **Section-by-section fact mapping:**
  - §1 Return window → F0301 (30 days from purchase), F0305 (after 30 days not accepted)
  - §2 Refund by device condition → F0302 (unopened → full refund, free shipping), F0303 (opened undamaged → full refund, customer pays shipping)
  - §3 Return exclusions → F0304 (customer-damaged not refundable unless warranty), F0306 (subscriptions not refundable via returns)
  - §4 Refund processing → F0307 (original payment method), F0308 (within 14 business days of receipt)
  - §5 Return process → F0309 (step 1: request authorization), F0310 (step 2: receive RA number + instructions), F0311 (step 3: ship with RA number)
- **Ambiguity risks:** The unopened/opened distinction differs only in *who pays return shipping* (refund is full in both) — keep that the sole difference. Return window (30 days) vs. warranty (2 years). Subscription exclusion (F0306) cross-references D04.
- **Terminology notes:** "Return authorization (RA) number" is one controlled term; do not alternate with "return reference." Distinct from warranty "claim reference" (D02).
- **Facts that must not be confused:** F0302 vs. F0303 (shipping cost, not refund amount); F0304 (damage exclusion) routes to warranty, not refund; refund processing window (14 business days) vs. repair turnaround (10 business days, D07).
- **Forbidden prose additions:** No restocking fee; no partial-refund tier; no return window other than 30 days.
- **Expected retrieval chunks:** 5 chunks. "Can I return an opened device" → §2; "how do I return" → §5; "subscriptions refundable?" → §3 (and cross-link to D04).

---

### D04 — Subscription plan rules

- **Document purpose:** Describe the Camera Plus Plan, its storage feature, eligibility, trial, cancellation, and change timing.
- **Target reader:** A Camera owner deciding about or managing the cloud subscription.
- **Fact IDs covered:** F0401–F0409 (9 facts)
- **Proposed section headings:**
  1. Plan overview
  2. What the plan provides
  3. Plan requirements
  4. Free trial
  5. Cancellation and changes
- **Section-by-section fact mapping:**
  - §1 Plan overview → F0401 (Camera Plus Plan is the cloud subscription)
  - §2 What the plan provides → F0402 (30 days cloud video storage for Camera), F0403 (without subscription: live view yes, cloud storage no)
  - §3 Plan requirements → F0404 (requires Camera + Hub)
  - §4 Free trial → F0405 (14-day trial), F0406 (once per account)
  - §5 Cancellation and changes → F0407 (access to end of billing period), F0408 (no pro-rated refund), F0409 (changes take effect next billing period)
- **Ambiguity risks:** 30-day storage (F0402) vs. 30-day return window (D03 F0301) — same number, different meaning; keep terms lexically distinct. 14-day trial (F0405) vs. 30-day storage (F0402) — two numbers in one document. Live view (F0403) is subscription-independent but Hub-dependent (D01 F0110).
- **Terminology notes:** "Camera Plus Plan" rendered consistently as a proper plan name. "Cloud storage"/"cloud video storage" distinct from "live view." "Billing period" is the cancellation/change reference unit; no price is ever stated.
- **Facts that must not be confused:** Trial length (14 days) vs. storage length (30 days); cancellation continuation (F0407) vs. refund (there is none, F0408); live view (always available, subscription-free) vs. cloud storage (subscription-only).
- **Forbidden prose additions:** No price/cost figures; no storage duration other than 30 days; no trial length other than 14 days; no claim that live view needs the subscription.
- **Expected retrieval chunks:** 5 chunks. "What do I get" → §2; "how do I cancel / do I get a refund" → §5; "is there a trial" → §4.

---

### D05 — Shipping and delivery policy

- **Document purpose:** State shipping methods and timeframes, express eligibility, order-modification window, and handling of delayed/lost shipments.
- **Target reader:** A user placing an order or with a shipment problem.
- **Fact IDs covered:** F0501–F0508 (8 facts)
- **Proposed section headings:**
  1. Shipping methods and timeframes
  2. Express eligibility
  3. Changing or cancelling an order
  4. Delayed or lost shipments
- **Section-by-section fact mapping:**
  - §1 Shipping methods and timeframes → F0501 (Standard + Express), F0502 (Standard 5–7 business days), F0503 (Express 2 business days)
  - §2 Express eligibility → F0504 (Express only for in-stock items)
  - §3 Changing or cancelling an order → F0505 (modify/cancel within 2 hours), F0506 (after 2 hours: no cancel, but return after delivery)
  - §4 Delayed or lost shipments → F0507 (delayed → shipping-fee refund on request), F0508 (lost → free replacement)
- **Ambiguity risks:** Delayed (F0507, refund of shipping fee only) vs. lost (F0508, replacement) — distinct remedies; neither refunds the product price. Order-modification 2-hour window (F0505) vs. return window (D03).
- **Terminology notes:** "Business days" consistently (not "days"). "Shipping fee" (the refundable element in F0507) distinct from "product price" (never refunded for shipping issues).
- **Facts that must not be confused:** Standard vs. Express timeframes (5–7 vs. 2 business days); delay remedy vs. loss remedy; 2-hour order window vs. 30-day return window; F0506 bridges to D03 returns.
- **Forbidden prose additions:** No specific country/region lists (only "supported delivery regions" in the abstract, and that fact was not included — do not introduce geography); no overnight/same-day option; no shipping price figures.
- **Expected retrieval chunks:** 4 chunks. "How long does shipping take" → §1; "can I cancel my order" → §3; "my package is late/lost" → §4.

---

### D06 — Troubleshooting guide

- **Document purpose:** Provide ordered diagnostic procedures for connectivity, pairing, power (Plug), and sensor calibration, plus the escalation rule.
- **Target reader:** A user with a malfunctioning device trying to self-resolve.
- **Fact IDs covered:** F0601–F0613 (13 facts)
- **Proposed section headings:**
  1. Connectivity troubleshooting
  2. Hub status indicators
  3. Pairing a device
  4. Unresponsive Plug
  5. Inaccurate Sensor readings
  6. When to contact support
- **Section-by-section fact mapping:**
  - §1 Connectivity troubleshooting → F0601 (step 1: check Hub light), F0602 (step 2: light off → check cable/outlet), F0603 (step 3: light on but offline → restart Hub), F0604 (step 4: still offline → check network/router)
  - §2 Hub status indicators → F0605 (blinking red = lost network connection)
  - §3 Pairing a device → F0606 (step 1: app → Add device), F0607 (step 2: hold setup button 5 seconds), F0608 (step 3: follow app prompts), F0609 (pairing fails → ensure within Hub range)
  - §4 Unresponsive Plug → F0610 (toggle off/on in app), F0611 (still unresponsive → soft reset)
  - §5 Inaccurate Sensor readings → F0612 (recalibrate from app settings)
  - §6 When to contact support → F0613 (unresolved → contact support)
- **Ambiguity risks:** Three "reset-like" operations span documents — Hub *restart* (F0603, here), Plug *soft reset* (F0611, here), *factory reset* (D08 F0805/F0806). They must read as three distinct actions. The 5-second pairing hold (F0607) vs. the 10-second Hub factory-reset hold (D08 F0806).
- **Terminology notes:** "Restart the Hub" (F0603) ≠ "soft reset" (F0611) ≠ "factory reset" (D08). Keep all three lexically separate per language. Step conditions ("if the light is off…") must be preserved — the procedures are conditional sequences, not flat lists.
- **Facts that must not be confused:** Restart vs. soft reset vs. factory reset; 5-second pairing hold vs. 10-second factory-reset hold; "blinking red" (F0605) vs. other indicator states (none others defined — do not invent).
- **Forbidden prose additions:** No new diagnostic steps; no hardware-internal explanations; no circular diagnostics; no device-replacement advice except via the escalation fact (F0613).
- **Expected retrieval chunks:** 6 chunks. Critically, each *ordered procedure* (connectivity §1; pairing §3) should remain a single chunk so the full sequence is retrieved together (see §6). "My Hub won't connect" → §1 (+§2); "how do I add a device" → §3.

---

### D07 — Repair and replacement policy

- **Document purpose:** State repair/replacement eligibility (in/out of warranty), replacement nature (new/refurbished), the refurbished-warranty floor, cost responsibility, turnaround, the accidental/liquid-damage exclusion, and the request entry point.
- **Target reader:** A user with a device that needs repair, in or out of warranty.
- **Fact IDs covered:** F0701–F0709 (9 facts)
- **Proposed section headings:**
  1. In-warranty repair and replacement
  2. Out-of-warranty repair
  3. Replacement devices
  4. Damage exclusions
  5. Turnaround and how to request
- **Section-by-section fact mapping:**
  - §1 In-warranty repair and replacement → F0701 (in-warranty covered defect → free repair/replace), F0703 (in-warranty unrepairable → replaced)
  - §2 Out-of-warranty repair → F0702 (out-of-warranty → service fee), F0706 (customer pays shipping both ways)
  - §3 Replacement devices → F0704 (new or refurbished), F0705 (refurbished carries remainder of warranty, min 90 days)
  - §4 Damage exclusions → F0708 (accidental/liquid damage → out-of-warranty service quote, not standard repair)
  - §5 Turnaround and how to request → F0707 (10 business days after receipt), F0709 (request step: contact support → repair reference + instructions)
- **Ambiguity risks:** Refurbished warranty floor (F0705): "remainder of original warranty OR 90 days, whichever is longer" — must not render as a flat 90-day reset or a full 2-year reset. In-warranty free shipping (D02 prepaid label) vs. out-of-warranty customer-paid both-ways shipping (F0706).
- **Terminology notes:** "Repair" vs. "replacement" vs. "refurbished replacement" kept distinct (§3 terminology). "Service fee" (out-of-warranty) and "service quote" (damage exclusion) are distinct from "free" in-warranty service.
- **Facts that must not be confused:** In-warranty (free) vs. out-of-warranty (fee + shipping); repair turnaround (10 business days) vs. refund processing (14 business days, D03); accidental/liquid damage (F0708) connects to warranty exclusion F0203.
- **Forbidden prose additions:** No specific fee amounts; no warranty-reset-to-full-period claim; no turnaround other than 10 business days.
- **Expected retrieval chunks:** 5 chunks. "Is my repair free" → §1/§2; "will I get a new or used device" → §3; "I spilled water on it" → §4.

---

### D08 — Account access and device reset policy

- **Document purpose:** State the password-recovery procedure, the soft-vs-factory reset distinction, the Hub factory-reset procedure, post-reset re-pairing, remote removal of a lost device, and the cloud-video carve-out.
- **Target reader:** A user managing account access or resetting a device.
- **Fact IDs covered:** F0801–F0809 (9 facts)
- **Proposed section headings:**
  1. Password recovery
  2. Soft reset vs. factory reset
  3. Factory resetting the Hub
  4. After a factory reset
  5. Managing a lost device
- **Section-by-section fact mapping:**
  - §1 Password recovery → F0801 (step 1: Forgot password), F0802 (step 2: enter email → reset link), F0803 (step 3: follow link → new password)
  - §2 Soft reset vs. factory reset → F0804 (soft reset keeps settings), F0805 (factory reset erases settings + unlinks)
  - §3 Factory resetting the Hub → F0806 (hold reset button 10 seconds), F0807 (wait for blink = re-pair required after)
  - §4 After a factory reset → F0807 (device must be re-paired), F0809 (factory reset does not delete cloud video)
  - §5 Managing a lost device → F0808 (remove from account remotely via app)
- **Ambiguity risks:** Soft reset (F0804) vs. factory reset (F0805) vs. Hub restart (D06 F0603) — three distinct operations. 10-second factory-reset hold (F0806) vs. 5-second pairing hold (D06 F0607). Factory reset erases device settings (F0805) but NOT cloud video (F0809) — the carve-out must be explicit.
- **Terminology notes:** "Soft reset" and "factory reset" lexically distinct and stable. "Re-pair" (after factory reset) ties to D06 pairing terminology. "Cloud video" tied to subscription (D04), not device.
- **Facts that must not be confused:** Soft vs. factory reset vs. restart; 10-second vs. 5-second hold; what factory reset deletes (settings + account link) vs. what it does not (cloud video, F0809).
- **Note on F0807 appearing in two sections:** F0807 is mapped to both §3 (it is the terminal state of the reset procedure) and §4 (it is the gating rule for reuse). To avoid duplicating a policy fact across chunks, the prose should state the re-pair requirement once, in §4, and §3 should end at the blink confirmation (F0807's indicator half) with a forward reference. See ambiguity control AC9 in §5.
- **Forbidden prose additions:** No claim that factory reset deletes cloud video; no hold duration other than 10 seconds for the Hub; no recovery method other than the email link.
- **Expected retrieval chunks:** 5 chunks. "I forgot my password" → §1; "difference between resets" → §2; "how do I factory reset my Hub" → §3 (+§4); "I lost my device" → §5.

---

## 5. Cross-document ambiguity controls

Each control (AC) addresses a known risk and states the structural + terminological measure that resolves it. These are binding on all three renderings.

- **AC1 — 30-day return window vs. 30-day cloud storage retention.** Different documents (D03 §1 vs. D04 §2) and lexically distinct terms ("return window" vs. "cloud storage retention/period"). Renderings must never use the same noun phrase for both.
- **AC2 — 5-second pairing hold vs. 10-second Hub factory reset.** Different documents (D06 §3 vs. D08 §3). The hold action verb may be shared, but the durations and the operation names ("pairing mode" vs. "factory reset") must be unmistakably different. Each fact's prose explicitly names the duration.
- **AC3 — 14-day trial vs. 30-day storage.** Both in D04 but in different sections (§4 vs. §2). Prose must attach each number to its noun ("14-day free trial", "30 days of cloud storage") and never present them adjacently without their nouns.
- **AC4 — Live view depends on Hub-online but not on subscription.** Two facts in two documents: D01 §4 (F0110, Hub-online dependency) and D04 §2 (F0403, subscription-independence). Renderings must state both dependencies separately and never imply live view requires the subscription.
- **AC5 — Soft reset vs. factory reset vs. Hub restart.** Three operations across D06 §1/§4 and D08 §2. D08 §2 carries the canonical soft-vs-factory contrast; D06 uses "restart the Hub" (F0603) and "soft reset the Plug" (F0611). Three distinct lexical items per language, fixed in `language-rendering-plan.md`.
- **AC6 — Delayed shipping fee refund vs. lost-shipment replacement.** Both in D05 §4 but as two separate sentences with two separate remedies. Neither refunds the product price; prose must not merge them.
- **AC7 — 2-year warranty vs. 30-day return window.** Different documents (D02 §1 vs. D03 §1). The two timeframes must never appear as alternatives for the same situation; warranty is about defects, returns are about buyer's remorse / condition.
- **AC8 — Refurbished replacement warranty floor.** D07 §3 (F0705). The rendering must express "the longer of (remainder of original warranty) and (90 days)" — a minimum floor, not a reset. This is the single most error-prone fact; its prose is reviewed specifically against the flat-90-day and full-reset misreadings.
- **AC9 — F0807 dual placement.** Stated once in D08 §4 (re-pair requirement), with D08 §3 ending at the blink confirmation and forward-referencing §4. Prevents the same policy fact from generating two divergent chunks.

---

## 6. Retrieval chunking implications

The renderings will later be chunked for Agent B (Simple RAG). The plan constrains chunking now so that chunk boundaries are language-neutral and fact-traceable.

- **Chunks preserve complete policy conditions.** The chunk boundary is the section boundary (§4). A conditional rule and its conditions live in the same chunk, so retrieving the rule retrieves its conditions.
- **Exception facts stay near the rule they modify.** Exceptions are placed in the same document as their primary fact, in an adjacent section: F0203/F0204 (D02 §3) sit beside coverage (D02 §2); F0304/F0306 (D03 §3) beside the refund conditions (D03 §2); F0809 (D08 §4) beside the factory-reset definition (D08 §2/§3). Where an exception is in a different document (none here cross documents for retrieval), a cross-reference is used.
- **Ordered steps are not split across chunks.** Each ordered procedure is a single chunk: the warranty claim (D02 §4), the return process (D03 §5), connectivity diagnosis (D06 §1), pairing (D06 §3), password recovery (D08 §1), Hub factory reset (D08 §3). A multi-step answer should be retrievable from one chunk.
- **Chunks carry fact IDs.** Each chunk's source section maps to a known list of fact IDs (the §4 mappings). This mapping is metadata used to populate the logging schema's `semantic_units_retrieved` field — see §10 open question on how chunk IDs map to fact IDs.
- **Retrieval is evaluated in semantic units (fact IDs), not only text.** Per the dual-reporting rule (`baseline-token-tax-calculation-v0.1.md`), retrieval volume is reported in both raw tokens and fact IDs present. The section-as-chunk convention makes the fact-ID set of any retrieved chunk deterministic.

A consequence worth stating: documents vary in section count (D01:4, D02:5, D03:5, D04:5, D05:4, D06:6, D07:5, D08:5), so they vary in chunk count. This is acceptable because chunk count is held constant *across languages* for each document — the experimental control is cross-language parallelism, not cross-document uniformity.

---

## 7. Language rendering implications

- **Same section structure across languages.** English, Dutch, and Turkish renderings of a given document have the same sections, in the same order, covering the same fact IDs. Headings are rendered per language; structure is identical.
- **Preserve meaning, not literal phrasing.** A rendering expresses the fact-set's meaning in natural target-language prose. It is not a word-for-word translation of any other rendering.
- **Avoid idioms and culturally specific phrasing.** Plain language only; no expressions that lack a clean cross-language equivalent or that import meaning absent from the fact-set.
- **Keep device names stable.** "NiceHome Hub/Sensor/Plug/Camera" and "Camera Plus Plan" are rendered identically (brand names not translated) in all three languages.
- **Do not make English the hidden original.** No rendering is authored by adapting the English document. The authoring input is (this plan + the fact-set), independently for each language.
- **Turkish review.** The project owner, a native Turkish speaker, may review the Turkish renderings at run level. Independent bilingual review is recommended before any public or publication-grade claim, per `evaluation-method-v0.1.md` and `language-selection-v0.1.md`.

---

## 8. Quality gates for future prose renderings

Each rendering must pass these gates before it is frozen (these specialize `dataset-specification.md` §11 to the rendering step):

| Gate | Check |
|---|---|
| Fact coverage | Every fact ID assigned to a document in §4 appears in that document's intended section in the rendering |
| Meaning preservation | No fact ID appears with changed meaning; required_entities and rule/action content are present |
| No unsupported facts | No policy claim appears that is not in the canonical fact-set (connective language is allowed; policy is not) |
| Exceptions attached | Every exception fact appears adjacent to the rule it modifies, per the §6 chunking placement |
| Terminology consistency | One controlled term per concept (§3) throughout; no synonym drift within a rendering |
| Ambiguity resolution | Every applicable AC1–AC9 control is satisfied in the rendering |
| Structural parallelism | Section headings and order match across the three language renderings for each document |
| Number fidelity | All fixed quantities (§3) appear as stated values, not recomputed or altered |

---

## 9. Future files enabled by this plan

```
docs/benchmark/v0.1/language-rendering-plan.md  — per-language controlled terminology (the word choices §3 defers), register decisions, chunk-ID scheme
docs/benchmark/v0.1/kb-rendering-en.md          — English KB rendering (from plan + fact-set)
docs/benchmark/v0.1/kb-rendering-nl.md          — Dutch KB rendering (from plan + fact-set)
docs/benchmark/v0.1/kb-rendering-tr.md          — Turkish KB rendering (from plan + fact-set)
docs/benchmark/v0.1/intent-set.md               — 36 intent specifications
docs/benchmark/v0.1/expected-fact-mapping.md    — intent → required facts (evaluator reference)
docs/benchmark/v0.1/quality-gates.md            — pre-run checklist with pass/fail status
```

Recommended next: `language-rendering-plan.md` (fixes the per-language terminology this plan deferred), then the three KB renderings in parallel, then `intent-set.md`.

---

## 10. Open questions

- **DP1 — Should each document have exactly the same number of sections across languages?** Yes within a document (cross-language parallelism is required, §7). The plan does *not* require the same section count across different documents (§6). Confirmed direction; recorded for visibility.
- **DP2 — Should fact IDs appear visibly in prose KB renderings or only as metadata?** Leaning metadata-only: visible fact IDs in prose would leak structure to the model and contaminate retrieval realism. Fact-ID-to-chunk mapping lives in rendering metadata, not in the user-visible text. Decide in `language-rendering-plan.md`.
- **DP3 — How long should each retrieval chunk be?** Open. The chunk *boundary* is the section (§6); the resulting token length varies by section and language (a token-tax effect to be measured, not engineered away). Confirm whether any section is too long for a single chunk during rendering.
- **DP4 — Should troubleshooting steps be one chunk or multiple chunks?** Direction set: one chunk per ordered procedure (§6), so a full multi-step answer is retrievable together. Confirm against DP3 chunk-length limits for the longest procedure (connectivity, D06 §1, four steps).
- **DP5 — Should subscription (D04) and account (D08) documents cross-reference each other?** Yes, minimally: the cloud-video carve-out (F0809, D08 §4) references that cloud video is governed by the subscription (D04). Keep cross-references as pointers, not as duplicated policy facts (AC9 principle).
- **DP6 — How much redundancy is allowed across documents?** Minimal. A policy fact lives in exactly one document/section (its mapping in §4). Cross-document relationships are expressed as references, not repetition, to avoid divergent chunks and double-counted retrieval units.
- **DP7 — How will chunk IDs map to fact IDs?** Each chunk = one document section; each section maps to a fixed fact-ID list (§4). Proposed chunk ID scheme: `<document_id>-S<section_number>` (e.g., `D03-S2`), with its fact-ID list stored in rendering metadata. Finalize the scheme in `language-rendering-plan.md`; it must be identical across languages so `semantic_units_retrieved` is comparable.

---

## Summary

- **Sections planned per document:** D01:4, D02:5, D03:5, D04:5, D05:4, D06:6, D07:5, D08:5 — **39 sections total**, each the unit of one retrieval chunk. All 78 facts are mapped to a section.
- **Ambiguity risks addressed:** all eight from the fact-set summary, as controls AC1–AC8, plus a ninth (AC9) discovered during planning — see below.
- **Fact-set issue discovered:** one structural issue, not a content error — **F0807 naturally belongs to two sections** (the terminal state of the Hub factory-reset procedure, and the gating rule for device reuse). Rather than duplicate a policy fact across two chunks (which would create divergent retrieval units and risk double-counting), the plan states it once in D08 §4 with a forward reference from §3 (control AC9). No fact-set edit is required; the fact remains a single canonical entry. All other 77 facts map cleanly to exactly one section.
- **Next artifact:** `docs/benchmark/v0.1/language-rendering-plan.md` — fixes the per-language controlled terminology that §3 defines conceptually, the register decisions (DS6), the chunk-ID scheme (DP7), and the fact-ID-visibility decision (DP2). The three KB renderings follow, then `intent-set.md`.

---

*This document plan adds structure only; it introduces no policy content. The canonical fact-set remains the single source of truth. Version: kb-plan-v0.1.0, not yet frozen.*
