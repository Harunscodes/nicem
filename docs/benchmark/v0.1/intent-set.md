# NiceM Intent Set v0.1

**Status:** 36 language-neutral intent specifications — the evaluation targets for the v0.1 benchmark
**Role:** Defines what the benchmark asks. Each intent is a language-neutral specification; the English, Dutch, and Turkish query renderings are authored separately from this file. Every intent maps to fact IDs, required_facts, expected_outcome, and forbidden_claims so that evaluation is deterministic.
**Version:** intent-v0.1.0 (not yet frozen)
**Depends on:** `canonical-fact-set.md` (fs-v0.1.0), `document-plan.md` (kb-plan-v0.1.0), `dataset-specification.md`
**Feeds into:** `expected-fact-mapping.md` (the evaluator's reference), `intent-set-rendering.md` (future: EN/NL/TR query text)

**Total intents:** 36
**Distribution:** 12 simple factual (INT-001–012) / 12 conditional policy (INT-013–024) / 12 troubleshooting/process (INT-025–036)

**Methodological note:** These intents define evaluation targets; they say nothing about execution-tax. Execution-tax is the hypothesis under test when agents run against the KB renderings to answer these intents. The intents themselves are language-neutral structured specifications.

---

## Simple factual intents (INT-001–INT-012)

*Simple factual intents require one or at most two facts, no branching conditions, and a direct factual lookup. They are designed to produce clean PASS/FAIL signals with minimal ambiguity.*

---

## INT-001 — Warranty period for all devices

- **intent_id:** INT-001
- **task_category:** warranty_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D02]
- **linked_chunk_ids:** [D02-S1]
- **linked_fact_ids:** [F0201]
- **required_facts:** [F0201]
- **user_scenario_language_neutral:** A user asks how long the standard warranty is for a NiceHome device.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states the standard warranty is 2 years from the date of purchase, applying to all NiceHome devices.
- **forbidden_claims:** ["warranty is 1 year", "warranty is lifetime", "warranty varies by device"]
- **likely_failure_modes:** Hallucinating a different warranty period; confusing warranty with return window (30 days).
- **ambiguity_controls:** AC7 (warranty period vs. return window) — wrong answer here is 30 days.
- **evaluation_notes:** Binary: 2 years from purchase = PASS. Any other period = FAIL. "From purchase date" is required (not delivery date).
- **rendering_notes:** Straightforward lookup. Query should ask for the warranty period without specifying a device type, to verify the "all devices" scope.

---

## INT-002 — Return window duration

- **intent_id:** INT-002
- **task_category:** return_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D03]
- **linked_chunk_ids:** [D03-S1]
- **linked_fact_ids:** [F0301]
- **required_facts:** [F0301]
- **user_scenario_language_neutral:** A user asks how many days they have to return a NiceHome device.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states the return window is 30 days from the date of purchase.
- **forbidden_claims:** ["14 days", "60 days", "window starts from delivery date", "return window is 2 years"]
- **likely_failure_modes:** Confusing return window with warranty period (2 years); stating delivery date instead of purchase date.
- **ambiguity_controls:** AC7 (return window vs. warranty) — wrong answer here is 2 years; AC1 (return window vs. cloud storage, both "30 days") — context must be return, not storage.
- **evaluation_notes:** Binary: 30 days from purchase = PASS.
- **rendering_notes:** Query should ask plainly for the return window without device condition details.

---

## INT-003 — What NiceHome Sensor measures

- **intent_id:** INT-003
- **task_category:** product_feature_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D01]
- **linked_chunk_ids:** [D01-S1]
- **linked_fact_ids:** [F0102]
- **required_facts:** [F0102]
- **user_scenario_language_neutral:** A user asks what the NiceHome Sensor measures.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response lists all three: temperature, humidity, and motion.
- **forbidden_claims:** ["the Sensor records video", "the Sensor measures air quality", "the Sensor measures only temperature"]
- **likely_failure_modes:** Listing only one or two of the three measurements; incorrectly adding capabilities (e.g., air quality).
- **ambiguity_controls:** None directly, but partial lists are an evaluation edge case.
- **evaluation_notes:** All three measurements required for PASS. Omitting any one = UNCERTAIN (flag for human review: is it a partial answer or an incorrect answer?). Listing all three plus one incorrect extra = FAIL.
- **rendering_notes:** Query asks "what does the Sensor measure" or "what can the Sensor detect." Do not embed the answer in the query.

---

## INT-004 — Refund payment method

- **intent_id:** INT-004
- **task_category:** refund_process_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D03]
- **linked_chunk_ids:** [D03-S4]
- **linked_fact_ids:** [F0307]
- **required_facts:** [F0307]
- **user_scenario_language_neutral:** A user asks where or how their refund will be sent after a return is processed.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states the refund is issued to the original payment method.
- **forbidden_claims:** ["refunds are issued as store credit only", "refunds can go to any bank account", "cash refunds are available"]
- **likely_failure_modes:** Suggesting store credit or alternative payment methods.
- **ambiguity_controls:** None.
- **evaluation_notes:** Binary: "original payment method" = PASS.
- **rendering_notes:** Query asks where the refund goes, not how long it takes (F0308 is a separate intent).

---

## INT-005 — Cloud storage retention period

- **intent_id:** INT-005
- **task_category:** subscription_feature_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D04]
- **linked_chunk_ids:** [D04-S2]
- **linked_fact_ids:** [F0402]
- **required_facts:** [F0402]
- **user_scenario_language_neutral:** A user with the Camera Plus Plan asks how long their cloud video recordings are kept.
- **condition_count:** 0 (subscription is assumed active)
- **expected_outcome_language_neutral:** Response states cloud video storage lasts 30 days.
- **forbidden_claims:** ["unlimited storage", "7 days", "recordings are kept forever", "applies to all devices including the Sensor"]
- **likely_failure_modes:** Stating 14 days (confusing with trial period); stating unlimited.
- **ambiguity_controls:** AC1 (30-day storage vs. 30-day return window) — context is cloud storage; AC3 (30-day storage vs. 14-day trial) — must not give trial length instead.
- **evaluation_notes:** Binary: 30 days (for Camera video) = PASS. 14 days = FAIL.
- **rendering_notes:** Query should specify an active subscription context so it tests the storage fact, not the eligibility fact.

