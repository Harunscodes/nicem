# NiceM Query Rendering Plan v0.1

**Status:** Pre-query-authoring specification — defines how to render 36 language-neutral intents into 108 user queries
**Role:** Does for queries what `language-rendering-plan.md` does for KB documents. Fixes register, pronoun, style, difficulty-preservation, and AC controls before any query text is written. Authoring a query rendering is a constrained task executed against this plan; it is not a free composition.
**Version:** qr-plan-v0.1.0 (not yet frozen)
**Depends on:** `intent-set.md` (intent-v0.1.0), `expected-fact-mapping.md` (efm-v0.1.0), `language-rendering-plan.md` (lr-plan-v0.1.0)
**Feeds into:** `query-rendering-en.md`, `query-rendering-nl.md`, `query-rendering-tr.md`

---

## 1. Purpose

Query rendering needs its own plan before any user-query text is written for two reasons that mirror the reasons `language-rendering-plan.md` existed before the KB renderings.

**First, parity.** If English queries are written first and Dutch/Turkish queries are adapted from them, the English phrasing becomes the hidden canonical form. An English query written in natural, compressed product-support English ("How long is the warranty?") may take fewer tokens than an equivalently natural Dutch or Turkish query. That difference is part of the token-tax signal — but only if the difference reflects language/tokenizer behavior, not a choice to compress English while leaving the others looser. Controlled authoring from the intent specification (not from each other) eliminates this artifact.

**Second, evaluation integrity.** The query wording determines what conditions are available to the model. A query that vaguely describes a conditional scenario ("I have an issue with my device") may not surface the required condition, making the model's failure to apply it ambiguous. A query that over-specifies the answer ("My device broke by itself — not accidental damage — is it covered?") leads the model to the answer, invalidating the test. This plan fixes how much information each query type must and must not include.

A query rendering plan is cheap to write now and prevents expensive rework later (queries that fail during Stage 1 tokenizer analysis because of inconsistent length or missing conditions, or that invalidate evaluation during Stage 2 because they contain answer hints).

---

## 2. Core principles

1. **Render from intent specifications, not from English queries.** Each query in each language is authored from the `user_scenario_language_neutral` field of the intent and the relevant conditions — not by translating a previously written English query. The English query is one of three peer renderings.

2. **English is not the canonical query source.** English queries must be reviewed for over-compression on the same terms as Dutch and Turkish queries are reviewed for over-verbosity.

3. **Preserve user intent and required conditions.** A conditional intent has conditions that must be present in the query. Stripping a condition to simplify the query produces a different test — the model cannot be evaluated on a condition it was not given.

4. **Use natural but controlled user language.** Queries should read as genuine user-support questions. They should not read as academic test items, structured prompts, or internal system descriptions.

5. **Avoid idioms and culture-specific phrasing.** Product-support questions should be expressible in any of the three languages without requiring cultural context.

6. **Avoid unnecessary verbosity.** A query should include all required conditions and no more. Padding a Turkish query with formal niceties to match a longer surface form does not represent natural Turkish and adds noise.

7. **Avoid overly compressed English.** A three-word English query ("Warranty period?") is not comparable to a natural Dutch or Turkish question. English queries should use complete questions.

8. **Avoid literal translation artifacts.** Each language's query should read as natural user-support phrasing in that language, not as a word-for-word rendering of another language's syntax.

9. **Keep equivalent difficulty across languages.** A conditional scenario in English ("I opened my device but I haven't damaged it — can I return it and who pays for shipping?") must be rendered with the same conditions in Dutch and Turkish. Making one language's query more explicit than another creates an unfair asymmetry.

10. **Do not add facts not present in the intent spec.** The query introduces the user scenario; it does not introduce policy content. A query that says "I know opened returns get a full refund — who pays for shipping?" leads the model to the answer.

11. **Do not remove conditions needed for evaluation.** Any condition listed in `condition_count` for the intent must be present in the query. Removing it changes the test.

---

## 3. Query style

**Format:** One query per intent per language. A single question or a brief scenario + question. No multi-turn dialogue in v0.1 — each query is self-contained.

**Voice:** First-person or second-person (support portal) style, depending on what is more natural in each language. English: "How long is the warranty on my NiceHome Hub?" or "I'm trying to pair my sensor — what steps do I follow?" Dutch and Turkish follow equivalent natural styles (§4/§5).

**Length:** Complete sentences. For simple factual intents, one clear question. For conditional intents, one or two sentences: the scenario setup + the question. For troubleshooting intents, a brief problem description + the question.

