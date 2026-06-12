# NiceM Language Rendering Plan v0.1

**Status:** Pre-rendering specification — defines how to author the three KB renderings from the canonical fact-set and document plan
**Role:** Fixes the per-language terminology, register, chunk-ID scheme, and ambiguity-control preservation rules that the document plan deferred. Authoring a KB rendering is a constrained task executed against this plan; it is not a free composition.
**Version:** lr-plan-v0.1.0 (not yet frozen)
**Depends on:** `canonical-fact-set.md` (fs-v0.1.0), `document-plan.md` (kb-plan-v0.1.0), `dataset-specification.md`
**Feeds into:** `kb-rendering-en.md`, `kb-rendering-nl.md`, `kb-rendering-tr.md`

---

## 1. Purpose

The language rendering plan exists because **three independently authored documents can only be experimentally comparable if the authoring process is equally constrained for all three**. Without this plan, the English rendering might be written more concisely because its author thinks in English; the Turkish rendering might be more verbose because its author expanded conditions into natural Turkish prose; and any measured token-count difference would then be partly an authoring artifact, not a language/tokenizer effect.

This plan fixes, before any prose is written:
- the register and tone each rendering must adopt
- the controlled terminology for every key concept in each language
- how fact IDs and chunk IDs are recorded alongside (not inside) the prose
- how each of the nine ambiguity controls (AC1–AC9 from `document-plan.md`) must be preserved in every language
- what is and is not permitted when rendering meaning from the fact-set

The goal is not to produce three documents of equal length. Token-tax is a real effect of language and tokenizer, and forcing equal length would eliminate the signal the benchmark is designed to measure. The goal is to produce three documents that are **equally constrained representations of the same canonical content**, so that any token-count difference reflects language/tokenizer behavior, not authoring quality.

---

## 2. Core rendering principles

1. **All language renderings are authored from the structured fact-set and document plan — not from each other.** English is not authored first and translated. Dutch and Turkish are not authored by adapting the English document. Each rendering is an independent instance of (fact-set + document plan).

2. **English is not the canonical source.** English is one of three peer renderings and serves as the analytic baseline in the benchmark. It is not privileged as the original.

3. **Preserve meaning, not literal phrasing.** The task for each rendering is to express the content of each fact in natural, idiomatic prose in the target language, at the register defined in §4. Literal syntax transfer from English is not a goal.

4. **Use parallel section structure across languages.** Every rendering follows the 39-section structure from `document-plan.md`. Section titles are natural in each language (§9); section order is fixed. Chunk IDs are identical across all three renderings (§3).

5. **Use controlled terminology.** For every concept in §6, one term is used consistently throughout a rendering. No synonym drift within or across sections of the same document.

6. **Avoid idioms and culture-specific phrasing.** Plain product-support register (§4). No expressions that import meaning absent from the fact-set or that require cultural context to interpret.

7. **Do not add unsupported facts.** Connective language ("To start a return, follow these steps") is permitted. Policy claims not in the canonical fact-set are not.

8. **Do not remove conditions or exceptions.** A conditional rule must be rendered with its condition. An exception must remain attached to (or forward-reference) the rule it modifies. Omitting a condition or exception is a rendering error.

9. **Keep ambiguity controls AC1–AC9 intact.** §8 specifies exactly how each control must be preserved in rendering. Any rendering that conflates two facts that AC1–AC9 are designed to keep distinct fails the rendering quality gate.

10. **Every rendering preserves fact IDs and chunk IDs in metadata.** Fact IDs do not appear in user-visible prose (§3). They appear in structured metadata alongside each section. This ensures semantic retrieval evaluation can be done in canonical fact units (`semantic_units_retrieved` in the logging schema).

---

## 3. Fact ID and chunk ID visibility decision

**Decision: fact IDs and chunk IDs appear in metadata, not in user-visible prose.**

Rationale: If fact IDs appeared in the text ("per policy F0302, an unopened device…"), the language model would see them during Agent B retrieval and could use them as shortcuts, contaminating the retrieval realism. The benchmark asks whether the model can retrieve and apply the relevant content from natural-language KB documents — not whether it can parse structured identifiers.