---

## INT-006 — Free trial length

- **intent_id:** INT-006
- **task_category:** subscription_trial_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D04]
- **linked_chunk_ids:** [D04-S4]
- **linked_fact_ids:** [F0405]
- **required_facts:** [F0405]
- **user_scenario_language_neutral:** A user considering the Camera Plus Plan asks how long the free trial lasts.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states the free trial lasts 14 days.
- **forbidden_claims:** ["30-day trial", "7-day trial", "no trial is available"]
- **likely_failure_modes:** Stating 30 days (confusing with storage period).
- **ambiguity_controls:** AC3 (14-day trial vs. 30-day storage) — this intent specifically tests whether the model distinguishes the two D04 numbers.
- **evaluation_notes:** Binary: 14 days = PASS. 30 days = FAIL.
- **rendering_notes:** Query must ask specifically about trial duration, not about the plan in general. The 14-vs-30 confusion is the key failure mode.

---

## INT-007 — Standard shipping timeframe

- **intent_id:** INT-007
- **task_category:** shipping_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D05]
- **linked_chunk_ids:** [D05-S1]
- **linked_fact_ids:** [F0502]
- **required_facts:** [F0502]
- **user_scenario_language_neutral:** A user asks how long Standard shipping takes.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states Standard shipping takes 5 to 7 business days.
- **forbidden_claims:** ["Standard shipping is same-day", "2 business days", "10 business days", "5 to 7 calendar days"]
- **likely_failure_modes:** Giving Express timeframe (2 business days) instead of Standard; omitting "business days" qualifier.
- **ambiguity_controls:** None directly, but confusing Standard vs. Express is the key failure.
- **evaluation_notes:** "5 to 7 business days" = PASS. "Business days" qualifier required (not just "days").
- **rendering_notes:** Query should specify "Standard" shipping to make this a direct lookup, not a comparison query.

---

## INT-008 — NiceHome Camera indoor/outdoor classification

- **intent_id:** INT-008
- **task_category:** product_feature_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D01]
- **linked_chunk_ids:** [D01-S1]
- **linked_fact_ids:** [F0104]
- **required_facts:** [F0104]
- **user_scenario_language_neutral:** A user asks whether the NiceHome Camera is suitable for indoor or outdoor use.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states the Camera is an indoor camera (not designed for outdoor use).
- **forbidden_claims:** ["the Camera is for outdoor use", "the Camera works both indoors and outdoors"]
- **likely_failure_modes:** Hallucinating outdoor capability; omitting the indoor constraint.
- **ambiguity_controls:** None.
- **evaluation_notes:** Binary: states indoor / not outdoor = PASS.
- **rendering_notes:** Query should ask about placement ("can I use the Camera outside?"). Tests whether the model respects the explicit scope fact.

---

## INT-009 — Repair turnaround time

- **intent_id:** INT-009
- **task_category:** repair_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D07]
- **linked_chunk_ids:** [D07-S5]
- **linked_fact_ids:** [F0707]
- **required_facts:** [F0707]
- **user_scenario_language_neutral:** A user asks how long a device repair takes.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states repair turnaround is typically 10 business days after the device is received.
- **forbidden_claims:** ["same-day repair", "2 business days", "repair takes several months", "10 calendar days"]
- **likely_failure_modes:** Confusing with refund processing time (14 business days); omitting "business days"; omitting "after receipt."
- **ambiguity_controls:** None directly, but repair (10 business days) vs. refund processing (14 business days) is an easy confusion.
- **evaluation_notes:** "Typically 10 business days from receipt" = PASS. Must include the "after receipt" anchor; "typically" qualifier acceptable.
- **rendering_notes:** Query should ask about repair time generically to produce a direct lookup.

---

## INT-010 — What the Camera Plus Plan is called

- **intent_id:** INT-010
- **task_category:** subscription_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D04]
- **linked_chunk_ids:** [D04-S1]
- **linked_fact_ids:** [F0401]
- **required_facts:** [F0401]
- **user_scenario_language_neutral:** A user asks whether NiceHome offers any cloud subscription and what it is called.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response identifies the Camera Plus Plan as the cloud subscription.
- **forbidden_claims:** ["there is no subscription", "the plan is called NiceHome Cloud", "the plan is called Camera Basic Plan"]
- **likely_failure_modes:** Giving a fabricated plan name.
- **ambiguity_controls:** None.
- **evaluation_notes:** Plan name "Camera Plus Plan" = PASS.
- **rendering_notes:** Simple vocabulary test and grounding check for the plan name controlled term.

---

## INT-011 — Refund processing time

- **intent_id:** INT-011
- **task_category:** refund_process_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D03]
- **linked_chunk_ids:** [D03-S4]
- **linked_fact_ids:** [F0308]
- **required_facts:** [F0308]
- **user_scenario_language_neutral:** A user asks how long it takes to receive a refund after returning a device.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states refunds are processed within 14 business days after the returned device is received.
- **forbidden_claims:** ["refunds are instant", "refunds take 60 days", "14 calendar days"]
- **likely_failure_modes:** Confusing 14 business days with 10 business days (repair turnaround); omitting "business days"; omitting "after receipt."
- **ambiguity_controls:** None directly, but refund processing (14 bdays) vs. repair turnaround (10 bdays) is a cross-document confusion risk.
- **evaluation_notes:** 14 business days from receipt = PASS. Must include "business days" and the "after receipt" anchor.
- **rendering_notes:** Query should ask how long a refund takes, giving a return context.

---

## INT-012 — NiceHome Plug remote switching without Hub

