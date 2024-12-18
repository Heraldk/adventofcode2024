from abc import ABC, abstractmethod


class AdventSolution(ABC):
    @abstractmethod
    def part_one(self, input_file: str, **kwargs): ...

    @abstractmethod
    def part_two(self, input_file: str, **kwargs): ...
