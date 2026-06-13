# NiceM Expected Fact Mapping v0.1

**Status:** Evaluator reference — the authoritative PASS/FAIL/UNCERTAIN decision guide for v0.1 benchmark runs
**Role:** Maps each of the 36 intents to required facts, PASS criteria, FAIL criteria, forbidden claims, UNCERTAIN conditions, and evaluator notes. This is what the human evaluator consults when auditing model outputs. The gate is blind to cost and trajectory data — the evaluator sees only the model output and this mapping.
**Version:** efm-v0.1.0 (not yet frozen)
**Depends on:** `intent-set.md` (intent-v0.1.0), `canonical-fact-set.md` (fs-v0.1.0), `evaluation-method-v0.1.md`, `success-rubric-v0.1.md`
**Feeds into:** Human audit, deterministic checker, `quality-gates.md`

---

## Global evaluation rules

These rules apply to every intent. Per-intent notes refine but do not override them.

**PASS** requires all of the following:
1. All required facts are present in the output, with correct meaning.
2. No forbidden claim appears.
3. No required condition is silently dropped (see Condition rule below).

**FAIL** requires any of the following:
- A required fact is absent, wrong, or materially distorted.
- A forbidden claim appears.
- A required ordered step is given in the wrong position (when order is essential — see Order rule).
- A required condition is dropped AND the dropped condition changes the answer materially.

**UNCERTAIN** applies when:
- The output is present but its correctness cannot be determined without domain expertise beyond what the fact-set provides (e.g., ambiguous phrasing).
- A partial answer omits some required facts but does not give wrong facts (see Partial rule below).
- The output language cannot be evaluated by the available reviewer (language-competence issue).
- The output is evasive or too general to classify.

**Condition rule:** For conditional intents, the PASS requires not only the correct conclusion but also that the relevant condition is acknowledged or implicit in the framing. A response that gives the right conclusion for the wrong reason (e.g., "you cannot return it" stated as a general rule when the intended claim is "you cannot return it *because it is damaged*") is UNCERTAIN, not PASS.

**Order rule:** For troubleshooting/process intents marked as ordered, steps must appear in the specified order. Giving all steps but in wrong order = FAIL if the correct order is causally essential (e.g., contact support before shipping). Giving all steps in substantially correct order with minor phrasing variation = PASS. Omitting a step entirely = FAIL if that step is in `required_fact_ids`; UNCERTAIN if it is only in `optional_context_fact_ids`.

**Partial answer rule (IS4 resolution):** A partial answer that omits one or more `required_fact_ids` but does not assert anything wrong defaults to UNCERTAIN, not FAIL — *except* where the omission itself constitutes a materially wrong implication (e.g., omitting the condition on a conditional rule implies the rule is unconditional). Per-intent notes specify which omissions are FAIL vs. UNCERTAIN.

**Extra information rule:** Correct extra information beyond the required facts is acceptable and does not reduce a PASS to a lower grade, *unless* it introduces a forbidden claim or creates a conflict with a required fact.

**Language-neutrality rule:** The evaluator judges whether the *meaning* expressed is correct, not whether the phrasing matches an English reference sentence. An output in any of the three languages is evaluated against the language-neutral `expected_outcome` and the fact-set.

---

## IS1–IS7 resolutions (pre-registered before any model run)

- **IS1 (AC4 coverage):** No dedicated AC4 intent exists in v0.1. AC4 (live view is not subscription-dependent) is covered only indirectly. This is a known coverage gap. Pre-registered: if a model response to INT-005 incorrectly states live view requires the subscription, the evaluator flags this as a secondary observation (not a FAIL for INT-005, which tests storage duration) and records it under `ac4_violation_observed` in the log. A dedicated AC4 intent is deferred to v0.2 (IS1).

- **IS2 (Sensor recalibration):** F0612 has no direct intent. Not addressed in v0.1.

- **IS3 (Liquid damage path):** F0708 has no direct intent. Not addressed in v0.1.

- **IS4 (Partial Sensor measurements, INT-003):** If the response gives 2 of 3 required measurements, the verdict is **UNCERTAIN** (partial, not wrong). If the response gives all 3 but adds a fabricated 4th (e.g., air quality), the verdict is **FAIL** (forbidden claim). If the response gives only 1, the verdict is **FAIL** (too incomplete to be useful; equivalent to a wrong answer in context).

- **IS5 (Step order):** For INT-025 (connectivity, 4 steps) and INT-026 (pairing, 3 steps), correct step order is required. Rationale: the steps are causally ordered — checking the Hub light must precede checking the cable; reaching "Add device" must precede pairing mode. Giving all steps out of order = **FAIL**. Giving all steps in correct order with minor phrasing variation = **PASS**.

- **IS6 (Refurbished warranty FAIL patterns, INT-019):** Three pre-registered FAIL patterns: (a) "you get a 90-day warranty" [flat reset]; (b) "you get a new 2-year warranty" [full reset]; (c) "refurbished devices have no warranty" [no warranty]. All three = FAIL. The correct answer must express the minimum-floor logic: "the longer of the remaining original warranty or 90 days."

- **IS7 (INT-035 delay vs. loss):** Giving both remedies correctly (delay → shipping-fee refund; loss → replacement) is **PASS** even though the scenario describes a delay. The key requirement is that the delay-specific remedy (shipping-fee refund) is correctly identified for the described scenario. Stating only the loss remedy (replacement) for a delay scenario = **FAIL**. Stating only the delay remedy (fee refund) without mentioning loss = **PASS** (minimal correct).

---

## Mapping entries

*Format per entry:*
```
intent_id | difficulty | required_chunks
required_fact_ids | optional_context_fact_ids
PASS criteria | FAIL criteria | UNCERTAIN conditions
forbidden_claims | evaluator_notes
```

---

### INT-001 — Warranty period for all devices

