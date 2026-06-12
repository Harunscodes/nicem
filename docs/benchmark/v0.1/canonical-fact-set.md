# NiceM Canonical Fact-Set v0.1

**Status:** First real benchmark artifact — the canonical source of truth for all v0.1 KB renderings and intents
**Role:** Language-neutral structured representation of the NiceHome knowledge base. Every KB rendering (English, Dutch, Turkish) and every intent's expected outcome derives from this file.
**Schema:** Defined in `dataset-specification.md` §5
**Version:** fs-v0.1.0 (not yet frozen)
**Depends on:** `dataset-specification.md`
**Feeds into:** `document-plan.md`, `intent-set.md`, `language-rendering-plan.md`, `expected-fact-mapping.md`

---

## How to read this file

This is the **canonical artifact**. It is not English prose pretending to be canonical — it is a structured representation from which all three language renderings (including English) are independently authored. If any KB rendering ever conflicts with a fact here, this file governs.

Each fact follows the schema from `dataset-specification.md` §5. Fields that do not apply to a given fact (e.g., `condition(s)` for a simple fact, `exceptions` where there are none) are marked `—`.

`fact_type` values: **simple** (one entity/attribute, no conditions), **conditional** (preconditions determine the outcome), **sequential** (an ordered step in a procedure), **exception** (a carve-out modifying another fact).

**Methodological note:** This fact-set says nothing about execution-tax. It is benchmark content. Execution-tax remains a hypothesis to be tested by running agents against renderings of this content — not something inferable from the content itself.

---

## Document D01 — Product overview and device compatibility