**Hidden information prohibited:**
- No fact IDs, chunk IDs, or document IDs in the query text.
- No expected-answer hints ("Is it true that…?" structured to confirm the answer).
- No direct policy quotes from the KB.
- No phrasing that negates a forbidden claim as context ("I know it's not covered for misuse — but what about normal use?").

**Device and plan names:** Same controlled terminology as the KB — "NiceHome Hub," "NiceHome Camera," "Camera Plus Plan" — not translated, not abbreviated.

---

## 4. Language-specific query rules

### English

- Neutral product-support user style. Complete questions.
- Avoid artificially short phrasing that would be unnatural in any other language (e.g., "Warranty length?" instead of "How long is the warranty?").
- Avoid over-formal phrasing ("To what period does the standard warranty pertain?") — conversational but clear.
- Avoid making English the ideal form: the English query should not be the one that most closely matches the KB wording, creating a retrieval advantage.
- Do not use abbreviations or informal contractions that have no equivalent register in Dutch or Turkish.

### Dutch

- Neutral, clear Dutch product-support style. Complete questions.
- Prefer "ik" / "mijn apparaat" framing in first-person questions (see §5 pronoun decision).
- Avoid direct translation from English — Dutch has its own natural question phrasing.
- Avoid legal or bureaucratic register.
- Mark any phrasing that is uncertain with `TODO_REVIEW` — these must be resolved before Stage 1 (no unresolved markers permitted at tokenizer-only stage).
- English device names in Dutch context are correct and expected ("Hoe lang duurt de garantie op mijn NiceHome Hub?").

### Turkish

- Natural Turkish product-support style. Complete questions.
- Use "cihazım" ("my device") phrasing where natural; avoid the verbose "cihazımın" construction where "cihazım" suffices.
- Avoid bureaucratic forms; avoid passive-heavy constructions when active is more natural.
- Product-name suffixes with an apostrophe are correct and expected ("NiceHome Hub'ımın garantisi ne kadar sürer?").
- Project-owner review required before Stage 1 — all Turkish queries must be reviewed before the tokenizer-only sanity gate runs.
- No `TODO_REVIEW` markers may remain unresolved in the Turkish file before Stage 1.

---

## 5. Register and pronoun decisions

These decisions are pre-committed for the entire query set. Per-intent notes may refine where a specific intent's scenario requires different framing.

| Language | Default register | Pronoun / address form | Notes |
|---|---|---|---|
| English | Neutral conversational support-style | First-person "I / my device" for experience-based queries; direct questions ("How long is the warranty?") for factual lookups | No "you" addressing the user to themselves; no formal "one" constructions |
| Dutch | Neutral conversational support-style | First-person "ik / mijn" for experience-based queries; direct questions for factual lookups; avoid excessive "u" | "Mijn NiceHome Hub" is the standard device reference; impersonal forms ("Hoe lang duurt de garantie?") acceptable for factual intents |
| Turkish | Natural conversational support-style | "Cihazım" / "benim NiceHome Hub'ım" for ownership contexts; direct questions ("Garanti süresi ne kadar?") for simple factual intents | Avoid "siz" address form unless a specific intent requires formal phrasing; impersonal imperative or direct question is preferred |

**Consistency rule:** the same intent rendered in all three languages should reflect approximately the same level of personalization and directness. If the English query uses first-person ("I opened my device…"), the Dutch and Turkish queries use equivalent first-person forms, not impersonal passive constructions.

---

## 6. Difficulty preservation

**Simple factual intents (INT-001–012):** One direct question, no scenario setup needed. Condition count = 0. The query simply asks for the fact. Example type: "How long is the warranty?" or "What does the Sensor measure?"

**Conditional policy intents (INT-013–024):** One to two sentences. The first sentence sets up the condition(s); the second asks the question. Every condition from `condition_count` must be present in the query text. The condition must be phrased as a user situation, not as a policy question. Examples:
- Correct: "I have a Gen 1 Hub — can I use a Gen 2 Sensor with it?"
- Incorrect: "Does a Gen 1 Hub support Gen 2 devices?" (policy-question form; acceptable difficulty-wise but slightly more abstract)
- Incorrect: "I bought a device. Does the Hub matter?" (condition stripped)