**Chunk ID scheme:** Each section of each document is identified by `<document_id>-S<section_number>`. Examples:
- `D01-S2` = D01 §2 (Hub requirement and standalone capability)
- `D03-S5` = D03 §5 (Return process, steps F0309–F0311)
- `D06-S1` = D06 §1 (Connectivity troubleshooting, all four steps)

This ID scheme is identical across all three language renderings. `D03-S5` in the English rendering and `D03-S5` in the Turkish rendering cover the same fact IDs. This is the anchor for cross-language semantic-unit comparison.

**Metadata block format (per section):**
```
<!-- chunk: D03-S5 | facts: F0309, F0310, F0311 | lang: en | version: kb-en-v0.1.0 -->
```
The metadata block appears immediately before (or after) each section in the source file but is stripped when the document is served as KB content to the agent. The stripping step is documented in the instrumentation plan; the metadata is logged separately.

**Why this matters for semantic retrieval evaluation:** The dual-reporting rule (`baseline-token-tax-calculation-v0.1.md` §4, `logging-schema-v0.1.md`) requires retrieval volume to be reported in both raw tokens AND semantic units (canonical fact IDs). When a chunk is retrieved, the fact IDs it contains are deterministic from the chunk ID. This makes the semantic-unit count computable from the retrieval log without re-parsing the retrieved text. The fact-ID list is the lookup table between chunk ID and meaning units.

---

## 4. Register and tone decisions

**English:** Neutral, plain product-support style. Direct and concise. Imperative voice for procedural steps ("Contact support," not "You should contact support"). No legal formality; no marketing language. Suitable for an English-language help center.

**Dutch:** Neutral, clear product-support Dutch. Use instructional/impersonal phrasing where possible to avoid the formal/informal address choice (see §13, open question LR1). Where direct address cannot be avoided, default to formal ("u") until confirmed otherwise. Avoid overly legal or bureaucratic phrasing that Dutch formal writing can drift toward. Compound nouns should follow natural Dutch conventions — do not leave English phrases unmodified where a clean Dutch compound exists; but also do not coin awkward compounds (see §7).

**Turkish:** Neutral, clear product-support Turkish. Use instructional forms ("Destek ile iletişime geçin") rather than first-person-plural or highly formal constructions. Default to formal "siz" register (see §13, open question LR2) until confirmed. Avoid overly bureaucratic Turkish; avoid literal English-syntax calques. Agglutinative suffixes attaching to product names are handled per §5 and §7.

**Governing principle:** The goal is **semantic equivalence at natural register**, not length equivalence. If expressing a conditional rule naturally in Turkish requires more words than English, that is the expected rendering — not a mistake to be corrected. Forced brevity to match English length would distort the token-tax signal.

---

## 5. Device and product name policy

All four device names and the subscription plan name are **brand names**. They are rendered identically in all three languages. They are not translated, localized, or given language-specific aliases.

| Name | Rendered as (all languages) |
|---|---|
| NiceHome Hub | NiceHome Hub |
| NiceHome Sensor | NiceHome Sensor |
| NiceHome Plug | NiceHome Plug |
| NiceHome Camera | NiceHome Camera |
| Camera Plus Plan | Camera Plus Plan |
| NiceHome (brand) | NiceHome |

**Turkish suffix handling:** Turkish agglutinative morphology will attach case suffixes to product names in context (e.g., "NiceHome Hub'ı" for accusative, "NiceHome Hub'a" for dative). This is grammatically correct Turkish and **is expected** — do not avoid it by restructuring sentences unnaturally. Use an apostrophe before the suffix when attaching to brand names (standard Turkish orthographic convention for foreign proper nouns). The base name itself remains "NiceHome Hub" (no localization).

**Dutch handling:** English product names appear as loanwords in Dutch technical prose without adaptation. "De NiceHome Hub" (with Dutch article) is correct; do not coin a Dutch translation like "NiceHome-knooppunt."

---

## 6. Controlled terminology table

For each concept, the table fixes the canonical meaning (from `canonical-fact-set.md` and `document-plan.md` §3) and the rendering choice in each language. Where a choice is **TODO**, the term requires review before the rendering is authored. TODOs do not block rendering of other sections; they block only the sections containing that term.

