import unittest

from collatz_surrogate import build_report, evaluate_poly, fit_collatz_step_surrogate
from collatz_bridge import collatz_step


class CollatzSurrogateTest(unittest.TestCase):
    def test_exact_on_training_window(self) -> None:
        coeffs = fit_collatz_step_surrogate(8)
        for n in range(1, 9):
            self.assertEqual(evaluate_poly(coeffs, n), collatz_step(n))

    def test_report_has_full_training_hits(self) -> None:
        report = build_report(10, 15)
        self.assertEqual(report.train_exact_hits, report.train_total)
        self.assertEqual(report.train_total, 10)


if __name__ == "__main__":
    unittest.main()
