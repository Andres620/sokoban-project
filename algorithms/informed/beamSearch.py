import heapq

from agents.boxAgent import BoxAgent
from agents.wallAgent import WallAgent
from algorithms.baseAlgorithm import BaseAlgorithm
from algorithms.heuristicFactory import HeuristicFactory


class BeamSearch(BaseAlgorithm):
    def __init__(self, grid, heuristic_function, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):
        self.grid = grid
        self.heuristic = HeuristicFactory.create_heuristic(heuristic_type=heuristic_function)
        self.priority_order = priority_order
        self.beam_width = 2

    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        if not self.is_valid_move(start, include_box_agent=False) or not self.is_valid_move(goal,
                                                                                            include_box_agent=True):
            return [[],[]]

        frontier = [(self.heuristic(goal, start), 0, start)]  # (heurística, nivel, posición)
        came_from = {}
        visited = set()
        expansion_nodes = []
        exit_while = False

        while frontier and not exit_while:
            print('Cola de prioridad:', frontier)
            level_nodes = heapq.nsmallest(self.beam_width, frontier)

            for node in level_nodes:
                frontier.remove(node)

            for _, level, current in level_nodes:
                print('Current: ', current, ' level: ', level)
                visited.add(current)
                if current != start:
                    expansion_nodes.append(current)

                if current == goal:
                    exit_while = True
                    break

                for dx, dy in self.priority_order:
                    x, y = current
                    neighbor = (x + dx, y + dy)
                    opposite_neighbor = (x - dx, y - dy)  # Posición opuesta
                    new_heuristic = self.heuristic(goal, neighbor)

                    if (
                        self.is_valid_move(neighbor, include_box_agent=include_box_agent)
                        and neighbor not in came_from
                        and neighbor not in visited
                    ):
                        if take_opposite:
                            if self.is_valid_move(opposite_neighbor, include_box_agent=False):
                                heapq.heappush(frontier, (new_heuristic, level + 1, neighbor))
                                came_from[neighbor] = current
                        else:
                            heapq.heappush(frontier, (new_heuristic, level + 1, neighbor))
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