| Concept | Canonical meaning | English rendering | Dutch rendering | Turkish rendering | Notes / ambiguity risk |
|---|---|---|---|---|---|
| standard warranty | 2-year from-purchase coverage for all devices (F0201) | standard warranty | standaardgarantie | standart garanti | Must be lexically distinct from "return window" in every language |
| return window | 30-day from-purchase return eligibility period (F0301) | return window | retourtermijn | iade süresi | AC1: distinct from "cloud storage period" in all three languages |
| refund | Money returned to original payment method (F0307) | refund | terugbetaling | geri ödeme | Applies to both return refund and shipping-delay refund; confirm scope from context |
| cloud storage | 30-day cloud video retention on subscription (F0402) | cloud storage / cloud video storage | cloudopslag / cloudvideo-opslag | bulut depolama / bulut video depolama | AC1: distinct from "return window" in all three; "cloud" kept as loanword in Dutch/Turkish |
| live view | Real-time Camera viewing; subscription-free (F0403, F0104) | live view | live weergave | TODO: canlı görüntü? | AC4: must not imply subscription requirement; TODO on Turkish term |
| pairing mode | Device state for connecting to Hub, entered by 5-second setup-button hold (F0607) | pairing mode | koppelingsmodus | eşleştirme modu | AC2: "pairing" lexically distinct from "reset" in all three |
| soft reset | Restart without erasing settings (F0804) | soft reset | zachte reset | yumuşak sıfırlama | AC5: distinct from factory reset and Hub restart in all three |
| factory reset | Full erase of settings + account unlink (F0805) | factory reset | fabrieksreset | fabrika ayarlarına sıfırlama | AC5: "fabrika ayarları" is natural Turkish; distinct from "yumuşak sıfırlama" |
| Hub restart | Restarting the Hub without resetting (F0603, D06 troubleshooting step) | restart the Hub | start de Hub opnieuw op | Hub'ı yeniden başlatın | AC5: distinct from both soft reset and factory reset; "opnieuw opstarten" vs. "reset" in Dutch |
| repair | Fixing a device (in- or out-of-warranty) (F0701, F0702) | repair | reparatie | onarım | Distinct from replacement |
| replacement | Providing a different device (F0703) | replacement | vervanging | değişim / yedek cihaz | TODO: confirm Turkish term consistency; "değişim" is clean but "yedek cihaz" may be more natural in context |
| refurbished replacement | A replacement device that is refurbished (F0704, F0705) | refurbished replacement | gereviseerde vervanging | yenilenmiş yedek cihaz | AC8: "gereviseerd" is standard Dutch for refurbished; must carry warranty-floor meaning |
| subscription plan | Camera Plus Plan cloud subscription (F0401) | subscription plan / Camera Plus Plan | abonnement / Camera Plus Plan | abonelik planı / Camera Plus Plan | Plan name "Camera Plus Plan" kept untranslated; generic term translated |
| trial period | 14-day free Camera Plus Plan trial (F0405) | free trial / trial period | gratis proefperiode | ücretsiz deneme süresi | AC3: "14-day trial" and "30-day storage" must use distinct terms and carry their numbers |
| account recovery | Password-reset procedure via email link (F0801–F0803) | account recovery / password recovery | accountherstel / wachtwoordherstel | hesap kurtarma / şifre sıfırlama | Distinct from "device reset" in all three |
| shipping delay | Shipment arriving after its estimated delivery window (F0507) | shipping delay | vertraging bij bezorging | teslimat gecikmesi | AC6: delay → shipping-fee refund only; distinct from "lost shipment" |
| lost shipment | Shipment that has not arrived and is confirmed lost (F0508) | lost shipment | verloren zending | kayıp kargo / kaybolmuş gönderi | AC6: lost → free replacement, not shipping-fee refund |
| accidental damage | Damage from accidental impact (F0203) | accidental damage | onopzettelijke schade | kaza sonucu hasar | Must be distinct from "manufacturing defect" (F0202); warranty exclusion |
| manufacturing defect | Defect arising from the production process (F0202) | manufacturing defect | fabricagefout | üretim hatası | Covered by warranty; distinct from accidental damage |
| prepaid shipping label | Shipping label provided by NiceHome for in-warranty claims (F0207) | prepaid shipping label | vooraf betaald verzendetiket | önceden ödenmiş gönderi etiketi | AC7-adjacent: prepaid = in-warranty; customer-pays = out-of-warranty (F0706) |

