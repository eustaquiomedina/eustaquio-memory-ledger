from collections import defaultdict, deque


class Graph:
    def __init__(self, edges: list[tuple[int, int]]):
        self._adj = defaultdict(list)
        self._nodes = set()
        for left, right in edges:
            self._adj[left].append(right)
            self._adj[right].append(left)
            self._nodes.add(left)
            self._nodes.add(right)

        for node in self._adj:
            self._adj[node].sort()

    def bfs(self, start: int) -> list[int]:
        if start not in self._nodes:
            return []

        visited = {start}
        order = []
        queue = deque([start])
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self._adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: int) -> list[int]:
        if start not in self._nodes:
            return []

        visited = set()
        order = []

        def visit(node: int) -> None:
            visited.add(node)
            order.append(node)
            for neighbor in self._adj[node]:
                if neighbor not in visited:
                    visit(neighbor)

        visit(start)
        return order

    def has_path(self, start: int, end: int) -> bool:
        return end in set(self.bfs(start))

    def connected_components(self) -> list[list[int]]:
        components = []
        seen = set()
        for node in sorted(self._nodes):
            if node in seen:
                continue
            component = self.bfs(node)
            seen.update(component)
            components.append(component)
        return components


if __name__ == "__main__":
    g = Graph([(0, 1), (0, 2), (1, 3), (2, 3), (4, 5)])
    bfs = g.bfs(0)
    assert bfs[0] == 0
    assert set(bfs[:4]) == {0, 1, 2, 3}
    dfs = g.dfs(0)
    assert dfs[0] == 0
    assert set(dfs) == {0, 1, 2, 3}
    assert g.has_path(0, 3) is True
    assert g.has_path(0, 4) is False
    components = g.connected_components()
    assert len(components) == 2
    assert any(set(c) == {0, 1, 2, 3} for c in components)
    assert any(set(c) == {4, 5} for c in components)
    print("ALL TESTS PASSED")