### F0101
- **document_id:** D01
- **category:** product_description
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** The NiceHome Hub is the central device that manages all other NiceHome devices.
- **exceptions:** —
- **required_entities:** ["NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must identify the Hub as the central/managing device of the NiceHome ecosystem.
- **forbidden_claims:** ["the Sensor is the central device", "no central device is required", "the Camera manages other devices"]
- **ambiguity_notes:** "Central device" should be rendered as a managing/coordinating role, not as a physical-location claim.

### F0102
- **document_id:** D01
- **category:** product_description
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** The NiceHome Sensor measures temperature, humidity, and motion.
- **exceptions:** —
- **required_entities:** ["NiceHome Sensor"]
- **language_neutral_expected_outcome:** Response must state the Sensor measures temperature, humidity, and motion (all three).
- **forbidden_claims:** ["the Sensor records video", "the Sensor measures air quality", "the Sensor measures only temperature"]
- **ambiguity_notes:** All three measurement types are required; omitting one is incomplete, not wrong — flag as evaluation edge in intents that ask for the full list.

### F0103
- **document_id:** D01
- **category:** product_description
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** The NiceHome Plug is a smart power outlet that provides remote switching and energy monitoring.
- **exceptions:** —
- **required_entities:** ["NiceHome Plug"]
- **language_neutral_expected_outcome:** Response must identify the Plug as a smart outlet with remote switching and energy monitoring.
- **forbidden_claims:** ["the Plug includes a camera", "the Plug measures temperature"]
- **ambiguity_notes:** "Energy monitoring" is a measurement capability, not a billing feature.

### F0104
- **document_id:** D01
- **category:** product_description
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** The NiceHome Camera is an indoor security camera that provides motion alerts and live view.
- **exceptions:** F0110 (live view unavailable when Hub offline)
- **required_entities:** ["NiceHome Camera"]
- **language_neutral_expected_outcome:** Response must identify the Camera as an indoor camera with motion alerts and live view.
- **forbidden_claims:** ["the Camera is for outdoor use", "the Camera includes cloud storage by default"]
- **ambiguity_notes:** "Indoor" is a stated constraint; cloud storage is a subscription feature (D04), not a base feature.

### F0105
- **document_id:** D01
- **category:** compatibility
- **fact_type:** conditional
- **condition(s):** ["device is NiceHome Sensor"]
- **rule/action:** The NiceHome Sensor requires a NiceHome Hub to operate; it cannot function without a Hub.
- **exceptions:** —
- **required_entities:** ["NiceHome Sensor", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must state the Sensor requires a Hub and cannot work standalone.
- **forbidden_claims:** ["the Sensor works without a Hub", "the Sensor connects directly to the app without a Hub"]
- **ambiguity_notes:** —

### F0106
- **document_id:** D01
- **category:** compatibility
- **fact_type:** conditional
- **condition(s):** ["device is NiceHome Camera"]
- **rule/action:** The NiceHome Camera requires a NiceHome Hub to operate.
- **exceptions:** —
- **required_entities:** ["NiceHome Camera", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must state the Camera requires a Hub.
- **forbidden_claims:** ["the Camera works without a Hub"]
- **ambiguity_notes:** —

### F0107
- **document_id:** D01
- **category:** compatibility
- **fact_type:** conditional
- **condition(s):** ["device is NiceHome Plug"]
- **rule/action:** The NiceHome Plug supports basic remote on/off switching without a Hub, but requires a Hub for automation features (scheduling and energy monitoring).
- **exceptions:** —
- **required_entities:** ["NiceHome Plug", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must distinguish: basic on/off works without a Hub; automation (scheduling, energy monitoring) requires a Hub.
- **forbidden_claims:** ["the Plug requires a Hub for all functions", "the Plug supports energy monitoring without a Hub"]
- **ambiguity_notes:** This is the only device with partial standalone capability; the distinction is the point of the fact.

### F0108
- **document_id:** D01
- **category:** compatibility
- **fact_type:** conditional
- **condition(s):** ["device is generation Gen 2"]
- **rule/action:** NiceHome devices exist in two generations, Gen 1 and Gen 2. Gen 2 devices require a Gen 2 Hub; a Gen 1 Hub does not support Gen 2 devices.
- **exceptions:** —
- **required_entities:** ["Gen 1", "Gen 2", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must state Gen 2 devices require a Gen 2 Hub and are not supported by a Gen 1 Hub.
- **forbidden_claims:** ["all Hubs support all devices", "Gen 1 Hub supports Gen 2 devices"]
- **ambiguity_notes:** Pairs with F0109 (backward compatibility runs only in one direction). Renderers must keep the asymmetry.

### F0109
- **document_id:** D01
- **category:** compatibility
- **fact_type:** conditional
- **condition(s):** ["Hub is generation Gen 2"]
- **rule/action:** A Gen 2 Hub is backward compatible and supports both Gen 1 and Gen 2 devices.
- **exceptions:** —
- **required_entities:** ["Gen 2", "Gen 1", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must state a Gen 2 Hub supports both Gen 1 and Gen 2 devices.
- **forbidden_claims:** ["a Gen 2 Hub supports only Gen 2 devices", "Gen 2 Hub is not backward compatible"]
- **ambiguity_notes:** Mirror of F0108; together they define a one-directional compatibility rule.

### F0110
- **document_id:** D01
- **category:** compatibility
- **fact_type:** exception
- **condition(s):** ["Hub is offline"]
- **rule/action:** Camera live view is not available while the Hub is offline.
- **exceptions:** Modifies F0104.
- **required_entities:** ["NiceHome Camera", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must state live view does not work when the Hub is offline.
- **forbidden_claims:** ["live view works without the Hub", "the Camera works fully when the Hub is offline"]
- **ambiguity_notes:** Distinct from subscription/cloud storage (D04); this is about live view, not recordings.

---

## Document D02 — Warranty policy

### F0201
- **document_id:** D02
- **category:** warranty_coverage
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** All NiceHome devices include a standard warranty of 2 years from the date of purchase.
- **exceptions:** —
- **required_entities:** ["NiceHome", "2 years"]
- **language_neutral_expected_outcome:** Response must state the standard warranty period is 2 years from purchase, applying to all devices.
- **forbidden_claims:** ["warranty is 1 year", "warranty is lifetime", "warranty differs by device"]
- **ambiguity_notes:** Period is relative ("2 years from purchase"); evaluation checks the period, not a computed expiry date.

### F0202
- **document_id:** D02
- **category:** warranty_coverage
- **fact_type:** conditional
- **condition(s):** ["failure occurs under normal use"]
- **rule/action:** The warranty covers manufacturing defects and hardware failures that occur under normal use.
- **exceptions:** F0203, F0204
- **required_entities:** ["manufacturing defect", "hardware failure"]
- **language_neutral_expected_outcome:** Response must state the warranty covers manufacturing defects and hardware failures under normal use.
- **forbidden_claims:** ["warranty covers all damage", "warranty covers accidental damage"]
- **ambiguity_notes:** "Normal use" is the gating condition; pairs with the exclusion facts F0203/F0204.

### F0203
- **document_id:** D02
- **category:** warranty_exclusion
- **fact_type:** exception
- **condition(s):** ["damage is accidental"]
- **rule/action:** The warranty does not cover accidental damage.
- **exceptions:** Modifies F0202.
- **required_entities:** ["accidental damage"]
- **language_neutral_expected_outcome:** Response must state accidental damage is not covered by the warranty.
- **forbidden_claims:** ["accidental damage is covered", "all damage is covered under warranty"]
- **ambiguity_notes:** Connects to repair policy F0708 (accidental/liquid damage needs out-of-warranty quote).

### F0204
- **document_id:** D02
- **category:** warranty_exclusion
- **fact_type:** exception
- **condition(s):** ["damage results from misuse or unauthorized modification"]
- **rule/action:** The warranty does not cover damage caused by misuse or unauthorized modification of the device.
- **exceptions:** Modifies F0202.
- **required_entities:** ["misuse", "unauthorized modification"]
- **language_neutral_expected_outcome:** Response must state misuse and unauthorized modification void warranty coverage for the resulting damage.
- **forbidden_claims:** ["misuse is covered", "modifications do not affect warranty"]
- **ambiguity_notes:** —

### F0205
- **document_id:** D02
- **category:** warranty_claim
- **fact_type:** conditional
- **condition(s):** ["customer makes a warranty claim"]
- **rule/action:** To make a warranty claim, the customer must provide proof of purchase.
- **exceptions:** —
- **required_entities:** ["proof of purchase"]
- **language_neutral_expected_outcome:** Response must state proof of purchase is required to make a warranty claim.
- **forbidden_claims:** ["no proof of purchase is needed", "serial number alone is never required"]
- **ambiguity_notes:** Distinct from the serial number required in the claim process (F0206).

### F0206
- **document_id:** D02
- **category:** warranty_claim
- **fact_type:** sequential
- **condition(s):** ["warranty claim process", "step 1"]
- **rule/action:** Warranty claim step 1: contact NiceHome support with the device serial number.
- **exceptions:** —
- **required_entities:** ["NiceHome support", "device serial number"]
- **language_neutral_expected_outcome:** Response must identify contacting support with the serial number as the first claim step.
- **forbidden_claims:** ["ship the device first without contacting support"]
- **ambiguity_notes:** Ordered step; precedes F0207.

### F0207
- **document_id:** D02
- **category:** warranty_claim
- **fact_type:** sequential
- **condition(s):** ["warranty claim process", "step 2", "step 1 completed"]
- **rule/action:** Warranty claim step 2: support issues a warranty claim reference and a prepaid shipping label.
- **exceptions:** —
- **required_entities:** ["warranty claim reference", "prepaid shipping label"]
- **language_neutral_expected_outcome:** Response must state that, after contact, support provides a claim reference and prepaid label.
- **forbidden_claims:** ["the customer pays for warranty shipping"]
- **ambiguity_notes:** Prepaid label distinguishes in-warranty (free) from out-of-warranty repair shipping (F0706).

### F0208
- **document_id:** D02
- **category:** warranty_claim
- **fact_type:** sequential
- **condition(s):** ["warranty claim process", "step 3", "step 2 completed"]
- **rule/action:** Warranty claim step 3: the customer ships the device using the prepaid label, including the claim reference.
- **exceptions:** —
- **required_entities:** ["prepaid shipping label", "warranty claim reference"]
- **language_neutral_expected_outcome:** Response must identify shipping the device with the prepaid label and claim reference as the final claim step.
- **forbidden_claims:** ["the device does not need to be shipped"]
- **ambiguity_notes:** —

### F0209
- **document_id:** D02
- **category:** warranty_outcome
- **fact_type:** conditional
- **condition(s):** ["covered defect is confirmed"]
- **rule/action:** If a covered defect is confirmed, the device is repaired or replaced at no cost to the customer.
- **exceptions:** —
- **required_entities:** ["repair", "replacement"]
- **language_neutral_expected_outcome:** Response must state a confirmed covered defect leads to free repair or replacement.
- **forbidden_claims:** ["the customer always pays a fee", "only repair is offered, never replacement"]
- **ambiguity_notes:** Connects to repair policy F0701/F0703.

---

## Document D03 — Return and refund policy

### F0301
- **document_id:** D03
- **category:** return_window
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** The return window is 30 days from the date of purchase.
- **exceptions:** —
- **required_entities:** ["30 days"]
- **language_neutral_expected_outcome:** Response must state the return window is 30 days from purchase.
- **forbidden_claims:** ["return window is 14 days", "return window is 60 days", "window runs from delivery date"]
- **ambiguity_notes:** Window runs from purchase, not delivery — a common confusion; flag in intents.

### F0302
- **document_id:** D03
- **category:** return_condition
- **fact_type:** conditional
- **condition(s):** ["device is unopened", "within 30 days of purchase"]
- **rule/action:** An unopened device returned within 30 days receives a full refund with free return shipping.
- **exceptions:** F0304, F0306
- **required_entities:** ["full refund", "free return shipping"]
- **language_neutral_expected_outcome:** Response must state unopened + within window → full refund and free return shipping.
- **forbidden_claims:** ["a restocking fee applies to unopened returns", "unopened devices cannot be returned"]
- **ambiguity_notes:** Contrast with F0303 (opened pays its own return shipping).

### F0303
- **document_id:** D03
- **category:** return_condition
- **fact_type:** conditional
- **condition(s):** ["device is opened", "device is undamaged", "within 30 days of purchase"]
- **rule/action:** An opened but undamaged device returned within 30 days receives a full refund, but the customer pays return shipping.
- **exceptions:** F0304, F0306
- **required_entities:** ["full refund", "return shipping"]
- **language_neutral_expected_outcome:** Response must state opened + undamaged + within window → full refund, customer pays return shipping.
- **forbidden_claims:** ["opened devices get only partial refund", "opened devices cannot be returned"]
- **ambiguity_notes:** The shipping-cost difference vs. F0302 is the key distinction; refund amount is full in both.

### F0304
- **document_id:** D03
- **category:** return_exclusion
- **fact_type:** exception
- **condition(s):** ["device is damaged by the customer"]
- **rule/action:** A device damaged by the customer is not eligible for a refund, unless the damage is covered under warranty.
- **exceptions:** Modifies F0302, F0303.
- **required_entities:** ["customer damage", "warranty"]
- **language_neutral_expected_outcome:** Response must state customer-damaged devices are not refundable except where warranty applies.
- **forbidden_claims:** ["all returns are refunded regardless of damage"]
- **ambiguity_notes:** Boundary between return policy and warranty (D02) — keep both paths explicit.

### F0305
- **document_id:** D03
- **category:** return_window
- **fact_type:** conditional
- **condition(s):** ["more than 30 days since purchase"]
- **rule/action:** Returns are not accepted after 30 days from purchase.
- **exceptions:** —
- **required_entities:** ["30 days"]
- **language_neutral_expected_outcome:** Response must state returns after 30 days are not accepted.
- **forbidden_claims:** ["late returns are accepted with a fee", "returns are accepted anytime"]
- **ambiguity_notes:** Warranty (2 years) is separate from returns (30 days) — do not conflate.

### F0306
- **document_id:** D03
- **category:** return_exclusion
- **fact_type:** exception
- **condition(s):** ["item is a subscription plan"]
- **rule/action:** Subscription plans are not refundable through the device return process; subscription cancellation is handled separately.
- **exceptions:** Modifies F0302, F0303.
- **required_entities:** ["subscription plan"]
- **language_neutral_expected_outcome:** Response must state subscriptions are not refunded via device returns and are handled by cancellation rules.
- **forbidden_claims:** ["subscriptions can be returned for a refund like a device"]
- **ambiguity_notes:** Cross-references D04 (F0407, F0408).

### F0307
- **document_id:** D03
- **category:** refund_process
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Refunds are issued to the original payment method.
- **exceptions:** —
- **required_entities:** ["original payment method"]
- **language_neutral_expected_outcome:** Response must state refunds go to the original payment method.
- **forbidden_claims:** ["refunds are issued as store credit only", "refunds go to any chosen method"]
- **ambiguity_notes:** —

### F0308
- **document_id:** D03
- **category:** refund_process
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Refunds are processed within 14 business days after the returned device is received.
- **exceptions:** —
- **required_entities:** ["14 business days"]
- **language_neutral_expected_outcome:** Response must state refunds are processed within 14 business days of receipt of the returned device.
- **forbidden_claims:** ["refunds are instant", "refunds take 60 days"]
- **ambiguity_notes:** "Business days" not calendar days; clock starts at receipt, not at return request.

### F0309
- **document_id:** D03
- **category:** return_process
- **fact_type:** sequential
- **condition(s):** ["return process", "step 1"]
- **rule/action:** Return step 1: request a return authorization from NiceHome support.
- **exceptions:** —
- **required_entities:** ["return authorization", "NiceHome support"]
- **language_neutral_expected_outcome:** Response must identify requesting a return authorization as the first return step.
- **forbidden_claims:** ["ship the device back without authorization"]
- **ambiguity_notes:** —

### F0310
- **document_id:** D03
- **category:** return_process
- **fact_type:** sequential
- **condition(s):** ["return process", "step 2", "step 1 completed"]
- **rule/action:** Return step 2: receive a return authorization number and shipping instructions.
- **exceptions:** —
- **required_entities:** ["return authorization number", "shipping instructions"]
- **language_neutral_expected_outcome:** Response must state the customer receives a return authorization number and instructions after the request.
- **forbidden_claims:** ["no authorization number is issued"]
- **ambiguity_notes:** —

### F0311
- **document_id:** D03
- **category:** return_process
- **fact_type:** sequential
- **condition(s):** ["return process", "step 3", "step 2 completed"]
- **rule/action:** Return step 3: ship the device with the return authorization number included.
- **exceptions:** —
- **required_entities:** ["return authorization number"]
- **language_neutral_expected_outcome:** Response must identify shipping the device with the authorization number as the final return step.
- **forbidden_claims:** ["the authorization number is not needed when shipping"]
- **ambiguity_notes:** —

---

## Document D04 — Subscription plan rules

### F0401
- **document_id:** D04
- **category:** subscription_feature
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** NiceHome offers a cloud subscription called the Camera Plus Plan.
- **exceptions:** —
- **required_entities:** ["Camera Plus Plan"]
- **language_neutral_expected_outcome:** Response must name the Camera Plus Plan as the cloud subscription.
- **forbidden_claims:** ["there is no subscription plan", "the plan is called something else"]
- **ambiguity_notes:** Plan name is fixed terminology; renderers use the controlled term per `language-rendering-plan.md`.

### F0402
- **document_id:** D04
- **category:** subscription_feature
- **fact_type:** conditional
- **condition(s):** ["account has Camera Plus Plan"]
- **rule/action:** The Camera Plus Plan provides 30 days of cloud video storage for the NiceHome Camera.
- **exceptions:** —
- **required_entities:** ["Camera Plus Plan", "NiceHome Camera", "30 days"]
- **language_neutral_expected_outcome:** Response must state the plan provides 30 days of cloud video storage for the Camera.
- **forbidden_claims:** ["unlimited cloud storage", "7 days of storage", "storage for all devices"]
- **ambiguity_notes:** Storage applies to Camera video only, not Sensor or Plug data.

### F0403
- **document_id:** D04
- **category:** subscription_feature
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Without a subscription, the NiceHome Camera supports live view but not cloud video storage.
- **exceptions:** —
- **required_entities:** ["NiceHome Camera", "live view", "cloud video storage"]
- **language_neutral_expected_outcome:** Response must state that without a subscription, live view works but cloud storage does not.
- **forbidden_claims:** ["live view requires a subscription", "the Camera is unusable without a subscription"]
- **ambiguity_notes:** Distinguish from F0110 (live view also depends on Hub being online). Both conditions are independent.

### F0404
- **document_id:** D04
- **category:** subscription_eligibility
- **fact_type:** conditional
- **condition(s):** ["account subscribes to Camera Plus Plan"]
- **rule/action:** The Camera Plus Plan requires a NiceHome Camera and a NiceHome Hub.
- **exceptions:** —
- **required_entities:** ["Camera Plus Plan", "NiceHome Camera", "NiceHome Hub"]
- **language_neutral_expected_outcome:** Response must state the plan requires both a Camera and a Hub.
- **forbidden_claims:** ["the plan works without a Camera", "the plan does not need a Hub"]
- **ambiguity_notes:** —

### F0405
- **document_id:** D04
- **category:** subscription_trial
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** The Camera Plus Plan includes a free trial lasting 14 days.
- **exceptions:** F0406
- **required_entities:** ["Camera Plus Plan", "14 days"]
- **language_neutral_expected_outcome:** Response must state the free trial lasts 14 days.
- **forbidden_claims:** ["the trial is 30 days", "there is no free trial"]
- **ambiguity_notes:** Trial length (14 days) differs from storage length (30 days) — do not confuse the two numbers.

### F0406
- **document_id:** D04
- **category:** subscription_trial
- **fact_type:** conditional
- **condition(s):** ["account has previously used the free trial"]
- **rule/action:** The free trial can be used only once per account.
- **exceptions:** —
- **required_entities:** ["free trial", "account"]
- **language_neutral_expected_outcome:** Response must state the free trial is limited to once per account.
- **forbidden_claims:** ["the trial can be renewed repeatedly"]
- **ambiguity_notes:** —

### F0407
- **document_id:** D04
- **category:** subscription_cancellation
- **fact_type:** conditional
- **condition(s):** ["subscription is cancelled"]
- **rule/action:** If the subscription is cancelled, cloud storage access continues until the end of the current billing period.
- **exceptions:** F0408
- **required_entities:** ["subscription", "billing period"]
- **language_neutral_expected_outcome:** Response must state access continues to the end of the current billing period after cancellation.
- **forbidden_claims:** ["access ends immediately on cancellation", "cancellation deletes video immediately"]
- **ambiguity_notes:** Pairs with F0408 (no refund) — cancellation does not equal immediate termination, but also does not equal a refund.

### F0408
- **document_id:** D04
- **category:** subscription_cancellation
- **fact_type:** exception
- **condition(s):** ["subscription is cancelled mid-period"]
- **rule/action:** Cancelled subscriptions do not receive a pro-rated refund for the current billing period.
- **exceptions:** Modifies F0407.
- **required_entities:** ["subscription", "billing period"]
- **language_neutral_expected_outcome:** Response must state no pro-rated refund is given for the current period on cancellation.
- **forbidden_claims:** ["cancellation gives a partial refund"]
- **ambiguity_notes:** Cross-references return policy F0306 (subscriptions not refundable via returns).

### F0409
- **document_id:** D04
- **category:** subscription_change
- **fact_type:** conditional
- **condition(s):** ["subscription plan is changed"]
- **rule/action:** Subscription plan changes (upgrade or downgrade) take effect at the start of the next billing period.
- **exceptions:** —
- **required_entities:** ["subscription", "billing period"]
- **language_neutral_expected_outcome:** Response must state plan changes take effect at the next billing period.
- **forbidden_claims:** ["plan changes take effect immediately"]
- **ambiguity_notes:** —

---

## Document D05 — Shipping and delivery policy

### F0501
- **document_id:** D05
- **category:** shipping_method
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Two shipping methods are available: Standard and Express.
- **exceptions:** —
- **required_entities:** ["Standard shipping", "Express shipping"]
- **language_neutral_expected_outcome:** Response must identify Standard and Express as the two shipping methods.
- **forbidden_claims:** ["only one shipping method exists", "overnight shipping is available"]
- **ambiguity_notes:** Method names are controlled terms; renderers keep them consistent.

### F0502
- **document_id:** D05
- **category:** shipping_timeframe
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Standard shipping is delivered within 5 to 7 business days.
- **exceptions:** —
- **required_entities:** ["Standard shipping", "5 to 7 business days"]
- **language_neutral_expected_outcome:** Response must state Standard shipping takes 5 to 7 business days.
- **forbidden_claims:** ["Standard shipping is same-day", "Standard takes 2 days"]
- **ambiguity_notes:** Business days, not calendar days.

### F0503
- **document_id:** D05
- **category:** shipping_timeframe
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Express shipping is delivered within 2 business days.
- **exceptions:** F0504
- **required_entities:** ["Express shipping", "2 business days"]
- **language_neutral_expected_outcome:** Response must state Express shipping takes 2 business days.
- **forbidden_claims:** ["Express is instant", "Express takes a week"]
- **ambiguity_notes:** Business days, not calendar days.

### F0504
- **document_id:** D05
- **category:** shipping_eligibility
- **fact_type:** conditional
- **condition(s):** ["item is in stock"]
- **rule/action:** Express shipping is available only for in-stock items.
- **exceptions:** —
- **required_entities:** ["Express shipping", "in-stock item"]
- **language_neutral_expected_outcome:** Response must state Express requires the item to be in stock.
- **forbidden_claims:** ["Express is available for backordered items"]
- **ambiguity_notes:** —

### F0505
- **document_id:** D05
- **category:** order_modification
- **fact_type:** conditional
- **condition(s):** ["within 2 hours of placing the order"]
- **rule/action:** An order can be modified or cancelled within 2 hours of being placed.
- **exceptions:** F0506
- **required_entities:** ["2 hours", "order"]
- **language_neutral_expected_outcome:** Response must state orders can be modified or cancelled within 2 hours of placement.
- **forbidden_claims:** ["orders can be cancelled anytime before shipping", "orders cannot be changed at all"]
- **ambiguity_notes:** Window runs from order placement, not from shipping.

### F0506
- **document_id:** D05
- **category:** order_modification
- **fact_type:** exception
- **condition(s):** ["more than 2 hours since the order was placed"]
- **rule/action:** After 2 hours, an order cannot be cancelled, but the device can be returned after delivery under the return policy.
- **exceptions:** Modifies F0505.
- **required_entities:** ["order", "return policy"]
- **language_neutral_expected_outcome:** Response must state that after 2 hours cancellation is unavailable but post-delivery return remains possible.
- **forbidden_claims:** ["the order can still be cancelled after 2 hours", "no recourse exists after 2 hours"]
- **ambiguity_notes:** Bridges shipping (D05) and returns (D03).

### F0507
- **document_id:** D05
- **category:** shipping_problem
- **fact_type:** conditional
- **condition(s):** ["shipment is delayed beyond the estimated window"]
- **rule/action:** If a shipment is delayed beyond its estimated delivery window, the customer may request a refund of the shipping fee.
- **exceptions:** —
- **required_entities:** ["shipping fee", "estimated delivery window"]
- **language_neutral_expected_outcome:** Response must state a delayed shipment entitles the customer to request a shipping-fee refund.
- **forbidden_claims:** ["a delay refunds the full order", "no compensation for delays"]
- **ambiguity_notes:** Only the shipping fee is refundable here, not the product price.

### F0508
- **document_id:** D05
- **category:** shipping_problem
- **fact_type:** conditional
- **condition(s):** ["shipment is lost in transit"]
- **rule/action:** If a shipment is lost in transit, a replacement is sent at no additional cost.
- **exceptions:** —
- **required_entities:** ["replacement", "lost shipment"]
- **language_neutral_expected_outcome:** Response must state a lost shipment results in a free replacement.
- **forbidden_claims:** ["the customer must repurchase a lost item", "lost shipments are only partially refunded"]
- **ambiguity_notes:** Distinguish "lost" (F0508, replacement) from "delayed" (F0507, shipping-fee refund).

---

## Document D06 — Troubleshooting guide

### F0601
- **document_id:** D06
- **category:** troubleshooting_connectivity
- **fact_type:** sequential
- **condition(s):** ["connectivity issue", "step 1"]
- **rule/action:** Connectivity troubleshooting step 1: check that the Hub power light is on.
- **exceptions:** —
- **required_entities:** ["NiceHome Hub", "power light"]
- **language_neutral_expected_outcome:** Response must identify checking the Hub power light as the first connectivity step.
- **forbidden_claims:** ["reset the Hub first", "replace the Hub first"]
- **ambiguity_notes:** First step in an ordered sequence F0601→F0604.

### F0602
- **document_id:** D06
- **category:** troubleshooting_connectivity
- **fact_type:** sequential
- **condition(s):** ["connectivity issue", "step 2", "Hub power light is off"]
- **rule/action:** Connectivity step 2: if the Hub power light is off, check the power cable and the outlet.
- **exceptions:** —
- **required_entities:** ["power cable", "outlet"]
- **language_neutral_expected_outcome:** Response must state that if the light is off, the next action is checking the power cable and outlet.
- **forbidden_claims:** ["if the light is off, contact support immediately"]
- **ambiguity_notes:** Conditional on the result of step 1.

### F0603
- **document_id:** D06
- **category:** troubleshooting_connectivity
- **fact_type:** sequential
- **condition(s):** ["connectivity issue", "step 3", "Hub power light is on", "devices offline"]
- **rule/action:** Connectivity step 3: if the light is on but devices are offline, restart the Hub.
- **exceptions:** —
- **required_entities:** ["NiceHome Hub", "restart"]
- **language_neutral_expected_outcome:** Response must state that if the light is on but devices are offline, restarting the Hub is the next step.
- **forbidden_claims:** ["factory reset the Hub at this step"]
- **ambiguity_notes:** Restart (F0603) is not a factory reset (F0806); keep them distinct.

### F0604
- **document_id:** D06
- **category:** troubleshooting_connectivity
- **fact_type:** sequential
- **condition(s):** ["connectivity issue", "step 4", "devices still offline after restart"]
- **rule/action:** Connectivity step 4: if devices remain offline after restarting the Hub, check the home network and router.
- **exceptions:** —
- **required_entities:** ["home network", "router"]
- **language_neutral_expected_outcome:** Response must state that if devices stay offline after restart, the next step is checking the home network/router.
- **forbidden_claims:** ["replace the devices at this step"]
- **ambiguity_notes:** Final diagnostic step before escalation (F0613).

### F0605
- **document_id:** D06
- **category:** troubleshooting_connectivity
- **fact_type:** conditional
- **condition(s):** ["Hub light is blinking red"]
- **rule/action:** A blinking red Hub light indicates the Hub has lost its network connection.
- **exceptions:** —
- **required_entities:** ["NiceHome Hub", "blinking red light"]
- **language_neutral_expected_outcome:** Response must state a blinking red light means lost network connection.
- **forbidden_claims:** ["blinking red means hardware failure", "blinking red means the Hub is updating"]
- **ambiguity_notes:** Specific indicator state; do not confuse with other light states.

### F0606
- **document_id:** D06
- **category:** troubleshooting_pairing
- **fact_type:** sequential
- **condition(s):** ["pairing process", "step 1"]
- **rule/action:** Pairing step 1: open the NiceHome app and select "Add device".
- **exceptions:** —
- **required_entities:** ["NiceHome app", "Add device"]
- **language_neutral_expected_outcome:** Response must identify opening the app and selecting "Add device" as the first pairing step.
- **forbidden_claims:** ["hold the device button first before opening the app"]
- **ambiguity_notes:** —

### F0607
- **document_id:** D06
- **category:** troubleshooting_pairing
- **fact_type:** sequential
- **condition(s):** ["pairing process", "step 2", "step 1 completed"]
- **rule/action:** Pairing step 2: put the device into pairing mode by holding its setup button for 5 seconds.
- **exceptions:** —
- **required_entities:** ["setup button", "5 seconds"]
- **language_neutral_expected_outcome:** Response must state pairing mode is entered by holding the setup button for 5 seconds.
- **forbidden_claims:** ["hold the button for 10 seconds", "no button press is needed"]
- **ambiguity_notes:** 5-second pairing hold differs from 10-second Hub factory-reset hold (F0806); keep durations distinct.

### F0608
- **document_id:** D06
- **category:** troubleshooting_pairing
- **fact_type:** sequential
- **condition(s):** ["pairing process", "step 3", "step 2 completed"]
- **rule/action:** Pairing step 3: follow the app prompts to complete pairing.
- **exceptions:** —
- **required_entities:** ["NiceHome app", "app prompts"]
- **language_neutral_expected_outcome:** Response must identify following the app prompts as the final pairing step.
- **forbidden_claims:** ["pairing completes automatically without app prompts"]
- **ambiguity_notes:** —

### F0609
- **document_id:** D06
- **category:** troubleshooting_pairing
- **fact_type:** conditional
- **condition(s):** ["pairing fails"]
- **rule/action:** If pairing fails, ensure the device is within range of the Hub.
- **exceptions:** —
- **required_entities:** ["NiceHome Hub", "range"]
- **language_neutral_expected_outcome:** Response must state that on pairing failure, the device should be brought within Hub range.
- **forbidden_claims:** ["pairing failure always means a defective device"]
- **ambiguity_notes:** —

### F0610
- **document_id:** D06
- **category:** troubleshooting_power
- **fact_type:** conditional
- **condition(s):** ["Plug does not respond"]
- **rule/action:** If a NiceHome Plug does not respond, toggle it off and on from the app.
- **exceptions:** —
- **required_entities:** ["NiceHome Plug", "NiceHome app"]
- **language_neutral_expected_outcome:** Response must state the first action for an unresponsive Plug is toggling it off/on in the app.
- **forbidden_claims:** ["factory reset the Plug first"]
- **ambiguity_notes:** Precedes the soft reset in F0611.

### F0611
- **document_id:** D06
- **category:** troubleshooting_power
- **fact_type:** conditional
- **condition(s):** ["Plug still does not respond after app toggle"]
- **rule/action:** If a NiceHome Plug still does not respond after toggling, perform a soft reset of the Plug.
- **exceptions:** —
- **required_entities:** ["NiceHome Plug", "soft reset"]
- **language_neutral_expected_outcome:** Response must state that if toggling fails, a soft reset is the next step.
- **forbidden_claims:** ["perform a factory reset as the immediate next step"]
- **ambiguity_notes:** Soft reset (F0804) preserves settings; do not escalate to factory reset here.

### F0612
- **document_id:** D06
- **category:** troubleshooting_sensor
- **fact_type:** conditional
- **condition(s):** ["Sensor readings appear inaccurate"]
- **rule/action:** If NiceHome Sensor readings appear inaccurate, recalibrate the Sensor from the app settings.
- **exceptions:** —
- **required_entities:** ["NiceHome Sensor", "recalibrate", "app settings"]
- **language_neutral_expected_outcome:** Response must state inaccurate Sensor readings are addressed by recalibrating from app settings.
- **forbidden_claims:** ["replace the Sensor immediately", "inaccurate readings cannot be fixed"]
- **ambiguity_notes:** —

### F0613
- **document_id:** D06
- **category:** troubleshooting_escalation
- **fact_type:** conditional
- **condition(s):** ["troubleshooting steps do not resolve the issue"]
- **rule/action:** If the troubleshooting steps do not resolve an issue, contact NiceHome support.
- **exceptions:** —
- **required_entities:** ["NiceHome support"]
- **language_neutral_expected_outcome:** Response must state that unresolved issues should be escalated to NiceHome support.
- **forbidden_claims:** ["the customer must repair the device themselves", "there is no support escalation path"]
- **ambiguity_notes:** Generic terminal escalation for all D06 paths.

---

## Document D07 — Repair and replacement policy

### F0701
- **document_id:** D07
- **category:** repair_eligibility
- **fact_type:** conditional
- **condition(s):** ["device is in warranty", "defect is covered"]
- **rule/action:** An in-warranty device with a covered defect is repaired or replaced at no cost.
- **exceptions:** F0708
- **required_entities:** ["warranty", "repair", "replacement"]
- **language_neutral_expected_outcome:** Response must state in-warranty covered defects are repaired or replaced free of charge.
- **forbidden_claims:** ["in-warranty repairs always cost a fee"]
- **ambiguity_notes:** Aligns with warranty outcome F0209.

### F0702
- **document_id:** D07
- **category:** repair_eligibility
- **fact_type:** conditional
- **condition(s):** ["device is out of warranty"]
- **rule/action:** An out-of-warranty device may be repaired for a service fee.
- **exceptions:** —
- **required_entities:** ["out of warranty", "service fee"]
- **language_neutral_expected_outcome:** Response must state out-of-warranty repairs are available for a service fee.
- **forbidden_claims:** ["out-of-warranty repairs are free", "out-of-warranty devices cannot be repaired"]
- **ambiguity_notes:** No specific fee amount is stated; do not invent one.

### F0703
- **document_id:** D07
- **category:** repair_outcome
- **fact_type:** conditional
- **condition(s):** ["device is in warranty", "device cannot be repaired"]
- **rule/action:** If an in-warranty device cannot be repaired, it is replaced.
- **exceptions:** —
- **required_entities:** ["warranty", "replacement"]
- **language_neutral_expected_outcome:** Response must state an unrepairable in-warranty device is replaced.
- **forbidden_claims:** ["unrepairable devices are refunded in cash by default"]
- **ambiguity_notes:** —

### F0704
- **document_id:** D07
- **category:** repair_outcome
- **fact_type:** conditional
- **condition(s):** ["device is replaced"]
- **rule/action:** A replacement device may be either new or refurbished.
- **exceptions:** —
- **required_entities:** ["replacement", "refurbished"]
- **language_neutral_expected_outcome:** Response must state replacements may be new or refurbished.
- **forbidden_claims:** ["replacements are always new", "replacements are always refurbished"]
- **ambiguity_notes:** —

### F0705
- **document_id:** D07
- **category:** repair_warranty
- **fact_type:** conditional
- **condition(s):** ["replacement is refurbished"]
- **rule/action:** A refurbished replacement carries the remainder of the original warranty, with a minimum of 90 days.
- **exceptions:** —
- **required_entities:** ["refurbished", "original warranty", "90 days"]
- **language_neutral_expected_outcome:** Response must state a refurbished replacement keeps the remaining original warranty, at least 90 days.
- **forbidden_claims:** ["a refurbished replacement has no warranty", "the warranty resets to a full 2 years"]
- **ambiguity_notes:** "Remainder of original warranty OR 90 days, whichever is longer" — keep the minimum-floor meaning.

### F0706
- **document_id:** D07
- **category:** repair_cost
- **fact_type:** conditional
- **condition(s):** ["repair is out of warranty"]
- **rule/action:** For out-of-warranty repairs, the customer pays shipping both ways.
- **exceptions:** —
- **required_entities:** ["out of warranty", "shipping"]
- **language_neutral_expected_outcome:** Response must state out-of-warranty repair shipping is paid by the customer in both directions.
- **forbidden_claims:** ["out-of-warranty shipping is free", "the customer pays one-way only"]
- **ambiguity_notes:** Contrast with in-warranty prepaid label (F0207).

### F0707
- **document_id:** D07
- **category:** repair_process
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** Repair turnaround is typically 10 business days after the device is received.
- **exceptions:** —
- **required_entities:** ["10 business days"]
- **language_neutral_expected_outcome:** Response must state repair turnaround is about 10 business days after receipt.
- **forbidden_claims:** ["repairs are same-day", "repairs take several months"]
- **ambiguity_notes:** "Typically" signals an estimate; business days, measured from receipt.

### F0708
- **document_id:** D07
- **category:** repair_exclusion
- **fact_type:** exception
- **condition(s):** ["device has accidental or liquid damage"]
- **rule/action:** Devices with accidental or liquid damage are not eligible for standard repair and require an out-of-warranty service quote.
- **exceptions:** Modifies F0701.
- **required_entities:** ["accidental damage", "liquid damage", "out-of-warranty service quote"]
- **language_neutral_expected_outcome:** Response must state accidental/liquid damage needs an out-of-warranty service quote, not standard repair.
- **forbidden_claims:** ["liquid damage is covered by standard warranty repair"]
- **ambiguity_notes:** Connects to warranty exclusion F0203.

### F0709
- **document_id:** D07
- **category:** repair_process
- **fact_type:** sequential
- **condition(s):** ["repair request", "step 1"]
- **rule/action:** Repair request step 1: contact NiceHome support and describe the issue to receive a repair reference and shipping instructions.
- **exceptions:** —
- **required_entities:** ["NiceHome support", "repair reference", "shipping instructions"]
- **language_neutral_expected_outcome:** Response must identify contacting support (to get a repair reference and instructions) as the first repair step.
- **forbidden_claims:** ["ship the device without contacting support first"]
- **ambiguity_notes:** Single-step entry point; full process detail is deferred to later artifacts.

---

## Document D08 — Account access and device reset policy

### F0801
- **document_id:** D08
- **category:** account_recovery
- **fact_type:** sequential
- **condition(s):** ["password recovery", "step 1"]
- **rule/action:** Password recovery step 1: select "Forgot password" on the sign-in screen.
- **exceptions:** —
- **required_entities:** ["Forgot password", "sign-in screen"]
- **language_neutral_expected_outcome:** Response must identify selecting "Forgot password" as the first recovery step.
- **forbidden_claims:** ["contact support to reset every password"]
- **ambiguity_notes:** —

### F0802
- **document_id:** D08
- **category:** account_recovery
- **fact_type:** sequential
- **condition(s):** ["password recovery", "step 2", "step 1 completed"]
- **rule/action:** Password recovery step 2: enter the account email to receive a reset link.
- **exceptions:** —
- **required_entities:** ["account email", "reset link"]
- **language_neutral_expected_outcome:** Response must state entering the account email to receive a reset link is the second step.
- **forbidden_claims:** ["a reset code is sent by phone"]
- **ambiguity_notes:** —

### F0803
- **document_id:** D08
- **category:** account_recovery
- **fact_type:** sequential
- **condition(s):** ["password recovery", "step 3", "step 2 completed"]
- **rule/action:** Password recovery step 3: follow the reset link to set a new password.
- **exceptions:** —
- **required_entities:** ["reset link", "new password"]
- **language_neutral_expected_outcome:** Response must identify following the reset link to set a new password as the final step.
- **forbidden_claims:** ["the old password is emailed back to the user"]
- **ambiguity_notes:** —

### F0804
- **document_id:** D08
- **category:** device_reset
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** A soft reset restarts a device without deleting its settings.
- **exceptions:** —
- **required_entities:** ["soft reset"]
- **language_neutral_expected_outcome:** Response must state a soft reset restarts the device and keeps its settings.
- **forbidden_claims:** ["a soft reset erases all settings", "a soft reset unlinks the device"]
- **ambiguity_notes:** Explicit contrast with factory reset (F0805) — the distinction is the point.

### F0805
- **document_id:** D08
- **category:** device_reset
- **fact_type:** simple
- **condition(s):** —
- **rule/action:** A factory reset erases all device settings and unlinks the device from the account.
- **exceptions:** F0809
- **required_entities:** ["factory reset", "account"]
- **language_neutral_expected_outcome:** Response must state a factory reset erases all settings and unlinks the device from the account.
- **forbidden_claims:** ["a factory reset keeps settings", "a factory reset does not affect account linkage"]
- **ambiguity_notes:** Contrast with soft reset (F0804); cloud video is out of scope (F0809).

### F0806
- **document_id:** D08
- **category:** device_reset
- **fact_type:** sequential
- **condition(s):** ["Hub factory reset", "step 1"]
- **rule/action:** Hub factory reset step 1: hold the Hub reset button for 10 seconds.
- **exceptions:** —
- **required_entities:** ["NiceHome Hub", "reset button", "10 seconds"]
- **language_neutral_expected_outcome:** Response must state the Hub factory reset begins by holding the reset button for 10 seconds.
- **forbidden_claims:** ["hold the reset button for 5 seconds"]
- **ambiguity_notes:** 10-second factory-reset hold differs from the 5-second pairing hold (F0607).

### F0807
- **document_id:** D08
- **category:** device_reset
- **fact_type:** conditional
- **condition(s):** ["a factory reset has been performed"]
- **rule/action:** After a factory reset, the device must be re-paired through the app before it can be used again.
- **exceptions:** —
- **required_entities:** ["factory reset", "re-pair", "NiceHome app"]
- **language_neutral_expected_outcome:** Response must state a device must be re-paired via the app after a factory reset.
- **forbidden_claims:** ["the device works immediately after a factory reset without re-pairing"]
- **ambiguity_notes:** Links to the pairing sequence F0606–F0608.

### F0808
- **document_id:** D08
- **category:** account_security
- **fact_type:** conditional
- **condition(s):** ["device is lost"]
- **rule/action:** A lost device can be removed from the account remotely through the app.
- **exceptions:** —
- **required_entities:** ["account", "NiceHome app"]
- **language_neutral_expected_outcome:** Response must state a lost device can be removed remotely from the account via the app.
- **forbidden_claims:** ["a lost device cannot be removed without physical access"]
- **ambiguity_notes:** —

### F0809
- **document_id:** D08
- **category:** device_reset
- **fact_type:** exception
- **condition(s):** ["a factory reset has been performed"]
- **rule/action:** A factory reset does not delete cloud-stored video; cloud video is managed by the subscription, not by the device.
- **exceptions:** Modifies F0805.
- **required_entities:** ["factory reset", "cloud video", "subscription"]
- **language_neutral_expected_outcome:** Response must state a factory reset does not remove cloud-stored video, which is governed by the subscription.
- **forbidden_claims:** ["a factory reset deletes cloud video"]
- **ambiguity_notes:** Cross-references D04 subscription rules (F0402, F0407).

---

## Summary

| Document | Category | Fact IDs | Count |
|---|---|---|---|
| D01 | Product overview and device compatibility | F0101–F0110 | 10 |
| D02 | Warranty policy | F0201–F0209 | 9 |
| D03 | Return and refund policy | F0301–F0311 | 11 |
| D04 | Subscription plan rules | F0401–F0409 | 9 |
| D05 | Shipping and delivery policy | F0501–F0508 | 8 |
| D06 | Troubleshooting guide | F0601–F0613 | 13 |
| D07 | Repair and replacement policy | F0701–F0709 | 9 |
| D08 | Account access and device reset policy | F0801–F0809 | 9 |
| **Total** | | | **78** |

### Fact type distribution (approximate)

| Fact type | Count | Notes |
|---|---|---|
| simple | ~18 | Single-attribute lookups (device features, periods, refund processing) |
| conditional | ~32 | Policy rules gated by one or more conditions |
| sequential | ~20 | Ordered steps across warranty claim, returns, pairing, connectivity, recovery, factory reset |
| exception | ~8 | Carve-outs modifying a primary fact (warranty exclusions, return exclusions, subscription no-refund, reset/cloud-video) |

(Counts are approximate because a few sequential facts also carry conditions; the `fact_type` field records the primary type.)

### Coverage check against required question types

- **Warranty:** F0201–F0209, plus repair link F0701/F0709
- **Returns/refunds:** F0301–F0311
- **Subscriptions:** F0401–F0409
- **Shipping:** F0501–F0508
- **Troubleshooting:** F0601–F0613
- **Repair/replacement:** F0701–F0709
- **Account/device reset:** F0801–F0809
- **Compatibility:** F0101–F0110

All eight required question types are supported.

### Ambiguity risks identified during authoring

1. **Two "30-day" facts with different meanings** — return window (F0301) vs. cloud storage retention (F0402). Renderers and intent authors must not conflate them.
2. **Two button-hold durations** — 5-second pairing hold (F0607) vs. 10-second Hub factory-reset hold (F0806). Easy to swap; flagged in both facts.
3. **Trial length vs. storage length** — 14-day trial (F0405) vs. 30-day storage (F0402). Distinct numbers in the same document.
4. **Live view depends on two independent conditions** — Hub online (F0110) and is unrelated to subscription (F0403). A response could wrongly tie live view to the subscription.
5. **Reset terminology** — soft reset (F0804, keeps settings) vs. factory reset (F0805, erases + unlinks) vs. Hub restart (F0603, troubleshooting). Three distinct operations.
6. **Refund scope on shipping problems** — delayed shipment refunds only the shipping fee (F0507); lost shipment yields a replacement (F0508). Neither refunds the full order price.
7. **Warranty vs. return windows** — 2 years (warranty) vs. 30 days (returns). Conflating them is a plausible model error; forbidden claims guard against it.
8. **Refurbished warranty floor** — "remainder of original warranty OR 90 days, whichever is longer" (F0705) is a minimum-floor rule that is easy to render as a flat 90-day reset. Flagged.

These ambiguity risks are the basis for several `forbidden_claims` entries and should directly inform the conditional and troubleshooting intents.

### Next artifact

The next artifact in the construction sequence (`validation-plan-v0.1.md` §5, `dataset-specification.md` §13) is **`docs/benchmark/v0.1/document-plan.md`** — the section-level content plan for each of the eight synthetic documents, mapping facts to document sections and fixing terminology decisions before any prose KB rendering is authored. The `intent-set.md` follows once both the fact-set and document plan are stable.

---

*This fact-set is the canonical artifact. It is not frozen. Version: fs-v0.1.0. No KB renderings or intents are authored in this file.*