- **intent_id:** INT-012
- **task_category:** product_feature_lookup
- **difficulty_level:** simple
- **linked_document_ids:** [D01]
- **linked_chunk_ids:** [D01-S2]
- **linked_fact_ids:** [F0107]
- **required_facts:** [F0107]
- **user_scenario_language_neutral:** A user asks whether they can turn the NiceHome Plug on and off remotely if they do not have a Hub.
- **condition_count:** 0 (no Hub assumed)
- **expected_outcome_language_neutral:** Response confirms basic on/off switching works without a Hub, but states automation features (scheduling, energy monitoring) require a Hub.
- **forbidden_claims:** ["the Plug requires a Hub for all functions", "the Plug works fully without a Hub"]
- **likely_failure_modes:** Applying the general Hub-requirement rule without noticing the Plug's partial exception; stating the Plug works fully standalone.
- **ambiguity_controls:** None but this tests the partial-exception fact (F0107 vs. the general rule F0105/F0106).
- **evaluation_notes:** PASS requires: (1) on/off works without Hub AND (2) automation features require Hub. Either part missing = UNCERTAIN.
- **rendering_notes:** Query should specifically ask about operation without a Hub to target the exception logic.

---

## Conditional policy intents (INT-013–INT-024)

*Conditional policy intents require two or more facts, or a rule plus an exception, or a condition that routes to different outcomes. They are designed to test whether the model retrieves and applies the relevant condition, not just the general rule.*

---

## INT-013 — Gen 2 device with Gen 1 Hub

- **intent_id:** INT-013
- **task_category:** compatibility
- **difficulty_level:** conditional
- **linked_document_ids:** [D01]
- **linked_chunk_ids:** [D01-S3]
- **linked_fact_ids:** [F0108, F0109]
- **required_facts:** [F0108]
- **user_scenario_language_neutral:** A user with a Gen 1 Hub asks if they can use a Gen 2 NiceHome Sensor.
- **condition_count:** 1 (Hub generation = Gen 1)
- **expected_outcome_language_neutral:** Response states the Gen 2 Sensor is NOT compatible with a Gen 1 Hub; a Gen 2 Hub is required.
- **forbidden_claims:** ["Gen 1 Hub supports Gen 2 devices", "all Hubs support all devices", "Gen 2 Sensor works with any Hub"]
- **likely_failure_modes:** Applying backward compatibility in the wrong direction (Gen 2 Hub → Gen 1 devices, not the other way); giving a generic "compatible" answer.
- **ambiguity_controls:** AC1 (asymmetric generation compatibility) — this tests F0108 (Gen 1 Hub cannot support Gen 2) vs. F0109 (Gen 2 Hub supports both).
- **evaluation_notes:** Must state Gen 1 Hub does NOT support Gen 2 devices = PASS. Response recommending a Gen 2 Hub upgrade is acceptable additional info.
- **rendering_notes:** Query must specify the Gen 1 Hub and Gen 2 device to force the condition; do not ask generically.

---

## INT-014 — Opened device return: who pays shipping

- **intent_id:** INT-014
- **task_category:** return_condition
- **difficulty_level:** conditional
- **linked_document_ids:** [D03]
- **linked_chunk_ids:** [D03-S2]
- **linked_fact_ids:** [F0302, F0303]
- **required_facts:** [F0303]
- **user_scenario_language_neutral:** A user opened their NiceHome Plug but decided they do not want it; they are within the return window and the device is undamaged. They ask if they can return it and who pays for return shipping.
- **condition_count:** 2 (opened, undamaged, within window)
- **expected_outcome_language_neutral:** Response confirms: (1) return is accepted; (2) full refund is given; (3) the customer pays return shipping.
- **forbidden_claims:** ["opened devices cannot be returned", "free return shipping for opened devices", "only a partial refund for opened devices"]
- **likely_failure_modes:** Applying the unopened rule (free return shipping); giving only partial refund.
- **ambiguity_controls:** AC-adjacent: this tests the F0302 vs. F0303 distinction — refund is full in both, but shipping cost differs.
- **evaluation_notes:** All three components required: return accepted + full refund + customer pays shipping. Missing "full refund" = UNCERTAIN; missing shipping-cost assignment = FAIL.
- **rendering_notes:** Query should specify opened + undamaged + within window to set all conditions unambiguously.

---

## INT-015 — Warranty coverage: accidental damage

- **intent_id:** INT-015
- **task_category:** warranty_coverage
- **difficulty_level:** conditional
- **linked_document_ids:** [D02]
- **linked_chunk_ids:** [D02-S2, D02-S3]
- **linked_fact_ids:** [F0202, F0203]
- **required_facts:** [F0203]
- **user_scenario_language_neutral:** A user dropped their NiceHome Camera and it stopped working. They ask if the warranty covers the repair.
- **condition_count:** 1 (damage type = accidental)
- **expected_outcome_language_neutral:** Response states accidental damage is NOT covered by the warranty.
- **forbidden_claims:** ["accidental damage is covered", "dropping counts as a manufacturing defect"]
- **likely_failure_modes:** Applying the general coverage rule (F0202) without the accidental-damage exclusion (F0203).
- **ambiguity_controls:** Rule + exception pattern (F0202 + F0203).
- **evaluation_notes:** Must state accidental damage is excluded = PASS. Mentioning the out-of-warranty service quote (D07 F0708) is acceptable additional info.
- **rendering_notes:** Query should specify "dropped" to make damage type unambiguous.

---

## INT-016 — Warranty coverage: misuse

- **intent_id:** INT-016
- **task_category:** warranty_coverage
- **difficulty_level:** conditional
- **linked_document_ids:** [D02]
- **linked_chunk_ids:** [D02-S2, D02-S3]
- **linked_fact_ids:** [F0202, F0204]
- **required_facts:** [F0204]
- **user_scenario_language_neutral:** A user modified their NiceHome Hub by opening the casing and replacing internal components. The Hub now fails. They ask if the warranty still applies.
- **condition_count:** 1 (damage type = unauthorized modification)
- **expected_outcome_language_neutral:** Response states the warranty does NOT apply to damage caused by unauthorized modification.
- **forbidden_claims:** ["modifying the device does not affect the warranty", "the warranty still covers defects even after modification"]
- **likely_failure_modes:** Applying general warranty coverage without the misuse/unauthorized-modification exclusion.
- **ambiguity_controls:** Rule + exception pattern (F0202 + F0204).
- **evaluation_notes:** Must state unauthorized modification voids warranty for resulting damage = PASS.
- **rendering_notes:** Specify "opened the casing and replaced components" to make the unauthorized modification explicit.

---