**Troubleshooting/process intents (INT-025–036):** Two to three sentences or a brief problem description. The user's problem state must be described clearly enough that the model knows to provide a procedure, not just a policy statement. Do not describe the expected steps in the query (that would be an answer hint). Example type: "My NiceHome Hub light is on but all my devices are showing as offline — how do I fix this?"

**Do not make one language more explicit than another:** if the English query specifies "within the return window" for a conditional return intent, the Dutch and Turkish queries must also specify the time constraint, not leave it implied.

---

## 7. Ambiguity control preservation

Queries must be worded so they do not accidentally resolve ambiguities that the model is supposed to resolve from the KB. The relevant ACs:

- **AC1 (30-day return vs. 30-day cloud storage):** Queries for return-window intents (INT-002, INT-029) must clearly frame a return context; queries for storage intents (INT-005) must clearly frame a subscription/storage context. Neither query should contain vocabulary that primes the other fact.
- **AC2 (5-second pairing vs. 10-second factory reset):** Pairing queries (INT-026) ask about pairing/adding a device, not resetting. Factory-reset queries (INT-031) ask about resetting, not pairing. The query wording must not blur the operation type.
- **AC3 (14-day trial vs. 30-day storage):** Trial-length query (INT-006) asks "how long is the free trial?" Storage query (INT-005) asks "how long are recordings kept?" — different questions; neither answer primes the other.
- **AC4 (live view / Hub-online):** Not directly tested by a query in v0.1; the IS1 secondary-observation protocol applies if an AC4 violation surfaces in INT-005 responses.
- **AC5 (soft reset vs. factory reset vs. Hub restart):** Each query in INT-025, INT-031, INT-033 must describe the specific problem or procedure that maps to one reset type. The connectivity-troubleshooting query (INT-025) describes an offline state, not a reset request. The factory-reset query (INT-031) asks explicitly about factory resetting. The soft-reset query (INT-033) describes an unresponsive Plug, not a factory-reset request.
- **AC6 (delay vs. loss):** INT-035 query must describe a delay scenario (shipment late, not confirmed lost). The query must not say "lost" — that would pre-resolve the condition.
- **AC7 (warranty vs. return window):** Warranty-period query (INT-001) asks about warranty. Return-window query (INT-002) asks about returns. Neither uses the other's terminology.
- **AC8 (refurbished warranty floor):** INT-019 query asks about the warranty on a refurbished replacement unit. It must not contain the floor value ("90 days") — that is the answer.
- **AC9 (F0807 two-chunk):** INT-031 query asks both how to factory reset the Hub AND what happens next. It must span both the procedure and the post-reset requirement, because both chunks are required for a PASS verdict.

---

## 8. Query rendering file structure

**Three files, one per language:**
```
docs/benchmark/v0.1/query-rendering-en.md
docs/benchmark/v0.1/query-rendering-nl.md
docs/benchmark/v0.1/query-rendering-tr.md
```

Each file contains exactly 36 entries. **Entry format:**

```
## INT-001

- intent_id: INT-001
- language: en  (or nl / tr)
- query_text: [the natural-language user query]
- linked_fact_ids: [from intent-set.md]
- expected_fact_set_id: INT-001  (resolves via expected-fact-mapping.md)
- notes: [any authoring notes, e.g. why a phrasing was chosen]
- review_status: DRAFT / NEEDS_REVIEW / APPROVED
```

`review_status` must reach APPROVED for all 36 entries before Stage 1 begins for that language. For Turkish, APPROVED requires project-owner sign-off. For Dutch, APPROVED requires either native-speaker sign-off or an explicit WAIVED_WITH_LIMITATION for internal use.

**No fact IDs, chunk IDs, or expected outcomes appear in `query_text`** — only in the metadata fields above the query. The content served to the agent is `query_text` only.

---

## 9. Quality gates for query renderings

These gates must pass before Stage 1 (tokenizer-only) begins. They extend the `quality-gates.md` Stage 1 readiness gate.

| Gate | Criterion | Check |
|---|---|---|
| Count | Exactly 36 queries per language | grep count on entry headers |
| Intent alignment | All 108 queries map to the same 36 intent IDs | diff intent_id lists across the three files |
| No answer hints | No query contains expected-answer content, KB quotes, or fact-ID references in `query_text` | Human review |
| No unsupported facts | No query introduces a policy claim not in the intent spec | Human review |
| Conditions preserved | Every `condition_count > 0` intent has its condition(s) present in all three query renderings | Human review against intent-set.md |
| Difficulty parity | No language's query is materially more explicit or more vague than the others for the same intent | Comparative human review |
| No `TODO_REVIEW` unresolved | Zero unresolved markers in any file before Stage 1 | grep |
| Dutch review status | APPROVED or WAIVED_WITH_LIMITATION with documented scope | Status field in each entry |
| Turkish review status | APPROVED (project-owner sign-off) | Status field in each entry |
| English compression check | No English query is materially shorter than Dutch/Turkish without a structural reason | Comparative review after Stage 1 tokenizer output |