- **intent_id:** INT-001
- **difficulty_level:** simple
- **required_chunk_ids:** [D02-S1]
- **required_fact_ids:** [F0201]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Standard warranty is 2 years from date of purchase, applying to all devices.
- **PASS criteria:** Output states "2 years" AND "from purchase" (or equivalent temporal anchor). "All devices" scope need not be stated explicitly if not queried — inference acceptable.
- **FAIL criteria:** Any period other than 2 years stated as the warranty. "Delivery date" as the start anchor.
- **UNCERTAIN conditions:** Output says "up to 2 years" or "approximately 2 years" without commitment — flag for human.
- **forbidden_claims:** ["1 year", "lifetime", "varies by device", "30 days", "from delivery date"]
- **ambiguity_controls:** AC7 — the model should not confuse warranty (2 years) with return window (30 days).
- **evaluator_notes:** This is the simplest intent in the set. FAIL verdict here is a strong signal of either poor retrieval (Agent B) or poor grounding (Agent A). A response saying "30 days" = immediate FAIL; log separately as an AC7 violation.

---

### INT-002 — Return window duration

- **intent_id:** INT-002
- **difficulty_level:** simple
- **required_chunk_ids:** [D03-S1]
- **required_fact_ids:** [F0301]
- **optional_context_fact_ids:** [F0305]
- **expected_outcome_language_neutral:** Return window is 30 days from the date of purchase.
- **PASS criteria:** Output states "30 days" AND "from purchase." "From delivery" is FAIL.
- **FAIL criteria:** Any window other than 30 days. "From delivery date" as anchor. Stating "2 years" (confusing with warranty).
- **UNCERTAIN conditions:** Output says "about a month" without a precise number — UNCERTAIN.
- **forbidden_claims:** ["14 days", "60 days", "from delivery date", "2 years"]
- **ambiguity_controls:** AC7 (return vs. warranty); AC1 (30-day return vs. 30-day cloud storage — context must clearly be return).
- **evaluator_notes:** "From purchase" anchor is required, not optional — the policy specifically says purchase date. If a response says "from delivery," it is FAIL even if the day count is right.

---

### INT-003 — What NiceHome Sensor measures

- **intent_id:** INT-003
- **difficulty_level:** simple
- **required_chunk_ids:** [D01-S1]
- **required_fact_ids:** [F0102]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** The Sensor measures temperature, humidity, and motion — all three.
- **PASS criteria:** All three measurements present (temperature, humidity, motion). Any ordering acceptable. Extra correct context acceptable.
- **FAIL criteria:** Forbidden claim present (video recording, air quality). Only 1 measurement given (too incomplete — IS4 resolution: ≤1 = FAIL). Fabricated 4th capability added.
- **UNCERTAIN conditions:** Exactly 2 of 3 measurements given, none wrong (IS4 resolution: UNCERTAIN, not FAIL).
- **forbidden_claims:** ["records video", "measures air quality", "measures CO2", "measures noise"]
- **ambiguity_controls:** None specific.
- **evaluator_notes:** IS4 pre-registration applies here. Mark the specific missing measurement in the audit log. "Humidity" is the most commonly omitted in similar models; track per-language.

---

### INT-004 — Refund payment method

- **intent_id:** INT-004
- **difficulty_level:** simple
- **required_chunk_ids:** [D03-S4]
- **required_fact_ids:** [F0307]
- **optional_context_fact_ids:** [F0308]
- **expected_outcome_language_neutral:** Refund is issued to the original payment method.
- **PASS criteria:** "Original payment method" or equivalent (e.g., "the card/account used to purchase").
- **FAIL criteria:** "Store credit," "gift card," "any bank account of your choice."
- **UNCERTAIN conditions:** Response says "we will contact you to arrange the refund method" — UNCERTAIN (does not confirm the policy).
- **forbidden_claims:** ["store credit only", "cash refund", "any payment method of your choice"]
- **ambiguity_controls:** None.
- **evaluator_notes:** Simple lookup. Extra mention of F0308 (14-business-day processing time) is acceptable bonus.

---

### INT-005 — Cloud storage retention period

- **intent_id:** INT-005
- **difficulty_level:** simple
- **required_chunk_ids:** [D04-S2]
- **required_fact_ids:** [F0402]
- **optional_context_fact_ids:** [F0403]
- **expected_outcome_language_neutral:** Camera Plus Plan provides 30 days of cloud video storage for the Camera.
- **PASS criteria:** "30 days" of cloud storage for Camera video.
- **FAIL criteria:** "14 days" (trial length); "unlimited"; "7 days"; "applies to all devices."
- **UNCERTAIN conditions:** "About a month" without number — UNCERTAIN.
- **forbidden_claims:** ["unlimited cloud storage", "14-day storage", "applies to all NiceHome devices including Sensor"]
- **ambiguity_controls:** AC1 (30-day storage vs. 30-day return window — wording must make the storage context clear); AC3 (30-day storage vs. 14-day trial — wrong number = FAIL).
- **evaluator_notes:** IS1 note: if the response also incorrectly states that live view requires the subscription, record as `ac4_violation_observed = true` in the log, but do not change the INT-005 verdict unless that claim is the primary answer.

---

### INT-006 — Free trial length

- **intent_id:** INT-006
- **difficulty_level:** simple
- **required_chunk_ids:** [D04-S4]
- **required_fact_ids:** [F0405]
- **optional_context_fact_ids:** [F0406]
- **expected_outcome_language_neutral:** The Camera Plus Plan free trial lasts 14 days.
- **PASS criteria:** "14 days" stated for the trial.
- **FAIL criteria:** "30 days" (confusing trial with storage); "7 days"; "no trial available."
- **UNCERTAIN conditions:** "About two weeks" — UNCERTAIN (imprecise number).
- **forbidden_claims:** ["30-day trial", "7-day trial", "no trial available"]
- **ambiguity_controls:** AC3 (14-day trial vs. 30-day storage) — this is the dedicated AC3 test. "30 days" = FAIL, log as AC3 violation.
- **evaluator_notes:** AC3 violation logging: if the model says "30 days," that is both a FAIL on INT-006 and an AC3 violation — record both.

---

### INT-007 — Standard shipping timeframe

- **intent_id:** INT-007
- **difficulty_level:** simple
- **required_chunk_ids:** [D05-S1]
- **required_fact_ids:** [F0502]
- **optional_context_fact_ids:** [F0501]
- **expected_outcome_language_neutral:** Standard shipping takes 5 to 7 business days.
- **PASS criteria:** "5 to 7 business days" or equivalent range ("five to seven working days").
- **FAIL criteria:** "2 business days" (Express); "10 business days"; "5 to 7 calendar days" (missing "business").
- **UNCERTAIN conditions:** "5 to 7 days" without "business" qualifier — UNCERTAIN (calendar vs. business days ambiguity).
- **forbidden_claims:** ["same-day delivery", "2 business days", "10 business days"]
- **ambiguity_controls:** None directly; Standard vs. Express confusion is the key failure.
- **evaluator_notes:** "Business days" qualifier is required. "Working days" is acceptable as a synonym. Bare "days" = UNCERTAIN.

