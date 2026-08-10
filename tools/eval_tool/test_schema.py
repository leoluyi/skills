from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from eval_tool.cli import summarize_verdict
from eval_tool.legacy_config import load_fixture
from eval_tool.legacy_errors import FixtureError
from eval_tool.schema import EvalError, load_cases, load_config, resolve_ids, rows


ROOT = Path(__file__).resolve().parents[2]


class SchemaTests(unittest.TestCase):
    def test_all_existing_fixtures_load(self) -> None:
        skills = [p for p in (ROOT / "skills").iterdir() if (p / "evals" / "evals.json").exists()]
        self.assertGreaterEqual(len(skills), 10)
        for skill in skills:
            cases = load_cases(skill)
            config = load_config(skill, cases)
            self.assertTrue(cases)
            self.assertTrue(config["quick_ids"] or len(cases) <= 6)

    def test_resolve_ids_rejects_unknown_and_holes(self) -> None:
        self.assertEqual(resolve_ids("1-3,5", {1, 2, 3, 5}), (1, 2, 3, 5))
        with self.assertRaises(EvalError):
            resolve_ids("4", {1, 2, 3})

    def test_annotation_fixture_errors_keep_fixture_error_type(self) -> None:
        with TemporaryDirectory() as tmp:
            skill = Path(tmp)
            (skill / "evals").mkdir()
            (skill / "evals" / "evals.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaises(FixtureError):
                load_fixture(skill)

    def test_critical_regression_blocks(self) -> None:
        cases = load_cases(ROOT / "skills" / "humanizer-zh")
        config = load_config(ROOT / "skills" / "humanizer-zh", cases)
        row = next(item for item in rows(cases, config) if item.critical)
        history = {
            (row.case_id, row.slug): [
                (1, {"A": "fail", "B": "pass"}),
                (2, {"A": "fail", "B": "pass"}),
                (3, {"A": "fail", "B": "pass"}),
                (4, {"A": "fail", "B": "pass"}),
                (5, {"A": "fail", "B": "pass"}),
                (6, {"A": "fail", "B": "pass"}),
            ]
        }
        verdict, summary = summarize_verdict(history, (row,))
        self.assertEqual(verdict, "NO-SHIP")
        self.assertEqual(len(summary["critical_regressions"]), 1)

    def test_clear_improvement_ships(self) -> None:
        cases = load_cases(ROOT / "skills" / "briefing-outline")
        config = load_config(ROOT / "skills" / "briefing-outline", cases)
        row = rows(cases, config)[0]
        history = {
            (row.case_id, row.slug): [
                (1, {"A": "pass", "B": "fail"}),
                (2, {"A": "pass", "B": "fail"}),
                (3, {"A": "pass", "B": "fail"}),
            ]
        }
        verdict, _ = summarize_verdict(history, (row,))
        self.assertEqual(verdict, "SHIP")


if __name__ == "__main__":
    unittest.main()
