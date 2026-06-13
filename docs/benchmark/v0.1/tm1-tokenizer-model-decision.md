# TM1 Tokenizer / Model Decision v0.1

**Status:** PROPOSED — awaiting project-owner confirmation
**Role:** Resolves open question TM1 (which provider/model v0.1 uses) with a concrete recommended default. This is the operational decision note that sits beneath the decision *rules* in `tokenizer-model-choice-v0.1.md`. That document defines the criteria and staged approach; this document records the actual proposed choice and its consequences.
**Version:** tm1-v0.1.0
**Depends on:** `docs/methodology/tokenizer-model-choice-v0.1.md`, `docs/methodology/baseline-token-tax-calculation-v0.1.md`, `docs/benchmark/v0.1/quality-gates.md`
**Feeds into:** Stage 1 tokenizer-only sanity gate (unblocks it once confirmed); Stage 2/3 model execution

---

## 1. Purpose

TM1 is the last remaining blocker before Stage 1 can run. Stage 1 is a tokenizer-only sanity gate: it tokenizes all 108 query renderings and all 117 KB chunks (39 EN + 39 NL + 39 TR) and computes per-intent and per-chunk token-tax ratios (Dutch/English, Turkish/English). It requires **no API calls**.

Even though Stage 1 makes no API calls, the tokenizer cannot be chosen arbitrarily. Three reasons make TM1 load-bearing:

1. **Token-tax ratios are tokenizer-dependent.** A Turkish/English ratio of 1.8× under one tokenizer may be 1.3× under another. The numbers Stage 1 produces are only meaningful, and only comparable to the literature (Petrov, Ahia, Lundin), if the tokenizer is fixed and named.
2. **The Stage 1 tokenizer must match the Stage 2/3 execution model's tokenizer.** The residual-overhead method (baseline-token-tax §9) subtracts a token-scaled cost expectation from observed run costs. If counting and execution use different tokenizers, the residual is computed in the wrong unit and becomes meaningless. Choosing the tokenizer therefore commits us, in effect, to the model family for later execution.
3. **Re-running Stage 1 is the cost of getting this wrong.** If the model family changes after Stage 1, Stage 1 must be repeated under the new tokenizer. Deciding TM1 now — before Stage 1 — avoids that rework.

This note exists so the choice is explicit, justified, and reversible only by an explicit version bump rather than by drift.

---

## 2. Decision rule

> **Use the tokenizer associated with the model family intended for later Agent A (Direct LLM) and Agent B (Simple RAG) execution.**

The tokenizer used in Stage 1 is not an independent choice. It is determined by the model family we intend to run in Stage 2/3. Picking the tokenizer *is* picking the model family. This is a direct application of the core principle in `tokenizer-model-choice-v0.1.md` §2: one model family, one tokenizer, across all language conditions and both agent designs.

---

## 3. Candidate options

All candidates assume a single model family for the entire v0.1 pilot. The relevant question for each is: *is the tokenizer accessible for local Stage 1 counting, and is later API execution easy to operationalize?*

| Option | Tokenizer | Stage 1 accessibility | Later execution | Notes |
|---|---|---|---|---|
| **OpenAI GPT-4.1 / GPT-4.1-mini** | The model family's published byte-level BPE encoding, accessible locally via `tiktoken` (encoding name `TO_BE_CONFIRMED_IN_STAGE_1_TOOLING` — verify the exact `tiktoken` encoding mapped to the GPT-4.1 family) | High — `tiktoken` runs locally at zero cost; counts match provider billing for this family | Easy — stable hosted API, per-call token usage reported, version-pinnable model IDs | Dutch coverage strong; Turkish adequate but must be confirmed in the Stage 2 smoke test |
| **OpenAI GPT-5-class** | The newer family's encoding, *if* `tiktoken` (or equivalent) tooling exposes it at Stage 1 time | Conditional — only if the local tokenizer for the family is published and available; otherwise Stage 1 cannot be run locally for this family | Easy if available via the same hosted API | Use only if tooling clearly supports local counting; do not adopt a family whose tokenizer cannot be inspected locally for Stage 1 |
| **Anthropic Claude** | Claude's tokenizer | Conditional — viable only if Claude is the intended Stage 2/3 execution model; local exact-count tooling availability must be confirmed before relying on it for Stage 1 | Easy — stable hosted API | Legitimate choice *if and only if* later experiments will run on Claude. Do not count tokens with a Claude tokenizer and then execute on a different family. |
| **Local / open-weights tokenizer** | A Hugging Face tokenizer for a specific open model family | Maximum — exact tokenizer object, fully inspectable | Heavier — requires local/cloud GPU runtime; multilingual (esp. Turkish) competence varies and must be verified | Choose **only** if Stage 2/3 execution will also use that same open model family. Do not mix an open tokenizer with a commercial execution model. |

**Cross-cutting constraint:** whichever option is chosen, the Stage 1 counting tokenizer and the Stage 2/3 execution model must belong to the same family. Mixing them violates the decision rule in §2 and invalidates the residual-overhead calculation.

---

## 4. Recommended v0.1 choice

**Recommended default (use unless the project owner overrides):**

> **OpenAI GPT-4.1-mini (or GPT-4.1) — model family and tokenizer — for all of v0.1.**

Rationale:

