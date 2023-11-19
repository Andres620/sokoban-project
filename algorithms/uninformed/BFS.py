from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm


class BFS(BaseAlgorithm):
    def __init__(self, grid, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]): # Izquierda, Arriba, Derecha, Abajo
        self.grid = grid
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start) or not self.is_valid_move(goal):
            raise ValueError("Start and end must be valid coordinates")   #Manejar Error propio

        queue = [start]
        came_from = {start: None}
        expansion_nodes = []

        while queue:
            print('queue: ', queue)
            current = queue.pop(0)
            if current == goal:
                break

            for dx, dy in self.priority_order:
                x, y = current
                neighbor = (x + dx, y + dy)
                if self.is_valid_move(neighbor) and neighbor not in came_from :
                    queue.append(neighbor)
                    came_from[neighbor] = current
                    expansion_nodes.append(neighbor)

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from.get(current, None)
            if current is None:
                return [], expansion_nodes
        path.append(start)
        path.reverse()

        return path, expansion_nodes

    def is_valid_move(self, pos: tuple[int, int]):
        if self.grid.out_of_bounds(pos):
            return False

        cell_contents = self.grid.get_cell_list_contents(pos)
        for content in cell_contents:
            if isinstance(content, WallAgent) or isinstance(content, BoxAgent):
                return False

        return True

    def get_orthogonal_neighbors(self, position):
        x, y = position
        neighbors = [(x + dx, y + dy) for dx, dy in self.priority_order]
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor)]

    def update_grid(self, grid):
        self.grid = grid
