"""Export toy-conjecture counterexample witnesses as machine-checkable JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from toy_conjectures import CONJECTURES, Counterexample


DEFAULT_PROFILES: dict[str, dict[str, Any]] = {
    "short_cycle": {"low": -10, "high": 10, "steps": 25, "bound": 1e6, "max_cycle_length": 4},
    "nonnegative": {"low": 0, "high": 10, "steps": 10},
    "bounded_growth": {"low": -10, "high": 10, "steps": 10, "bound": 100},
    "fast_cycle": {"low": -10, "high": 10, "steps": 10},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export counterexample witnesses to JSON.")
    parser.add_argument(
        "--output",
        default="artifacts/witnesses.json",
        help="Output JSON path (default: artifacts/witnesses.json).",
    )
    return parser.parse_args()


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def serialize_counterexample(counterexample: Counterexample) -> dict[str, Any]:
    record = asdict(counterexample)
    # Preserve exact integer magnitude and avoid float representation surprises.
    record["value"] = str(counterexample.value)
    record["orbit"] = [str(value) for value in counterexample.orbit]
    record["value_digits"] = len(str(abs(int(counterexample.value)))) if isinstance(counterexample.value, int) else None
    return record


def collect_witnesses() -> dict[str, Any]:
    results: dict[str, Any] = {}

    for key, (statement, search_fn) in CONJECTURES.items():
        params = dict(DEFAULT_PROFILES[key])
        counterexample = search_fn(**params)
        entry: dict[str, Any] = {
            "statement": statement,
            "parameters": params,
            "status": "counterexample_found" if counterexample is not None else "none_found",
            "counterexample": serialize_counterexample(counterexample) if counterexample is not None else None,
        }
        results[key] = entry

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(),
        "map": "f(x) = -2x^2 + 3x + 1",
        "results": results,
    }


def main() -> None:
    args = parse_args()
    payload = collect_witnesses()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote witness artifact: {output_path}")


if __name__ == "__main__":
    main()