## INT-017 — Subscription cancellation: access and refund

- **intent_id:** INT-017
- **task_category:** subscription_cancellation
- **difficulty_level:** conditional
- **linked_document_ids:** [D04]
- **linked_chunk_ids:** [D04-S5]
- **linked_fact_ids:** [F0407, F0408]
- **required_facts:** [F0407, F0408]
- **user_scenario_language_neutral:** A user cancels the Camera Plus Plan mid-billing period. They ask (a) whether they still have access to cloud storage and (b) whether they receive a partial refund.
- **condition_count:** 1 (cancellation mid-period)
- **expected_outcome_language_neutral:** Response states: (1) cloud storage access continues until the end of the current billing period; (2) no pro-rated refund is given.
- **forbidden_claims:** ["access ends immediately", "a partial refund is issued", "cancellation deletes cloud video immediately"]
- **likely_failure_modes:** Stating access ends immediately; stating a partial refund is available.
- **ambiguity_controls:** Both sub-facts required; this is a two-part answer where both parts matter.
- **evaluation_notes:** Both components required for PASS: access continues to period end + no pro-rated refund. Missing one = UNCERTAIN.
- **rendering_notes:** Query should ask both questions together to require both facts. Multi-part intent.

---

## INT-018 — Out-of-warranty repair: cost and shipping

- **intent_id:** INT-018
- **task_category:** repair_condition
- **difficulty_level:** conditional
- **linked_document_ids:** [D07]
- **linked_chunk_ids:** [D07-S2]
- **linked_fact_ids:** [F0702, F0706]
- **required_facts:** [F0702, F0706]
- **user_scenario_language_neutral:** A user's 3-year-old NiceHome Hub has a hardware fault. They ask if it can be repaired and what they would need to pay.
- **condition_count:** 1 (device out of warranty)
- **expected_outcome_language_neutral:** Response states: (1) out-of-warranty repair is available for a service fee; (2) the customer pays shipping in both directions.
- **forbidden_claims:** ["out-of-warranty repairs are free", "NiceHome pays return shipping for out-of-warranty repairs", "out-of-warranty devices cannot be repaired"]
- **likely_failure_modes:** Applying in-warranty free-repair rule; stating only a service fee without mentioning two-way shipping cost.
- **ambiguity_controls:** Contrasts with in-warranty (F0701, free + prepaid label) on both cost and shipping.
- **evaluation_notes:** Both components required: service fee + customer pays two-way shipping. Missing shipping = UNCERTAIN.
- **rendering_notes:** Specify "3 years old" to make the out-of-warranty condition unambiguous (warranty is 2 years).

---

## INT-019 — Refurbished replacement warranty

- **intent_id:** INT-019
- **task_category:** repair_outcome
- **difficulty_level:** conditional
- **linked_document_ids:** [D07]
- **linked_chunk_ids:** [D07-S3]
- **linked_fact_ids:** [F0704, F0705]
- **required_facts:** [F0705]
- **user_scenario_language_neutral:** A user's device is being replaced under warranty and they are told the replacement will be a refurbished unit. They ask how long the warranty on the refurbished replacement will be.
- **condition_count:** 1 (replacement is refurbished)
- **expected_outcome_language_neutral:** Response states the refurbished replacement carries the remainder of the original warranty, with a minimum of 90 days (whichever is longer).
- **forbidden_claims:** ["refurbished devices have no warranty", "the warranty resets to a full 2 years", "the warranty is exactly 90 days regardless"]
- **likely_failure_modes:** The three AC8 misreadings: (a) flat 90-day reset, (b) full 2-year reset, (c) no warranty.
- **ambiguity_controls:** AC8 — this intent directly tests the refurbished warranty minimum-floor rule.
- **evaluation_notes:** Must express "longer of: remaining original warranty or 90 days" = PASS. Stating only "90 days" = FAIL (flat reset). Stating "2 years" = FAIL.
- **rendering_notes:** Must specify refurbished replacement to target F0705 specifically.

---

## INT-020 — Order cancellation after 2-hour window

- **intent_id:** INT-020
- **task_category:** order_modification
- **difficulty_level:** conditional
- **linked_document_ids:** [D05]
- **linked_chunk_ids:** [D05-S3]
- **linked_fact_ids:** [F0505, F0506]
- **required_facts:** [F0506]
- **user_scenario_language_neutral:** A user placed an order 4 hours ago and now wants to cancel it before it ships. They ask if they can cancel.
- **condition_count:** 1 (time elapsed > 2 hours)
- **expected_outcome_language_neutral:** Response states: (1) cancellation is no longer possible after 2 hours; (2) the user can return the device after delivery under the return policy.
- **forbidden_claims:** ["the order can still be cancelled", "no recourse exists", "cancellation is available until it ships"]
- **likely_failure_modes:** Applying the within-window rule (cancellation possible) without checking the time condition; not mentioning the post-delivery return option.
- **ambiguity_controls:** Time condition critical: the answer hinges entirely on whether the 2-hour window has passed.
- **evaluation_notes:** Both components required: no cancel now + return after delivery available. Missing the return option = UNCERTAIN.
- **rendering_notes:** Specify "4 hours ago" to make the post-window condition explicit.

---

## INT-021 — Express shipping eligibility: backordered item

- **intent_id:** INT-021
- **task_category:** shipping_condition
- **difficulty_level:** conditional
- **linked_document_ids:** [D05]
- **linked_chunk_ids:** [D05-S1, D05-S2]
- **linked_fact_ids:** [F0503, F0504]
- **required_facts:** [F0504]
- **user_scenario_language_neutral:** A user wants Express shipping for a NiceHome Camera that is backordered. They ask if Express shipping is available.
- **condition_count:** 1 (item out of stock)
- **expected_outcome_language_neutral:** Response states Express shipping is NOT available for backordered/out-of-stock items.
- **forbidden_claims:** ["Express is available for all orders", "backorder items can use Express shipping"]
- **likely_failure_modes:** Stating Express is available without applying the in-stock condition.
- **ambiguity_controls:** Condition test: Express requires in-stock (F0504).
- **evaluation_notes:** Must state Express unavailable for backordered items = PASS.
- **rendering_notes:** Specify "backordered" to make the out-of-stock condition clear.

