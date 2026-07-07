from __future__ import annotations

from typing import Iterator


class _Node:
    __slots__ = ("left", "right", "up", "down", "column", "row_id", "size", "name")

    def __init__(self, name=None):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = self
        self.row_id = None
        self.size = 0
        self.name = name


class DancingLinks:
    def __init__(self, num_columns: int, secondary: set[int] | None = None):
        self.root = _Node("root")
        self.columns: list[_Node] = []
        secondary = secondary or set()
        prev = self.root
        for c in range(num_columns):
            col = _Node(c)
            col.column = col
            self.columns.append(col)
            if c in secondary:
                col.left = col
                col.right = col
            else:
                col.left = prev
                col.right = self.root
                prev.right = col
                self.root.left = col
                prev = col

    def add_row(self, row_id, columns: list[int]) -> None:
        first = None
        for c in sorted(columns):
            col = self.columns[c]
            node = _Node()
            node.column = col
            node.row_id = row_id
            node.up = col.up
            node.down = col
            col.up.down = node
            col.up = node
            col.size += 1
            if first is None:
                first = node
                node.left = node
                node.right = node
            else:
                node.left = first.left
                node.right = first
                first.left.right = node
                first.left = node

    def _cover(self, col: _Node) -> None:
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i is not col:
            j = i.right
            while j is not i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def _uncover(self, col: _Node) -> None:
        i = col.up
        while i is not col:
            j = i.left
            while j is not i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def _choose_column(self) -> _Node:
        best = None
        best_size = None
        c = self.root.right
        while c is not self.root:
            if best_size is None or c.size < best_size:
                best_size = c.size
                best = c
            c = c.right
        return best

    def solve(self) -> Iterator[list]:
        solution: list[_Node] = []
        yield from self._search(solution)

    def _search(self, solution: list[_Node]) -> Iterator[list]:
        if self.root.right is self.root:
            yield [n.row_id for n in solution]
            return
        col = self._choose_column()
        if col.size == 0:
            return
        self._cover(col)
        r = col.down
        while r is not col:
            solution.append(r)
            j = r.right
            while j is not r:
                self._cover(j.column)
                j = j.right
            yield from self._search(solution)
            j = r.left
            while j is not r:
                self._uncover(j.column)
                j = j.left
            solution.pop()
            r = r.down
        self._uncover(col)