**Note on TODO items:** `live view` (Turkish) and `replacement` (Turkish) are marked TODO. These do not block sections that do not use them. The Turkish rendering must not begin authoring until all TODOs in its sections are resolved. Recommended: project owner (native Turkish speaker) confirms these two terms before the Turkish rendering is authored.

---

## 7. Language-specific rendering risks

### English

- **Risk: becoming the hidden canonical source.** Because project documentation (including this plan) is written in English, there is a natural tendency for the English KB rendering to be written first and the others treated as adaptations. The authoring instruction must explicitly enforce independent derivation from (fact-set + plan) for all three, and the English rendering must be reviewed with the same critical eye for "did it add anything?" as the other two.
- **Risk: over-concision setting the norm.** English product-support prose tends toward brevity. If the English rendering is unusually short because its author compressed conditions into subordinate clauses, other languages will look artificially verbose by comparison. The register instruction (§4) asks for plain prose, not maximally compressed prose.
- **Mitigation:** The English rendering author should write each conditional rule as a complete conditional sentence (e.g., "If the shipment is delayed beyond its estimated delivery window, you may request a refund of the shipping fee"), not as a compressed clause.

### Dutch

- **Risk: compound noun formation.** Dutch forms compounds naturally, and this will often produce shorter token spans for multi-word English phrases (e.g., "retourtermijn" for "return window"). This is the expected token-tax direction for Dutch and should not be avoided. However, novel compounds should only be coined if they are natural Dutch — do not invent "retourvenster" as a literal calque of "return window" when "retourtermijn" is the established term.
- **Risk: formal vs. informal address (u vs. jij/je).** Dutch product-support writing varies. The controlled choice is "u" (see §4 and LR1). This affects procedural steps ("Neem contact op met de ondersteuning" for impersonal, or "Neemt u contact op..." for formal you). Where instructional impersonal can be used naturally, prefer it.
- **Risk: English device names in Dutch prose.** "De NiceHome Hub" mixes English brand with Dutch syntax. This is correct and expected; do not avoid it. Suffixes follow Dutch patterns (genitive: "NiceHome Hub's", but in product-support writing genitive compounds like "NiceHome Hub-garantie" are more natural).
- **Risk: legal-style verbose phrasing.** Dutch formal prose can become wordy with nominalizations. The register instruction (§4, "avoid overly formal legal style") governs.

### Turkish

- **Risk: agglutinative morphology inflating token count.** Turkish case suffixes, tense markers, and evidentiality markers will produce longer token sequences for equivalent meaning in most current tokenizers. This is the primary token-tax signal this benchmark is designed to capture for Turkish. It must not be suppressed by unnaturally restructuring Turkish sentences to reduce suffix load.
- **Risk: suffixes on product names.** As noted in §5, case suffixes attach to product names with an apostrophe separator ("NiceHome Hub'ı"). This is correct orthography. Do not restructure to avoid these forms; do not use "NiceHome Hub cihazı" as a workaround unless it reads naturally in context.
- **Risk: literal calquing from English.** Turkish has its own syntactic patterns (verb-final, topic-prominent, postpositional). Calquing English clause order produces unnatural Turkish. The rendering should read as natural Turkish product-support text, which may be substantially different in word order and sentence construction.
- **Risk: overly bureaucratic phrasing.** Turkish formal writing can produce highly nominalized, passive constructions ("iade işleminin gerçekleştirilmesi için yetkili servis birimleriyle temasa geçilmesi gerekmektedir"). Product-support register (§4) means clearer constructions ("Lütfen yetkili destek birimi ile iletişime geçin").
- **Risk: formal vs. informal address (siz vs. sen).** Default is "siz" register (LR2). This affects procedural steps ("Destek birimiyle iletişime geçin" for impersonal, or "Lütfen destek birimiyle iletişime geçiniz" for formal). Impersonal imperative is natural in Turkish product documentation; use it where natural.

---

## 8. Ambiguity control preservation

Each AC from `document-plan.md` §5 has a specific rendering requirement.

**AC1 — 30-day return window vs. 30-day cloud storage retention.**
The terms "return window" (§6: EN "return window", NL "retourtermijn", TR "iade süresi") and "cloud storage" (EN "cloud storage", NL "cloudopslag", TR "bulut depolama") must be lexically distinct in every rendering. The number "30 days/dagen/gün" will appear in both D03 and D04; it must always be accompanied by the appropriate noun ("30-day return window" / "30 days of cloud storage"), never as a bare number.

