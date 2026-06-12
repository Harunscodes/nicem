# NiceHome Knowledge Base — English Rendering (v0.1)

**Rendering ID:** kb-en-v0.1.0 (not yet frozen)
**Language:** English (analytic baseline — not the canonical source)
**Authored from:** `canonical-fact-set.md` (fs-v0.1.0) + `document-plan.md` (kb-plan-v0.1.0) + `language-rendering-plan.md` (lr-plan-v0.1.0)
**Structure:** 8 documents, 39 sections/chunks. Chunk IDs and fact IDs are metadata; they are stripped before the content is served to an agent.
**Review status:** Project-owner review pending. This rendering introduces no policy facts beyond the canonical fact-set.

---

## D01 — Product overview and device compatibility

### D01-S1 — Device overview
```
chunk_id: D01-S1
fact_ids: [F0101, F0102, F0103, F0104]
document_id: D01
section_title: Device overview
```
The NiceHome Hub is the central device that manages all other NiceHome devices. The NiceHome Sensor measures temperature, humidity, and motion. The NiceHome Plug is a smart power outlet that provides remote switching and energy monitoring. The NiceHome Camera is an indoor security camera that provides motion alerts and live view.

### D01-S2 — Hub requirement and standalone capability
```
chunk_id: D01-S2
fact_ids: [F0105, F0106, F0107]
document_id: D01
section_title: Hub requirement and standalone capability
```
The NiceHome Sensor requires a NiceHome Hub to operate and cannot function without one. The NiceHome Camera also requires a NiceHome Hub to operate. The NiceHome Plug supports basic remote on/off switching without a Hub, but it requires a Hub for its automation features, which are scheduling and energy monitoring.

### D01-S3 — Generation compatibility
```
chunk_id: D01-S3
fact_ids: [F0108, F0109]
document_id: D01
section_title: Generation compatibility
```
NiceHome devices exist in two generations, Gen 1 and Gen 2. Gen 2 devices require a Gen 2 Hub; a Gen 1 Hub does not support Gen 2 devices. A Gen 2 Hub is backward compatible and supports both Gen 1 and Gen 2 devices.

### D01-S4 — Live view availability
```
chunk_id: D01-S4
fact_ids: [F0110]
document_id: D01
section_title: Live view availability
```
Camera live view is not available while the Hub is offline.

---

## D02 — Warranty policy

### D02-S1 — Warranty period
```
chunk_id: D02-S1
fact_ids: [F0201]
document_id: D02
section_title: Warranty period
```
All NiceHome devices include a standard warranty of 2 years from the date of purchase.

### D02-S2 — What is covered
```
chunk_id: D02-S2
fact_ids: [F0202]
document_id: D02
section_title: What is covered
```
The warranty covers manufacturing defects and hardware failures that occur under normal use.

### D02-S3 — What is not covered
```
chunk_id: D02-S3
fact_ids: [F0203, F0204]
document_id: D02
section_title: What is not covered
```
The warranty does not cover accidental damage. It also does not cover damage caused by misuse or by unauthorized modification of the device.

### D02-S4 — Making a warranty claim
```
chunk_id: D02-S4
fact_ids: [F0205, F0206, F0207, F0208]
document_id: D02
section_title: Making a warranty claim
```
To make a warranty claim, you must provide proof of purchase. The claim has three steps. First, contact NiceHome support with the device serial number. Second, support issues a warranty claim reference and a prepaid shipping label. Third, ship the device using the prepaid label and include the claim reference.

### D02-S5 — Claim outcome
```
chunk_id: D02-S5
fact_ids: [F0209]
document_id: D02
section_title: Claim outcome
```
If a covered defect is confirmed, the device is repaired or replaced at no cost.

---

## D03 — Return and refund policy

### D03-S1 — Return window
```
chunk_id: D03-S1
fact_ids: [F0301, F0305]
document_id: D03
section_title: Return window
```
The return window is 30 days from the date of purchase. Returns are not accepted after 30 days from purchase.

### D03-S2 — Refund by device condition
```
chunk_id: D03-S2
fact_ids: [F0302, F0303]
document_id: D03
section_title: Refund by device condition
```
An unopened device returned within 30 days receives a full refund with free return shipping. An opened but undamaged device returned within 30 days also receives a full refund, but in this case you pay the return shipping.

