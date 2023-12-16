from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm


class BFS(BaseAlgorithm):
    def __init__(self, grid, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):  # Izquierda, Arriba, Derecha, Abajo
        self.grid = grid
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True) -> tuple[
        list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start, include_box_agent=False) or not self.is_valid_move(goal,
                                                                                            include_box_agent=True):
            # raise ValueError("Start and end must be valid coordinates", ' start: ', start, ' end: ',
            #                  start)  # Manejar Error propio
            return [[],[]]

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
                opposite_neighbor = (x - dx, y - dy)  # Posición opuesta

                if self.is_valid_move(neighbor, include_box_agent=False) and neighbor not in came_from:
                    if take_opposite:
                        if self.is_valid_move(opposite_neighbor,include_box_agent=False):
                            queue.append(neighbor)
                            queue.append(neighbor)
                            came_from[neighbor] = current
                            expansion_nodes.append(neighbor)
                    else:
                        queue.append(neighbor)
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
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor, include_box_agent=True)]

    def update_grid(self, grid):
        self.grid = grid
