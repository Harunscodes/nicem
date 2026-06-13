# NiceM Query Rendering — English v0.1

**Status:** 36 English query texts for the NiceM v0.1 benchmark
**Role:** One of three peer query renderings (EN/NL/TR). Each query is authored from the intent specification and expected fact mapping, not from the other language renderings.
**Version:** qr-en-v0.1.0 (not yet frozen)
**Depends on:** `query-rendering-plan.md` (qr-plan-v0.1.0), `intent-set.md` (intent-v0.1.0), `expected-fact-mapping.md` (efm-v0.1.0)
**Feeds into:** Stage 1 tokenizer sanity gate (tokenize queries; compute EN token counts as analytic baseline)
**Review status:** Draft — owner review recommended before freezing

**Note:** English is NOT the canonical query source. Dutch and Turkish renderings are authored independently from the intent specs, not from these English queries.

---

## Simple factual intents (INT-001–INT-012)

---

## INT-001

- **intent_id:** INT-001
- **language:** en
- **query_text:** "How long is the warranty on NiceHome devices?"
- **linked_fact_ids:** [F0201]
- **expected_fact_set_id:** INT-001
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Straightforward warranty lookup. Does not specify device type — tests the "all devices" scope. AC7 alert: wrong answer is 30 days (return window).

---

## INT-002

- **intent_id:** INT-002
- **language:** en
- **query_text:** "How many days do I have to return a NiceHome device?"
- **linked_fact_ids:** [F0301]
- **expected_fact_set_id:** INT-002
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Return window lookup. AC7 alert: wrong answer is 2 years (warranty). AC1 alert: 30 days here is the return window, not cloud storage.

---

## INT-003

- **intent_id:** INT-003
- **language:** en
- **query_text:** "What does the NiceHome Sensor measure?"
- **linked_fact_ids:** [F0102]
- **expected_fact_set_id:** INT-003
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** All three measurements required (temperature, humidity, motion). "Detect" is an acceptable paraphrase of "measure" and not embedded in query to avoid answer hinting.

---

## INT-004

- **intent_id:** INT-004
- **language:** en
- **query_text:** "After I return my device, where does my refund go?"
- **linked_fact_ids:** [F0307]
- **expected_fact_set_id:** INT-004
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Refund destination only. Does not ask how long it takes (INT-011 covers that).

---

## INT-005

- **intent_id:** INT-005
- **language:** en
- **query_text:** "I have the Camera Plus Plan. How long are my cloud video recordings kept?"
- **linked_fact_ids:** [F0402]
- **expected_fact_set_id:** INT-005
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Active subscription context stated explicitly. AC1 alert: 30 days here is storage, not return window. AC3 alert: wrong answer is 14 days (trial). AC4: query involves live view context only indirectly — no hint about live view.

---

## INT-006

- **intent_id:** INT-006
- **language:** en
- **query_text:** "How long is the free trial for the Camera Plus Plan?"
- **linked_fact_ids:** [F0405]
- **expected_fact_set_id:** INT-006
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Trial duration only. AC3 alert: wrong answer is 30 days (storage period).

---

## INT-007

- **intent_id:** INT-007
- **language:** en
- **query_text:** "How long does Standard shipping take?"
- **linked_fact_ids:** [F0502]
- **expected_fact_set_id:** INT-007
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Standard" specified explicitly to make this a direct lookup. Wrong answer is Express timeframe (2 business days). "Business days" required in model response.

---

## INT-008

- **intent_id:** INT-008
- **language:** en
- **query_text:** "Can I use the NiceHome Camera outside?"
- **linked_fact_ids:** [F0104]
- **expected_fact_set_id:** INT-008
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Placement query. Tests the "indoor only" constraint. Phrased as a yes/no to trigger the constraint fact.

---

## INT-009

- **intent_id:** INT-009
- **language:** en
- **query_text:** "How long does it typically take to repair a NiceHome device?"
- **linked_fact_ids:** [F0707]
- **expected_fact_set_id:** INT-009
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** "Typically" matches the fact wording and the "after receipt" anchor is required in the model response. Wrong answer is 14 business days (refund processing).

