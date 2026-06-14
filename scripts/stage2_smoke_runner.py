#!/usr/bin/env python3
"""
NiceM Stage 2 smoke-test logging runner (minimal skeleton).

This runner builds the 30 planned Stage 2 runs from the benchmark artifacts,
validates the logging fields, enforces the budget rules structurally, and
writes dry-run outputs WITHOUT calling any external API or creating any
embeddings.

Design constraints (see docs/benchmark/v0.1/stage2-smoke-test-run-plan.md):
  - Default mode is dry-run.
  - Dry-run makes NO API calls, creates NO embeddings, and does NOT require
    an API key.
  - API mode is refused unless every precondition is explicitly satisfied
    (see can_run_api_mode). No real API or embedding code is implemented;
    the network functions are unreachable stubs that raise.

Stage 2 remains BLOCKED until the runner is reviewed and the placeholders in
CONFIG (response_model_id, pricing_version) are confirmed.
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

CONFIG = {
    # Model / tokenizer / pricing
    "response_model_id": "TO_CONFIRM_EXACT_MODEL_ID",   # placeholder (TM1-b/c)
    "embedding_model_id": "text-embedding-3-small",      # CONFIRMED (TM8)
    "embedding_model_version": "TO_CONFIRM",             # placeholder
    "tokenizer_name": "o200k_base",                      # encoding family
    "pricing_version": "TO_CONFIRM_BEFORE_API_RUN",      # placeholder

    # Pricing table (USD per 1,000 tokens) — placeholders (None) until the
    # pricing_version is confirmed. Live mode is refused while any is None.
    "pricing": {
        "completion_input_usd_per_1k": None,   # TO_CONFIRM
        "completion_output_usd_per_1k": None,  # TO_CONFIRM
        "embedding_usd_per_1k": None,          # TO_CONFIRM
    },

    # Budget (CONFIRMED, TM5/BS6)
    "budget_hard_cap_usd": 25.00,
    "budget_stop_review_usd": 20.00,

    # Execution safety: dry-run only until explicitly flipped AND reviewed.
    "allow_api_calls": False,

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

    all_passed = all(c["passed"] for c in checks)
    return {"checks": checks, "all_passed": all_passed}


# --------------------------------------------------------------------------
# Cost estimation (live-mode scaffolding; not used in dry-run)
# --------------------------------------------------------------------------
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


def _call_completion_api(*_args, **_kwargs):  # pragma: no cover - stub
    """Unreachable stub. Real completion calls are NOT implemented yet."""
    raise NotImplementedError(
        "Completion API calls are not implemented in this skeleton. "
        "Stage 2 live execution is intentionally blocked.")


def _create_embeddings(*_args, **_kwargs):  # pragma: no cover - stub
    """Unreachable stub. Real embedding calls are NOT implemented yet."""
    raise NotImplementedError(
        "Embedding creation is not implemented in this skeleton. "
        "Stage 2 live execution is intentionally blocked.")


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
    lines.append("Additionally, no real completion or embedding code is implemented: "
                 "`_call_completion_api` and `_create_embeddings` are unreachable "
                 "stubs that raise `NotImplementedError`. Stage 2 live execution "
                 "cannot occur from this skeleton.")
    lines.append("")
    lines.append("## Remaining blockers before the first live API call")
    lines.append("")
    lines.append("1. Confirm `response_model_id` (TM1-b/c) — replace placeholder.")
    lines.append("2. Confirm `pricing_version` — replace placeholder.")
    lines.append("3. Implement and review the live completion + embedding paths "
                 "(currently stubs).")
    lines.append("4. Implement programmatic budget-cap enforcement (or document "
                 "manual enforcement).")
    lines.append("5. Set `allow_api_calls = True` only after review.")
    lines.append("6. Provide `OPENAI_API_KEY` in the environment at run time.")
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
        # Strict guard: live mode is refused unless every precondition holds.
        allowed, blockers = can_run_api_mode(args)
        if not allowed:
            print("LIVE mode refused. Unsatisfied preconditions:")
            for b in blockers:
                print(f"  - {b}")
            print("\nNo API calls were made. Exiting.")
            return 1
        # Even if every config + CLI precondition passes, the live paths are
        # unreachable stubs — no API call can occur from this skeleton.
        print("LIVE preconditions satisfied, but live call paths are not "
              "implemented in this skeleton (intentional). No API calls made.")
        return 1

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