---

### INT-008 — Camera indoor/outdoor classification

- **intent_id:** INT-008
- **difficulty_level:** simple
- **required_chunk_ids:** [D01-S1]
- **required_fact_ids:** [F0104]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** The NiceHome Camera is an indoor camera; it is not designed for outdoor use.
- **PASS criteria:** States indoor only, or states not suitable for outdoor use.
- **FAIL criteria:** States outdoor use is supported; states "both indoor and outdoor."
- **UNCERTAIN conditions:** Says "we recommend indoor use" implying outdoor is possible but not ideal — UNCERTAIN.
- **forbidden_claims:** ["suitable for outdoor use", "waterproof", "outdoor-rated"]
- **ambiguity_controls:** None.
- **evaluator_notes:** "Recommend" framing is UNCERTAIN because it implies outdoor is an option. Hard "indoor camera" or "not designed for outdoor use" = PASS.

---

### INT-009 — Repair turnaround time

- **intent_id:** INT-009
- **difficulty_level:** simple
- **required_chunk_ids:** [D07-S5]
- **required_fact_ids:** [F0707]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Repair turnaround is typically 10 business days after the device is received.
- **PASS criteria:** "10 business days" + "after receipt" anchor. "Typically" or "approximately" qualifiers acceptable (they are in the fact).
- **FAIL criteria:** "14 business days" (confusing with refund processing); "10 calendar days"; "same day."
- **UNCERTAIN conditions:** "About 2 weeks" — UNCERTAIN (ambiguous: could mean 10 or 14 business days).
- **forbidden_claims:** ["same-day repair", "14 business days", "10 calendar days"]
- **ambiguity_controls:** None directly; repair (10 bdays) vs. refund processing (14 bdays) confusion is the key failure.
- **evaluator_notes:** "After receipt" anchor is required. If the response says "10 business days from when you request the repair," that is FAIL (wrong starting point).

---

### INT-010 — Camera Plus Plan name

- **intent_id:** INT-010
- **difficulty_level:** simple
- **required_chunk_ids:** [D04-S1]
- **required_fact_ids:** [F0401]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** NiceHome's cloud subscription is called the Camera Plus Plan.
- **PASS criteria:** "Camera Plus Plan" named as the cloud subscription.
- **FAIL criteria:** Any other plan name given. Stating no subscription exists.
- **UNCERTAIN conditions:** Response describes the plan's features but never names it — UNCERTAIN.
- **forbidden_claims:** ["NiceHome Cloud", "Camera Basic Plan", "NiceHome Plus", "there is no subscription"]
- **ambiguity_controls:** None.
- **evaluator_notes:** Plan name is a controlled term; exact match required (case-insensitive). Description without name = UNCERTAIN.

---

### INT-011 — Refund processing time

- **intent_id:** INT-011
- **difficulty_level:** simple
- **required_chunk_ids:** [D03-S4]
- **required_fact_ids:** [F0308]
- **optional_context_fact_ids:** [F0307]
- **expected_outcome_language_neutral:** Refunds are processed within 14 business days after the returned device is received.
- **PASS criteria:** "14 business days" AND "after receipt/device received."
- **FAIL criteria:** "10 business days" (confusing with repair); "14 calendar days"; "instantly."
- **UNCERTAIN conditions:** "About two weeks" — UNCERTAIN; "14 days" without "business" — UNCERTAIN.
- **forbidden_claims:** ["instant refund", "10 business days", "14 calendar days"]
- **ambiguity_controls:** None directly; refund processing (14 bdays) vs. repair turnaround (10 bdays) confusion.
- **evaluator_notes:** The "after receipt" anchor and "business days" qualifier are both required. Track the 10-vs-14 confusion rate — it is the key cross-document confound between D03 and D07.

---

### INT-012 — Plug remote switching without Hub

- **intent_id:** INT-012
- **difficulty_level:** simple
- **required_chunk_ids:** [D01-S2]
- **required_fact_ids:** [F0107]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Basic on/off switching works without a Hub. Automation features (scheduling, energy monitoring) require a Hub.
- **PASS criteria:** Both parts present: (1) on/off works without Hub AND (2) automation features require Hub.
- **FAIL criteria:** States Hub required for all functions (over-applying F0105/F0106 to the Plug). States the Plug works fully without a Hub.
- **UNCERTAIN conditions:** Only one of the two parts given — UNCERTAIN (partial answer on a two-part required fact).
- **forbidden_claims:** ["Hub required for all Plug functions", "the Plug is fully standalone", "energy monitoring works without a Hub"]
- **ambiguity_controls:** Tests the partial exception in F0107 vs. the general Hub-requirement rule.
- **evaluator_notes:** Both parts of F0107 are jointly required. Missing either = UNCERTAIN per the partial answer rule. Listing "scheduling and energy monitoring" explicitly is not required, but "automation features" or equivalent must be present.

---

### INT-013 — Gen 2 device with Gen 1 Hub

- **intent_id:** INT-013
- **difficulty_level:** conditional
- **required_chunk_ids:** [D01-S3]
- **required_fact_ids:** [F0108]
- **optional_context_fact_ids:** [F0109]
- **expected_outcome_language_neutral:** A Gen 2 device CANNOT be used with a Gen 1 Hub. A Gen 2 Hub is required.
- **PASS criteria:** States incompatibility (Gen 1 Hub does not support Gen 2 devices). May additionally note Gen 2 Hub supports both.
- **FAIL criteria:** States Gen 1 Hub supports Gen 2 devices. States all Hubs support all devices. States Gen 2 is backward compatible (reversing the direction).
- **UNCERTAIN conditions:** Says "compatibility depends on the model" without specifying the rule — UNCERTAIN.
- **forbidden_claims:** ["Gen 1 Hub supports Gen 2 devices", "all NiceHome Hubs are compatible with all devices"]
- **ambiguity_controls:** Asymmetric compatibility test — the backward-compatibility fact (F0109) runs in the Gen 2 Hub → Gen 1 devices direction, not the other way. Reversing the direction = FAIL.
- **evaluator_notes:** The condition in the query is Gen 1 Hub + Gen 2 device → incompatible. A response that only says "Gen 2 Hub supports both" without addressing the Gen 1 Hub situation = UNCERTAIN (it does not answer the question asked).