---

## INT-022 — Subscription refund via returns process

- **intent_id:** INT-022
- **task_category:** return_exclusion
- **difficulty_level:** conditional
- **linked_document_ids:** [D03, D04]
- **linked_chunk_ids:** [D03-S3, D04-S5]
- **linked_fact_ids:** [F0306, F0408]
- **required_facts:** [F0306]
- **user_scenario_language_neutral:** A user paid for a Camera Plus Plan and wants to return the subscription for a refund through the device return process.
- **condition_count:** 1 (item type = subscription)
- **expected_outcome_language_neutral:** Response states subscriptions are NOT refundable via the device return process; subscription cancellation is a separate process.
- **forbidden_claims:** ["subscriptions can be returned like a device", "a subscription refund is processed with the device return"]
- **likely_failure_modes:** Applying the device return rules to a subscription.
- **ambiguity_controls:** Cross-document: D03 return exclusion + D04 cancellation process.
- **evaluation_notes:** Must state subscription not in return scope + cancellation is separate = PASS.
- **rendering_notes:** Query must be clear the user wants a subscription refund via the return process to target the exclusion.

---

## INT-023 — Damaged device return: not eligible unless warranty

- **intent_id:** INT-023
- **task_category:** return_exclusion
- **difficulty_level:** conditional
- **linked_document_ids:** [D03]
- **linked_chunk_ids:** [D03-S3]
- **linked_fact_ids:** [F0304]
- **required_facts:** [F0304]
- **user_scenario_language_neutral:** A user cracked the screen of a NiceHome Camera (customer-caused damage) and wants to return it for a refund.
- **condition_count:** 1 (damage is customer-caused)
- **expected_outcome_language_neutral:** Response states customer-damaged devices are not eligible for a refund, except where the damage is covered under the warranty (which accidental damage is not — F0203 provides that context).
- **forbidden_claims:** ["all returns are refunded regardless of damage", "cracked screen is always covered by warranty"]
- **likely_failure_modes:** Allowing a return without applying the damage exclusion; applying warranty to accidental damage.
- **ambiguity_controls:** Return exclusion + optional warranty-exclusion cross-reference.
- **evaluation_notes:** Must state customer damage excludes return refund = PASS. Noting the warranty also excludes accidental damage is a bonus, not required.
- **rendering_notes:** Specify "cracked screen" as customer-caused to make the condition unambiguous.

---

## INT-024 — Subscription plan change timing

- **intent_id:** INT-024
- **task_category:** subscription_change
- **difficulty_level:** conditional
- **linked_document_ids:** [D04]
- **linked_chunk_ids:** [D04-S5]
- **linked_fact_ids:** [F0409]
- **required_facts:** [F0409]
- **user_scenario_language_neutral:** A user upgrades their Camera Plus Plan mid-billing period. They ask when the new plan takes effect.
- **condition_count:** 1 (plan change triggered)
- **expected_outcome_language_neutral:** Response states the plan change takes effect at the start of the next billing period.
- **forbidden_claims:** ["changes take effect immediately", "upgrades are immediate but downgrades are deferred"]
- **likely_failure_modes:** Stating immediate effect; distinguishing upgrades and downgrades (the policy does not).
- **ambiguity_controls:** None specific; tests the condition on F0409.
- **evaluation_notes:** "Next billing period" = PASS. No immediate effect exception exists.
- **rendering_notes:** Query should specify the upgrade scenario; note in rendering that upgrade and downgrade follow the same rule.

---

## Troubleshooting/process intents (INT-025–INT-036)

*Troubleshooting/process intents require ordered steps, conditional branching in a diagnostic procedure, or sequential process reasoning. The expected outcome must list required steps, not just a policy fact.*

---

## INT-025 — Hub connectivity: full diagnostic sequence

- **intent_id:** INT-025
- **task_category:** troubleshooting_connectivity
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D06]
- **linked_chunk_ids:** [D06-S1]
- **linked_fact_ids:** [F0601, F0602, F0603, F0604]
- **required_facts:** [F0601, F0602, F0603, F0604]
- **user_scenario_language_neutral:** A user reports that their NiceHome devices are showing as offline and asks what steps to take to diagnose and fix the connectivity.
- **condition_count:** 0 (initial connectivity failure; conditions revealed by diagnostic steps)
- **expected_outcome_language_neutral:** Response lists all four steps in order: (1) check Hub power light; (2) if light off, check power cable and outlet; (3) if light on but offline, restart the Hub; (4) if still offline, check home network/router.
- **forbidden_claims:** ["factory reset the Hub as the first step", "replace the Hub immediately"]
- **likely_failure_modes:** Skipping steps; reordering steps; jumping to factory reset instead of restart; omitting the network/router check.
- **ambiguity_controls:** AC5 (restart vs. factory reset) — step 3 is "restart," not "factory reset."
- **evaluation_notes:** Ordered sequence. All four steps required; order matters. Substituting "factory reset" for "restart" in step 3 = FAIL. Missing step 4 = UNCERTAIN (partial procedure).
- **rendering_notes:** Query should describe devices offline without specifying which step has been tried; evaluator checks the full four-step sequence.

---

## INT-026 — Device pairing: full sequence

- **intent_id:** INT-026
- **task_category:** troubleshooting_pairing
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D06]
- **linked_chunk_ids:** [D06-S3]
- **linked_fact_ids:** [F0606, F0607, F0608]
- **required_facts:** [F0606, F0607, F0608]
- **user_scenario_language_neutral:** A user wants to add a new NiceHome Sensor to their system and asks how to pair it.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response lists all three steps in order: (1) open the app and select "Add device"; (2) hold the setup button for 5 seconds; (3) follow app prompts to complete pairing.
- **forbidden_claims:** ["hold the button for 10 seconds", "pairing completes without any button press"]
- **likely_failure_modes:** Giving 10 seconds (confusing with factory-reset hold); skipping the "Add device" app step; omitting the app-prompts step.
- **ambiguity_controls:** AC2 (5-second pairing hold vs. 10-second factory reset) — this intent directly tests whether the model retrieves 5 seconds, not 10.
- **evaluation_notes:** Three ordered steps required. "5 seconds" specifically required; 10 seconds = FAIL.
- **rendering_notes:** Query should ask how to add/pair a device. "5 seconds" vs. "10 seconds" is the key evaluation point.

