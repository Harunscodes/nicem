# NiceM Retrieval Design Decision v0.1

**Status:** Internal working document. Not public. Not a benchmark specification.
**Version:** 0.1 — first analysis of TF5 (retrieval design)
**Scope:** Analyzes the retrieval-design choice for NiceM's first validation benchmark. Does not write code, generate datasets, or finalize the choice if uncertainty remains — but makes the tradeoff explicit.
**Relationship to prior documents:** Follows `docs/methodology/task-family-selection-v0.1.md` (which flagged TF5 as the most consequential open design question) and operates within the success-gate and decomposition constraints of `docs/methodology/success-rubric-v0.1.md` and `docs/methodology/nicem-methodology-framework-v0.1.md` §7.

---

## 1. Purpose

Retrieval design is not an implementation detail. It determines what the experiment can observe.

NiceM's execution-tax hypothesis predicts that some languages incur overhead in the execution path — including the retrieval step: more retrieval calls, more retrieved tokens, more irrelevant retrievals, more retries triggered by poor retrieval. But whether that overhead can *appear* in the measurement at all depends on how retrieval is configured:

- If all language conditions retrieve from the same canonical knowledge base via multilingual embeddings, retrieval behavior may be largely equalized across languages — suppressing exactly the signal NiceM is looking for, or revealing that the signal is an artifact of avoidable design choices.
- If each language condition retrieves from its own same-language knowledge base, language-specific retrieval behavior is preserved — but a new variance source enters: the quality of each language's knowledge base and the embedding model's uneven multilingual competence.

In other words: the retrieval design choice decides whether retrieval overhead is *measured*, *suppressed*, or *confounded*. Making this choice deliberately — and documenting what the chosen design can and cannot show — is a precondition for interpreting any result. A cost difference found under one retrieval design does not automatically generalize to the other.

---

## 2. Context

Decisions already made that this document builds on:

- **Task family:** Fictional Product FAQ / policy QA with a synthetic knowledge base (FAQ, warranty policy, return policy, troubleshooting guide). See `task-family-selection-v0.1.md` §4.
- **Success gate:** Binary PASS/FAIL checked against **language-neutral expected fact-sets** (structured facts, not target strings in any language). See `success-rubric-v0.1.md` §3, §6 and task-family §11 (TF6).
- **Measurement:** Execution-tax is measured on the trajectories of successful runs — retrieval calls, retrieval tokens, reasoning steps, retries — after controlling for representation/generation token-tax. See framework §7.

The success gate is therefore already independent of retrieval design: regardless of which option is chosen below, success is checked against the same structured fact-set. What changes between options is the *path* the agent takes to reach (or fail to reach) that fact-set — which is precisely the thing execution-tax measurement is about.

---

## 3. Option A — Language-matched retrieval

**Definition:** Each language condition uses a knowledge base written in the same language as the user query. The Turkish query retrieves from a Turkish-language KB; the Dutch query from a Dutch KB; the English query from an English KB. All KBs are renderings of the same canonical fact-set.

```
Turkish query → Turkish KB
Dutch query   → Dutch KB
English query → English KB
```

**What it measures:** The full multilingual execution pipeline as a real deployment in that language would experience it — query tokenization, same-language embedding and retrieval, same-language reasoning over retrieved content, same-language generation. This is the closest analogue to "an enterprise deploys its FAQ assistant in Turkish for Turkish users."

**Strengths:**
- Ecologically valid: this is how monolingual production deployments actually work.
- Preserves language-specific retrieval behavior — if Turkish-language retrieval is genuinely harder (worse embedding quality, higher fragmentation interfering with chunking, longer chunks consuming more context), this design lets that show up.
- Each language condition is internally coherent: no cross-lingual hop inside a single run.
- The execution-tax signal, if found, is interpretable as "operating this workload in language X costs more end-to-end."

**Weaknesses:**
- Requires producing a full KB per language — translation or parallel authoring effort, plus bilingual review.
- Introduces KB-quality variance: if the Turkish KB is a slightly worse rendering of the canonical fact-set than the English KB, retrieval differences may reflect translation quality, not language properties.
- Cannot distinguish "retrieval is harder in Turkish" from "this Turkish KB was harder to retrieve from."

**Multilingual risks:**
- Embedding models perform unevenly across languages; retrieval quality differences may reflect the embedding model's training distribution rather than anything intrinsic to the language. This is arguably still execution-tax (the deployed stack really does serve that language worse), but it must be attributed honestly to the component responsible.
- Chunking strategies tuned on English text (sentence boundaries, chunk sizes in tokens) may behave differently on high-fertility languages — chunk size in tokens covers less semantic content.

