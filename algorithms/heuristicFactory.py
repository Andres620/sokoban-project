import math


class HeuristicFactory:
    @staticmethod
    def create_heuristic(heuristic_type='EUCLIDEAN'):
        if heuristic_type == 'EUCLIDEAN':
            return HeuristicFactory.euclidean_heuristic
        elif heuristic_type == 'MANHATTAN':
            return HeuristicFactory.manhattan_heuristic
        else:
            raise ValueError("Tipo de heurística no válido")

    @staticmethod
    def euclidean_heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        return math.sqrt((b[0]*10 - a[0]*10) ** 2 + (b[1]*10 - a[1]*10) ** 2)

    @staticmethod
    def manhattan_heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        return abs(b[0]*10 - a[0]*10) + abs(b[1]*10 - a[1]*10)
