from algorithms.baseAlgorithm import BaseAlgorithm


class HillClimbing(BaseAlgorithm):
    def __init__(self, grid, heuristic_function):
        self.grid = grid
        self.heuristic_function = heuristic_function

    def search(self, start, goal):
        pass