**AC2 — 5-second pairing hold vs. 10-second Hub factory reset.**
Both procedures appear in different documents (D06 §3 vs. D08 §3). Each rendering must state the duration explicitly with the action name ("hold the setup button for 5 seconds to enter pairing mode" / "hold the reset button for 10 seconds to factory reset"). The two hold durations must never appear in the same section.

**AC3 — 14-day trial vs. 30-day cloud storage.**
Both appear in D04. Each number is always paired with its noun: "14-day free trial" / "30 days of cloud video storage" (and equivalents). Renderings must not juxtapose the two numbers without clear labeling.

**AC4 — Live view depends on Hub-online status, not subscription.**
D01 §4 (Hub-online condition, F0110) and D04 §2 (subscription-independence, F0403) must each state their respective condition clearly. No rendering of D04 §2 may imply live view requires the subscription; no rendering of D01 §4 may imply the Camera is otherwise unusable without the Hub.

**AC5 — Soft reset vs. factory reset vs. Hub restart.**
Three operations, three lexically distinct terms in each language (§6: soft reset / factory reset / Hub restart). D08 §2 (the contrast section) must name both reset types and state the difference explicitly. D06 §1 uses "restart" only; D06 §4 uses "soft reset" only. No rendering conflates these.

**AC6 — Shipping delay fee refund vs. lost-shipment replacement.**
Both in D05 §4. The remedy differs: delay → refund of shipping fee only; lost → free replacement of the device. Renderings must keep these as two separate sentences with distinct subjects and distinct outcomes. The product price is never mentioned as refundable under either scenario.

**AC7 — 2-year warranty vs. 30-day return window.**
Different documents (D02 §1 vs. D03 §1). The risk is a reader inferring they can "return" a device under warranty — renderings must not create that confusion. D02 and D03 deal with different situations (defects vs. buyer return), and any cross-reference between them (D03 F0304 referencing warranty) must make the separation clear.

**AC8 — Refurbished replacement warranty floor.**
D07 §3 (F0705). The rendering must convey "the remainder of the original warranty, with a minimum of 90 days" — a minimum-floor rule. The three misreadings to guard against: (a) flat 90-day reset ("you get a 90-day warranty"), (b) full 2-year reset ("you get a new 2-year warranty"), (c) no warranty ("refurbished devices have no warranty"). The rendering should make the "longer of the two" logic explicit even if slightly verbose.

**AC9 — F0807 single-source / forward-reference rule.**
F0807 (after factory reset, device must be re-paired) is stated once in D08 §4. D08 §3 ends with the blink-confirmation result of holding the reset button and adds a forward reference ("After the reset completes, re-pair the device as described in the next section"). The forward reference must be present in all three language renderings; the rule itself only in §4.

---

## 9. Parallel section structure

Every language rendering follows the 39-section structure from `document-plan.md` §4 exactly. The same 39 chunk IDs apply across all three renderings.

Section *titles* are natural in each language. They are not required to be word-for-word translations of each other — but their structure (topic and scope) must be identical. A reviewer comparing D03 §2 in English and Turkish should find the same conditional content, structured the same way, at the same position in the document.

Chunk ID alignment check: before any rendering is accepted, its chunk IDs must be verified against the master list (39 IDs from `document-plan.md` §4). Missing, extra, or reordered chunks fail the rendering quality gate.

---

## 10. Rendering quality gates

These specialize the §8 gates from `document-plan.md` and the §11 gates from `dataset-specification.md` to the rendering step. All must pass before a rendering is frozen.

| Gate | Check | If it fails |
|---|---|---|
| Chunk completeness | All 39 chunk IDs present in the rendering | Add missing sections; do not freeze |
| Chunk-fact alignment | Each chunk maps to the same fact IDs as in the master mapping | Fix the section that diverges |
| Meaning preservation | All `rule/action`, `condition(s)`, and `exceptions` content present in each section | Fix the incomplete section |
| No unsupported facts | No policy claim added that is not in the canonical fact-set | Remove the addition; check for connective-language overreach |
| No missing conditions | No conditional fact rendered as if it were unconditional | Fix and re-review |
| No missing exceptions | No exception fact omitted or detached from its parent rule | Fix and re-review |
| Terminology consistency | §6 controlled terms used throughout (one term per concept, no drift) | Fix inconsistencies |
| AC1–AC9 compliance | All nine ambiguity controls are satisfied per §8 | Fix the failing control(s) and re-review |
| Number fidelity | All fixed quantities appear as their stated values (§6, §3 of document-plan.md) | Fix all number errors |
| Turkish review | Turkish rendering reviewed by project owner (native speaker) | Do not freeze until reviewed |
| Independent review (pre-public) | Independent bilingual review completed for claims made in public or publication-grade contexts | Do not publish until reviewed |

