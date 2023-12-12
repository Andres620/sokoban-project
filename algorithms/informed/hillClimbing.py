import heapq
from collections import defaultdict

from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm
from algorithms.heuristicFactory import HeuristicFactory


class HillClimbing(BaseAlgorithm):
    def __init__(self, grid, heuristic_function, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):
        self.grid = grid
        self.heuristic = HeuristicFactory.create_heuristic(heuristic_type=heuristic_function)
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start) or not self.is_valid_move(goal):
            raise ValueError("Start and end must be valid coordinates")

        frontier = [(self.heuristic(goal, start), 0, start)]  # (heurística, nivel, posición)
        came_from = {}
        expansion_nodes = []
        max_level = 0

        while frontier:
            print('Cola de prioridad:', frontier)
            _, level, current = heapq.heappop(frontier)
            max_level = max(max_level, level)
            print('Current: ', current, ' level: ', level)
            if current != start:
                expansion_nodes.append(current)

            if current == goal:
                break

            for dx, dy in self.priority_order:
                x, y = current
                neighbor = (x + dx, y + dy)
                new_heuristic = self.heuristic(goal, neighbor)

                if self.is_valid_move(neighbor) and neighbor not in came_from:
                    heapq.heappush(frontier, (new_heuristic, max_level + 1, neighbor))
                    came_from[neighbor] = current

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