import unittest

from collatz_bridge import collatz_step, collatz_trajectory, evaluate_alignment


class CollatzBridgeTest(unittest.TestCase):
    def test_collatz_step(self) -> None:
        self.assertEqual(collatz_step(1), 4)
        self.assertEqual(collatz_step(2), 1)
        self.assertEqual(collatz_step(3), 10)

    def test_collatz_trajectory(self) -> None:
        self.assertEqual(collatz_trajectory(3, 4), [3, 10, 5, 16, 8])

    def test_alignment_identity_hits(self) -> None:
        # f(x)=x matches only the first value against real Collatz on most starts.
        result = evaluate_alignment(a=0, b=1, c=0, start=3, steps=4)
        self.assertGreaterEqual(result.exact_hits, 1)
        self.assertGreaterEqual(result.parity_hits, 1)


if __name__ == "__main__":
    unittest.main()
