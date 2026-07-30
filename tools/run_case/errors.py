"""Shared vocabulary: the error hierarchy, the scored-row types, and the two
constants more than one module needs (the config path and the verdict classes).
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

CONFIG_PATH = Path("evals") / "run-case.json"

PROTECTION = "保護"
HIT = "命中"
CLASSES = (PROTECTION, HIT)


class RunCaseError(Exception):
    """Base class for every legible, non-traceback failure of this tool."""


class ConfigError(RunCaseError):
    """Raised when evals/run-case.json is present but unusable."""


class FixtureError(RunCaseError):
    """Raised when evals.json cannot back the config's declarations."""


class DispatchError(RunCaseError):
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
