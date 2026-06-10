# NiceM — Language Selection v0.1

**Status:** Decision made — English, Dutch, Turkish recommended for v0.1
**Addresses:** TF3 (language selection) from `docs/open-questions.md`
**Depends on:** `docs/methodology/task-family-selection-v0.1.md`, `docs/methodology/retrieval-design-decision-v0.1.md`
**Feeds into:** Dataset construction, KB authoring, success rubric application, execution-tax measurement

---

## 1. Purpose

Language selection is not a cosmetic choice. It determines:

- Which tokenization profiles are represented in the measurement
- Whether token-tax variation is detectable across conditions
- Whether KB quality control is feasible before a benchmark run
- Whether success evaluation can be done without English-language-shaped bias

The goal of v0.1 language selection is to choose a **minimal, tractable set** that produces meaningful token-tax variation, is evaluable by the project owner, and does not create insurmountable KB quality-control burden before the first validation run.

**Important framing:** English is included as a high-resource baseline condition — not as the canonical source of truth. The canonical artifact for all language conditions is the **structured fact-set** (a language-neutral representation of KB content). English-language KB renderings are authored from that fact-set, exactly as all other language renderings are. This prevents English from functioning as a hidden upstream reference that shapes what "correct" looks like in other languages.

---

## 2. Selection Criteria

A language is suitable for v0.1 if it meets all of the following:

| Criterion | Requirement |
|---|---|
| **Tokenization profile** | Meaningfully different from English (or: English-like as baseline) |
| **Evaluator competence** | Project owner can read and verify KB content and success judgments |
| **KB feasibility** | Synthetic KB can be authored from the fact-set without translation artifacts |
| **Script diversity** | At least one non-Latin script or significantly different morphological structure |
| **Resource tier** | At least one lower-resource or structurally unusual language to probe execution-tax |
| **Manageability** | Full set is small enough that KB quality control can be completed before a benchmark run |

A language is **not suitable for v0.1** if:
- Project owner cannot verify KB content in that language
- No bilingual reviewer is available for pre-run completeness check
- The language requires a KB rendering approach that has not yet been tested

---

## 3. Recommended v0.1 Language Set

### English — High-resource Latin-script baseline

| Property | Value |
|---|---|
| Script | Latin |
| Morphology | Analytic (low inflection) |
| Tokenization profile | Reference condition — baseline fertility |
| Token-tax expectation | Baseline (by definition) |
| KB feasibility | High — native authoring |
| Evaluator competence | High — project owner |
| Role in measurement | Baseline execution-tax condition |

**Note:** English is the baseline measurement condition. It is not the canonical source. The structured fact-set is the canonical artifact. The English KB is authored from that fact-set, not the other way around.

---

### Dutch — High-resource Latin-script comparison

| Property | Value |
|---|---|
| Script | Latin |
| Morphology | Moderately inflected; compound formation differs from English |
| Tokenization profile | Close to English but with systematic differences in compound words and inflected forms |
| Token-tax expectation | Mild premium over English — estimated 1.1×–1.4× based on Petrov et al. range for European languages |
| KB feasibility | High — project owner can author and verify |
| Evaluator competence | High — project owner native-level Dutch |
| Role in measurement | Near-baseline comparison; controls for script while introducing mild morphological difference |

**Why Dutch:** It allows a measurement within the Latin-script family where the project owner can directly inspect KB quality and judge success without reliance on a third-party reviewer. A near-baseline comparison is necessary — without it, any difference between English and Turkish conflates script, morphology, and tokenization effects.

---

### Turkish — Agglutinative, moderate-resource Latin-script condition

| Property | Value |
|---|---|
| Script | Latin (since 1928 reform) |
| Morphology | Agglutinative — suffixes stack onto roots; single words routinely express what English phrases require |
| Tokenization profile | Higher fertility expected — agglutinative words may tokenize into many subword units |
| Token-tax expectation | Moderate-to-significant premium — potentially 1.5×–2.5× based on morphological load; specific measurement needed |
| KB feasibility | Moderate — project owner has inspection capability; bilingual review required before benchmark |
| Evaluator competence | Moderate — project owner can inspect Turkish; bilingual review for KB completeness check |
| Role in measurement | Key execution-tax probe condition — morphological difference without script change; allows isolation of morphological token-tax |