---

### INT-014 — Opened device return: who pays shipping

- **intent_id:** INT-014
- **difficulty_level:** conditional
- **required_chunk_ids:** [D03-S2]
- **required_fact_ids:** [F0303]
- **optional_context_fact_ids:** [F0302]
- **expected_outcome_language_neutral:** Return accepted; full refund given; customer pays return shipping.
- **PASS criteria:** All three present: (1) return accepted, (2) full refund, (3) customer pays return shipping.
- **FAIL criteria:** "Free return shipping for opened devices" (applying F0302 instead of F0303). "Partial refund for opened devices."
- **UNCERTAIN conditions:** States return accepted + full refund but does not mention who pays shipping — UNCERTAIN (the shipping-cost distinction is the point of the intent).
- **forbidden_claims:** ["free return shipping", "restocking fee applies", "partial refund for opened devices", "opened devices cannot be returned"]
- **ambiguity_controls:** The distinction between F0302 (unopened → free return shipping) and F0303 (opened → customer pays) is the core test. Swapping the shipping rule = FAIL.
- **evaluator_notes:** "Full refund" AND "customer pays shipping" must both be present for PASS. One missing = UNCERTAIN. Confusing with F0302 = FAIL.

---

### INT-015 — Warranty coverage: accidental damage

- **intent_id:** INT-015
- **difficulty_level:** conditional
- **required_chunk_ids:** [D02-S3]
- **required_fact_ids:** [F0203]
- **optional_context_fact_ids:** [F0202, F0708]
- **expected_outcome_language_neutral:** Accidental damage is NOT covered by the warranty.
- **PASS criteria:** States accidental damage is excluded from warranty coverage. May mention out-of-warranty service option as extra context.
- **FAIL criteria:** States accidental damage is covered. States dropping counts as a manufacturing defect.
- **UNCERTAIN conditions:** Says "it depends on how it happened" without committing to the exclusion — UNCERTAIN.
- **forbidden_claims:** ["accidental damage is covered", "dropped devices are covered under manufacturing defect"]
- **ambiguity_controls:** Rule (F0202, coverage) + exception (F0203, accidental exclusion) pattern. Applying the rule without the exception = FAIL.
- **evaluator_notes:** The condition rule applies: the exclusion condition must be acknowledged (accidental = excluded), not just "it's not covered" as a general statement. If the response says "not covered" without identifying why (the accidental damage condition), that is UNCERTAIN per the condition rule.

---

### INT-016 — Warranty coverage: unauthorized modification

- **intent_id:** INT-016
- **difficulty_level:** conditional
- **required_chunk_ids:** [D02-S3]
- **required_fact_ids:** [F0204]
- **optional_context_fact_ids:** [F0202]
- **expected_outcome_language_neutral:** Unauthorized modification voids warranty coverage for the resulting damage.
- **PASS criteria:** States modification/unauthorized changes void/exclude warranty for resulting damage.
- **FAIL criteria:** States warranty still applies despite modification.
- **UNCERTAIN conditions:** "It depends on what was modified" — UNCERTAIN (the policy does not distinguish by type of modification).
- **forbidden_claims:** ["modification does not affect warranty", "warranty covers all defects even after modification"]
- **ambiguity_controls:** Rule + exception pattern (F0202 + F0204). Same structure as INT-015.
- **evaluator_notes:** The condition (unauthorized modification) must be reflected in the answer. "Not covered" without naming the modification condition = UNCERTAIN per condition rule.

---

### INT-017 — Subscription cancellation: access and refund

- **intent_id:** INT-017
- **difficulty_level:** conditional
- **required_chunk_ids:** [D04-S5]
- **required_fact_ids:** [F0407, F0408]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** (1) Cloud storage access continues to end of current billing period. (2) No pro-rated refund.
- **PASS criteria:** Both facts present: access continues to period end + no partial refund.
- **FAIL criteria:** "Access ends immediately." "A partial/pro-rated refund is issued." Either part stated incorrectly.
- **UNCERTAIN conditions:** Only one of the two facts present — UNCERTAIN (this is a two-part required answer per the partial answer rule).
- **forbidden_claims:** ["access ends immediately on cancellation", "pro-rated refund available", "cancellation deletes cloud video immediately"]
- **ambiguity_controls:** Both sub-facts of this intent are required. The cancellation-does-not-delete-video fact (F0809) is a background note but not required for PASS here.
- **evaluator_notes:** Both parts required jointly. Missing either = UNCERTAIN. Both wrong = FAIL.

---

### INT-018 — Out-of-warranty repair: cost and shipping

- **intent_id:** INT-018
- **difficulty_level:** conditional
- **required_chunk_ids:** [D07-S2]
- **required_fact_ids:** [F0702, F0706]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Out-of-warranty repair is available for a service fee; customer pays shipping in both directions.
- **PASS criteria:** Both facts present: (1) service fee applies AND (2) customer pays two-way shipping.
- **FAIL criteria:** "Out-of-warranty repair is free." "NiceHome pays return shipping." "Out-of-warranty devices cannot be repaired."
- **UNCERTAIN conditions:** Mentions service fee but omits shipping — UNCERTAIN (shipping cost is required given the query asks "what would I need to pay?").
- **forbidden_claims:** ["free out-of-warranty repair", "NiceHome covers shipping for out-of-warranty repairs", "out-of-warranty devices cannot be repaired"]
- **ambiguity_controls:** Contrasts with in-warranty (F0701: free + prepaid label); both cost and shipping direction differ.
- **evaluator_notes:** "Two-way shipping" or "shipping both ways" or "you pay shipping both to and from" all acceptable. "You pay return shipping" (one-way only) = UNCERTAIN.

---

### INT-019 — Refurbished replacement warranty

