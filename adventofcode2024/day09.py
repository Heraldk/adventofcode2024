from enum import StrEnum, auto

from common import AdventSolution


class Mode(StrEnum):
    BLOCK = auto()
    SPACE = auto()


def unpack_map(input: str) -> tuple[list[int], list[int]]:
    spaces: list[int] = []
    memory: list[int] = []

    mode = Mode.BLOCK
    id = 0
    index = 0
    for char in input.strip():
        val = int(char)
        if mode == Mode.BLOCK:
            memory.extend([id for _ in range(val)])
            id += 1
            mode = Mode.SPACE
        else:
            spaces.extend([index + count for count in range(val)])
            memory.extend([-1 for _ in range(val)])
            mode = Mode.BLOCK
        index += val
    return spaces, memory


# compresses memory in place
def compress(spaces: list[int], memory: list[int]) -> list[int]:
    index = len(memory) - 1
    space_index = 0

    while index > spaces[space_index]:
        if memory[index] >= 0:
            memory[spaces[space_index]] = memory[index]
            memory[index] = -1
            space_index += 1
        index -= 1
    return memory


def calc_checksum(memory: list[int]) -> int:
    checksum = 0
    for index, id in enumerate(memory):
        if id >= 0:
            checksum += index * id
    return checksum


# compresses moving blocks into contiguous spaces, in place
def compress_contiguous(memory: list[int]) -> int:
    # a little more precomputation:
    field_size_lookup: dict[int, int] = {}
    space_size_lookup: dict[int, int] = {}
    start_index = -1
    current_id = -1
    current_size = 0
    for index, val in enumerate(memory):
        if val == current_id:
            current_size += 1
        else:
            if current_id >= 0:
                field_size_lookup[current_id] = current_size
            if current_id < 0 and current_size > 0:
                space_size_lookup[start_index] = current_size
            current_id = val
            current_size = 1
            start_index = index
    if current_id >= 0:
        field_size_lookup[current_id] = current_size
    if current_id < 0:
        space_size_lookup[start_index] = current_size

    index = len(memory) - 1
    while index > 0:
        if memory[index] >= 0:
            file_size = field_size_lookup[memory[index]]
            # look for a place for this file
            spaces = {
                k: v
                for k, v in space_size_lookup.items()
                if v >= file_size and k < index
            }
            if len(spaces) > 0:
                lowest_space = min([k for k in spaces.keys()])
                # move the file
                memory[lowest_space : lowest_space + file_size] = [
                    memory[index] for _ in range(file_size)
                ]
                memory[index + 1 - file_size : index + 1] = [
                    -1 for _ in range(file_size)
                ]
                # update the space_size_lookup
                rem_space = space_size_lookup[lowest_space] - file_size
                del space_size_lookup[lowest_space]
                if rem_space > 0:
                    space_size_lookup[lowest_space + file_size] = rem_space
            index = index - file_size
        else:
            index -= 1
    return memory


class Day09(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            spaces, memory = unpack_map(file.readline())
            memory = compress(spaces, memory)
            print(calc_checksum(memory))

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            spaces, memory = unpack_map(file.readline())
            memory = compress_contiguous(memory)
            print(calc_checksum(memory))