**Why Turkish:** Turkish introduces agglutinative morphology within the Latin script family. This allows token-tax effects from morphological structure to be isolated from script effects. Turkish is also well-represented in major tokenizers (better coverage than, say, Swahili), making token-tax measurement more tractable than a low-resource language at v0.1. The user can inspect Turkish content, which satisfies the evaluator-competence criterion.

**Turkish token-tax note:** The academic literature (Petrov et al., Ahia et al.) does not specifically report Turkish in the headline findings, but the morphological structure of Turkish is well-established as a tokenization challenge. The NiceM v0.1 benchmark will produce direct Turkish fertility measurements rather than relying on extrapolation.

---

### Summary: v0.1 Language Set

| Language | Script | Morphology | Token-tax expectation | Role |
|---|---|---|---|---|
| English | Latin | Analytic | Baseline | Reference condition |
| Dutch | Latin | Mildly inflected | Mild premium (~1.1×–1.4×) | Near-baseline Latin comparison |
| Turkish | Latin | Agglutinative | Moderate premium (~1.5×–2.5×, to be measured) | Morphological variation probe |

---

## 4. Why Not More Languages in v0.1

The primary constraint is **KB quality control**, not statistical power.

Each language condition requires:
1. A KB rendered in that language, authored from the structured fact-set
2. A bilingual review confirming the rendering covers all facts and introduces no translation artifacts
3. A pre-run completeness check (does the KB actually answer all five task skeletons in that language?)
4. A success evaluator who can judge task completion without English-shaped output bias

For v0.1, adding a fourth language means:
- An additional KB rendering cycle
- An additional bilingual reviewer (or an additional burden on the project owner)
- An additional pre-run completeness check
- Risk that KB quality is uneven across conditions, introducing a confound

**Three conditions is the practical minimum for v0.1:**
- One is not a comparison.
- Two conditions confound language with everything else.
- Three conditions allow a minimal comparison with one near-baseline and one divergent condition, while keeping KB-preparation work tractable.

Statistical power considerations (M8) will eventually set a floor on the number of task instances per language, but KB quality control sets the ceiling on how many languages v0.1 can support without compromising measurement integrity.

---

## 5. Candidate v0.2 Expansion Languages

These languages are analyzed but **not recommended for v0.1**. They are candidates for v0.2 or later once KB quality-control processes are established and a v0.1 baseline exists.

### Arabic — RTL, high-resource, morphologically rich

| Property | Value |
|---|---|
| Script | Arabic (RTL) |
| Morphology | Root-and-pattern; high inflection; vowel marking optional |
| Token-tax expectation | High — Ahia et al. reports Arabic ~3.04× vs. English; confirmed by Petrov et al. |
| KB feasibility | Requires dedicated Arabic KB author and bilingual reviewer |
| Risk | Script direction in KB rendering; vowelization choices affect tokenization |
| Priority | High — well-documented token-tax; highest academic-source support |

**Why defer:** No in-house Arabic KB authoring capacity at v0.1. Requires external bilingual reviewer. High value but non-trivial preparation cost.

---

### Hindi — Devanagari, high-resource

| Property | Value |
|---|---|
| Script | Devanagari |
| Morphology | Moderately inflected |
| Token-tax expectation | Moderate — Ahia et al. reports Hindi in the mid-range |
| KB feasibility | Requires Devanagari-capable KB author |
| Priority | Medium — important for South Asian coverage; script diversity value |

---

### Swahili — Latin-script, lower-resource, agglutinative

| Property | Value |
|---|---|
| Script | Latin |
| Morphology | Agglutinative (Bantu noun class system) |
| Token-tax expectation | Moderate-to-high; fewer training tokens → higher fertility expected |
| KB feasibility | Requires Swahili-capable KB author and bilingual reviewer |
| Priority | Medium — important for African-language representation; relevant to Lundin et al. findings |

---

### Korean — Hangul, moderate-resource, agglutinative

| Property | Value |
|---|---|
| Script | Hangul (phonemic syllabic blocks) |
| Morphology | Agglutinative; SOV word order |
| Token-tax expectation | Moderate — Hangul tokenizes differently from Latin scripts; subword units at syllable level |
| KB feasibility | Requires Korean-capable KB author |
| Priority | Medium — East Asian script diversity; high model coverage (Korean is well-represented in major LLMs) |

---

### Japanese — Multi-script, high-resource