- **intent_id:** INT-019
- **difficulty_level:** conditional
- **required_chunk_ids:** [D07-S3]
- **required_fact_ids:** [F0705]
- **optional_context_fact_ids:** [F0704]
- **expected_outcome_language_neutral:** Refurbished replacement carries the remainder of the original warranty, with a minimum floor of 90 days — whichever is longer.
- **PASS criteria:** Response expresses the minimum-floor logic: the longer of (remaining original warranty) and (90 days). Phrasing variants acceptable as long as the floor concept is present.
- **FAIL criteria:** IS6 pre-registered FAIL patterns: (a) "you get a 90-day warranty" [flat reset — no mention of remaining original]; (b) "you get a new 2-year warranty" [full reset]; (c) "refurbished replacements have no warranty." All three = FAIL.
- **UNCERTAIN conditions:** Response says "90 days minimum" without clarifying whether original warranty time can be longer — UNCERTAIN (omits the "longer of" logic).
- **forbidden_claims:** ["no warranty on refurbished devices", "warranty resets to 2 years", "exactly 90 days regardless of original warranty"]
- **ambiguity_controls:** AC8 — the primary AC8 test in the benchmark.
- **evaluator_notes:** This is the most failure-prone simple/conditional fact in the set. Evaluator must check for the three IS6 FAIL patterns explicitly. "90 days minimum with remaining original warranty if longer" = PASS. "90 days minimum" alone = UNCERTAIN.

---

### INT-020 — Order cancellation after 2-hour window

- **intent_id:** INT-020
- **difficulty_level:** conditional
- **required_chunk_ids:** [D05-S3]
- **required_fact_ids:** [F0506]
- **optional_context_fact_ids:** [F0505]
- **expected_outcome_language_neutral:** Cancellation is no longer possible. Return after delivery under the return policy remains an option.
- **PASS criteria:** Both facts: (1) cancellation not possible after 2 hours AND (2) post-delivery return remains available.
- **FAIL criteria:** "The order can still be cancelled." "No recourse exists after 2 hours."
- **UNCERTAIN conditions:** States cancellation not possible but does not mention the return option — UNCERTAIN (the partial answer rule: missing the return option omits a required component).
- **forbidden_claims:** ["cancellation available until it ships", "no recourse after 2 hours", "you can cancel by calling support"]
- **ambiguity_controls:** Time-condition test: the 4-hour framing in the scenario makes the post-window condition unambiguous.
- **evaluator_notes:** Both components required for PASS. The return-option mention is specifically required because F0506 explicitly includes it — omitting it = UNCERTAIN. "No recourse" = FAIL.

---

### INT-021 — Express shipping eligibility: backordered item

- **intent_id:** INT-021
- **difficulty_level:** conditional
- **required_chunk_ids:** [D05-S2]
- **required_fact_ids:** [F0504]
- **optional_context_fact_ids:** [F0503]
- **expected_outcome_language_neutral:** Express shipping is NOT available for backordered/out-of-stock items.
- **PASS criteria:** States Express unavailable for out-of-stock/backordered items.
- **FAIL criteria:** States Express is available. States "Express is available if in stock" without applying the condition to the scenario (i.e., does not conclude "therefore unavailable here").
- **UNCERTAIN conditions:** Gives the general rule ("Express requires in stock") without applying it to the scenario — UNCERTAIN per condition rule (general rule without conclusion about the specific case).
- **forbidden_claims:** ["Express available for backordered items", "you can choose Express regardless of stock"]
- **ambiguity_controls:** Condition application test: the evaluator checks that the response applies the in-stock condition to the described backordered scenario and concludes "unavailable."
- **evaluator_notes:** Condition rule is strict here. Stating the general rule but not applying it to the given scenario = UNCERTAIN, not PASS.

---

### INT-022 — Subscription refund via returns process

- **intent_id:** INT-022
- **difficulty_level:** conditional
- **required_chunk_ids:** [D03-S3]
- **required_fact_ids:** [F0306]
- **optional_context_fact_ids:** [F0408]
- **expected_outcome_language_neutral:** Subscription plans are NOT refundable through the device return process. Subscription cancellation is a separate process.
- **PASS criteria:** States subscriptions excluded from device returns; mentions cancellation as separate.
- **FAIL criteria:** States subscription can be returned/refunded via the return process.
- **UNCERTAIN conditions:** States subscription is excluded but does not mention any alternative path — UNCERTAIN (leaving the user with no direction).
- **forbidden_claims:** ["subscriptions can be returned like hardware", "subscription refund via return form"]
- **ambiguity_controls:** Cross-document: D03 exclusion + D04 cancellation.
- **evaluator_notes:** Mentioning cancellation as the correct alternative path is required for PASS (F0306 explicitly states "handled separately"). Exclusion-only without mentioning cancellation = UNCERTAIN.

---

### INT-023 — Customer-damaged device: return not eligible

- **intent_id:** INT-023
- **difficulty_level:** conditional
- **required_chunk_ids:** [D03-S3]
- **required_fact_ids:** [F0304]
- **optional_context_fact_ids:** [F0203]
- **expected_outcome_language_neutral:** Customer-caused damage disqualifies a device from the return/refund policy.
- **PASS criteria:** States customer-damaged devices are not eligible for a return refund.
- **FAIL criteria:** States damage does not affect return eligibility. States all returns are accepted regardless of condition.
- **UNCERTAIN conditions:** Says "it depends on how it was damaged" without identifying the customer-caused condition — UNCERTAIN.
- **forbidden_claims:** ["all returns accepted regardless of condition", "cracked screen is a manufacturing defect"]
- **ambiguity_controls:** Rule + exception: F0302/F0303 (returns generally accepted) + F0304 (customer damage excluded).
- **evaluator_notes:** The condition (customer-caused) must be identified. Condition rule: "not eligible for return" without attributing it to customer-caused damage = UNCERTAIN.

---

### INT-024 — Subscription plan change timing

- **intent_id:** INT-024
- **difficulty_level:** conditional
- **required_chunk_ids:** [D04-S5]
- **required_fact_ids:** [F0409]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Plan changes (upgrade or downgrade) take effect at the start of the next billing period.
- **PASS criteria:** "Next billing period" stated for plan changes. Both upgrade and downgrade treated the same.
- **FAIL criteria:** "Changes take effect immediately." Distinguishing upgrade (immediate) from downgrade (deferred) — the policy does not make this distinction.
- **UNCERTAIN conditions:** "Changes are processed within a few days" — UNCERTAIN (does not confirm next-period timing).
- **forbidden_claims:** ["upgrades are immediate", "downgrades are immediate", "changes take effect within 24 hours"]
- **ambiguity_controls:** None specific; tests the next-billing-period condition.
- **evaluator_notes:** The policy treats upgrade and downgrade identically. A response that correctly says "next billing period" but adds "unless it's an upgrade" = FAIL (inventing a distinction).

