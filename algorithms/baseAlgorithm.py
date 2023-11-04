from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    @abstractmethod
    def search(self, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        pass
