"""Finance domain hooks."""
from __future__ import annotations

from typing import Dict

from ..core.risk import risk_score


def portfolio_risk(exposures: Dict[str, float]) -> float:
    sensitivities = {k: 1.0 for k in exposures}
    return risk_score(exposures, sensitivities)