---

### INT-025 — Hub connectivity: full diagnostic sequence

- **intent_id:** INT-025
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D06-S1]
- **required_fact_ids:** [F0601, F0602, F0603, F0604]
- **optional_context_fact_ids:** [F0605]
- **expected_outcome_language_neutral:** Four ordered steps: (1) check Hub power light; (2) if off, check cable/outlet; (3) if on but offline, restart Hub; (4) if still offline, check network/router.
- **PASS criteria:** All four steps present in correct causal order. Step 3 must be "restart" not "factory reset." Minor wording variation acceptable.
- **FAIL criteria:** Step 3 = "factory reset" instead of restart (AC5 violation). Steps given in incorrect causal order (IS5 resolution). Any required step absent.
- **UNCERTAIN conditions:** Three of four steps present, one omitted — UNCERTAIN per partial rule. All four present but order unclear from response structure — UNCERTAIN.
- **forbidden_claims:** ["factory reset the Hub as the first step", "replace the Hub if it won't connect"]
- **ambiguity_controls:** AC5 (restart vs. factory reset) — step 3 is restart, not factory reset. This is the primary AC5 test for the restart operation.
- **evaluator_notes:** IS5 applies: exact causal order required. Checking the cable (step 2) before the light (step 1) = FAIL. Restarting (step 3) before checking the light (step 1) = FAIL. "Factory reset" at any step = FAIL + AC5 violation logged.

---

### INT-026 — Device pairing: full sequence

- **intent_id:** INT-026
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D06-S3]
- **required_fact_ids:** [F0606, F0607, F0608]
- **optional_context_fact_ids:** [F0609]
- **expected_outcome_language_neutral:** Three ordered steps: (1) open app → "Add device"; (2) hold setup button 5 seconds; (3) follow app prompts.
- **PASS criteria:** All three steps in correct order. Step 2 specifically states 5 seconds. Minor wording variation acceptable.
- **FAIL criteria:** "10 seconds" in step 2 (AC2 violation). Steps out of causal order. Any step absent.
- **UNCERTAIN conditions:** Two of three steps present — UNCERTAIN. "Hold the button" without duration — UNCERTAIN.
- **forbidden_claims:** ["hold the button for 10 seconds", "pairing completes automatically without following app prompts"]
- **ambiguity_controls:** AC2 (5-second pairing vs. 10-second factory reset) — primary AC2 test. "10 seconds" = FAIL + AC2 violation logged.
- **evaluator_notes:** IS5 applies: "Add device" must precede pairing mode. "5 seconds" is required precisely. Track 5-vs-10 confusion rate per language.

---

### INT-027 — Pairing fails: range check

- **intent_id:** INT-027
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D06-S3]
- **required_fact_ids:** [F0609]
- **optional_context_fact_ids:** [F0606, F0607, F0608]
- **expected_outcome_language_neutral:** On pairing failure, check that the device is within Hub range.
- **PASS criteria:** States "within range of the Hub" or equivalent as the first-response diagnostic action.
- **FAIL criteria:** "Device is defective — replace it." "Factory reset the device immediately." "Contact support as the first step."
- **UNCERTAIN conditions:** Response says "retry the pairing process" without mentioning range — UNCERTAIN (not wrong but incomplete).
- **forbidden_claims:** ["pairing failure always indicates a defective device", "factory reset on first failure"]
- **ambiguity_controls:** None specific; tests escalation routing (F0609 before factory reset or replacement).
- **evaluator_notes:** The range check is the specific prescribed action for pairing failure. Escalation to support (F0613) is a fallback, not a first step.

---

### INT-028 — Warranty claim: full process

- **intent_id:** INT-028
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D02-S4]
- **required_fact_ids:** [F0205, F0206, F0207, F0208]
- **optional_context_fact_ids:** [F0209]
- **expected_outcome_language_neutral:** Four required elements: (1) have proof of purchase; (2) contact support with serial number; (3) receive claim reference and prepaid label; (4) ship device with prepaid label and claim reference.
- **PASS criteria:** All four elements present. Prepaid label present (signals no cost to customer for shipping). Proof of purchase mentioned.
- **FAIL criteria:** "Customer pays for shipping to send the device in" (prepaid label absent). "No proof of purchase required." Steps given in wrong causal order (contact after shipping).
- **UNCERTAIN conditions:** Three of four elements present — UNCERTAIN. Mentions "send device back" without prepaid label or claim reference — UNCERTAIN.
- **forbidden_claims:** ["ship the device without contacting support first", "customer pays warranty shipping", "no proof of purchase needed"]
- **ambiguity_controls:** Prepaid label (in-warranty, free) vs. customer-pays (out-of-warranty, F0706). "Customer pays" = FAIL + flag as warranty-vs-repair shipping confusion.
- **evaluator_notes:** All four elements are causally ordered and all required. Prepaid label is the clearest indicator of correct retrieval — its absence usually means the model retrieved only a summary, not D02-S4 in full.

---

### INT-029 — Return process: step sequence

- **intent_id:** INT-029
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D03-S5]
- **required_fact_ids:** [F0309, F0310, F0311]
- **optional_context_fact_ids:** [F0302]
- **expected_outcome_language_neutral:** Three ordered steps: (1) request return authorization from support; (2) receive RA number and shipping instructions; (3) ship device with RA number.
- **PASS criteria:** All three steps in order. RA number mentioned in step 3. May additionally state full refund + free shipping given the unopened scenario.
- **FAIL criteria:** "Ship device without authorization." No mention of RA number. Steps out of order.
- **UNCERTAIN conditions:** Two of three steps — UNCERTAIN. "Contact support and send back the device" without RA number — UNCERTAIN.
- **forbidden_claims:** ["ship the device back without any authorization", "no authorization number needed"]
- **ambiguity_controls:** Return authorization (D03) is a distinct identifier from the warranty claim reference (D02) — evaluator checks no confusion.
- **evaluator_notes:** RA number in step 3 is specifically required (it is in the fact). Omitting it = UNCERTAIN. Authorization-without-RA-number = UNCERTAIN.

---

### INT-030 — Password recovery: full sequence

