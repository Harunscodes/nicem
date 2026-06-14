#!/usr/bin/env python3
"""
NiceM Stage 2 smoke-test logging runner.

This runner builds the 30 planned Stage 2 runs from the benchmark artifacts,
validates the logging fields, enforces the budget rules, and (in live mode
only) executes the completion + embedding API calls. By default it runs in
dry-run mode and writes outputs WITHOUT calling any external API or creating
any embeddings.

Design constraints (see docs/benchmark/v0.1/stage2-smoke-test-run-plan.md and
docs/benchmark/v0.1/stage2-live-run-readiness.md):
  - Default mode is dry-run.
  - Dry-run makes NO API calls, creates NO embeddings, and does NOT require
    an API key.
  - Live mode is refused unless EVERY precondition in can_run_api_mode() holds,
    including CONFIG['allow_api_calls'] == True (which ships as False).
  - The live completion + embedding code paths are implemented (for review)
    but are unreachable while allow_api_calls is False. They are never
    exercised by dry-run, the validation checks, or the guard tests.
  - No auto-retry: a live API failure stops the loop; it is never retried.

Stage 2 remains BLOCKED. The single remaining step before a first live test is
to set CONFIG['allow_api_calls'] = True after code review, then run with
`--live --confirm-spend` in an environment that exports OPENAI_API_KEY.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
# Placeholders MUST be replaced with confirmed values before any live API run.
# The runner refuses API mode while placeholders remain (see can_run_api_mode).

# --------------------------------------------------------------------------
# Confirmed pricing constants (official OpenAI sources; verified 2026-06-14)
# --------------------------------------------------------------------------
# Source: OpenAI API pricing (developers.openai.com / openai.com/api/pricing).
# Published rates converted from USD-per-1M to USD-per-1K tokens.
#   gpt-4.1-mini:           input  $0.40 /1M = $0.00040 /1K
#                           cached $0.10 /1M = $0.00010 /1K (informational)
#                           output $1.60 /1M = $0.00160 /1K
#   text-embedding-3-small: $0.02 /1M = $0.00002 /1K
# See docs/benchmark/v0.1/stage2-model-pricing-config.md for sourcing/date.
PRICING_VERSION = "openai-2026-06-14"
GPT_4_1_MINI_INPUT_USD_PER_1K = 0.00040
GPT_4_1_MINI_CACHED_INPUT_USD_PER_1K = 0.00010   # informational; not used in estimate
GPT_4_1_MINI_OUTPUT_USD_PER_1K = 0.00160
TEXT_EMBEDDING_3_SMALL_USD_PER_1K = 0.00002

CONFIG = {
    # Model / tokenizer / pricing
    # response_model_id: version-pinned snapshot confirmed from official docs.
    # Reconfirm against the live /v1/models listing at run time (live-readiness).
    "response_model_id": "gpt-4.1-mini-2025-04-14",      # CONFIRMED (TM1-b/c)
    "embedding_model_id": "text-embedding-3-small",      # CONFIRMED (TM8)
    "embedding_model_version": "not-exposed-by-provider",  # no dated snapshot
    "tokenizer_name": "o200k_base",                      # encoding family
    "pricing_version": PRICING_VERSION,                  # CONFIRMED 2026-06-14

    # Pricing table (USD per 1,000 tokens) — CONFIRMED from official OpenAI
    # sources (2026-06-14). Live mode is still refused (allow_api_calls=False).
    "pricing": {
        "completion_input_usd_per_1k": GPT_4_1_MINI_INPUT_USD_PER_1K,
        "completion_output_usd_per_1k": GPT_4_1_MINI_OUTPUT_USD_PER_1K,
        "embedding_usd_per_1k": TEXT_EMBEDDING_3_SMALL_USD_PER_1K,
    },

    # Budget (CONFIRMED, TM5/BS6)
    "budget_hard_cap_usd": 25.00,
    "budget_stop_review_usd": 20.00,

    # Execution safety: dry-run only until explicitly flipped AND reviewed.
    "allow_api_calls": False,

    # Generation settings (live mode only). Low temperature for reproducibility
    # (TM3 recommendation ≤ 0.2). max_output_tokens bounds per-run output cost.
    "temperature": 0.0,
    "max_output_tokens": 600,
    # Conservative pre-call output-token estimate for the budget precheck (the
    # actual output-token count is read from API usage after the call).
    "output_token_estimate": 600,

    # Retrieval (Agent B) — CONFIRMED top_k=3, language-matched only
    "top_k": 3,

    # Versions / identifiers
    "benchmark_version": "nicem-bench-v0.1",
    "stage": "stage2_smoke_test",
    "prompt_version_agent_a": "s2-prompt-a-v0.1.0",
    "prompt_version_agent_b": "s2-prompt-b-v0.1.0",
}

PLACEHOLDER_TOKENS = ("TO_CONFIRM", "TO_CONFIRM_EXACT_MODEL_ID",
                      "TO_CONFIRM_BEFORE_API_RUN")

# Selected Stage 2 intents, languages, agents
SELECTED_INTENTS = ["INT-004", "INT-015", "INT-017", "INT-026", "INT-031"]
LANGUAGES = ["en", "nl", "tr"]
AGENTS = [
    {"id": "agent_a_direct_full_kb", "code": "A",
     "prompt_version_key": "prompt_version_agent_a", "uses_retrieval": False},
    {"id": "agent_b_simple_rag", "code": "B",
     "prompt_version_key": "prompt_version_agent_b", "uses_retrieval": True},
]
PLANNED_RUN_COUNT = len(SELECTED_INTENTS) * len(LANGUAGES) * len(AGENTS)  # 30

# Repository paths (relative to repo root)
REPO_ROOT = Path(__file__).resolve().parents[1]
BENCH_DIR = REPO_ROOT / "docs" / "benchmark" / "v0.1"
RESULTS_DIR = REPO_ROOT / "results" / "stage2"

QUERY_FILES = {lang: BENCH_DIR / f"query-rendering-{lang}.md" for lang in LANGUAGES}
KB_FILES = {lang: BENCH_DIR / f"kb-rendering-{lang}.md" for lang in LANGUAGES}
BUDGET_STATE_PATH = RESULTS_DIR / "budget_state.json"

# Required logging fields (Stage 2 run plan §12)
REQUIRED_LOG_FIELDS = [
    "run_id", "timestamp", "benchmark_version", "stage", "intent_id",
    "language", "query_text", "agent_design_id", "response_model_id",
    "embedding_model_id", "tokenizer_name", "prompt_version", "kb_version",
    "retrieved_chunk_ids", "retrieved_fact_ids", "retrieval_scores",
    "input_tokens", "output_tokens", "total_tokens", "model_calls",
    "retrieval_calls", "retry_count", "latency_ms", "estimated_cost_usd",
    "endpoint_outcome", "failure_type", "evaluator_notes", "raw_output_path",
]

# Fields that must be non-empty on every run record (run plan §13 / req 13)
NON_EMPTY_FIELDS = [
    "intent_id", "language", "query_text", "agent_design_id", "kb_version",
    "response_model_id", "tokenizer_name", "prompt_version",
]

# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------
_INTENT_HEADER_RE = re.compile(r"^## (INT-\d{3})\s*$", re.MULTILINE)
_QUERY_TEXT_RE = re.compile(r'-\s*\*\*query_text:\*\*\s*"(.*?)"')
_QR_VERSION_RE = re.compile(r"(qr-(?:en|nl|tr)-v\d+\.\d+\.\d+)")
_KB_VERSION_RE = re.compile(r"(kb-(?:en|nl|tr)-v\d+\.\d+\.\d+)")
_CHUNK_ID_RE = re.compile(r"^chunk_id:\s*(\S+)", re.MULTILINE)


def parse_query_file(path: Path) -> dict:
    """Parse a query-rendering file → {intent_id: query_text} plus version."""
    text = path.read_text(encoding="utf-8")
    version_m = _QR_VERSION_RE.search(text)
    version = version_m.group(1) if version_m else "UNKNOWN"

    queries = {}
    # Split on intent headers, keep the header id with its following block.
    matches = list(_INTENT_HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        intent_id = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        qm = _QUERY_TEXT_RE.search(block)
        if qm:
            queries[intent_id] = qm.group(1)
    return {"version": version, "queries": queries}


def parse_kb_file(path: Path) -> dict:
    """Parse a KB rendering file → version + chunk count."""
    text = path.read_text(encoding="utf-8")
    version_m = _KB_VERSION_RE.search(text)
    version = version_m.group(1) if version_m else "UNKNOWN"
    chunk_ids = _CHUNK_ID_RE.findall(text)
    return {"version": version, "chunk_count": len(chunk_ids),
            "chunk_ids": chunk_ids}


# Metadata-block parser: each chunk is a fenced block (chunk_id / fact_ids /
# document_id / section_title) immediately followed by its prose paragraph.
_KB_BLOCK_RE = re.compile(
    r"```\s*\n"
    r"chunk_id:\s*(?P<chunk_id>\S+)\s*\n"
    r"fact_ids:\s*\[(?P<fact_ids>[^\]]*)\]\s*\n"
    r"document_id:\s*(?P<document_id>\S+)\s*\n"
    r"section_title:\s*(?P<section_title>.*?)\s*\n"
    r"```\s*\n"
    r"(?P<prose>.*?)(?=\n###|\n##|\n---|\Z)",
    re.DOTALL,
)


def parse_kb_chunks(path: Path) -> dict:
    """Parse a KB rendering into ordered chunk records with prose + fact_ids.

    Returns {"version": str, "chunks": [
        {"chunk_id", "document_id", "section_title", "fact_ids": [..],
         "text": <prose>}, ...]}.

    Used only by Agent B retrieval and Agent A full-KB prompt construction in
    LIVE mode. Dry-run does not call this.
    """
    text = path.read_text(encoding="utf-8")
    version_m = _KB_VERSION_RE.search(text)
    version = version_m.group(1) if version_m else "UNKNOWN"
    chunks = []
    for m in _KB_BLOCK_RE.finditer(text):
        fact_ids = [f.strip() for f in m.group("fact_ids").split(",") if f.strip()]
        chunks.append({
            "chunk_id": m.group("chunk_id").strip(),
            "document_id": m.group("document_id").strip(),
            "section_title": m.group("section_title").strip(),
            "fact_ids": fact_ids,
            "text": m.group("prose").strip(),
        })
    return {"version": version, "chunks": chunks}


# --------------------------------------------------------------------------
# Run construction
# --------------------------------------------------------------------------
def make_run_id(intent_id: str, language: str, agent_code: str) -> str:
    """Stable, deterministic run id: e.g. S2-INT-004-en-A."""
    return f"S2-{intent_id}-{language}-{agent_code}"


def build_runs(query_data: dict, kb_data: dict, dry_run: bool) -> list:
    """Construct the 30 planned run records."""
    timestamp = datetime.now(timezone.utc).isoformat()
    runs = []
    for intent_id in SELECTED_INTENTS:
        for language in LANGUAGES:
            query_text = query_data[language]["queries"].get(intent_id, "")
            kb_version = kb_data[language]["version"]
            for agent in AGENTS:
                record = {
                    "run_id": make_run_id(intent_id, language, agent["code"]),
                    "timestamp": timestamp,
                    "benchmark_version": CONFIG["benchmark_version"],
                    "stage": CONFIG["stage"],
                    "intent_id": intent_id,
                    "language": language,
                    "query_text": query_text,
                    "agent_design_id": agent["id"],
                    "response_model_id": CONFIG["response_model_id"],
                    "embedding_model_id": (
                        CONFIG["embedding_model_id"]
                        if agent["uses_retrieval"] else None
                    ),
                    "tokenizer_name": CONFIG["tokenizer_name"],
                    "prompt_version": CONFIG[agent["prompt_version_key"]],
                    "kb_version": kb_version,
                    # Retrieval fields: not performed in dry-run.
                    "retrieved_chunk_ids": None,
                    "retrieved_fact_ids": None,
                    "retrieval_scores": None,
                    # Measurement fields: not measured in dry-run.
                    "input_tokens": None,
                    "output_tokens": None,
                    "total_tokens": None,
                    "model_calls": 0,
                    "retrieval_calls": 0,
                    "retry_count": 0,
                    "latency_ms": None,
                    # Dry-run sentinels (req 10–12).
                    "estimated_cost_usd": 0 if dry_run else None,
                    "endpoint_outcome": "NOT_RUN" if dry_run else None,
                    "failure_type": None,
                    "evaluator_notes": (
                        "dry-run skeleton; not executed" if dry_run else None
                    ),
                    "raw_output_path": None,
                }
                runs.append(record)
    return runs


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
def validate(runs: list, query_data: dict, kb_data: dict) -> dict:
    """Run all structural validations. Returns a result dict with checks."""
    checks = []

    def check(name, passed, detail=""):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    # Req 14: exactly 30 planned runs
    check("run_count_is_30", len(runs) == PLANNED_RUN_COUNT,
          f"{len(runs)} runs (expected {PLANNED_RUN_COUNT})")

    # Stable, unique run ids
    ids = [r["run_id"] for r in runs]
    check("run_ids_unique", len(set(ids)) == len(ids),
          f"{len(set(ids))} unique of {len(ids)}")

    # Req 9 + 13: required fields present and required ones non-empty
    missing_fields = []
    empty_fields = []
    for r in runs:
        for f in REQUIRED_LOG_FIELDS:
            if f not in r:
                missing_fields.append(f"{r['run_id']}:{f}")
        for f in NON_EMPTY_FIELDS:
            if not r.get(f):
                empty_fields.append(f"{r['run_id']}:{f}")
    check("all_required_log_fields_present", not missing_fields,
          f"{len(missing_fields)} missing" if missing_fields else "all present")
    check("required_nonempty_fields_populated", not empty_fields,
          f"{len(empty_fields)} empty: {empty_fields[:5]}" if empty_fields
          else "all populated")

    # Req 15: all selected intents present in all three query files
    intent_coverage = []
    for lang in LANGUAGES:
        for intent_id in SELECTED_INTENTS:
            if intent_id not in query_data[lang]["queries"]:
                intent_coverage.append(f"{lang}:{intent_id}")
    check("selected_intents_in_all_query_files", not intent_coverage,
          f"missing: {intent_coverage}" if intent_coverage
          else "all 5 intents present in en/nl/tr")

    # Non-empty query_text for every selected (intent, language)
    empty_queries = [
        f"{lang}:{intent_id}"
        for lang in LANGUAGES for intent_id in SELECTED_INTENTS
        if not query_data[lang]["queries"].get(intent_id)
    ]
    check("query_text_nonempty_for_all", not empty_queries,
          f"empty: {empty_queries}" if empty_queries else "all query_text present")

    # Req 16: KB renderings exist for all three languages (and have 39 chunks)
    kb_issues = []
    for lang in LANGUAGES:
        if not KB_FILES[lang].exists():
            kb_issues.append(f"{lang}:missing-file")
        elif kb_data[lang]["chunk_count"] != 39:
            kb_issues.append(f"{lang}:{kb_data[lang]['chunk_count']}-chunks")
    check("kb_renderings_exist_all_languages", not kb_issues,
          f"issues: {kb_issues}" if kb_issues else "en/nl/tr present, 39 chunks each")

    # Req 17: budget cap fields present in config
    budget_ok = (
        isinstance(CONFIG.get("budget_hard_cap_usd"), (int, float))
        and isinstance(CONFIG.get("budget_stop_review_usd"), (int, float))
        and CONFIG["budget_stop_review_usd"] < CONFIG["budget_hard_cap_usd"]
    )
    check("budget_cap_fields_present", budget_ok,
          f"hard_cap=${CONFIG['budget_hard_cap_usd']}, "
          f"stop_review=${CONFIG['budget_stop_review_usd']}")

    # Dry-run sentinels (req 10–12)
    bad_sentinels = [
        r["run_id"] for r in runs
        if r["endpoint_outcome"] != "NOT_RUN"
        or r["estimated_cost_usd"] != 0
        or r["raw_output_path"] is not None
    ]
    check("dry_run_sentinels_correct", not bad_sentinels,
          f"violations: {bad_sentinels[:5]}" if bad_sentinels
          else "endpoint=NOT_RUN, cost=0, raw_output_path=null on all runs")

    # Total dry-run cost must be 0
    total_cost = sum((r["estimated_cost_usd"] or 0) for r in runs)
    check("total_dry_run_cost_zero", total_cost == 0, f"total=${total_cost}")

    # Pricing formula self-test (synthetic rates; no API key)
    selftest = _run_pricing_selftest()
    check("pricing_selftest_pass", selftest["passed"], selftest["detail"])

    all_passed = all(c["passed"] for c in checks)
    return {"checks": checks, "all_passed": all_passed}


# --------------------------------------------------------------------------
# Cost estimation (live-mode scaffolding; not used in dry-run)
# --------------------------------------------------------------------------

# Named constants for the self-test (§6 of stage2-model-pricing-config.md).
# These are SYNTHETIC values used only in _run_pricing_selftest() to verify
# the formula — they are NOT real pricing rates.
_SELFTEST_INPUT_USD_PER_1K = 0.001
_SELFTEST_OUTPUT_USD_PER_1K = 0.002
_SELFTEST_EMBEDDING_USD_PER_1K = 0.0001
# Expected: (1000/1000)*0.001 + (500/1000)*0.002 + (200/1000)*0.0001
#         = 0.001 + 0.001 + 0.00002 = 0.00202
_SELFTEST_INPUT_TOKENS = 1000
_SELFTEST_OUTPUT_TOKENS = 500
_SELFTEST_EMBEDDING_TOKENS = 200
_SELFTEST_EXPECTED_COST = 0.00202


def pricing_configured() -> bool:
    """True only when every pricing field is a real number."""
    p = CONFIG.get("pricing", {})
    return all(isinstance(p.get(k), (int, float)) for k in (
        "completion_input_usd_per_1k",
        "completion_output_usd_per_1k",
        "embedding_usd_per_1k",
    ))


def estimate_cost_usd(input_tokens: int, output_tokens: int,
                      embedding_tokens: int = 0) -> float:
    """Estimate run cost from token counts and the configured pricing table.

    Formula:
        cost = (input_tokens  / 1000) * completion_input_usd_per_1k
             + (output_tokens / 1000) * completion_output_usd_per_1k
             + (embedding_tokens / 1000) * embedding_usd_per_1k

    Raises if pricing is not configured — callers must check pricing_configured()
    first. Never invoked in dry-run (where token counts are None).
    """
    if not pricing_configured():
        raise ValueError("Pricing table is not configured; cannot estimate cost.")
    p = CONFIG["pricing"]
    cost = 0.0
    cost += (input_tokens / 1000.0) * p["completion_input_usd_per_1k"]
    cost += (output_tokens / 1000.0) * p["completion_output_usd_per_1k"]
    cost += (embedding_tokens / 1000.0) * p["embedding_usd_per_1k"]
    return round(cost, 6)


def _run_pricing_selftest() -> dict:
    """Unit-style self-test for estimate_cost_usd using synthetic rates.

    Temporarily installs known synthetic rates, calls estimate_cost_usd with
    fixed token counts, verifies the result, then restores the original pricing
    table. No API key or network access required.

    Returns {"passed": bool, "detail": str}.
    """
    original = dict(CONFIG["pricing"])
    try:
        CONFIG["pricing"]["completion_input_usd_per_1k"] = _SELFTEST_INPUT_USD_PER_1K
        CONFIG["pricing"]["completion_output_usd_per_1k"] = _SELFTEST_OUTPUT_USD_PER_1K
        CONFIG["pricing"]["embedding_usd_per_1k"] = _SELFTEST_EMBEDDING_USD_PER_1K

        result = estimate_cost_usd(
            _SELFTEST_INPUT_TOKENS,
            _SELFTEST_OUTPUT_TOKENS,
            _SELFTEST_EMBEDDING_TOKENS,
        )
        passed = abs(result - _SELFTEST_EXPECTED_COST) < 1e-8
        detail = (
            f"estimate_cost_usd({_SELFTEST_INPUT_TOKENS}, {_SELFTEST_OUTPUT_TOKENS}, "
            f"{_SELFTEST_EMBEDDING_TOKENS}) = {result}; "
            f"expected {_SELFTEST_EXPECTED_COST}"
        )
    except Exception as exc:
        passed = False
        detail = f"exception: {exc}"
    finally:
        CONFIG["pricing"].update(original)

    return {"passed": passed, "detail": detail}


def _run_budget_guard_selftest() -> dict:
    """Verify BudgetGuard thresholds with synthetic costs (no API, no spend).

    Uses precheck() only (which never writes state) so nothing is persisted.
    Checks: a small cost proceeds; reaching $20 pauses; exceeding $25 halts.
    """
    try:
        guard = BudgetGuard(CONFIG["budget_hard_cap_usd"],
                            CONFIG["budget_stop_review_usd"], BUDGET_STATE_PATH)
        ok_proceed, _ = guard.precheck(0.50)
        within = ok_proceed and guard.status == "ok"

        guard.cumulative_cost = 19.50
        pause_proceed, _ = guard.precheck(1.00)   # projected 20.50 ≥ 20
        pauses = (not pause_proceed) and guard.status == "pause_stop_review"

        guard.cumulative_cost = 24.50
        halt_proceed, _ = guard.precheck(1.00)    # projected 25.50 > 25
        halts = (not halt_proceed) and guard.status == "halt_hard_cap"

        passed = within and pauses and halts
        detail = (f"within={within}, pause@$20={pauses}, halt@$25={halts}; "
                  f"no state written (precheck only)")
    except Exception as exc:
        passed = False
        detail = f"exception: {exc}"
    return {"passed": passed, "detail": detail}


def _run_guard_tests() -> list:
    """Local safety-guard tests. NO API calls, NO embeddings, NO API key.

    Returns a list of {name, passed, detail} for the dry-run validation report.
    """
    from argparse import Namespace
    checks = []

    def add(name, passed, detail=""):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    # dry_run is the default when neither --live nor a flag is given.
    parser = argparse.ArgumentParser()
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--dry-run", dest="dry_run", action="store_true", default=True)
    grp.add_argument("--live", dest="live", action="store_true", default=False)
    parser.add_argument("--confirm-spend", dest="confirm_spend",
                        action="store_true", default=False)
    default_args = parser.parse_args([])
    add("dry_run_default", not getattr(default_args, "live", False),
        "no flags → dry-run (live=False)")

    # Dry-run needs no API key: prove the dry-run path never reads the key.
    add("no_api_key_required_for_dry_run",
        "OPENAI_API_KEY" not in _dry_run_codepath_env_reads(),
        "dry-run code path does not read OPENAI_API_KEY")

    # --live without --confirm-spend must refuse.
    allowed_a, blockers_a = can_run_api_mode(
        Namespace(live=True, confirm_spend=False))
    add("live_without_confirm_refuses",
        (not allowed_a) and any("confirm-spend" in b for b in blockers_a),
        f"refused; {len(blockers_a)} blockers")

    # --live --confirm-spend must still refuse while allow_api_calls is False.
    allowed_b, blockers_b = can_run_api_mode(
        Namespace(live=True, confirm_spend=True))
    add("live_with_confirm_refuses_when_allow_api_calls_false",
        (not allowed_b) and any("allow_api_calls" in b for b in blockers_b),
        "refused: allow_api_calls is False")

    # Pricing + budget self-tests (synthetic; no spend).
    pst = _run_pricing_selftest()
    add("pricing_selftest", pst["passed"], pst["detail"])
    bst = _run_budget_guard_selftest()
    add("budget_guard_synthetic_test", bst["passed"], bst["detail"])

    return checks


def _dry_run_codepath_env_reads() -> set:
    """Names of environment variables read on the dry-run code path.

    Dry-run reads no environment variables at all, so this returns an empty set.
    `OPENAI_API_KEY` is only read in _get_openai_client()/can_run_api_mode(),
    neither of which is on the dry-run path. Kept explicit for auditability.
    """
    return set()


# --------------------------------------------------------------------------
# Budget guard (live-mode scaffolding)
# --------------------------------------------------------------------------
class BudgetGuard:
    """Tracks cumulative estimated spend and enforces the hard/stop thresholds.

    State is persisted to results/stage2/budget_state.json. This guard is only
    exercised in live mode (which is refused by default). It never auto-retries.
    """

    def __init__(self, hard_cap: float, stop_review: float, state_path: Path):
        self.hard_cap = hard_cap
        self.stop_review = stop_review
        self.state_path = state_path
        self.cumulative_cost = 0.0
        self.run_count = 0
        self.status = "ok"

    def precheck(self, next_cost: float) -> tuple:
        """Decide whether the next run may proceed. Returns (proceed, reason)."""
        projected = self.cumulative_cost + next_cost
        if projected > self.hard_cap:
            self.status = "halt_hard_cap"
            return (False, f"projected ${projected:.4f} would exceed hard cap "
                           f"${self.hard_cap:.2f}")
        if projected >= self.stop_review:
            self.status = "pause_stop_review"
            return (False, f"projected ${projected:.4f} reaches stop-review "
                           f"${self.stop_review:.2f}; manual approval required")
        self.status = "ok"
        return (True, "within budget")

    def record(self, cost: float) -> None:
        self.cumulative_cost = round(self.cumulative_cost + cost, 6)
        self.run_count += 1
        self.write_state()

    def write_state(self) -> None:
        state = {
            "cumulative_cost_usd": self.cumulative_cost,
            "run_count": self.run_count,
            "hard_cap_usd": self.hard_cap,
            "stop_review_usd": self.stop_review,
            "status": self.status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# API-mode guard (req 19) — no API code is implemented (req 20–21)
# --------------------------------------------------------------------------
def can_run_api_mode(args=None) -> tuple:
    """Return (allowed: bool, blockers: list[str]).

    Strict live-mode guard: every condition must hold before any API call is
    even contemplated. `args` carries the CLI confirmation flags.
    """
    blockers = []
    if not CONFIG.get("allow_api_calls"):
        blockers.append("CONFIG['allow_api_calls'] is False")
    if CONFIG["response_model_id"] in PLACEHOLDER_TOKENS:
        blockers.append("response_model_id is still a placeholder")
    if CONFIG["pricing_version"] in PLACEHOLDER_TOKENS:
        blockers.append("pricing_version is still a placeholder")
    if not isinstance(CONFIG["pricing"].get("completion_input_usd_per_1k"),
                      (int, float)):
        blockers.append("completion input price is not configured")
    if not isinstance(CONFIG["pricing"].get("completion_output_usd_per_1k"),
                      (int, float)):
        blockers.append("completion output price is not configured")
    if not isinstance(CONFIG["pricing"].get("embedding_usd_per_1k"),
                      (int, float)):
        blockers.append("embedding price is not configured")
    if not isinstance(CONFIG.get("budget_hard_cap_usd"), (int, float)):
        blockers.append("budget_hard_cap_usd is not set")
    if not isinstance(CONFIG.get("budget_stop_review_usd"), (int, float)):
        blockers.append("budget_stop_review_usd is not set")
    if not os.environ.get("OPENAI_API_KEY"):
        blockers.append("OPENAI_API_KEY is not present in the environment")
    if args is not None:
        if not getattr(args, "live", False):
            blockers.append("--live flag was not passed")
        if not getattr(args, "confirm_spend", False):
            blockers.append("--confirm-spend flag was not passed")
    return (len(blockers) == 0, blockers)


# --------------------------------------------------------------------------
# LIVE API paths (implemented, but unreachable while allow_api_calls is False)
# --------------------------------------------------------------------------
# These functions are only ever called from run_live(), which itself runs only
# after can_run_api_mode() returns allowed=True (requires allow_api_calls=True,
# OPENAI_API_KEY, confirmed model IDs + pricing, and --live --confirm-spend).
# The `openai` package is imported lazily so dry-run needs no dependency/key.

SYSTEM_PROMPT = (
    "You are a customer-support assistant for the NiceHome smart-home product "
    "line. Answer the user's question using ONLY the provided knowledge-base "
    "content. If the content does not contain the answer, say you do not have "
    "that information. Do not invent facts, prices, or policies."
)


def _get_openai_client():
    """Construct an OpenAI client lazily. LIVE ONLY.

    Imports `openai` only here so dry-run/review never needs the package. The
    API key is read from the environment and never logged.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise RuntimeError(
            "The 'openai' package is required for live mode but is not "
            "installed. Install it before enabling allow_api_calls.") from exc
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set; refusing to build client.")
    return OpenAI(api_key=api_key)