- **Tokenizer access for Stage 1 is easy.** The family's encoding is available locally via `tiktoken`, so Stage 1 runs at zero API cost and the local counts match what the provider bills.
- **Later API execution is easy to operationalize.** A stable hosted API, per-call input/output token reporting, version-pinnable model IDs, and a published price table satisfy the §6 selection criteria and §8 pricing requirements in `tokenizer-model-choice-v0.1.md`.
- **GPT-4.1-mini is the proposed default tier** because it is cheaper for the smoke test and likely sufficient for short-answer Product FAQ / Policy QA. Whether the full Stage 3 run needs GPT-4.1 instead of GPT-4.1-mini is an open question (§8) to be settled by the Stage 2 smoke test — but both share the same family and tokenizer, so this tier choice does **not** affect Stage 1.

**Tokenizer naming:** the exact `tiktoken` encoding name to use for the GPT-4.1 family is marked `TO_BE_CONFIRMED_IN_STAGE_1_TOOLING`. It must be verified against the installed tooling before Stage 1 counts are recorded, and logged as `tokenizer_name` / `tokenizer_version` per the logging schema.

**Override note:** if the project owner intends to run later experiments on Claude or an open model, choose that family's tokenizer instead — the decision rule (§2) then forces a different tokenizer for Stage 1, and this recommendation is superseded.

---

## 5. Non-goals

For the avoidance of doubt, v0.1 explicitly does **not**:

- **Compare tokenizers.** Only one tokenizer is used. Comparing tokenizers is a separate study.
- **Optimize for the cheapest model.** Cost matters (TM5/BS6 budget), but the v0.1 goal is a clean, interpretable single-family measurement — not minimizing spend.
- **Use one tokenizer for Stage 1 and an unrelated model family for Stage 2/3.** The Stage 1 counting tokenizer and the execution model must be the same family. Mixing them invalidates the residual-overhead calculation.
- **Claim universal token-tax from one tokenizer.** All v0.1 token-tax numbers are specific to the chosen tokenizer and must be reported with the tokenizer/model named. A different tokenizer would yield different ratios.

---

## 6. Stage 1 implications

With the tokenizer chosen, Stage 1 (tokenizer-only sanity gate) can proceed. It will:

- Compute **query token counts per intent and per language** for all 108 query renderings (36 × EN/NL/TR).
- Compute **KB chunk token counts per chunk and per language** for all 117 chunks (39 × EN/NL/TR).
- Compute **token-tax ratios**: Dutch/English and Turkish/English, per the baseline-token-tax §6 conventions.
- **Inspect outliers before any API run.** Dutch ratios are expected ~1.1×–1.5× (Petrov range); Turkish is expected clearly above Dutch (no strong literature headline figure — this is a NiceM empirical contribution). A Dutch ratio of 0.9× or a Turkish ratio of 3× signals a KB rendering or tokenizer-assumption problem to fix before spending budget.
- Establish **only the token-tax baseline** — Stage 1 produces no PASS/FAIL, no trajectory metrics, no cost-per-successful-completion, and therefore **says nothing about execution-tax**. Execution-tax remains a hypothesis to be tested in Stage 2/3.

---

## 7. Stage 2 implications

Once Stage 1 passes and the project owner approves the model:

- **Agent A and Agent B use the same selected model family** wherever possible. The only intended variable between them is whether retrieval is used; differing models would confound design with model.
- **The embedding model for Agent B is a separate decision (TM8/AD2).** The completion model chosen here does not determine the retrieval embedding model; that has its own tokenizer, cost, and multilingual-coverage requirement (it must retrieve correctly from the non-English KB renderings under the language-matched design).
- **`pricing_version` must be logged** per run once API execution begins, using a dated identifier for the price table (logging-schema §7).
- **Changing the model family after Stage 1 invalidates direct comparability** unless Stage 1 is rerun under the new tokenizer. If the provider updates the model or tokenizer between Stage 2 and Stage 3, the smoke test must be rerun on the new version (tokenizer-model-choice §9).

---

## 8. Open questions

| ID | Question | Status |
|---|---|---|
| TM1-a | Exact tokenizer package/tool and encoding name to use | `TO_BE_CONFIRMED_IN_STAGE_1_TOOLING` — verify the `tiktoken` encoding mapped to the GPT-4.1 family before recording Stage 1 counts |
| TM1-b | Exact model ID for Agent A (Direct LLM) | Open — a version-pinned GPT-4.1-mini/GPT-4.1 identifier, not a "latest" alias; confirm at Stage 2 setup |
| TM1-c | Exact model ID for Agent B (Simple RAG completion model) | Open — must be the same family/version as Agent A |
| TM1-d | Is GPT-4.1-mini sufficient for the smoke test, or is GPT-4.1 needed for Stage 3? | Open — settled by the Stage 2 smoke test; both share the same tokenizer, so this does not affect Stage 1 |
| TM8 | Embedding model for Agent B | Open — separate decision; not resolved here |
| TM5 / BS6 | Pilot budget | Open — must be approved before any API spend (Stage 2+); does not block Stage 1 |

---

## 9. Decision status

**PROPOSED, awaiting project-owner confirmation.**

The recommended default is OpenAI GPT-4.1-mini / GPT-4.1 (one family, one tokenizer) for all of v0.1. On project-owner approval:

- TM1 moves to RESOLVED in `quality-gates.md` and `open-questions.md`.
- Stage 1 becomes unblocked and can run (after confirming the exact `tiktoken` encoding name, TM1-a).
- TM1-b/c/d, TM8, and TM5/BS6 remain open but do **not** block Stage 1; they gate Stage 2+.

---

*Version: tm1-v0.1.0. This note records the proposed resolution of TM1. The governing decision rules are in `docs/methodology/tokenizer-model-choice-v0.1.md`. Token-tax results are tokenizer-specific and must always be reported with the tokenizer and model named.*