**Impact on token-tax measurement:** Clean. Representation overhead (query tokens), retrieved-content token counts, and generation overhead are all observed in the language itself, so the token-tax baseline per language is directly measurable within the same runs.

**Impact on execution-tax measurement:** This is the design most likely to *reveal* retrieval-side execution-tax, because nothing in the pipeline neutralizes language differences. The cost is that the revealed signal is a composite: language properties + KB rendering quality + embedding model bias. Disentangling these requires care (e.g., KB quality audits, embedding-model sensitivity checks).

**Risk of translation-quality variance:** High and structural. Mitigations: author from the canonical fact-set rather than translating English prose; bilingual review of every KB; verify that every expected fact is recoverable from each language's KB by a human reader before any agent run (a "KB completeness check").

**Suitability for v0.1:** **High, with the KB-quality mitigation as a hard prerequisite.** It measures the question NiceM actually asks — does the same intent cost more to execute in some languages? — in its most natural form.

---

## 4. Option B — Language-neutral / canonical retrieval

**Definition:** All language conditions retrieve from a single shared canonical knowledge base — most likely English, or a structured/neutral representation — using multilingual embeddings (cross-lingual retrieval) or query translation before retrieval.

```
Turkish query → shared canonical KB
Dutch query   → shared canonical KB
English query → shared canonical KB
```

**What it measures:** Cross-lingual execution: the agent receives intent in language X, retrieves from a canonical store, reasons over canonical-language content, and responds in language X. This is also a real production pattern — many multilingual products maintain one English knowledge base and serve all languages from it.

**Strengths:**
- One KB: no translation-quality variance across KBs, dramatically lower construction cost.
- KB content is identical for all conditions by construction — any retrieval difference is attributable to the query side (query language, embedding behavior on the query, or query translation quality).
- Operationally the simplest design to build and audit.

**Weaknesses:**
- The English condition is structurally privileged: English queries retrieve same-language; all other languages retrieve cross-lingually. The comparison is no longer "language A vs. language B on equal footing" but "same-language retrieval vs. cross-lingual retrieval."
- Cross-lingual embedding quality varies sharply by language pair; measured differences may reflect the embedding model's cross-lingual alignment rather than execution properties of the language.
- The agent must bridge languages mid-run (query in Turkish, evidence in English, answer in Turkish), which introduces its own overhead — interesting, but a different phenomenon from the one Option A measures.

**Multilingual risks:**
- **English as hidden canonical baseline — this is the central risk.** The canonical KB being English does not just risk biasing evaluation; it builds an asymmetry into the experiment's structure. English runs get a shortcut every other language pays a toll to cross. Any measured "execution-tax" under this design is partly the cost of *not being the canonical language* — a real and policy-relevant cost, but one that conflates language properties with an infrastructure choice.
- Mitigation worth considering: make the canonical KB a *structured fact-store* (the fact-triples themselves) rather than English prose, so that no natural language is the canonical one. This is cleaner but less ecologically valid — production KBs are usually prose.

**Does it suppress or reveal retrieval overhead?** Both, in different places. It *suppresses* language-internal retrieval differences (there is no Turkish KB whose chunking or embedding behaves differently) and *reveals* cross-lingual bridging overhead (translation or cross-lingual embedding cost, query-document language mismatch). It measures a real overhead — but a different one than Option A.

**Suitability for v0.1:** **Medium.** Simpler and cheaper, but the structural English privilege makes the headline comparison harder to interpret as a clean test of NiceM's first claim. Better suited as a *second* condition that, contrasted with Option A, shows how much of execution-tax is design-dependent.

---

## 5. Option C — Compare both retrieval designs

**Definition:** Run the same intents, same languages, same agent architecture under both Option A (language-matched) and Option B (language-neutral) retrieval. A 2×N design: two retrieval conditions × N language conditions.

**What it measures:** Not just whether execution-tax exists, but whether it is *architecture-dependent* — which is NiceM's product thesis in miniature. If the cross-language cost gap is large under language-matched retrieval and small under canonical retrieval (or vice versa), then execution-tax is partly a function of design choices, and "recommend a cheaper architecture for the same intent" — the core NiceM product motion — has its first concrete instance.