- **intent_id:** INT-030
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D08-S1]
- **required_fact_ids:** [F0801, F0802, F0803]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Three ordered steps: (1) select "Forgot password"; (2) enter email to receive reset link; (3) follow link to set new password.
- **PASS criteria:** All three steps in order. Email-based reset link mechanism present.
- **FAIL criteria:** "Reset code sent by SMS/phone." "Old password emailed back." Steps out of order.
- **UNCERTAIN conditions:** Two of three steps — UNCERTAIN. "We will send you instructions" without specifying email link — UNCERTAIN.
- **forbidden_claims:** ["SMS reset code", "old password can be retrieved", "call support to reset password"]
- **ambiguity_controls:** None specific.
- **evaluator_notes:** Email-link mechanism is required, not a phone code. Any SMS/phone-code reference = FAIL.

---

### INT-031 — Hub factory reset: procedure and next step

- **intent_id:** INT-031
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D08-S3, D08-S4]
- **required_fact_ids:** [F0806, F0807]
- **optional_context_fact_ids:** [F0805, F0809]
- **expected_outcome_language_neutral:** (1) Hold reset button 10 seconds; (2) wait for blink confirmation; (3) device must be re-paired via app after reset.
- **PASS criteria:** "10 seconds" present; re-pair requirement present. Both chunks (D08-S3 and D08-S4) effectively addressed.
- **FAIL criteria:** "5 seconds" (AC2 violation). "Device works immediately after reset without re-pairing." "10 seconds" correct but re-pair absent = FAIL (required component missing, not partial — because re-pairing is the essential next step the query asks about).
- **UNCERTAIN conditions:** "Hold until the light changes" without specifying 10 seconds — UNCERTAIN (duration not confirmed).
- **forbidden_claims:** ["hold for 5 seconds", "no re-pairing needed after factory reset", "factory reset deletes cloud video"]
- **ambiguity_controls:** AC2 (10-second factory reset vs. 5-second pairing) — primary 10-second AC2 test. AC9 (F0807 single-source / forward reference — D08-S3 references S4).
- **evaluator_notes:** IS9 note: this intent spans two chunks (D08-S3 and D08-S4). For Agent B, track whether both chunks are retrieved (semantic_units_retrieved should include F0806 and F0807 fact IDs). Single-chunk retrieval of S3 only misses F0807 in its policy role — log retrieval gap separately. "5 seconds" = FAIL + AC2 violation logged.

---

### INT-032 — What factory reset does and does not delete

- **intent_id:** INT-032
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D08-S2, D08-S4]
- **required_fact_ids:** [F0805, F0809]
- **optional_context_fact_ids:** [F0804]
- **expected_outcome_language_neutral:** Factory reset erases device settings and unlinks from account (F0805). Cloud-stored video is NOT deleted — it is subscription-managed (F0809).
- **PASS criteria:** Both facts present: (1) settings + account link erased AND (2) cloud video not deleted.
- **FAIL criteria:** "Factory reset deletes cloud video." States settings are kept (confusing with soft reset). Either required fact absent = FAIL (not UNCERTAIN) because each is a self-contained required answer to the query.
- **UNCERTAIN conditions:** Only mentions settings erasure without addressing cloud video — UNCERTAIN (the specific user concern in the scenario is cloud video).
- **forbidden_claims:** ["factory reset deletes cloud video", "settings are kept after factory reset", "account link is not affected"]
- **ambiguity_controls:** AC5 (factory reset vs. soft reset — F0804 is context only; the question asks about factory reset) and AC9 (F0809 cloud carve-out).
- **evaluator_notes:** The UNCERTAIN case for cloud video is important: the scenario specifically frames user concern about cloud recordings. Addressing settings without cloud video = UNCERTAIN, not PASS. "Factory reset deletes cloud video" = FAIL + log as AC9 violation.

---

### INT-033 — Unresponsive Plug: step sequence

- **intent_id:** INT-033
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D06-S4]
- **required_fact_ids:** [F0610, F0611]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Two ordered steps: (1) toggle off/on in the app; (2) if still unresponsive, soft reset.
- **PASS criteria:** Both steps in order; step 2 specifically "soft reset" (not factory reset).
- **FAIL criteria:** "Factory reset as first or second step" (AC5 violation). Steps reversed (soft reset before app toggle). Either step absent.
- **UNCERTAIN conditions:** Only one step given — UNCERTAIN. "Soft reset or factory reset" given as alternatives — UNCERTAIN (the policy specifies soft reset only at this stage).
- **forbidden_claims:** ["factory reset the Plug immediately", "perform a soft reset first before the app toggle"]
- **ambiguity_controls:** AC5 (soft reset vs. factory reset) — step 2 is soft reset, not factory reset. "Factory reset" at step 2 = FAIL + AC5 violation.
- **evaluator_notes:** Causal order required (IS5). App toggle first because it is the least destructive action. "Factory reset" anywhere in the primary recommendation = FAIL.

---

### INT-034 — Hub blinking red: meaning and next step

- **intent_id:** INT-034
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D06-S2]
- **required_fact_ids:** [F0605]
- **optional_context_fact_ids:** [F0603, F0604]
- **expected_outcome_language_neutral:** Blinking red = Hub lost network connection. Next step: check network/router (or restart Hub per D06-S1 sequence).
- **PASS criteria:** Correct indicator meaning (lost network connection). Network/router check or Hub restart as next step.
- **FAIL criteria:** "Blinking red = hardware failure." "Blinking red = Hub is updating." "Replace the Hub immediately."
- **UNCERTAIN conditions:** Identifies network issue but gives no actionable next step — UNCERTAIN. "Blinking red = connection problem" without specifying lost network — UNCERTAIN (slightly imprecise but not wrong; flag for human).
- **forbidden_claims:** ["blinking red indicates hardware failure", "blinking red means the Hub is updating", "replace the Hub when it blinks red"]
- **ambiguity_controls:** Indicator-state test: blinking red is specifically defined in F0605; any other interpretation = FAIL.
- **evaluator_notes:** This intent tests single-indicator retrieval (D06-S2) but a good response may additionally draw from D06-S1 (connectivity steps). The connectivity step pull is optional_context — its presence improves quality but absence does not reduce PASS to UNCERTAIN.

---

### INT-035 — Delayed shipment vs. lost shipment: which remedy applies

