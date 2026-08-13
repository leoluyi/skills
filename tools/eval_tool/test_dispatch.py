from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from eval_tool.dispatch import GRADER_TIMEOUT, RUNNER_TIMEOUT, cli_command
from eval_tool.legacy_errors import DispatchError


class DispatchTests(unittest.TestCase):
    def test_codex_command_uses_isolated_auth_only_home(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_home = root / "source-codex-home"
            source_home.mkdir()
            (source_home / "auth.json").write_text("test credential", encoding="utf-8")
            empty = root / "empty"
            empty.mkdir()

            with patch.dict(os.environ, {"CODEX_HOME": str(source_home)}):
                command = cli_command("codex", "Reply OK", empty, root / "answer.txt")

            isolated = empty.parent / "codex-home"
            self.assertIn(f"CODEX_HOME={isolated}", command)
            self.assertTrue((isolated / "auth.json").is_symlink())
            self.assertIn("--ignore-rules", command)
            self.assertIn("--ephemeral", command)

    def test_codex_command_fails_clearly_without_auth(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty = root / "empty"
            empty.mkdir()
            with patch.dict(os.environ, {"CODEX_HOME": str(root / "missing")}, clear=False):
                with self.assertRaisesRegex(DispatchError, "needs auth.json"):
                    cli_command("codex", "Reply OK", empty, root / "answer.txt")

    def test_timeouts_leave_room_for_full_skill_outputs(self) -> None:
        self.assertGreaterEqual(RUNNER_TIMEOUT, 300)
        self.assertGreaterEqual(GRADER_TIMEOUT, 180)


if __name__ == "__main__":
    unittest.main()
