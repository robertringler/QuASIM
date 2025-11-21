"""SubAgent orchestrating partial goals."""
from __future__ import annotations

from typing import Any, Dict, List

from ..planning.planners.greedy import GreedyPlanner
from ..planning.base import PlanningSystem


class SubAgent:
    def __init__(self, name: str):
        self.name = name
        self._planner = PlanningSystem(GreedyPlanner())

    def handle(self, goal: Dict[str, Any], state: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self._planner.evaluate(goal, state)