---

## INT-010

- **intent_id:** INT-010
- **language:** en
- **query_text:** "Does NiceHome offer a cloud subscription, and what is it called?"
- **linked_fact_ids:** [F0401]
- **expected_fact_set_id:** INT-010
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Plan name grounding test. "Camera Plus Plan" is the controlled term; fabricated names = FAIL.

---

## INT-011

- **intent_id:** INT-011
- **language:** en
- **query_text:** "How long does it take to receive my refund after I return a device?"
- **linked_fact_ids:** [F0308]
- **expected_fact_set_id:** INT-011
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Refund processing time. "Business days" and "after receipt" required. Wrong answer is 10 business days (repair turnaround).

---

## INT-012

- **intent_id:** INT-012
- **language:** en
- **query_text:** "Can I turn the NiceHome Plug on and off remotely if I don't have a Hub?"
- **linked_fact_ids:** [F0107]
- **expected_fact_set_id:** INT-012
- **difficulty_level:** simple
- **review_status:** draft
- **notes:** Tests the partial-exception fact. Both parts required: on/off works without Hub AND automation requires Hub.

---

## Conditional policy intents (INT-013–INT-024)

---

## INT-013

- **intent_id:** INT-013
- **language:** en
- **query_text:** "I have a Gen 1 Hub. Can I use a Gen 2 NiceHome Sensor with it?"
- **linked_fact_ids:** [F0108, F0109]
- **expected_fact_set_id:** INT-013
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Both conditions stated: Gen 1 Hub, Gen 2 device. AC1 compatibility asymmetry. Expected: NOT compatible; a Gen 2 Hub is required.

---

## INT-014

- **intent_id:** INT-014
- **language:** en
- **query_text:** "I opened my NiceHome Plug but decided I don't want it. It's undamaged and I'm still within the return window. Can I return it, and who pays for return shipping?"
- **linked_fact_ids:** [F0302, F0303]
- **expected_fact_set_id:** INT-014
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** All three conditions stated: opened, undamaged, within window. Three-part answer required: return accepted + full refund + customer pays shipping.

---

## INT-015

- **intent_id:** INT-015
- **language:** en
- **query_text:** "I dropped my NiceHome Camera and now it doesn't work. Does the warranty cover this?"
- **linked_fact_ids:** [F0202, F0203]
- **expected_fact_set_id:** INT-015
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Dropped" makes accidental damage unambiguous. Expected: NOT covered. Applying general coverage (F0202) without the exclusion (F0203) = FAIL.

---

## INT-016

- **intent_id:** INT-016
- **language:** en
- **query_text:** "I opened the casing of my NiceHome Hub and replaced some internal parts. Now it won't work. Does the warranty still apply?"
- **linked_fact_ids:** [F0202, F0204]
- **expected_fact_set_id:** INT-016
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Unauthorized modification stated explicitly. Expected: warranty voided for damage from modification. Both facts required (general coverage + exclusion).

---

## INT-017

- **intent_id:** INT-017
- **language:** en
- **query_text:** "If I cancel my Camera Plus Plan in the middle of a billing period, do I still have access to cloud storage until the end of the period? And will I get a partial refund?"
- **linked_fact_ids:** [F0407, F0408]
- **expected_fact_set_id:** INT-017
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Both sub-questions asked together to require both facts. Both parts required: access continues to period end + no pro-rated refund.

---

## INT-018

- **intent_id:** INT-018
- **language:** en
- **query_text:** "My NiceHome Hub is 3 years old and has a hardware fault. Can it still be repaired, and what would I need to pay?"
- **linked_fact_ids:** [F0702, F0706]
- **expected_fact_set_id:** INT-018
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "3 years old" makes out-of-warranty condition unambiguous (warranty is 2 years). Both components required: service fee + customer pays two-way shipping.

---

## INT-019

