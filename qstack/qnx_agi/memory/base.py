from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, List, Tuple


@dataclass
class MemorySystem:
    capacity: int = 32
    _buffer: Deque[Tuple[str, Any]] = field(default_factory=deque, init=False)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")
        self._buffer = deque(maxlen=self.capacity)

    def record(self, key: str, value: Any) -> None:
        self._buffer.append((key, value))

    def recall(self, key: str) -> List[Any]:
        return [v for k, v in self._buffer if k == key]

    def latest(self) -> Tuple[str, Any] | None:
        return self._buffer[-1] if self._buffer else None

    def clear(self) -> None:
        self._buffer.clear()