---

## 11. Relationship to token-tax measurement

Rendering choices can affect measured token counts in three ways:

1. **Language/tokenizer effect (the signal).** Turkish agglutinative morphology, Dutch compound formation, and English analytic structure all affect tokenization differently under the same tokenizer. This is the token-tax we intend to measure.
2. **Register/verbosity effect (noise if inconsistent).** If English is rendered in maximally compressed product-support prose and Turkish is rendered in expansive formal prose, the count difference includes a verbosity artifact. Consistent register (§4) and the principle of meaning-not-length equivalence limit this noise.
3. **Structural effect (controlled by this plan).** Identical section structure (§9) and fact coverage mean structural variation is eliminated. A renderer cannot "simplify" a document by omitting a section.

**Implication:** Token-tax measurement in this benchmark is a lower bound on the "true" token-tax for this language-domain combination, because we have actively controlled register and structure. If candidate execution-tax is observed, it is on top of this controlled token-tax baseline — not confounded with it. This is the design intent.

---

## 12. Future rendering files

```
docs/benchmark/v0.1/kb-rendering-en.md  — English KB rendering (8 documents, 39 sections)
docs/benchmark/v0.1/kb-rendering-nl.md  — Dutch KB rendering (8 documents, 39 sections)
docs/benchmark/v0.1/kb-rendering-tr.md  — Turkish KB rendering (8 documents, 39 sections)
```

Each file contains all 8 documents for its language, with:
- Natural-language prose section text
- Metadata blocks (per §3) before or after each section in the source file
- Reviewed against the quality gates in §10 before freezing

Recommended authoring order: author all three renderings before freezing any of them, so a cross-language comparison pass can catch structural divergence. Freeze all three together as `kb-rendering-v0.1.0`.

---

## 13. Open questions

- **LR1 — Dutch address register.** Should Dutch prose use "u" (formal direct address) or instructional impersonal phrasing ("Neem contact op…") throughout? Direction: prefer impersonal instructional where natural; fall back to "u" for direct-address contexts. Confirm with a Dutch-language reviewer before the Dutch rendering is frozen.
- **LR2 — Turkish address register.** Should Turkish prose use formal "siz" constructions or impersonal imperatives? Direction: prefer impersonal imperative ("Destek birimiyle iletişime geçin") for procedural steps; use "siz" constructions where impersonal reads awkwardly. Project owner to confirm during Turkish rendering review.
- **LR3 — Turkish product-name suffix forms.** Are there cases where attaching case suffixes to "NiceHome Hub" with an apostrophe produces unnatural results in context? Project owner to flag and propose alternatives on a per-case basis during review.
- **LR4 — Section title translation style.** Should section titles be natural translations ("Retourvenster" for "Return window" in Dutch) or more literal labels? Direction: natural translations — section titles are reader-facing; their meaning and scope must match across languages, but wording should be idiomatic.
- **LR5 — Fact ID and chunk ID visibility.** Confirmed direction in §3 (metadata only, not in prose). Record this as resolved for document-plan.md open question DP2.
- **LR6 — Second-speaker review for Dutch.** Dutch KB rendering should be reviewed by a Dutch speaker before any public or publication-grade claim. The project owner is not a native Dutch speaker; this remains an open dependency analogous to LS1 (Turkish KB bilingual review).
- **LR7 — English concision control.** Is the register guidance in §4 sufficient to prevent the English rendering from being significantly more compact than the others, or should an explicit minimum-verbosity check be added to the quality gates? Deferred to authoring stage; flag if the English rendering is substantially shorter per section than Dutch without a clear structural reason.

---

*This plan adds authoring constraints only; it introduces no policy content. The canonical fact-set remains the single source of truth. Version: lr-plan-v0.1.0, not yet frozen.*