- **intent_id:** INT-019
- **language:** en
- **query_text:** "My device is being replaced under warranty and I've been told the replacement will be a refurbished unit. How long will the warranty on the refurbished replacement be?"
- **linked_fact_ids:** [F0704, F0705]
- **expected_fact_set_id:** INT-019
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** AC8 intent. Three FAIL patterns pre-registered: flat 90 days, full 2-year reset, no warranty. Required: "longer of remaining original warranty or 90 days."

---

## INT-020

- **intent_id:** INT-020
- **language:** en
- **query_text:** "I placed an order 4 hours ago and want to cancel it before it ships. Is that still possible?"
- **linked_fact_ids:** [F0505, F0506]
- **expected_fact_set_id:** INT-020
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "4 hours ago" makes the post-window condition explicit. Both components required: no cancel now + return after delivery available.

---

## INT-021

- **intent_id:** INT-021
- **language:** en
- **query_text:** "I want Express shipping for a NiceHome Camera that is currently backordered. Is Express shipping available?"
- **linked_fact_ids:** [F0503, F0504]
- **expected_fact_set_id:** INT-021
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Backordered" makes out-of-stock condition unambiguous. Expected: Express NOT available for backordered items.

---

## INT-022

- **intent_id:** INT-022
- **language:** en
- **query_text:** "I paid for the Camera Plus Plan and want to get a refund through the device return process. Is that possible?"
- **linked_fact_ids:** [F0306, F0408]
- **expected_fact_set_id:** INT-022
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** Subscription refund via return process — cross-document exclusion. Expected: subscriptions not in return scope; cancellation is a separate process.

---

## INT-023

- **intent_id:** INT-023
- **language:** en
- **query_text:** "I cracked the screen of my NiceHome Camera myself. Can I return it for a refund?"
- **linked_fact_ids:** [F0304]
- **expected_fact_set_id:** INT-023
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Myself" makes customer-caused damage unambiguous. Expected: not eligible for return refund.

---

## INT-024

- **intent_id:** INT-024
- **language:** en
- **query_text:** "I upgraded my Camera Plus Plan in the middle of a billing period. When does the new plan take effect?"
- **linked_fact_ids:** [F0409]
- **expected_fact_set_id:** INT-024
- **difficulty_level:** conditional
- **review_status:** draft
- **notes:** "Upgraded" stated (upgrade and downgrade follow the same rule per F0409). Expected: next billing period.

---

## Troubleshooting/process intents (INT-025–INT-036)

---

## INT-025

- **intent_id:** INT-025
- **language:** en
- **query_text:** "My NiceHome devices are all showing as offline. What steps should I take to diagnose and fix the problem?"
- **linked_fact_ids:** [F0601, F0602, F0603, F0604]
- **expected_fact_set_id:** INT-025
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** No prior steps mentioned. Triggers full four-step diagnostic sequence. AC5: step 3 must be "restart," not "factory reset."

---

## INT-026

- **intent_id:** INT-026
- **language:** en
- **query_text:** "How do I add a new NiceHome Sensor to my system?"
- **linked_fact_ids:** [F0606, F0607, F0608]
- **expected_fact_set_id:** INT-026
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC2: "5 seconds" required, not 10. Three ordered steps required. "Add device" in app is step 1.

---

## INT-027

- **intent_id:** INT-027
- **language:** en
- **query_text:** "I followed the pairing steps but my device didn't pair successfully. What should I try next?"
- **linked_fact_ids:** [F0606, F0607, F0608, F0609]
- **expected_fact_set_id:** INT-027
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Pairing failure stated. Expected: check that device is within range of Hub. First-response step must not be factory reset.

---

## INT-028

- **intent_id:** INT-028
- **language:** en
- **query_text:** "My NiceHome Sensor is still under warranty and has stopped working. How do I make a warranty claim?"
- **linked_fact_ids:** [F0205, F0206, F0207, F0208]
- **expected_fact_set_id:** INT-028
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** In-warranty stated. Four ordered steps required; prepaid label required (customer does not pay shipping).

---

## INT-029

- **intent_id:** INT-029
- **language:** en
- **query_text:** "I want to return an unopened NiceHome Hub and I'm still within the return window. What steps do I need to follow?"
- **linked_fact_ids:** [F0309, F0310, F0311]
- **expected_fact_set_id:** INT-029
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Unopened + within window stated. Three ordered steps required; authorization step is critical; shipping without authorization = FAIL.

