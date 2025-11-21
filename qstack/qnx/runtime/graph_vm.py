"""Graph-based deterministic execution for operator DAGs."""
from __future__ import annotations

from collections import deque
from typing import Any, Dict, List

from .tracing import TraceRecorder


class OperatorGraph:
    """DAG of operator names with explicit dependencies."""

    def __init__(self):
        self._edges: Dict[str, List[str]] = {}
        self._reverse: Dict[str, List[str]] = {}

    def add_edge(self, src: str, dst: str) -> None:
        self._edges.setdefault(src, []).append(dst)
        self._reverse.setdefault(dst, []).append(src)
        self._edges.setdefault(dst, [])
        self._reverse.setdefault(src, [])

    def topological(self) -> List[str]:
        indegree: Dict[str, int] = {node: len(parents) for node, parents in self._reverse.items()}
        queue = deque(sorted([n for n, deg in indegree.items() if deg == 0]))
        order: List[str] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self._edges.get(node, []):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        if len(order) != len(indegree):
            raise ValueError("cycle detected in operator graph")
        return order


class GraphVM:
    """Executes operators following a DAG ordering with deterministic tracing."""

    def __init__(self, operators, graph: OperatorGraph):
        self._operators = operators
        self._graph = graph
        self._trace = TraceRecorder()
        self._tick = 0

    def run(self, state: Any, goal: Any) -> List[Dict[str, Any]]:
        trace: List[Dict[str, Any]] = []
        for name in self._graph.topological():
            op = self._operators.available().get(name)
            if op is None:
                raise KeyError(f"operator {name} not registered")
            result = op.execute(state, goal)
            record = {"tick": self._tick, "op": name, "result": result}
            self._trace.record("execute", record)
            trace.append(record)
            self._tick += 1
        return trace

    def replay_buffer(self) -> List[Dict[str, Any]]:
        return [entry["payload"] for entry in self._trace.snapshot()]
