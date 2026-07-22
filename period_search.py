"""Exact-period search helpers for Collatz-inspired polynomial maps."""

from __future__ import annotations

import argparse
from typing import Callable, Iterable, List, Sequence

from collatz_maps import Number, one_dimensional_map


def orbit_values(func: Callable[[Number], Number], start: Number, steps: int) -> List[Number]:
    values = [start]
    value = start
    for _ in range(steps):
        value = func(value)
        values.append(value)
    return values


def minimal_period(func: Callable[[Number], Number], start: Number, max_period: int) -> int | None:
    """Return the smallest positive period of `start`, if found within `max_period`."""

    value = start
    for period in range(1, max_period + 1):
        value = func(value)
        if value == start:
            return period
    return None


def exact_period_points(
    func: Callable[[Number], Number],
    candidates: Iterable[Number],
    period: int,
) -> List[Number]:
    """Return points whose minimal period is exactly `period`."""

    results: List[Number] = []
    for candidate in candidates:
        candidate_period = minimal_period(func, candidate, period)
        if candidate_period == period:
            results.append(candidate)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search for exact-period points of a polynomial map.")
    parser.add_argument("period", type=int, help="Target exact period.")
    parser.add_argument("low", type=int, help="Lower bound of the integer search range.")
    parser.add_argument("high", type=int, help="Upper bound of the integer search range.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidates = range(args.low, args.high + 1)
    points = exact_period_points(one_dimensional_map, candidates, args.period)
    print(f"exact period {args.period} points in [{args.low}, {args.high}]: {points}")


if __name__ == "__main__":
    main()