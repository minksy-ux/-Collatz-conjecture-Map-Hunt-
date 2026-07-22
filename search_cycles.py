"""Small command-line helper for exploring Collatz-inspired polynomial maps.

Examples:
    python search_cycles.py --start 5 --steps 12
    python search_cycles.py --fixed-points -5 5
    python search_cycles.py --period 2 -10 10
"""

from __future__ import annotations

import argparse
from typing import Iterable

from collatz_maps import cycle_points, fixed_points, one_dimensional_map, summarize_orbit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explore Collatz-inspired polynomial maps.")
    parser.add_argument("--start", type=float, help="Starting value for orbit iteration.")
    parser.add_argument("--steps", type=int, default=10, help="Number of iteration steps.")
    parser.add_argument("--fixed-points", nargs=2, type=float, metavar=("LOW", "HIGH"), help="Search for fixed points in an integer range.")
    parser.add_argument("--period", type=int, help="Search for points of the given period in an integer range.")
    parser.add_argument("range", nargs="*", type=int, help="Integer search range when using --fixed-points or --period.")
    return parser.parse_args()


def print_orbit(start: float, steps: int) -> None:
    summary = summarize_orbit(start, steps)
    print(f"start = {summary.start}")
    print("orbit:")
    for index, value in enumerate(summary.orbit):
        print(f"  {index:>2}: {value}")
    if summary.cycle is None:
        print("cycle: none detected")
    else:
        mu, lam = summary.cycle
        print(f"cycle: begins at index {mu}, length {lam}")


def integer_range(bounds: Iterable[int]) -> range:
    low, high = list(bounds)
    return range(low, high + 1)


def main() -> None:
    args = parse_args()

    if args.start is not None:
        print_orbit(args.start, args.steps)
        return

    if args.fixed_points is not None:
        search_range = integer_range(args.range or [int(args.fixed_points[0]), int(args.fixed_points[1])])
        points = fixed_points(one_dimensional_map, search_range)
        print("fixed points:", points)
        return

    if args.period is not None:
        if len(args.range) != 2:
            raise SystemExit("provide a two-value integer range after --period, for example: --period 2 -10 10")
        search_range = integer_range(args.range)
        points = cycle_points(one_dimensional_map, search_range, args.period)
        print(f"period-{args.period} points:", points)
        return

    raise SystemExit("choose one mode: --start, --fixed-points, or --period")


if __name__ == "__main__":
    main()