| Property | Value |
|---|---|
| Script | Hiragana + Katakana + Kanji (mixed-script) |
| Morphology | Agglutinative; no spaces between words |
| Token-tax expectation | Variable — no word-boundary spaces create unusual tokenization behavior |
| KB feasibility | Requires Japanese-capable KB author |
| Priority | Medium — high practical relevance; unusual tokenization profile |

---

### Finnish — Latin-script, moderate-resource, agglutinative

| Property | Value |
|---|---|
| Script | Latin |
| Morphology | Highly agglutinative (15 grammatical cases; long compound words) |
| Token-tax expectation | High fertility within Latin script — useful comparison with Turkish (both agglutinative, both Latin) |
| KB feasibility | Requires Finnish-capable KB author |
| Priority | Low-medium — interesting as a second agglutinative Latin-script language; lower practical relevance than Arabic or Hindi |

---

### Spanish / French — High-resource Latin-script

| Property | Value |
|---|---|
| Script | Latin |
| Morphology | Moderately inflected; gendered nouns |
| Token-tax expectation | Low — close to English; Petrov et al. shows European Romance languages within ~1.5× |
| KB feasibility | High |
| Priority | Low for execution-tax isolation — too close to English baseline to probe execution-tax meaningfully; useful only if the research question shifts to Romance-vs-Germanic comparison |

---

### v0.2 Language Priority Ranking

| Rank | Language | Rationale |
|---|---|---|
| 1 | Arabic | Highest academic-documented token-tax; script diversity; high practical relevance |
| 2 | Hindi | Devanagari script; South Asian coverage; moderate token-tax |
| 3 | Swahili | African-language representation; connects to Lundin findings; agglutinative |
| 4 | Korean | Hangul script; East Asian coverage; good model support |
| 5 | Japanese | Unique multi-script tokenization; high practical relevance |
| 6 | Finnish | Second agglutinative Latin-script; more controlled comparison with Turkish |

---

## 6. Relationship to Token-Tax

Token-tax enters the language selection decision in two ways:

**Direct:** The language set should span a meaningful range of tokenization profiles. English as the analytic baseline, Dutch as a mild premium, and Turkish as a moderate-to-high premium creates a gradient that makes token-tax variation detectable.

**Indirect:** Token-tax must be measured per-language before execution-tax can be decomposed. The token-tax component in the execution-tax decomposition (representation + generation overhead) requires per-language fertility measurements from the actual tokenizer used in the benchmark. These are NiceM v0.1 empirical measurements, not extrapolations from Petrov/Ahia/Lundin (which used different corpora and tasks).

**What the academic literature supports for v0.1 languages:**
- English: baseline (by definition — literature uses English as reference)
- Dutch: European language; expected in the 1.1×–1.4× range implied by Petrov's European-language findings
- Turkish: agglutinative; no specific Petrov/Ahia headline figure — NiceM v0.1 will generate the first direct measurement for Turkish in a Product FAQ task context

---

## 7. Relationship to Execution-Tax

Execution-tax is a NiceM hypothesis. Language selection affects execution-tax measurement in the following ways:

**Execution-tax components that may vary by language:**

| Component | Why language may matter |
|---|---|
| retrieval_call_count | If the KB rendering in one language requires more retrieval calls to find the relevant fact |
| retrieval_tokens | Depends on KB rendering length, which is language-dependent |
| reasoning_steps | If the agent requires more reasoning steps to reconcile a morphologically complex query with KB content |
| retry_count | If factual coverage gaps in the KB cause retries (KB quality control mitigates but does not eliminate) |
| correction_flag | If the agent misreads a morphologically complex form and produces a wrong answer requiring human correction |

**Important boundary:** These are hypotheses about which execution-tax components may be language-sensitive. They are not assumed to be true — they are what NiceM v0.1 will measure. English, Dutch, and Turkish were selected partly because they are predicted (from the token-tax literature and morphological reasoning) to produce detectable variation, and partly because they are evaluable by the project owner.

**What execution-tax measurement requires beyond token-tax:**
- Same human intent expressed in each language condition
- Same KB fact-set underlying each KB rendering
- Success gate applied equivalently in each language (per success-rubric-v0.1)
- Per-condition trajectory logging (all six execution-tax components)

---

## 8. Quality-Control Requirements Per Language

Before any benchmark run, each language condition must pass the following quality-control gate (from retrieval-design-decision-v0.1 §4):

### English

| Requirement | Notes |
|---|---|
| KB authored from fact-set | Direct authoring — no translation step |
| Bilingual review | Not required — project owner is native |
| Pre-run completeness check | Verify all five task skeletons answerable from KB |
| Evaluator competence | Project owner — no external reviewer needed |
| Risk | Low |