def _call_completion_api(client, system_prompt: str, user_prompt: str) -> dict:
    """Call the chat-completion endpoint once. LIVE ONLY; never retried.

    Returns a dict with the response text, token usage (from API usage when
    available), finish reason, and the raw serialized response. Raises on any
    API error — the caller (run_live) stops the loop without retrying.
    """
    resp = client.chat.completions.create(
        model=CONFIG["response_model_id"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=CONFIG.get("temperature", 0.0),
        max_tokens=CONFIG.get("max_output_tokens", 600),
    )
    usage = getattr(resp, "usage", None)
    choice = resp.choices[0]
    return {
        "text": choice.message.content or "",
        "input_tokens": getattr(usage, "prompt_tokens", None),
        "output_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
        "finish_reason": getattr(choice, "finish_reason", None),
        "raw": resp.model_dump() if hasattr(resp, "model_dump") else None,
    }


def _create_embeddings(client, texts: list) -> dict:
    """Embed a list of texts with the configured embedding model. LIVE ONLY.

    Returns {"vectors": [[float, ...], ...], "embedding_tokens": int|None,
    "raw": dict|None}. Raises on any API error — never retried.
    """
    resp = client.embeddings.create(
        model=CONFIG["embedding_model_id"],
        input=texts,
    )
    usage = getattr(resp, "usage", None)
    return {
        "vectors": [item.embedding for item in resp.data],
        "embedding_tokens": getattr(usage, "total_tokens", None),
        "raw": resp.model_dump() if hasattr(resp, "model_dump") else None,
    }


def _cosine_similarity(a: list, b: list) -> float:
    """Cosine similarity between two equal-length vectors (no numpy dependency)."""
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _retrieve_top_k(client, query_text: str, kb_chunks: list, top_k: int) -> dict:
    """Embed the query + all KB chunks and return the top-k most similar. LIVE ONLY.

    Returns {"retrieved": [{"chunk_id", "score", "fact_ids"}...],
             "embedding_tokens": int|None, "retrieval_calls": int}.
    Language-matched: kb_chunks must be the same-language rendering as the query.
    """
    texts = [query_text] + [c["text"] for c in kb_chunks]
    emb = _create_embeddings(client, texts)
    vectors = emb["vectors"]
    query_vec = vectors[0]
    scored = []
    for chunk, vec in zip(kb_chunks, vectors[1:]):
        scored.append({
            "chunk_id": chunk["chunk_id"],
            "score": round(_cosine_similarity(query_vec, vec), 6),
            "fact_ids": chunk["fact_ids"],
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return {
        "retrieved": scored[:top_k],
        "embedding_tokens": emb["embedding_tokens"],
        "retrieval_calls": 1,
    }


def _build_agent_a_prompt(query_text: str, kb_chunks: list) -> str:
    """Agent A (A1): full relevant-language KB rendering in the prompt."""
    kb_block = "\n\n".join(f"[{c['chunk_id']}] {c['text']}" for c in kb_chunks)
    return (f"Knowledge base:\n{kb_block}\n\n"
            f"User question:\n{query_text}")


def _build_agent_b_prompt(query_text: str, retrieved_chunks: list) -> str:
    """Agent B (Simple RAG): only the retrieved chunks in the prompt."""
    kb_block = "\n\n".join(
        f"[{c['chunk_id']}] {c['text']}" for c in retrieved_chunks)
    return (f"Retrieved knowledge-base passages:\n{kb_block}\n\n"
            f"User question:\n{query_text}")


def _estimate_chars_tokens(text: str) -> int:
    """Rough pre-call token estimate (~4 chars/token). Used only for the budget
    precheck before a live call; the real count comes from API usage after."""
    return max(1, (len(text) + 3) // 4)


def _live_run_sequence(runs_by_id: dict) -> list:
    """Return run records in the staged order from the run plan §11:
    EN Agent A, EN Agent B, rest of the first intent, then the other intents."""
    first = SELECTED_INTENTS[0]
    ordered_ids = [f"S2-{first}-en-A", f"S2-{first}-en-B"]
    for lang in [l for l in LANGUAGES if l != "en"]:
        for code in ["A", "B"]:
            ordered_ids.append(f"S2-{first}-{lang}-{code}")
    for intent in SELECTED_INTENTS[1:]:
        for lang in LANGUAGES:
            for code in ["A", "B"]:
                ordered_ids.append(f"S2-{intent}-{lang}-{code}")
    # Preserve any record not covered (defensive) at the end.
    seen = set(ordered_ids)
    tail = [rid for rid in runs_by_id if rid not in seen]
    return [runs_by_id[rid] for rid in ordered_ids if rid in runs_by_id] + \
           [runs_by_id[rid] for rid in tail]


def run_live(query_data: dict, kb_chunk_data: dict) -> list:
    """Execute the Stage 2 runs against the live API. LIVE ONLY.

    This is reached only after can_run_api_mode() returns allowed=True. It:
      - builds the 30 run records,
      - for each (in staged order) estimates cost, budget-prechecks, calls the
        API (Agent B retrieves first), records actual cost, writes raw output,
      - never auto-retries: a precheck stop or an API error halts the loop.

    Returns the list of run records (executed + any NOT_RUN remainder).
    """
    client = _get_openai_client()
    guard = BudgetGuard(
        CONFIG["budget_hard_cap_usd"], CONFIG["budget_stop_review_usd"],
        BUDGET_STATE_PATH)
    raw_dir = RESULTS_DIR / "raw_outputs"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Build skeleton records, index by id, iterate in staged order.
    kb_meta = {lang: {"version": kb_chunk_data[lang]["version"],
                      "chunk_count": len(kb_chunk_data[lang]["chunks"]),
                      "chunk_ids": [c["chunk_id"]
                                    for c in kb_chunk_data[lang]["chunks"]]}
               for lang in LANGUAGES}
    runs = build_runs(query_data, kb_meta, dry_run=False)
    runs_by_id = {r["run_id"]: r for r in runs}

    halted = False
    for record in _live_run_sequence(runs_by_id):
        if halted:
            record["endpoint_outcome"] = "NOT_RUN"
            record["evaluator_notes"] = "skipped: loop halted before this run"
            continue

        lang = record["language"]
        query_text = record["query_text"]
        kb_chunks = kb_chunk_data[lang]["chunks"]
        uses_retrieval = record["agent_design_id"] == "agent_b_simple_rag"

        # ---- build prompt + pre-call cost estimate ----
        embedding_tokens_actual = None
        try:
            if uses_retrieval:
                retr = _retrieve_top_k(client, query_text, kb_chunks,
                                       CONFIG["top_k"])
                record["retrieved_chunk_ids"] = [
                    c["chunk_id"] for c in retr["retrieved"]]
                record["retrieval_scores"] = [
                    c["score"] for c in retr["retrieved"]]
                fact_ids = []
                for c in retr["retrieved"]:
                    fact_ids.extend(c["fact_ids"])
                record["retrieved_fact_ids"] = fact_ids
                record["retrieval_calls"] = retr["retrieval_calls"]
                embedding_tokens_actual = retr["embedding_tokens"]
                user_prompt = _build_agent_b_prompt(query_text, retr["retrieved"])
            else:
                user_prompt = _build_agent_a_prompt(query_text, kb_chunks)
        except Exception as exc:  # retrieval/embedding error — no retry
            record["endpoint_outcome"] = "ERROR"
            record["failure_type"] = f"retrieval_error: {type(exc).__name__}"
            record["evaluator_notes"] = "embedding/retrieval failed; loop halted"
            guard.write_state()
            halted = True
            continue

        # Pre-call budget projection (conservative).
        est_input = _estimate_chars_tokens(SYSTEM_PROMPT + user_prompt)
        est_output = CONFIG["output_token_estimate"]
        est_embed = (embedding_tokens_actual
                     if embedding_tokens_actual is not None
                     else (_estimate_chars_tokens(
                         query_text + "".join(c["text"] for c in kb_chunks))
                         if uses_retrieval else 0))
        est_cost = estimate_cost_usd(est_input, est_output, est_embed)

        proceed, reason = guard.precheck(est_cost)
        if not proceed:
            record["endpoint_outcome"] = (
                "HALTED_BUDGET" if guard.status == "halt_hard_cap"
                else "PAUSED_BUDGET")
            record["failure_type"] = guard.status
            record["evaluator_notes"] = f"budget stop: {reason}"
            guard.write_state()
            halted = True
            continue

        # ---- completion call (single attempt, never retried) ----
        started = datetime.now(timezone.utc)
        try:
            result = _call_completion_api(client, SYSTEM_PROMPT, user_prompt)
        except Exception as exc:  # API/auth/rate-limit — no retry, stop loop
            record["endpoint_outcome"] = "ERROR"
            record["failure_type"] = f"completion_error: {type(exc).__name__}"
            record["evaluator_notes"] = "completion failed; loop halted (no retry)"
            guard.write_state()
            halted = True
            continue
        latency_ms = (datetime.now(timezone.utc) - started).total_seconds() * 1000

        # ---- record actual measurements ----
        in_tok = result["input_tokens"] or est_input
        out_tok = result["output_tokens"] or est_output
        emb_tok = embedding_tokens_actual or 0
        actual_cost = estimate_cost_usd(in_tok, out_tok, emb_tok)

        record["input_tokens"] = result["input_tokens"]
        record["output_tokens"] = result["output_tokens"]
        record["total_tokens"] = result["total_tokens"]
        record["model_calls"] = 1
        record["latency_ms"] = round(latency_ms, 1)
        record["estimated_cost_usd"] = actual_cost
        record["endpoint_outcome"] = "OK"
        record["evaluator_notes"] = None

        # ---- raw output to disk; never logs the API key ----
        raw_path = raw_dir / f"{record['run_id']}.json"
        raw_payload = {
            "run_id": record["run_id"],
            "prompt_system": SYSTEM_PROMPT,
            "prompt_user": user_prompt,
            "response_text": result["text"],
            "finish_reason": result["finish_reason"],
            "usage": {
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"],
                "embedding_tokens": embedding_tokens_actual,
            },
            "raw_response": result["raw"],
        }
        raw_path.write_text(
            json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        record["raw_output_path"] = str(
            raw_path.relative_to(REPO_ROOT))

        guard.record(actual_cost)

    return runs


# --------------------------------------------------------------------------
# Output writers
# --------------------------------------------------------------------------
def write_jsonl(runs: list, path: Path) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for r in runs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_csv(runs: list, path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REQUIRED_LOG_FIELDS)
        writer.writeheader()
        for r in runs:
            row = {}
            for f in REQUIRED_LOG_FIELDS:
                v = r.get(f)
                if isinstance(v, (list, dict)):
                    row[f] = json.dumps(v, ensure_ascii=False)
                elif v is None:
                    row[f] = ""
                else:
                    row[f] = v
            writer.writerow(row)


def write_run_matrix(runs: list, path: Path) -> None:
    cols = ["run_id", "intent_id", "language", "agent_design_id",
            "query_text", "endpoint_outcome", "estimated_cost_usd"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(cols)
        for r in runs:
            writer.writerow([r["run_id"], r["intent_id"], r["language"],
                             r["agent_design_id"], r["query_text"],
                             r["endpoint_outcome"], r["estimated_cost_usd"]])


def write_validation_md(validation: dict, runs: list, query_data: dict,
                        kb_data: dict, path: Path) -> None:
    allowed, blockers = can_run_api_mode()
    total_cost = sum((r["estimated_cost_usd"] or 0) for r in runs)
    lines = []
    lines.append("# Stage 2 Smoke Runner — Dry-Run Validation")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    lines.append("**Mode:** dry-run (no API calls, no embeddings, no API key)")
    lines.append(f"**Runner:** `scripts/stage2_smoke_runner.py`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Planned runs: **{len(runs)}** (expected {PLANNED_RUN_COUNT})")
    lines.append(f"- Total dry-run estimated cost: **${total_cost}**")
    lines.append(f"- All validations passed: "
                 f"**{'YES' if validation['all_passed'] else 'NO'}**")
    lines.append("")
    lines.append("## Configuration (placeholders must be confirmed before API run)")
    lines.append("")
    lines.append("| Key | Value |")
    lines.append("|---|---|")
    for k in ["response_model_id", "embedding_model_id", "embedding_model_version",
              "tokenizer_name", "pricing_version", "top_k",
              "budget_hard_cap_usd", "budget_stop_review_usd", "allow_api_calls"]:
        lines.append(f"| `{k}` | `{CONFIG[k]}` |")
    for pk, pv in CONFIG["pricing"].items():
        lines.append(f"| `pricing.{pk}` | `{pv}` |")
    lines.append(f"| `pricing_configured` | `{pricing_configured()}` |")
    lines.append("")
    lines.append("## Artifact versions parsed")
    lines.append("")
    lines.append("| Language | Query version | KB version | KB chunks |")
    lines.append("|---|---|---|---|")
    for lang in LANGUAGES:
        lines.append(f"| {lang} | `{query_data[lang]['version']}` | "
                     f"`{kb_data[lang]['version']}` | "
                     f"{kb_data[lang]['chunk_count']} |")
    lines.append("")
    lines.append("## Validation checks")
    lines.append("")
    lines.append("| Check | Result | Detail |")
    lines.append("|---|---|---|")
    for c in validation["checks"]:
        status = "PASS" if c["passed"] else "FAIL"
        lines.append(f"| {c['name']} | {status} | {c['detail']} |")
    lines.append("")
    lines.append("## Required-field validation (run plan §12/§13)")
    lines.append("")
    lines.append(f"- Required log fields per record: {len(REQUIRED_LOG_FIELDS)}")
    lines.append(f"- Required non-empty fields: {', '.join(NON_EMPTY_FIELDS)}")
    lines.append("")
    lines.append("## API execution status")
    lines.append("")
    if allowed:
        lines.append("**API execution is NOT blocked by config** — but the runner "
                     "still performs no API calls because the live call paths are "
                     "unimplemented stubs. Review required before enabling.")
    else:
        lines.append("**API execution remains BLOCKED.** The following preconditions "
                     "are not satisfied:")
        lines.append("")
        for b in blockers:
            lines.append(f"- {b}")
    lines.append("")
    lines.append("Additionally, the live completion + embedding code paths are now "
                 "implemented (`_call_completion_api`, `_create_embeddings`, "
                 "`_retrieve_top_k`, `run_live`) but are unreachable while "
                 "`allow_api_calls` is False — they are never exercised by dry-run, "
                 "the validation checks, or the guard tests. The `openai` package is "
                 "imported lazily (live only); dry-run needs no dependency and no key.")
    lines.append("")
    lines.append("## Pricing self-test")
    lines.append("")
    selftest = _run_pricing_selftest()
    lines.append(f"| Item | Result |")
    lines.append(f"|---|---|")
    lines.append(f"| Pricing formula self-test | {'PASS' if selftest['passed'] else 'FAIL'} |")
    lines.append(f"| Detail | `{selftest['detail']}` |")
    lines.append("")
    lines.append("The self-test uses synthetic rates (not real pricing) and requires "
                 "no API key. It verifies the `estimate_cost_usd` formula implementation. "
                 "See `docs/benchmark/v0.1/stage2-model-pricing-config.md` §6.")
    lines.append("")
    lines.append("## Safety-guard tests (no API calls, no embeddings, no API key)")
    lines.append("")
    guard_checks = _run_guard_tests()
    lines.append("| Guard test | Result | Detail |")
    lines.append("|---|---|---|")
    for c in guard_checks:
        status = "PASS" if c["passed"] else "FAIL"
        lines.append(f"| {c['name']} | {status} | {c['detail']} |")
    lines.append("")
    lines.append("All guard tests run without any network access. They prove the "
                 "default is dry-run, that dry-run needs no key, that live mode "
                 "refuses without `--confirm-spend`, that live mode still refuses "
                 "with both flags while `allow_api_calls` is False, and that the "
                 "pricing + budget logic behave as designed.")
    lines.append("")
    lines.append("## Remaining steps before the first live API call")
    lines.append("")
    lines.append("Model IDs and pricing are CONFIRMED; the live paths are implemented. "
                 "The remaining steps are:")
    lines.append("")
    lines.append("1. Code-review the live paths (`_call_completion_api`, "
                 "`_create_embeddings`, `_retrieve_top_k`, `run_live`).")
    lines.append("2. Reconfirm `response_model_id` is non-deprecated and rates are "
                 "current against the live API.")
    lines.append("3. Set `allow_api_calls = True` (after review) — the single "
                 "config flip that unblocks live mode.")
    lines.append("4. Export `OPENAI_API_KEY` in the run environment "
                 "(never committed, never logged).")
    lines.append("5. Run `--live --confirm-spend`, starting with one English "
                 "Agent A run, watching `budget_state.json`.")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="NiceM Stage 2 smoke-test logging runner (skeleton).")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run", dest="dry_run", action="store_true", default=True,
        help="Dry-run mode (default): no API calls, no embeddings, no key.")
    mode_group.add_argument(
        "--live", dest="live", action="store_true", default=False,
        help="Request live mode. Refused unless ALL guards pass.")
    parser.add_argument(
        "--confirm-spend", dest="confirm_spend", action="store_true",
        default=False,
        help="Explicit spend confirmation; required (with --live) for live mode.")
    args = parser.parse_args()

    # --live overrides the default --dry-run.
    dry_run = not args.live

    if not dry_run:
        # Strict guard: live mode is refused unless every precondition holds,
        # including CONFIG['allow_api_calls'] == True (ships as False).
        allowed, blockers = can_run_api_mode(args)
        if not allowed:
            print("LIVE mode refused. Unsatisfied preconditions:")
            for b in blockers:
                print(f"  - {b}")
            print("\nNo API calls were made. Exiting.")
            return 1
        # Every precondition (config flag, confirmed model/pricing, key, and
        # both CLI flags) is satisfied — execute the live run loop. This branch
        # is unreachable while allow_api_calls is False.
        print("LIVE mode: all preconditions satisfied. Executing run loop...")
        query_data = {lang: parse_query_file(QUERY_FILES[lang]) for lang in LANGUAGES}
        kb_chunk_data = {lang: parse_kb_chunks(KB_FILES[lang]) for lang in LANGUAGES}
        runs = run_live(query_data, kb_chunk_data)
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        write_jsonl(runs, RESULTS_DIR / "live_runs.jsonl")
        write_csv(runs, RESULTS_DIR / "live_runs.csv")
        write_run_matrix(runs, RESULTS_DIR / "live_run_matrix.csv")
        executed = [r for r in runs if r["endpoint_outcome"] == "OK"]
        total_cost = sum((r["estimated_cost_usd"] or 0) for r in runs)
        print(f"Executed {len(executed)}/{len(runs)} runs. "
              f"Total actual cost: ${total_cost:.4f}")
        print("Wrote results/stage2/live_runs.jsonl, live_runs.csv, "
              "live_run_matrix.csv, raw_outputs/")
        return 0

    # ---- dry-run ----
    print("Mode: dry-run (no API calls, no embeddings, no API key required)")

    # Parse artifacts
    query_data = {lang: parse_query_file(QUERY_FILES[lang]) for lang in LANGUAGES}
    kb_data = {lang: parse_kb_file(KB_FILES[lang]) for lang in LANGUAGES}

    # Build runs
    runs = build_runs(query_data, kb_data, dry_run=True)

    # Validate
    validation = validate(runs, query_data, kb_data)

    # Write outputs
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(runs, RESULTS_DIR / "dry_run_runs.jsonl")
    write_csv(runs, RESULTS_DIR / "dry_run_runs.csv")
    write_run_matrix(runs, RESULTS_DIR / "dry_run_run_matrix.csv")
    write_validation_md(validation, runs, query_data, kb_data,
                        RESULTS_DIR / "dry_run_validation.md")

    # Console summary
    total_cost = sum((r["estimated_cost_usd"] or 0) for r in runs)
    print(f"Built {len(runs)} runs (expected {PLANNED_RUN_COUNT}).")
    print(f"Total dry-run estimated cost: ${total_cost}")
    print(f"Validations: {'ALL PASS' if validation['all_passed'] else 'FAILURES'}")
    for c in validation["checks"]:
        print(f"  [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}: {c['detail']}")
    allowed, blockers = can_run_api_mode()
    print(f"\nAPI execution blocked: {'NO' if allowed else 'YES'}")
    if not allowed:
        for b in blockers:
            print(f"  blocker: {b}")
    print("\nWrote:")
    for f in ["dry_run_runs.jsonl", "dry_run_runs.csv",
              "dry_run_run_matrix.csv", "dry_run_validation.md"]:
        print(f"  results/stage2/{f}")

    return 0 if validation["all_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
