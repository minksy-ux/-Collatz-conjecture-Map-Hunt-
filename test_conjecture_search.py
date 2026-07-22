import unittest

from toy_conjectures import Counterexample, find_short_cycle_counterexample


class ConjectureSearchTest(unittest.TestCase):
    def test_find_counterexample(self) -> None:
        result = find_short_cycle_counterexample(0, 0, steps=5, bound=5)
        self.assertIsInstance(result, Counterexample)
        self.assertEqual(result.start, 0)
        self.assertGreater(abs(result.value), 5)


if __name__ == "__main__":
    unittest.main()