from __future__ import annotations

from collections import deque
from typing import Iterator


class _State:
    __slots__ = ("goto", "fail", "output", "depth")

    def __init__(self, depth: int = 0):
        self.goto: dict[str, int] = {}
        self.fail: int = 0
        self.output: list[int] = []
        self.depth = depth


class AhoCorasick:
    def __init__(self):
        self.states: list[_State] = [_State(0)]
        self.patterns: list[str] = []
        self._built = False

    def add(self, pattern: str) -> int:
        if not pattern:
            raise ValueError("empty pattern")
        pid = len(self.patterns)
        self.patterns.append(pattern)
        node = 0
        for ch in pattern:
            nxt = self.states[node].goto.get(ch)
            if nxt is None:
                nxt = len(self.states)
                self.states.append(_State(self.states[node].depth + 1))
                self.states[node].goto[ch] = nxt
            node = nxt
        self.states[node].output.append(pid)
        self._built = False
        return pid

    def build(self) -> None:
        q: deque[int] = deque()
        root = self.states[0]
        for ch, nxt in root.goto.items():
            self.states[nxt].fail = 0
            q.append(nxt)
        while q:
            u = q.popleft()
            state = self.states[u]
            for ch, v in state.goto.items():
                q.append(v)
                f = state.fail
                while f and ch not in self.states[f].goto:
                    f = self.states[f].fail
                fallback = self.states[f].goto.get(ch, 0)
                if fallback == v:
                    fallback = 0
                self.states[v].fail = fallback
                self.states[v].output.extend(self.states[fallback].output)
        self._built = True

    def _next(self, node: int, ch: str) -> int:
        while node and ch not in self.states[node].goto:
            node = self.states[node].fail
        return self.states[node].goto.get(ch, 0)

    def find(self, text: str) -> Iterator[tuple[int, int]]:
        if not self._built:
            self.build()
        node = 0
        for i, ch in enumerate(text):
            node = self._next(node, ch)
            for pid in self.states[node].output:
                start = i - len(self.patterns[pid]) + 1
                yield (start, pid)
