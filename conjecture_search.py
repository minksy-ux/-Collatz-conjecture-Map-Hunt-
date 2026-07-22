"""Search for counterexamples to Collatz-inspired toy conjectures.

The repository uses several deliberately falsifiable polynomial conjectures.
This CLI lets you pick one and scan a range of integer starts for a witness.
"""

from __future__ import annotations

import argparse

from toy_conjectures import CONJECTURES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search for counterexamples to a toy Collatz-inspired conjecture.")
    parser.add_argument("conjecture", choices=sorted(CONJECTURES), help="Toy conjecture to test.")
    parser.add_argument("low", type=int, help="Lower bound of the integer search range.")
    parser.add_argument("high", type=int, help="Upper bound of the integer search range.")
    parser.add_argument("--steps", type=int, default=25, help="Maximum number of iterations per start value.")
    parser.add_argument("--bound", type=float, default=1e6, help="Escape threshold for orbit magnitude.")
    parser.add_argument("--max-cycle-length", type=int, default=4, help="Largest cycle that counts as a short cycle.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    statement, search_fn = CONJECTURES[args.conjecture]
    search_kwargs = {"low": args.low, "high": args.high, "steps": args.steps}
    if args.conjecture == "short_cycle":
        search_kwargs["bound"] = args.bound
        search_kwargs["max_cycle_length"] = args.max_cycle_length
    elif args.conjecture == "bounded_growth":
        search_kwargs["bound"] = args.bound

    counterexample = search_fn(**search_kwargs)

    if counterexample is None:
        print(f"No counterexample found for: {statement}")
        return

    print(f"Counterexample candidate found for: {statement}")
    print(f"  conjecture key: {counterexample.conjecture}")
    print(f"  start: {counterexample.start}")
    print(f"  step: {counterexample.escaped_at_step}")
    print(f"  value: {counterexample.value}")
    print(f"  reason: {counterexample.reason}")
    print(f"  orbit prefix: {counterexample.orbit}")


if __name__ == "__main__":
    main()