**Stage 1 gate update (from quality-gates.md §12):** Stage 1 is BLOCKED until all three query-rendering files pass this gate.

---

## 10. Relationship to token-tax measurement

Query wording affects measured input token counts in two ways:

1. **Language/tokenizer effect (the signal):** A question expressed in Turkish agglutinative morphology will tokenize differently than the same question in English or Dutch — this is the expected token-tax effect, and it must not be suppressed.
2. **Authoring-length effect (noise):** If English queries are systematically shorter than Dutch/Turkish (e.g., English uses one-word noun-phrase questions while Turkish uses full sentences), the count difference includes an authoring artifact. Consistent sentence-style (§3) and the difficulty-parity gate (§9) limit this noise.

**Stage 1 will produce the first empirical query token-tax table** (input_token_tax_ratio = |t(query_nl)| / |t(query_en)|, etc.) before any API runs. This table should be inspected before Stage 2. If Dutch or Turkish query token counts are unexpectedly close to English (suggesting over-compression of Dutch/Turkish) or unexpectedly far (suggesting padding), the queries should be reviewed before API budget is spent.

The goal is natural controlled phrasing, not equal length. Token count differences are a measurement target, not a defect to be engineered away.

---

## 11. Open questions

- **QR1:** Should each query be strictly one sentence, or can a conditional intent use one setup sentence plus one question sentence?
  - *Direction: two sentences permitted for conditional and troubleshooting intents (setup + question); one sentence for simple factual intents where natural.*

- **QR2:** Should user queries mention exact dates or relative periods ("I bought it 35 days ago" vs. "I'm outside the return window")?
  - *Direction: use relative or status framing ("I'm within the 30-day window," "I bought it 3 years ago") rather than absolute calendar dates, to keep queries language-neutral and timeless.*

- **QR3:** Should conditional queries use natural uncertainty phrasing ("I think I might be outside the warranty — is that right?") or clear declarative conditions ("My device is 3 years old")?
  - *Direction: clear declarative conditions preferred for evaluation reliability; uncertainty phrasing risks making the condition ambiguous to the evaluator.*

- **QR4:** How much context should troubleshooting queries include?
  - *Direction: describe the observed symptom and any step already taken (if relevant), but not the expected diagnosis. Example: "My Hub light is on but my devices are showing offline" — correct. "My Hub light is on but my devices are offline — should I restart the Hub?" — incorrect (answer hint).*

- **QR5:** Should Dutch queries use "ik" consistently, or are impersonal ("Wat is de garantieduur?") and personal ("Hoe lang is de garantie op mijn apparaat?") mixed?
  - *Direction: simple factual intents use impersonal/direct questions; conditional and troubleshooting intents use "ik" / "mijn" to establish the user's situation. Consistent within each difficulty tier.*

- **QR6:** Should Turkish queries use "cihazım" consistently?
  - *Direction: yes for device-experience intents; direct impersonal questions for simple factual lookups ("Garanti süresi ne kadardır?"). Consistent within each difficulty tier.*

- **QR7:** What counts as over-compressed English?
  - *Direction: any English query shorter than 6 words that would naturally be longer in Dutch or Turkish is a candidate for compression review. Flag during Stage 1 token-ratio inspection. Threshold: if English input tokens for an intent are more than 25% fewer than Dutch, flag for review.*

- **QR8:** Who reviews Dutch query renderings?
  - *Direction: same as LR6 — for internal Stage 1, project owner reviews for obvious errors; for publication-grade claims, native Dutch reviewer required. Document the scope limitation.*

- **QR9:** Should Turkish query renderings be reviewed before or after Stage 1?
  - *Direction: before. Turkish project-owner review is a Stage 1 prerequisite (quality-gates.md §12, §9 gate for Turkish review_status = APPROVED). The tokenizer-only stage is low-cost but the review adds confidence that the query token ratios reflect natural Turkish, not awkward renderings.*

---

*This plan adds authoring constraints for queries only; it introduces no new policy content or intent definitions. Version: qr-plan-v0.1.0.*