---

## INT-027 — Pairing fails: within-range check

- **intent_id:** INT-027
- **task_category:** troubleshooting_pairing
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D06]
- **linked_chunk_ids:** [D06-S3]
- **linked_fact_ids:** [F0606, F0607, F0608, F0609]
- **required_facts:** [F0609]
- **user_scenario_language_neutral:** A user followed the pairing steps but the device failed to pair. They ask what to do.
- **condition_count:** 1 (pairing failed)
- **expected_outcome_language_neutral:** Response states that on pairing failure, the user should ensure the device is within range of the Hub.
- **forbidden_claims:** ["a pairing failure always means a defective device", "factory reset the device on first pairing failure"]
- **likely_failure_modes:** Jumping to replacement/factory reset instead of the range check.
- **ambiguity_controls:** None specific; tests escalation vs. range check (F0609).
- **evaluation_notes:** Range check must be identified as the first-response step = PASS.
- **rendering_notes:** Query must specify pairing already failed (not initial pairing setup).

---

## INT-028 — Warranty claim: full process

- **intent_id:** INT-028
- **task_category:** warranty_process
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D02]
- **linked_chunk_ids:** [D02-S4]
- **linked_fact_ids:** [F0205, F0206, F0207, F0208]
- **required_facts:** [F0205, F0206, F0207, F0208]
- **user_scenario_language_neutral:** A user's in-warranty NiceHome Sensor has stopped working and they ask how to make a warranty claim.
- **condition_count:** 0 (warranty assumed valid)
- **expected_outcome_language_neutral:** Response lists: (1) have proof of purchase ready; (2) contact support with serial number; (3) receive claim reference and prepaid label; (4) ship device with prepaid label and claim reference.
- **forbidden_claims:** ["ship the device without contacting support first", "the customer pays for warranty shipping"]
- **likely_failure_modes:** Omitting proof-of-purchase requirement; missing prepaid label (claiming customer pays); skipping contact-support step.
- **ambiguity_controls:** Prepaid label (in-warranty, free) vs. customer pays (out-of-warranty, D07 F0706).
- **evaluation_notes:** All four points required. Customer paying shipping = FAIL. Missing prepaid label = UNCERTAIN.
- **rendering_notes:** Specify in-warranty device and hardware failure to target the claim process.

---

## INT-029 — Return process: step sequence

- **intent_id:** INT-029
- **task_category:** return_process
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D03]
- **linked_chunk_ids:** [D03-S5]
- **linked_fact_ids:** [F0309, F0310, F0311]
- **required_facts:** [F0309, F0310, F0311]
- **user_scenario_language_neutral:** A user wants to return an unopened NiceHome Hub within the return window and asks what steps to follow.
- **condition_count:** 0 (eligible return assumed)
- **expected_outcome_language_neutral:** Response lists the three steps in order: (1) request a return authorization from support; (2) receive the return authorization number and shipping instructions; (3) ship the device with the authorization number included.
- **forbidden_claims:** ["ship the device back without obtaining authorization", "no authorization number is needed"]
- **likely_failure_modes:** Omitting the authorization step; omitting the authorization number in the shipping step.
- **evaluation_notes:** All three steps in order required. Shipping without authorization = FAIL.
- **ambiguity_controls:** Return authorization (D03) vs. warranty claim reference (D02) — different identifiers.
- **rendering_notes:** Specify unopened device within window to keep the process unambiguous (full refund, free return shipping from F0302 is acceptable bonus info).

---

## INT-030 — Password recovery: full sequence

- **intent_id:** INT-030
- **task_category:** account_recovery
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D08]
- **linked_chunk_ids:** [D08-S1]
- **linked_fact_ids:** [F0801, F0802, F0803]
- **required_facts:** [F0801, F0802, F0803]
- **user_scenario_language_neutral:** A user cannot log in because they forgot their password and asks how to reset it.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response lists three steps in order: (1) select "Forgot password" on the sign-in screen; (2) enter account email to receive reset link; (3) follow the reset link to set a new password.
- **forbidden_claims:** ["contact support to reset every password", "a reset code is sent by phone", "the old password is emailed back"]
- **likely_failure_modes:** Stating phone-based reset; stating contact-support-only; omitting the email link step.
- **ambiguity_controls:** None.
- **evaluation_notes:** Three ordered steps required; email-link mechanism required = PASS. Phone reset = FAIL.
- **rendering_notes:** Query should describe a forgotten-password situation. Straightforward process test.

---

## INT-031 — Hub factory reset: procedure and next step

- **intent_id:** INT-031
- **task_category:** device_reset_process
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D08]
- **linked_chunk_ids:** [D08-S3, D08-S4]
- **linked_fact_ids:** [F0806, F0807]
- **required_facts:** [F0806, F0807]
- **user_scenario_language_neutral:** A user needs to factory reset their NiceHome Hub and asks how to do it and what happens next.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states: (1) hold the Hub reset button for 10 seconds; (2) wait for the Hub light to blink (reset confirmation); (3) the device must be re-paired via the app afterward.
- **forbidden_claims:** ["hold the button for 5 seconds", "the Hub works immediately after reset without re-pairing"]
- **likely_failure_modes:** Giving 5 seconds (confusing with pairing hold); omitting the re-pair requirement.
- **ambiguity_controls:** AC2 (10-second factory reset vs. 5-second pairing hold) — this intent tests 10 seconds. Must not say 5.
- **evaluation_notes:** 10 seconds specifically required; re-pair requirement must be mentioned = PASS. 5 seconds = FAIL.
- **rendering_notes:** Query asks how to factory reset the Hub. Two chunks involved (S3 + S4) — tests whether Agent B retrieves both or only one.

---

## INT-032 — What factory reset does and does not delete

