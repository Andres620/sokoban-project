import heapq

from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm


class UCS(BaseAlgorithm):
    def __init__(self, grid, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):
        self.grid = grid
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start, include_box_agent=False) or not self.is_valid_move(goal,
                                                                                            include_box_agent=True):
            return [[],[]]

        queue = [(0, 0, start)]  # Inicializar la cola de prioridad con el costo acumulado, la preferencia y la posición
        came_from = {start: None}
        cost_so_far = {start: 0}
        expansion_nodes = []

        while queue:
            _, _, current = heapq.heappop(queue)
            if current == goal:
                break

            for dx, dy in self.priority_order:
                x, y = current
                neighbor = (x + dx, y + dy)
                opposite_neighbor = (x - dx, y - dy)  # Posición opuesta
                new_cost = cost_so_far[current] + 1  # Costo uniforme

                if self.is_valid_move(neighbor, include_box_agent=include_box_agent) and neighbor not in came_from and \
                        (neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]):
                    if take_opposite:
                        if self.is_valid_move(opposite_neighbor, include_box_agent=False):
                            cost_so_far[neighbor] = new_cost
                            priority = (
                                new_cost, self.priority_order.index((dx, dy)), neighbor)  # Agregar preferencia a la prioridad
                            heapq.heappush(queue, priority)
                            came_from[neighbor] = current
                            expansion_nodes.append(neighbor)
                    else:
                        cost_so_far[neighbor] = new_cost
                        priority = (
                            new_cost, self.priority_order.index((dx, dy)), neighbor)  # Agregar preferencia a la prioridad
                        heapq.heappush(queue, priority)
                        came_from[neighbor] = current
                        expansion_nodes.append(neighbor)
            print('pop: ', current,' Cola prioridad: ', queue)

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
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor)]

    def update_grid(self, grid):
        self.grid = grid