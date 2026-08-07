"""Shared vocabulary: the error hierarchy, the scored-row types, and the two
constants more than one module needs (the config path and the verdict classes).
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

CONFIG_PATH = Path("evals") / "score-evals.json"

PROTECTION = "保護"
HIT = "命中"
CLASSES = (PROTECTION, HIT)


class ScoreEvalsError(Exception):
    """Base class for every legible, non-traceback failure of this tool."""


class ConfigError(ScoreEvalsError):
    """Raised when evals/score-evals.json is present but unusable."""


class FixtureError(ScoreEvalsError):
    """Raised when evals.json cannot back the config's declarations."""


class DispatchError(ScoreEvalsError):
    """Raised when a runner or grader subprocess cannot be scored."""


class Row(NamedTuple):
    """One scored judgment: the unit both denominators count."""

    case_id: int
    slug: str
    detail: str
    klass: str
    origin: str


class Chunk(NamedTuple):
    lo: int
    hi: int
    case_ids: tuple[int, ...]