### D03-S3 — Return exclusions
```
chunk_id: D03-S3
fact_ids: [F0304, F0306]
document_id: D03
section_title: Return exclusions
```
A device damaged by the customer is not eligible for a refund, unless the damage is covered under the warranty. Subscription plans are not refundable through the device return process; subscription cancellation is handled separately.

### D03-S4 — Refund processing
```
chunk_id: D03-S4
fact_ids: [F0307, F0308]
document_id: D03
section_title: Refund processing
```
Refunds are issued to the original payment method. Refunds are processed within 14 business days after the returned device is received.

### D03-S5 — Return process
```
chunk_id: D03-S5
fact_ids: [F0309, F0310, F0311]
document_id: D03
section_title: Return process
```
The return has three steps. First, request a return authorization from NiceHome support. Second, you receive a return authorization number and shipping instructions. Third, ship the device with the return authorization number included.

---

## D04 — Subscription plan rules

### D04-S1 — Plan overview
```
chunk_id: D04-S1
fact_ids: [F0401]
document_id: D04
section_title: Plan overview
```
NiceHome offers a cloud subscription called the Camera Plus Plan.

### D04-S2 — What the plan provides
```
chunk_id: D04-S2
fact_ids: [F0402, F0403]
document_id: D04
section_title: What the plan provides
```
The Camera Plus Plan provides 30 days of cloud video storage for the NiceHome Camera. Without a subscription, the NiceHome Camera still supports live view, but it does not provide cloud video storage.

### D04-S3 — Plan requirements
```
chunk_id: D04-S3
fact_ids: [F0404]
document_id: D04
section_title: Plan requirements
```
The Camera Plus Plan requires a NiceHome Camera and a NiceHome Hub.

### D04-S4 — Free trial
```
chunk_id: D04-S4
fact_ids: [F0405, F0406]
document_id: D04
section_title: Free trial
```
The Camera Plus Plan includes a free trial that lasts 14 days. The free trial can be used only once per account.

### D04-S5 — Cancellation and changes
```
chunk_id: D04-S5
fact_ids: [F0407, F0408, F0409]
document_id: D04
section_title: Cancellation and changes
```
If you cancel the subscription, cloud storage access continues until the end of the current billing period. A cancelled subscription does not receive a pro-rated refund for the current billing period. Subscription plan changes, whether an upgrade or a downgrade, take effect at the start of the next billing period.

---

## D05 — Shipping and delivery policy

### D05-S1 — Shipping methods and timeframes
```
chunk_id: D05-S1
fact_ids: [F0501, F0502, F0503]
document_id: D05
section_title: Shipping methods and timeframes
```
Two shipping methods are available: Standard and Express. Standard shipping is delivered within 5 to 7 business days. Express shipping is delivered within 2 business days.

### D05-S2 — Express eligibility
```
chunk_id: D05-S2
fact_ids: [F0504]
document_id: D05
section_title: Express eligibility
```
Express shipping is available only for in-stock items.

### D05-S3 — Changing or cancelling an order
```
chunk_id: D05-S3
fact_ids: [F0505, F0506]
document_id: D05
section_title: Changing or cancelling an order
```
You can modify or cancel an order within 2 hours of placing it. After 2 hours, the order cannot be cancelled, but you can return the device after delivery under the return policy.

### D05-S4 — Delayed or lost shipments
```
chunk_id: D05-S4
fact_ids: [F0507, F0508]
document_id: D05
section_title: Delayed or lost shipments
```
If a shipment is delayed beyond its estimated delivery window, you may request a refund of the shipping fee. If a shipment is lost in transit, a replacement is sent at no additional cost.

---

## D06 — Troubleshooting guide

### D06-S1 — Connectivity troubleshooting
```
chunk_id: D06-S1
fact_ids: [F0601, F0602, F0603, F0604]
document_id: D06
section_title: Connectivity troubleshooting
```
Follow these steps for connectivity problems. First, check that the Hub power light is on. Second, if the light is off, check the power cable and the outlet. Third, if the light is on but devices are offline, restart the Hub. Fourth, if devices remain offline after restarting the Hub, check the home network and router.

### D06-S2 — Hub status indicators
```
chunk_id: D06-S2
fact_ids: [F0605]
document_id: D06
section_title: Hub status indicators
```
A blinking red Hub light indicates that the Hub has lost its network connection.