**Strengths:**
- Directly tests the diagnose→recommend value proposition, not just the observe step.
- Protects against overfitting conclusions to one retrieval strategy: a result that holds under only one design is reported as such, not generalized.
- The contrast between conditions helps attribute overhead: differences that vanish under Option B were retrieval-side; differences that persist under both are upstream (representation, reasoning) or downstream (generation).

**Weaknesses / extra complexity:**
- Doubles the run count for the same statistical power per cell — and M8 (power calculation) is still unresolved.
- Requires building both the per-language KBs *and* the canonical retrieval pipeline.
- Doubles the surface area for design errors precisely when the methodology itself (rubric calibration, evaluator reliability, decomposition validity) is unvalidated.
- Two conditions invite premature causal storytelling from what is still a small pilot.

**Why it is valuable for NiceM:** It is the experiment NiceM ultimately needs — the bridge from "execution-tax exists" to "execution-tax can be reduced by design choices." A v0.1 that only runs one retrieval design answers the existence question in one configuration; the comparison answers the actionability question.

**v0.1 or v0.2?** **v0.2.** The methodology stack (rubric application, evaluator reliability, KB quality control, decomposition) must be validated on a single-condition pilot before a factorial design is informative. Running both conditions before the instrument is trusted produces twice as many numbers and no more confidence.

---

## 6. Recommended decision

**For v0.1: one retrieval design, deliberately chosen, with the alternative pre-registered as the v0.2 comparison.**

Specifically:

1. **v0.1 uses language-matched retrieval (Option A)** — each language condition retrieves from its own rendering of the canonical fact-set.
   - Rationale: NiceM's first claim is about the full execution cost of operating the same intent in different languages. Option A is the configuration in which that claim is most directly testable and most naturally interpretable. Option B's structural English privilege would entangle the first result with an infrastructure asymmetry.