---

## INT-030

- **intent_id:** INT-030
- **language:** en
- **query_text:** "I forgot my password and can't log in to my account. How do I reset my password?"
- **linked_fact_ids:** [F0801, F0802, F0803]
- **expected_fact_set_id:** INT-030
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Three ordered steps required. Email-link mechanism required. Phone reset = FAIL.

---

## INT-031

- **intent_id:** INT-031
- **language:** en
- **query_text:** "How do I factory reset my NiceHome Hub, and what do I need to do afterward?"
- **linked_fact_ids:** [F0806, F0807]
- **expected_fact_set_id:** INT-031
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC2: "10 seconds" required (not 5). AC9: re-pair requirement must be mentioned (F0807 from D08-S4). Two chunks involved (D08-S3 + D08-S4).

---

## INT-032

- **intent_id:** INT-032
- **language:** en
- **query_text:** "I'm about to factory reset my NiceHome Camera and I'm worried about my cloud video recordings. Will a factory reset delete them?"
- **linked_fact_ids:** [F0804, F0805, F0809]
- **expected_fact_set_id:** INT-032
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** AC9: cloud video not deleted by factory reset (F0809). Both components required: settings/account erased + cloud video not deleted. AC5: factory reset context is explicit.

---

## INT-033

- **intent_id:** INT-033
- **language:** en
- **query_text:** "My NiceHome Plug is completely unresponsive — it won't turn on and doesn't react to the app at all. What should I do?"
- **linked_fact_ids:** [F0610, F0611]
- **expected_fact_set_id:** INT-033
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Full non-response stated. Two ordered steps: (1) app toggle, (2) soft reset. AC5: step 2 is soft reset, not factory reset.

---

## INT-034

- **intent_id:** INT-034
- **language:** en
- **query_text:** "My NiceHome Hub light is blinking red. What does this mean and what should I do?"
- **linked_fact_ids:** [F0605, F0603, F0604]
- **expected_fact_set_id:** INT-034
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Indicator symptom described. Meaning (lost network connection) is required; next step (network/router check) is expected. Misidentifying as hardware failure = FAIL.

---

## INT-035

- **intent_id:** INT-035
- **language:** en
- **query_text:** "My order is well past the estimated delivery window, but it hasn't been confirmed as lost. What am I entitled to — a full refund, a replacement, or something else?"
- **linked_fact_ids:** [F0507, F0508]
- **expected_fact_set_id:** INT-035
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Delay scenario stated explicitly (past window, not confirmed lost). AC6: shipping-fee refund is the applicable remedy, not product replacement. Query mentions both "refund" and "replacement" to surface the distinction.

---

## INT-036

- **intent_id:** INT-036
- **language:** en
- **query_text:** "My NiceHome Camera has been lost or stolen. Can I remove it from my account remotely to prevent unauthorized use?"
- **linked_fact_ids:** [F0808]
- **expected_fact_set_id:** INT-036
- **difficulty_level:** troubleshooting-process
- **review_status:** draft
- **notes:** Lost/stolen stated. Expected: remote removal via app is possible. Physical access required = FAIL.

---

## Quality check

| Check | Result |
|---|---|
| Exactly 36 entries | PASS — INT-001 through INT-036 |
| No fact IDs in query_text | PASS — verified |
| No document/chunk IDs in query_text | PASS — verified |
| No answer hints in query_text | PASS — queries ask, do not guide |
| All conditions preserved for conditional intents | PASS — checked per entry |
| Troubleshooting intents preserve problem state | PASS — checked per entry |
| No systematically over-compressed phrasing | PASS — natural clause structures used throughout |
| Controlled product names used correctly | PASS — NiceHome Hub/Sensor/Plug/Camera; Camera Plus Plan |

---

*Version: qr-en-v0.1.0. English is the analytic baseline; it is not the canonical query source. Dutch and Turkish queries are peer renderings, not translations of this file.*