- **intent_id:** INT-032
- **task_category:** device_reset_outcome
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D08]
- **linked_chunk_ids:** [D08-S2, D08-S4]
- **linked_fact_ids:** [F0804, F0805, F0809]
- **required_facts:** [F0805, F0809]
- **user_scenario_language_neutral:** A user is about to factory reset their NiceHome Camera and is worried about losing their cloud video recordings. They ask what a factory reset will delete.
- **condition_count:** 0
- **expected_outcome_language_neutral:** Response states: (1) factory reset erases all device settings and unlinks the device from the account; (2) cloud-stored video is NOT deleted by a factory reset — it is managed by the subscription.
- **forbidden_claims:** ["a factory reset deletes cloud video", "factory reset only resets settings, account link is unaffected"]
- **likely_failure_modes:** Stating cloud video is deleted; omitting the account-unlink consequence; confusing with soft reset.
- **ambiguity_controls:** AC5 (factory reset vs. soft reset) and AC9 (F0809 cloud-video carve-out).
- **evaluation_notes:** Both components required: settings/account erased + cloud video not deleted = PASS. Stating cloud video deleted = FAIL.
- **rendering_notes:** Frame query around concern about cloud recordings to make both F0805 and F0809 relevant.

---

## INT-033 — Unresponsive Plug: step sequence

- **intent_id:** INT-033
- **task_category:** troubleshooting_power
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D06]
- **linked_chunk_ids:** [D06-S4]
- **linked_fact_ids:** [F0610, F0611]
- **required_facts:** [F0610, F0611]
- **user_scenario_language_neutral:** A user's NiceHome Plug does not respond to any commands. They ask what to do.
- **condition_count:** 0 (initial unresponsive state)
- **expected_outcome_language_neutral:** Response lists two steps in order: (1) toggle the Plug off and on from the app; (2) if still unresponsive, perform a soft reset.
- **forbidden_claims:** ["factory reset the Plug as the first step", "perform a soft reset before trying the app toggle"]
- **likely_failure_modes:** Jumping to soft reset (or factory reset) before the app toggle; reversing the order.
- **ambiguity_controls:** AC5 (soft reset vs. factory reset) — step 2 is soft reset, not factory reset.
- **evaluation_notes:** Both steps in order; step 2 specifically "soft reset" (not factory reset) = PASS. "Factory reset" at either step = FAIL.
- **rendering_notes:** Query should describe complete non-response ("won't turn on, won't respond to app").

---

## INT-034 — Hub blinking red: meaning and next step

- **intent_id:** INT-034
- **task_category:** troubleshooting_connectivity
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D06]
- **linked_chunk_ids:** [D06-S2, D06-S1]
- **linked_fact_ids:** [F0605, F0603, F0604]
- **required_facts:** [F0605]
- **user_scenario_language_neutral:** A user notices their NiceHome Hub light is blinking red and asks what it means and what to do.
- **condition_count:** 1 (Hub light = blinking red)
- **expected_outcome_language_neutral:** Response states: (1) blinking red means the Hub has lost its network connection; (2) next step: check/restart the Hub (connectivity troubleshooting), including checking the home network/router.
- **forbidden_claims:** ["blinking red means hardware failure", "blinking red means the Hub is updating", "replace the Hub immediately"]
- **likely_failure_modes:** Misidentifying the indicator meaning; skipping the network troubleshooting recommendation.
- **ambiguity_controls:** Indicator state must be correctly identified (F0605).
- **evaluation_notes:** Meaning (lost network) = required. Next step (network/router check, per F0604) = expected but can be UNCERTAIN without it. Misidentifying as hardware failure = FAIL.
- **rendering_notes:** Query describes the blinking red light symptom. Two chunks may be retrieved (S2 for the indicator meaning, S1 for the fix).

---

## INT-035 — Delayed shipment vs. lost shipment: which remedy applies

- **intent_id:** INT-035
- **task_category:** shipping_problem
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D05]
- **linked_chunk_ids:** [D05-S4]
- **linked_fact_ids:** [F0507, F0508]
- **required_facts:** [F0507, F0508]
- **user_scenario_language_neutral:** A user's shipment is well past its estimated delivery window but has not been confirmed as lost. They ask what they are entitled to — a refund, a replacement, or something else.
- **condition_count:** 1 (shipment delayed, not yet confirmed lost)
- **expected_outcome_language_neutral:** Response states: (1) for a delayed shipment, the user may request a refund of the shipping fee (not a product refund or replacement); (2) if the shipment were confirmed lost, a free replacement would be sent instead. The situation described is a delay, so the shipping-fee refund applies.
- **forbidden_claims:** ["a delayed shipment gets a full product refund", "the customer must repurchase a delayed item", "delay and loss both result in a replacement"]
- **likely_failure_modes:** Applying the lost-shipment remedy (replacement) to a delayed shipment; conflating the two scenarios.
- **ambiguity_controls:** AC6 (delay remedy vs. loss remedy) — the key distinction this intent tests.
- **evaluation_notes:** Shipping-fee refund = the applicable remedy for delay. Distinguishing delay (fee refund) from loss (replacement) = PASS. Applying replacement to delay = FAIL.
- **rendering_notes:** Query should describe a delay scenario clearly (past window, not confirmed lost). The expected answer requires applying the delay rule, not the loss rule, but ideally the response also clarifies what would apply if lost.

---

## INT-036 — Lost device: remote account removal

- **intent_id:** INT-036
- **task_category:** account_management
- **difficulty_level:** troubleshooting-process
- **linked_document_ids:** [D08]
- **linked_chunk_ids:** [D08-S5]
- **linked_fact_ids:** [F0808]
- **required_facts:** [F0808]
- **user_scenario_language_neutral:** A user reports that their NiceHome Camera has been lost or stolen and asks whether they can prevent unauthorized use and remove it from their account.
- **condition_count:** 1 (device is lost)
- **expected_outcome_language_neutral:** Response states the lost device can be removed from the account remotely through the app.
- **forbidden_claims:** ["a lost device cannot be removed without physical access", "the user must contact support to remove a device"]
- **likely_failure_modes:** Claiming physical access is required; not mentioning the remote app removal option.
- **ambiguity_controls:** None.
- **evaluation_notes:** Remote removal via app = PASS. Physical access required = FAIL.
- **rendering_notes:** Specify "lost or stolen" to cover both scenarios; query should ask about account security and device removal.

