import heapq
from collections import defaultdict

from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm
from algorithms.heuristicFactory import HeuristicFactory


class HillClimbing(BaseAlgorithm):
    def __init__(self, grid, heuristic_function, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]): #abajo, arriba, izquierda y derecha.
        self.grid = grid
        self.heuristic = HeuristicFactory.create_heuristic(heuristic_type=heuristic_function)
        self.priority_order = priority_order

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[
        list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start, include_box_agent=False) or not self.is_valid_move(goal,
                                                                                            include_box_agent=True):
            return [[], []]

        current = start
        came_from = {start: None}
        expansion_nodes = [current]
        other_neighbors = []

        while current != goal:
            next_node = None
            next_node_score = float("inf")

            for dx, dy in self.priority_order:
                x, y = current
                neighbor = (x + dx, y + dy)
                opposite_neighbor = (x - dx, y - dy)  # Posición opuesta

                if self.is_valid_move(neighbor, include_box_agent=include_box_agent) and neighbor not in came_from:
                    if neighbor in expansion_nodes:
                        continue
                    if take_opposite:
                        if self.is_valid_move(opposite_neighbor,include_box_agent=False):
                            came_from[neighbor] = current
                            score = self.heuristic(goal, neighbor)
                            if score < next_node_score:
                                next_node_score = score
                                next_node = neighbor
                            else:
                                other_neighbors.append(neighbor)
                    else:
                        came_from[neighbor] = current
                        score = self.heuristic(goal, neighbor)
                        if score < next_node_score:
                            next_node_score = score
                            next_node = neighbor
                        else:
                            other_neighbors.append(neighbor)

            if next_node is None:
                if not other_neighbors:
                    return [], expansion_nodes
                next_node = other_neighbors.pop(0)

            current = next_node
            expansion_nodes.append(current)

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