from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm


class DFS(BaseAlgorithm):
    def __init__(self, grid, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]): # Izquierda, Arriba, Derecha, Abajo
        self.grid = grid
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start, include_box_agent=False) or not self.is_valid_move(goal,
                                                                                            include_box_agent=True):
            return [[],[]]

        visited = set()
        path = []
        expansion_nodes = []
        self._search(start, goal, visited, path, expansion_nodes, take_opposite, include_box_agent)

        return path, expansion_nodes

    def _search(self, start: tuple[int, int], goal: tuple[int, int], visited: set, path: list[tuple[int, int]],
                expansion_nodes: list[tuple[int, int]], take_opposite=True, include_box_agent=False) -> bool:
        if start == goal:
            return True

        visited.add(start)

        for dx, dy in self.priority_order:
            neighbor = (start[0] + dx, start[1] + dy)
            opposite_neighbor = (start[0] - dx, start[1] - dy)

            if self.is_valid_move(neighbor, include_box_agent=include_box_agent) and neighbor not in visited:
                if take_opposite:
                    if self.is_valid_move(opposite_neighbor, include_box_agent=False):
                        expansion_nodes.append(neighbor)
                        path.append(neighbor)
                        if self._search(neighbor, goal, visited, path, expansion_nodes, take_opposite, include_box_agent):
                            return True
                        path.pop()
                else:
                    expansion_nodes.append(neighbor)
                    path.append(neighbor)
                    if self._search(neighbor, goal, visited, path, expansion_nodes, take_opposite, include_box_agent):
                        return True
                    path.pop()

        return False

    def is_valid_move(self, pos: tuple[int, int], include_box_agent: bool = False):
        if self.grid.out_of_bounds(pos):
            return False

        cell_contents = self.grid.get_cell_list_contents(pos)
        for content in cell_contents:
            if isinstance(content, WallAgent):
                return False
            if include_box_agent and isinstance(content, BoxAgent):
                return False

        return True

    def get_orthogonal_neighbors(self, position):
        x, y = position
        neighbors = [(x + dx, y + dy) for dx, dy in self.priority_order]
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor)]

    def update_grid(self, grid):
        self.grid = grid