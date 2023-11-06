from algorithms.uninformed.BFS import BFS


class AlgorithmFactory:
    @staticmethod
    def create_algorithm(algorithm_type, grid=None, heuristic_function=None, priority_order=[(-1, 0), (0, 1), (1, 0), (0, -1)]):
        if algorithm_type == 'BFS':
            return BFS(grid, priority_order)