### Dutch

| Requirement | Notes |
|---|---|
| KB authored from fact-set | Direct authoring — project owner authors in Dutch from fact-set |
| Bilingual review | Project owner can self-review (native-level Dutch) |
| Pre-run completeness check | Verify all five task skeletons answerable from Dutch KB |
| Evaluator competence | Project owner — no external reviewer needed |
| Risk | Low |

### Turkish

| Requirement | Notes |
|---|---|
| KB authored from fact-set | Author in Turkish from fact-set — do NOT translate from English |
| Bilingual review | **Required** — project owner can inspect but a bilingual reviewer should confirm KB completeness |
| Pre-run completeness check | Verify all five task skeletons answerable from Turkish KB |
| Evaluator competence | Project owner can make pass/fail judgments; bilingual reviewer for borderline cases |
| Risk | Medium — agglutinative morphology creates more surface variation; KB completeness check is critical |
| Fallback | If bilingual review is infeasible: defer Turkish to v0.2 and run v0.1 as English + Dutch only |

**Turkish fallback rule:** If a qualified bilingual reviewer is not available before the benchmark run, Turkish should be deferred to v0.2. Running Turkish without KB quality control would introduce a confound between "execution-tax from language" and "execution-tax from KB gaps." This would invalidate the Turkish condition results.

---

## 9. Reporting Boundaries

Results from a v0.1 benchmark using this language set are valid only within the following scope:

| Boundary | Implication |
|---|---|
| Task family: Product FAQ / policy QA | Results do not generalize to other task families (travel planning, scheduling, etc.) |
| Languages: English, Dutch, Turkish | Results do not generalize to Arabic, Hindi, or other language families |
| KB type: Fictional synthetic product KB | Results do not generalize to real-world or proprietary KBs |
| Retrieval: Language-matched (Option A) | Results reflect language-matched retrieval architecture only |
| Tokenizer/model: TBD at dataset construction | Results are specific to the model(s) used — see open question LS4 |
| Agent design: TBD | Results are specific to the agent implementation used |

**Claims that v0.1 results DO support:**
- Whether English, Dutch, and Turkish show different token-counts, latency, cost, and trajectory metrics on Product FAQ tasks
- Whether agglutinative morphology (Turkish vs. English/Dutch) produces detectable execution overhead under language-matched retrieval
- Whether the success gate applies equivalently across the three language conditions

**Claims that v0.1 results DO NOT support:**
- Generalization to other language families
- Generalization to non-Latin scripts
- Generalization to other task families
- Proof that execution-tax exists across AI workflows in general

---

## 10. Open Questions (LS1–LS6)

| ID | Question | Status | Notes |
|---|---|---|---|
| LS1 | Who will perform the bilingual review of the Turkish KB? | Open | Must be identified before Turkish KB construction begins |
| LS2 | What formality register should KB and task prompts use in Turkish? | Open | Formal vs. informal affects morphology and tokenization; must be standardized before authoring |
| LS3 | Should Dutch and Turkish task prompts be authored independently or adapted from English task prompts? | Direction set | Author from fact-set (same instruction as KB) — do NOT translate from English task prompts |
| LS4 | Which tokenizer and model will be used as the primary measurement baseline? | Open | Token-tax component of execution-tax decomposition depends on this; must be decided before dataset construction |
| LS5 | Should v0.1 include a fourth language (e.g., Spanish) as a near-English Latin-script control, to isolate Dutch-specific effects? | Open | Would increase KB burden; only add if Dutch-English comparison shows unexpected results |
| LS6 | At what fertility threshold does the Turkish condition become the high-token-tax condition vs. merely a mild-premium condition? | Open | Answered empirically in v0.1 benchmark — no pre-specification needed |

---

## Dependencies and Update Log

| Document | What changes with this decision |
|---|---|
| `docs/methodology/task-family-selection-v0.1.md` | Language set now specified: English, Dutch, Turkish; TF3 now has a decision |
| `docs/methodology/retrieval-design-decision-v0.1.md` | Language-matched retrieval (Option A) now applies to English, Dutch, Turkish specifically |
| `docs/open-questions.md` | TF3 updated from Open to Decision made; LS1–LS6 added |
| `docs/source-map.md` | Language-selection-v0.1.md added to related internal documents |

---

*v0.1 — 2026-06-10*
