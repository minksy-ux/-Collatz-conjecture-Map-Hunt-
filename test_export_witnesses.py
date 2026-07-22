import unittest

from export_witnesses import collect_witnesses


class ExportWitnessesTest(unittest.TestCase):
    def test_collect_witnesses_shape(self) -> None:
        payload = collect_witnesses()
        self.assertIn("generated_at_utc", payload)
        self.assertIn("results", payload)
        results = payload["results"]
        self.assertIn("short_cycle", results)
        self.assertIn("nonnegative", results)
        self.assertIn("bounded_growth", results)
        self.assertIn("fast_cycle", results)

    def test_short_cycle_has_expected_witness_start(self) -> None:
        payload = collect_witnesses()
        short_cycle = payload["results"]["short_cycle"]
        self.assertEqual(short_cycle["status"], "counterexample_found")
        self.assertEqual(short_cycle["counterexample"]["start"], -10)


if __name__ == "__main__":
    unittest.main()