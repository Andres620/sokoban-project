import heapq
import math
from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm
from algorithms.heuristicFactory import HeuristicFactory


class AStar(BaseAlgorithm):
    def __init__(self, grid, heuristic_function, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):
        self.grid = grid
        self.heuristic = HeuristicFactory.create_heuristic(heuristic_type=heuristic_function)
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start) or not self.is_valid_move(goal):
            raise ValueError("Start and end must be valid coordinates")

        frontier = [(0 + self.heuristic(goal, start), 0, 0,
                     start)]  # (costo_acumulado + heurística, costo acumulado, preferencia, posición)
        came_from = {}
        cost_so_far = {start: 0}
        expansion_nodes = []

        while frontier:
            _, _, _, current = heapq.heappop(frontier)
            if current == goal:
                break

            for dx, dy in self.priority_order:
                x, y = current
                neighbor = (x + dx, y + dy)
                new_cost = cost_so_far[current] + 1

                if self.is_valid_move(neighbor) and (neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]):
                    cost_so_far[neighbor] = new_cost
                    priority = (
                    new_cost + self.heuristic(goal, neighbor), new_cost, self.priority_order.index((dx, dy)), neighbor)
                    heapq.heappush(frontier, priority)
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
            if isinstance(content, WallAgent):
                return False

        return True

    def get_orthogonal_neighbors(self, position):
        x, y = position
        neighbors = [(x + dx, y + dy) for dx, dy in self.priority_order]
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor)]

    def update_grid(self, grid):
        self.grid = grid