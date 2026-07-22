"""ASCII orbit plotting for the Collatz-inspired polynomial maps.

This script keeps the project dependency-free while still providing a visual
way to inspect how a 1D orbit evolves over time.
"""

from __future__ import annotations

import argparse
from typing import Iterable, Sequence

from collatz_maps import iterate_map, one_dimensional_map


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a simple ASCII plot of a 1D orbit.")
    parser.add_argument("--start", type=float, default=0.0, help="Starting value for the orbit.")
    parser.add_argument("--steps", type=int, default=20, help="Number of iteration steps to plot.")
    parser.add_argument("--height", type=int, default=12, help="Plot height in terminal rows.")
    return parser.parse_args()


def build_orbit(start: float, steps: int) -> list[float]:
    return list(iterate_map(one_dimensional_map, start, steps))


def scale_index(value: float, low: float, high: float, height: int) -> int:
    if height <= 1 or high == low:
        return 0
    normalized = (value - low) / (high - low)
    row = round((height - 1) * (1 - normalized))
    return max(0, min(height - 1, row))


def ascii_orbit_plot(values: Sequence[float], height: int = 12) -> str:
    if not values:
        return "(empty orbit)"

    height = max(1, height)
    low = min(values)
    high = max(values)
    rows = [[" " for _ in values] for _ in range(height)]

    for column, value in enumerate(values):
        row = scale_index(value, low, high, height)
        rows[row][column] = "*"

    lines = []
    for row_index, row in enumerate(rows):
        if height == 1:
            label = f"{low:.3g}"
        else:
            label_value = high - (high - low) * row_index / (height - 1)
            label = f"{label_value:.3g}"
        lines.append(f"{label:>8} | {''.join(row)}")

    lines.append("         +" + "-" * len(values))
    lines.append("          " + ''.join(str(index % 10) for index in range(len(values))))
    lines.append(f"range: [{low:.3g}, {high:.3g}]")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    orbit = build_orbit(args.start, args.steps)
    print(f"start = {args.start}")
    print(f"steps = {args.steps}")
    print(ascii_orbit_plot(orbit, height=args.height))


if __name__ == "__main__":
    main()