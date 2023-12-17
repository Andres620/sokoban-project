from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    @abstractmethod
    def search(self, start: tuple[int, int], goal: tuple[int, int], take_opposite=True, include_box_agent=False) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        pass

    @abstractmethod
    def is_valid_move(self, pos: tuple[int, int]):
        pass

    @abstractmethod
    def get_orthogonal_neighbors(self, position):
        pass

    @abstractmethod
    def update_grid(self, grid):
        pass