2. **Expected fact-sets remain language-neutral regardless of retrieval design.** The canonical representation is the structured fact-set (TF6, TF7); each language KB is a rendering of it; success is always checked against the fact-set, never against any KB's prose.
3. **Hard prerequisite for Option A: KB quality control.** Author each KB from the canonical fact-set (not by translating English prose), bilingual-review every KB, and run a human KB-completeness check (every expected fact recoverable from every language's KB) before any agent run. Without this, retrieval differences are uninterpretable.
4. **Option B is pre-registered as the v0.2 contrast condition.** The A-vs-B comparison is where the architecture-dependence of execution-tax — and the NiceM recommend step — gets its first test.

**Residual uncertainty, stated honestly:** If KB quality control turns out to be infeasible at acceptable cost (e.g., bilingual review cannot be arranged for a chosen language), Option B with a *structured fact-store* (not English prose) as the canonical KB becomes the fallback for v0.1 — it sacrifices ecological validity for internal control. This document does not force the final call past that contingency; it fixes the default (Option A) and the tripwire that would flip it.

---

## 7. Relationship to token-tax vs. execution-tax

How retrieval design interacts with the framework §7 decomposition:

- **Token-tax appears in representation and generation tokens** — the query and answer token counts per language. Both retrieval designs measure this identically; it is unaffected by the choice.
- **Retrieval design may amplify, suppress, or transform execution-tax.** Under Option A, language-specific retrieval friction (embedding quality, chunking behavior, fragmentation effects on similarity search) is free to appear. Under Option B, those frictions are replaced by cross-lingual bridging costs. Under Option C, the difference between the two quantifies how much of the measured overhead is a design artifact.
- **Language-neutral retrieval may hide some language-specific retrieval costs.** A null retrieval-overhead result under Option B would not falsify retrieval-side execution-tax in general — it would show only that canonical retrieval avoids it (at the price of structurally privileging the canonical language).
- **Language-matched retrieval may reveal them but adds translation-quality variance.** A positive retrieval-overhead result under Option A is a composite signal until KB quality and embedding-model bias are audited.
- **Comparing both designs may show whether agent design can reduce execution-tax.** If it can, that is the strongest possible support for NiceM's product direction: the tax is real *and* actionable. If the gap is identical under both designs, the overhead is upstream of retrieval — also informative.

Either way, the falsification logic of framework §8 applies within each retrieval condition separately: results must be reported per configuration, never pooled across designs as if they measured the same thing.

---

## 8. Metrics affected by retrieval design

From the framework §6 trajectory metric set, the following are directly sensitive to this decision:

| Metric | Option A (language-matched) | Option B (language-neutral) |
|---|---|---|
| `retrieval_calls` | May vary by language if same-language retrieval quality differs | May vary by query language's cross-lingual alignment; English likely lowest |
| `retrieval_tokens` | Varies with both retrieval count and per-language chunk token-inflation (high-fertility languages retrieve more tokens for the same content) | Retrieved content is canonical-language; token count of retrieved content roughly constant across conditions |
| `retrieved_context_length` | Confounds retrieval behavior with target-language token fertility — must be reported in both tokens and semantic units (chunks/facts) | Comparable across conditions in tokens; the query side carries the variance |
| `retrieval_latency` | Reflects per-language index/embedding behavior | Reflects cross-lingual embedding or query-translation step |
| `irrelevant_retrieval_rate` | The key candidate execution-tax signal in this design | If elevated for non-English queries, signals cross-lingual alignment failure rather than language-internal retrieval difficulty |
| `retry_count` | Retries triggered by poor same-language retrieval | Retries triggered by failed cross-lingual bridging |
| `total_tokens` | Composite of all above plus token-tax | Composite, but retrieval-side variance is structurally reduced |
| `cost_per_successful_completion` | The headline metric; interpretable as full per-language operating cost | Interpretable as cost of serving language X from a canonical store |
| `uncertainty_rate` | Elevated rates in one language may indicate KB rendering ambiguity — audit before attributing to the language | Elevated rates may indicate meaning loss at the cross-lingual hop |

One measurement note: `retrieval_tokens` under Option A needs dual reporting — raw tokens *and* number of facts/chunks retrieved — because a high-fertility language retrieving the same two policy clauses will log more tokens for identical retrieval behavior. Counting only tokens would double-count token-tax as retrieval overhead.

---

## 9. Risks

- **English hidden baseline.** Under Option B, structurally built in. Under Option A, still present if the canonical fact-set is drafted in English and other KBs are translated from English prose. Mitigation: canonical representation is the structured fact-set; all language KBs (including English) are renderings of it (TF7).
- **Translation artifacts.** Awkward or unnatural KB prose in one language degrades retrieval and reasoning for reasons unrelated to the language itself. Mitigation: author-from-facts rather than translate-from-English; bilingual review.
- **Unequal KB quality.** Even with review, KBs may differ in clarity or completeness. Mitigation: pre-run KB completeness check (every expected fact recoverable by a human from every KB); treat any failing KB as a blocker, not a noise source.
- **Embedding model multilingual bias.** The embedding model's uneven language competence affects both options (same-language retrieval quality in A; cross-lingual alignment in B). Mitigation: document the embedding model as part of the measured configuration; consider a sensitivity check with a second embedding model in v0.2.
- **Overfitting to one retrieval strategy.** A v0.1 result under Option A is a result *about Option A*. Mitigation: state the configuration scope in every reported result; pre-register Option B as the v0.2 contrast.
- **Confusing retrieval failure with language failure.** The failure taxonomy (rubric §9) separates retrieval failure from language/translation failure — evaluators must apply this distinction, and trajectory logs should record *what* was retrieved so failures can be audited.
- **Too many variables in v0.1.** The strongest argument against Option C now. The pilot's job is to validate the instrument; one retrieval design, fully controlled, is the conservative choice.

---

## 10. Open questions

- **Should the synthetic KB be authored language-neutrally first?** Recommended yes: the canonical artifact is the structured fact-set; every language KB, including English, is a rendering of it. This is the operational answer to TF7 but the authoring protocol (who renders, in what order, with what review) is not yet written.
- **Should translations be human-created or machine-translated and reviewed?** Open. Machine translation + bilingual human review is cheaper and probably adequate for a small KB; fully human authoring from the fact-set is more valid. Decision depends on language choice and available reviewers (links to rubric §13, bilingual reviewer question).
- **Should expected fact-sets be separate from prose KBs?** Yes — already the working position (TF6): the fact-set is the success-check artifact and the canonical source; the prose KBs are retrieval surfaces. These must never be the same document.
- **Should v0.1 use one retrieval design and v0.2 compare two?** This document recommends exactly that (Option A in v0.1, A-vs-B in v0.2), with the structured-fact-store fallback if KB quality control proves infeasible. The recommendation stands unless the contingency triggers.
- **Which retrieval condition best tests NiceM's first claim?** Language-matched (Option A), because the first claim is about the end-to-end cost of executing the same intent in different languages as actually deployed — not about the cost of bridging to a canonical store. But the *product* claim (execution-tax is reducible by design) requires the Option C comparison, which is why it is pre-registered for v0.2 rather than dropped.
