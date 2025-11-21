from __future__ import annotations

from typing import Dict


def pharma_step(state: Dict[str, float]) -> Dict[str, float]:
    a = float(state.get("A", 0.0))
    b = float(state.get("B", 0.0))
    k = float(state.get("rate", 0.05))
    delta = k * a
    return {"A": a - delta, "B": b + delta, "rate": k}