- **intent_id:** INT-035
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D05-S4]
- **required_fact_ids:** [F0507, F0508]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Delay scenario → shipping-fee refund on request. If lost → free replacement (contextual).
- **PASS criteria:** IS7 resolution: (1) delay remedy (shipping-fee refund) identified for the delay scenario AND (2) optionally, loss remedy (replacement) mentioned correctly. Minimal PASS = delay → shipping-fee refund correctly identified.
- **FAIL criteria:** Applying loss remedy (replacement) to the delay scenario. "Full product refund for a delayed shipment." Merging delay and loss into one undifferentiated remedy.
- **UNCERTAIN conditions:** States "you may be entitled to a refund or replacement" without distinguishing which applies to the delay — UNCERTAIN (IS7: must identify which remedy applies to the scenario).
- **forbidden_claims:** ["delayed shipment gets a full product refund", "delay and loss both result in a replacement"]
- **ambiguity_controls:** AC6 (delay fee refund vs. loss replacement) — the primary AC6 test.
- **evaluator_notes:** IS7 resolution: correctly identifying the delay remedy is required. Mentioning loss → replacement as additional context = PASS if delay remedy is correct. Saying "replacement" for a delay = FAIL + AC6 violation logged.

---

### INT-036 — Lost device: remote account removal

- **intent_id:** INT-036
- **difficulty_level:** troubleshooting-process
- **required_chunk_ids:** [D08-S5]
- **required_fact_ids:** [F0808]
- **optional_context_fact_ids:** []
- **expected_outcome_language_neutral:** Lost device can be removed from the account remotely via the app.
- **PASS criteria:** "Remote removal via app" stated. "Account" removal implied or explicit.
- **FAIL criteria:** "Physical access required." "Contact support — only support can remove it."
- **UNCERTAIN conditions:** "Contact support and they can help you" without specifying remote removal — UNCERTAIN (may be correct but doesn't confirm F0808).
- **forbidden_claims:** ["physical access required to remove the device", "the device cannot be removed remotely"]
- **ambiguity_controls:** None.
- **evaluator_notes:** "Via the app" is the specific mechanism; "contact support" as the only option = UNCERTAIN (support may help, but the app-based remote removal is the defined capability).

---

## Summary tables

### PASS/FAIL/UNCERTAIN operationalization

| Rule | Decision |
|---|---|
| All required facts present, no forbidden claims | PASS |
| Required fact absent or wrong | FAIL (unless partial rule applies) |
| Required ordered step in wrong position (causally essential) | FAIL |
| Required step absent | FAIL if in required_fact_ids; UNCERTAIN if in optional_context_fact_ids |
| Partial answer: some required facts missing, nothing wrong | UNCERTAIN (IS4) |
| Condition omitted from a conditional answer | UNCERTAIN per condition rule; FAIL if omission implies unconditional |
| Forbidden claim present | FAIL |
| General rule stated but not applied to scenario | UNCERTAIN per condition rule |
| Extra correct info beyond required | PASS (unchanged) |
| Extra info introducing a forbidden claim | FAIL |

### Intents requiring multiple required facts

| Count of required_fact_ids | Intent IDs |
|---|---|
| 4 | INT-025, INT-026, INT-028, INT-029 |
| 3 | INT-003, INT-030 |
| 2 | INT-012, INT-013†, INT-014, INT-017, INT-018, INT-019†, INT-020, INT-022†, INT-024†, INT-031, INT-032, INT-033, INT-035 |
| 1 | INT-001, INT-002, INT-004, INT-005, INT-006, INT-007, INT-008, INT-009, INT-010, INT-011, INT-015†, INT-016†, INT-021, INT-023, INT-027, INT-034, INT-036 |

† = single required_fact_id but the fact itself has an internal two-part structure (e.g., F0107 requires both parts; F0705 requires the floor logic).

### Intents requiring ordered steps

INT-025 (4 steps), INT-026 (3 steps), INT-028 (4 elements in order), INT-029 (3 steps), INT-030 (3 steps), INT-031 (2 steps + next), INT-033 (2 steps) = **7 intents** with IS5 causal-order requirement.

### Ambiguity control direct tests

| AC | Primary test intents |
|---|---|
| AC1 | INT-002 (return window) + INT-005 (storage) as discriminating pair |
| AC2 | INT-026 (5 seconds) + INT-031 (10 seconds) as discriminating pair |
| AC3 | INT-006 (14-day trial) + INT-005 (30-day storage) as discriminating pair |
| AC4 | No direct test — IS1 gap; indirect observation via INT-005 log |
| AC5 | INT-025 (restart), INT-033 (soft reset), INT-031/INT-032 (factory reset) |
| AC6 | INT-035 (delay vs. loss distinction) |
| AC7 | INT-001 (2-year warranty) + INT-002 (30-day return) as discriminating pair |
| AC8 | INT-019 (refurbished warranty floor, IS6 FAIL patterns) |
| AC9 | INT-031 + INT-032 (span D08-S3 and D08-S4) |

---

## Remaining evaluator risks

1. **AC4 gap (IS1):** No direct intent tests whether the model incorrectly ties live view to the subscription. Only logged as a secondary observation if it appears in INT-005 outputs. This remains the weakest coverage point in v0.1.
2. **UNCERTAIN rate:** If more than 25% of any condition group (language × agent) produces UNCERTAIN verdicts, the evaluation rubric may need recalibration before interpretation (per `falsification-and-decision-rules-v0.1.md` recalibration gate).
3. **Condition rule edge cases:** The condition rule (UNCERTAIN if condition is present but not attributed) requires human judgment. The automated deterministic checker cannot reliably apply it; human audit is required for all conditional intents (INT-013–INT-024).
4. **Cross-language evaluation parity:** The evaluator must judge meaning, not phrasing. Dutch and Turkish outputs should be evaluated against the language-neutral expected outcome, not against a hidden English reference. For the Turkish outputs, the project owner (native speaker) applies the same rubric.
5. **INT-019 (AC8) evaluator attention:** The refurbished warranty floor is the most likely single fact to generate all three FAIL patterns. The evaluator should check INT-019 outputs first in each batch to calibrate before reviewing similar intents.

---

*This mapping is the canonical evaluator reference. It is language-neutral: outputs in English, Dutch, and Turkish are all evaluated against the `expected_outcome_language_neutral` entries here. Version: efm-v0.1.0, not yet frozen.*