---

## Coverage analysis

### Fact coverage

| Document | Facts available | Facts required in at least one intent | Covered |
|---|---|---|---|
| D01 | F0101–F0110 (10) | F0101†, F0102, F0103†, F0104, F0105†, F0106†, F0107, F0108, F0109†, F0110† | ~8 directly, ~2 indirectly |
| D02 | F0201–F0209 (9) | F0201, F0202†, F0203, F0204, F0205, F0206, F0207, F0208, F0209† | ~8 directly, ~1 indirectly |
| D03 | F0301–F0311 (11) | F0301, F0302, F0303, F0304, F0305†, F0306, F0307, F0308, F0309, F0310, F0311 | ~11 all |
| D04 | F0401–F0409 (9) | F0401, F0402, F0403†, F0404†, F0405, F0406†, F0407, F0408, F0409 | ~9 all |
| D05 | F0501–F0508 (8) | F0501†, F0502, F0503†, F0504, F0505, F0506, F0507, F0508 | ~8 all |
| D06 | F0601–F0613 (13) | F0601, F0602, F0603, F0604, F0605, F0606, F0607, F0608, F0609, F0610, F0611, F0612†, F0613† | ~13 all |
| D07 | F0701–F0709 (9) | F0701†, F0702, F0703†, F0704, F0705, F0706, F0707, F0708†, F0709† | ~7 directly, ~2 indirectly |
| D08 | F0801–F0809 (9) | F0801, F0802, F0803, F0804†, F0805, F0806, F0807, F0808, F0809 | ~9 all |

† = fact covered indirectly as context or background in an intent requiring a related fact (e.g., F0202 is required background for INT-015/016 but the required_fact is the exception F0203/F0204).

**Facts with no direct intent coverage:** F0101 (Hub as central device — implied in many intents but not the main required fact), F0103 (Plug description — D01-S1), F0105/F0106 (Sensor/Camera Hub requirement — tested by INT-012/INT-013 for the Plug exception; F0105/F0106 are background), F0109 (Gen 2 Hub backward compatibility — background to INT-013), F0110 (live view offline — background to INT-034 and AC4 in INT-005), F0209 (warranty outcome — tested indirectly via INT-028), F0303 (opened return — tested by INT-014), F0612 (Sensor recalibration), F0613 (escalation), F0701/F0703 (in-warranty free repair — background to INT-028), F0708 (accidental/liquid damage exclusion), F0709 (repair process entry). These 10+ facts are present as required_facts context or referenced in evaluation notes and are indirectly probed. For a v0.2 expansion, targeted intents for F0110, F0612, F0708, and the in-warranty repair path would improve coverage.

### Ambiguity control coverage

| AC | Description | Tested by |
|---|---|---|
| AC1 | 30-day return window vs. 30-day cloud storage | INT-002 (return window), INT-005 (storage), rendering distinguishes them |
| AC2 | 5-second pairing hold vs. 10-second Hub factory reset | INT-026 (5-second), INT-031 (10-second) |
| AC3 | 14-day trial vs. 30-day cloud storage | INT-005 (storage), INT-006 (trial) — both required for the pair |
| AC4 | Live view: Hub-online dependency vs. subscription-independence | INT-005 (subscription doesn't prevent live view, F0403 background) |
| AC5 | Soft reset vs. factory reset vs. Hub restart | INT-025 (restart), INT-033 (soft reset), INT-031/INT-032 (factory reset) |
| AC6 | Shipping delay fee refund vs. lost-shipment replacement | INT-035 directly tests this distinction |
| AC7 | 2-year warranty vs. 30-day return window | INT-001 (warranty), INT-002 (return) — both required for the pair |
| AC8 | Refurbished warranty floor | INT-019 directly tests all three misreadings |
| AC9 | F0807 single-source / forward reference | INT-031 and INT-032 together — S3+S4 span required |

All nine ambiguity controls are covered. AC4 coverage is the thinnest (only indirect, via INT-005 background); a dedicated intent testing "does live view work without the subscription?" against F0403 would improve coverage.

### All 8 documents represented

D01 ✓ (INT-003, 008, 012, 013)
D02 ✓ (INT-001, 015, 016, 028)
D03 ✓ (INT-002, 004, 011, 014, 022, 023, 029)
D04 ✓ (INT-005, 006, 010, 017, 022, 024)
D05 ✓ (INT-007, 020, 021, 035)
D06 ✓ (INT-025, 026, 027, 033, 034)
D07 ✓ (INT-009, 018, 019)
D08 ✓ (INT-030, 031, 032, 036)

---

## Open questions for the intent set

- **IS1:** Should a dedicated simple intent be added for F0110 (live view unavailable when Hub offline) to directly test AC4, given AC4 coverage is currently only indirect?
- **IS2:** Should a dedicated simple intent for F0612 (Sensor recalibration) be added to improve D06 non-connectivity coverage?
- **IS3:** Should a troubleshooting intent for F0708 (accidental/liquid damage → out-of-warranty service quote) be added to cover D07's damage exclusion path? Currently tested as secondary context in INT-015.
- **IS4:** INT-003 requires all three Sensor measurement types. Should an UNCERTAIN flag be pre-registered for "two out of three" responses (partial but not wrong), or should any omission count as FAIL?
- **IS5:** INT-025 (connectivity) and INT-026 (pairing) each test full ordered sequences. Should the evaluation require exact step order, or is "all steps mentioned, order substantially correct" acceptable?
- **IS6:** INT-019 (refurbished warranty floor) requires the "longer of remainder or 90 days" meaning. Should all three misreadings (flat 90, full 2-year reset, no warranty) be explicitly pre-registered as FAIL patterns in expected-fact-mapping.md?
- **IS7:** INT-035 (delay vs. loss) requires condition-specific routing. Should the evaluator be instructed to FAIL if the response gives both remedies without identifying which applies to the delay scenario, or is mentioning both acceptable as long as the delay remedy is correctly identified?

---

*This file defines the evaluation targets. Execution-tax remains a hypothesis to be tested when agents run against the KB renderings to answer these intents. Version: intent-v0.1.0, not yet frozen.*
