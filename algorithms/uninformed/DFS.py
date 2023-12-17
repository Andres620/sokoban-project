from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm


class DFS(BaseAlgorithm):
    def __init__(self, grid, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]): # Izquierda, Arriba, Derecha, Abajo
        self.grid = grid
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start) or not self.is_valid_move(goal):
            raise ValueError("Start and end must be valid coordinates")

        visited = set()
        path = []
        expansion_nodes = []
        self._search(start, goal, visited, path, expansion_nodes)

        return path, expansion_nodes

    def _search(self, start: tuple[int, int], goal: tuple[int, int], visited: set, path: list[tuple[int, int]],
                expansion_nodes: list[tuple[int, int]]) -> bool:
        if start == goal:
            return True

        visited.add(start)

        for neighbor in self.get_orthogonal_neighbors(start):
            if neighbor not in visited:
                expansion_nodes.append(neighbor)
                path.append(neighbor)
                if self._search(neighbor, goal, visited, path, expansion_nodes):
                    return True
                path.pop()

        return False

    def is_valid_move(self, pos: tuple[int, int]):
        if self.grid.out_of_bounds(pos):
            return False

        cell_contents = self.grid.get_cell_list_contents(pos)
        for content in cell_contents:
            if isinstance(content, WallAgent):
                return False

        return True

    def get_orthogonal_neighbors(self, position):
        x, y = position
        neighbors = [(x + dx, y + dy) for dx, dy in self.priority_order]
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor)]

    def update_grid(self, grid):
        self.grid = grid