"""Search quadratic toy maps that align well with real Collatz trajectories."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from collatz_bridge import evaluate_alignment


@dataclass(frozen=True)
class Candidate:
    a: int
    b: int
    c: int
    score: float
    exact_hits: int
    parity_hits: int
    mse: float


def score_candidate(a: int, b: int, c: int, max_start: int, steps: int) -> Candidate:
    exact_total = 0
    parity_total = 0
    mse_total = 0.0

    for start in range(1, max_start + 1):
        result = evaluate_alignment(a, b, c, start=start, steps=steps)
        exact_total += result.exact_hits
        parity_total += result.parity_hits
        mse_total += result.mse

    # Larger exact/parity matches are better, smaller mse is better.
    score = (1000.0 * exact_total) + (50.0 * parity_total) - mse_total
    return Candidate(a=a, b=b, c=c, score=score, exact_hits=exact_total, parity_hits=parity_total, mse=mse_total)


def search(
    coeff_min: int,
    coeff_max: int,
    max_start: int,
    steps: int,
    top_k: int,
    require_anchors: bool,
) -> list[Candidate]:
    candidates: list[Candidate] = []

    for a in range(coeff_min, coeff_max + 1):
        for b in range(coeff_min, coeff_max + 1):
            for c in range(coeff_min, coeff_max + 1):
                if require_anchors:
                    # Collatz local anchors: f(1)=4 and f(2)=1
                    if a + b + c != 4:
                        continue
                    if 4 * a + 2 * b + c != 1:
                        continue

                candidates.append(score_candidate(a, b, c, max_start=max_start, steps=steps))

    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates[:top_k]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find Collatz-aligned quadratic toy maps.")
    parser.add_argument("--coeff-min", type=int, default=-5)
    parser.add_argument("--coeff-max", type=int, default=5)
    parser.add_argument("--max-start", type=int, default=20)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--require-anchors", action="store_true", help="Enforce f(1)=4 and f(2)=1")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    winners = search(
        coeff_min=args.coeff_min,
        coeff_max=args.coeff_max,
        max_start=args.max_start,
        steps=args.steps,
        top_k=args.top,
        require_anchors=args.require_anchors,
    )

    if not winners:
        print("No candidates found.")
        return

    print("Top Collatz-aligned toy quadratics:")
    for idx, item in enumerate(winners, start=1):
        print(f"{idx}. f(x) = {item.a}x^2 + {item.b}x + {item.c}")
        print(f"   score={item.score:.3f}, exact_hits={item.exact_hits}, parity_hits={item.parity_hits}, mse={item.mse:.3e}")

    best = winners[0]
    print("\nBest guess (alignment objective):")
    print(f"  f(x) = {best.a}x^2 + {best.b}x + {best.c}")


if __name__ == "__main__":
    main()