### D06-S3 — Pairing a device
```
chunk_id: D06-S3
fact_ids: [F0606, F0607, F0608, F0609]
document_id: D06
section_title: Pairing a device
```
To pair a new device, follow these steps. First, open the NiceHome app and select "Add device". Second, put the device into pairing mode by holding its setup button for 5 seconds. Third, follow the app prompts to complete pairing. If pairing fails, make sure the device is within range of the Hub.

### D06-S4 — Unresponsive Plug
```
chunk_id: D06-S4
fact_ids: [F0610, F0611]
document_id: D06
section_title: Unresponsive Plug
```
If a NiceHome Plug does not respond, first toggle it off and on from the app. If the Plug still does not respond after that, perform a soft reset of the Plug.

### D06-S5 — Inaccurate Sensor readings
```
chunk_id: D06-S5
fact_ids: [F0612]
document_id: D06
section_title: Inaccurate Sensor readings
```
If NiceHome Sensor readings appear inaccurate, recalibrate the Sensor from the app settings.

### D06-S6 — When to contact support
```
chunk_id: D06-S6
fact_ids: [F0613]
document_id: D06
section_title: When to contact support
```
If these troubleshooting steps do not resolve the issue, contact NiceHome support.

---

## D07 — Repair and replacement policy

### D07-S1 — In-warranty repair and replacement
```
chunk_id: D07-S1
fact_ids: [F0701, F0703]
document_id: D07
section_title: In-warranty repair and replacement
```
An in-warranty device with a covered defect is repaired or replaced at no cost. If an in-warranty device cannot be repaired, it is replaced.

### D07-S2 — Out-of-warranty repair
```
chunk_id: D07-S2
fact_ids: [F0702, F0706]
document_id: D07
section_title: Out-of-warranty repair
```
An out-of-warranty device may be repaired for a service fee. For out-of-warranty repairs, you pay shipping in both directions.

### D07-S3 — Replacement devices
```
chunk_id: D07-S3
fact_ids: [F0704, F0705]
document_id: D07
section_title: Replacement devices
```
A replacement device may be either new or refurbished. A refurbished replacement carries the remainder of the original warranty, with a minimum of 90 days; in other words, you receive whichever is longer, the time left on the original warranty or 90 days.

### D07-S4 — Damage exclusions
```
chunk_id: D07-S4
fact_ids: [F0708]
document_id: D07
section_title: Damage exclusions
```
Devices with accidental or liquid damage are not eligible for standard repair and require an out-of-warranty service quote.

### D07-S5 — Turnaround and how to request
```
chunk_id: D07-S5
fact_ids: [F0707, F0709]
document_id: D07
section_title: Turnaround and how to request
```
Repair turnaround is typically 10 business days after the device is received. To request a repair, contact NiceHome support and describe the issue; support then provides a repair reference and shipping instructions.

---

## D08 — Account access and device reset policy

### D08-S1 — Password recovery
```
chunk_id: D08-S1
fact_ids: [F0801, F0802, F0803]
document_id: D08
section_title: Password recovery
```
To recover your password, follow these steps. First, select "Forgot password" on the sign-in screen. Second, enter the account email to receive a reset link. Third, follow the reset link to set a new password.

### D08-S2 — Soft reset vs. factory reset
```
chunk_id: D08-S2
fact_ids: [F0804, F0805]
document_id: D08
section_title: Soft reset vs. factory reset
```
A soft reset restarts a device without deleting its settings. A factory reset erases all device settings and unlinks the device from the account.

### D08-S3 — Factory resetting the Hub
```
chunk_id: D08-S3
fact_ids: [F0806, F0807]
document_id: D08
section_title: Factory resetting the Hub
```
To factory reset the Hub, hold the Hub reset button for 10 seconds. Wait for the Hub light to blink, which indicates that the reset is complete. After the reset completes, the device must be re-paired, as described in the next section.

### D08-S4 — After a factory reset
```
chunk_id: D08-S4
fact_ids: [F0807, F0809]
document_id: D08
section_title: After a factory reset
```
After a factory reset, the device must be re-paired through the app before it can be used again. A factory reset does not delete cloud-stored video; cloud video is managed by the subscription, not by the device.

### D08-S5 — Managing a lost device
```
chunk_id: D08-S5
fact_ids: [F0808]
document_id: D08
section_title: Managing a lost device
```
If a device is lost, it can be removed from the account remotely through the app.

---

*End of English rendering. 8 documents, 39 chunks. kb-en-v0.1.0, not yet frozen.*
