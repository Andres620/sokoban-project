from algorithms.informed.beamSearch import BeamSearch
from algorithms.informed.hillClimbing import HillClimbing
from algorithms.uninformed.BFS import BFS
from algorithms.uninformed.DFS import DFS
from algorithms.uninformed.UCS import UCS
from algorithms.informed.AStar import AStar


class AlgorithmFactory:
    @staticmethod
    def create_algorithm(algorithm_type, grid=None, heuristic_function=None, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):
        if algorithm_type == 'BFS':
            return BFS(grid, priority_order)
        if algorithm_type == 'DFS':
            return DFS(grid, priority_order)
        if algorithm_type == 'UCS':
            return UCS(grid, priority_order)
        if algorithm_type == 'ASTAR':
            return AStar(grid, heuristic_function, priority_order)
        if algorithm_type == 'HILL CLIMBING':
            return HillClimbing(grid, heuristic_function, priority_order)
        if algorithm_type == 'BEAM SEARCH':
            return BeamSearch(grid, heuristic_function, priority_order)
