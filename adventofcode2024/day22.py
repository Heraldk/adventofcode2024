from itertools import pairwise

from common import AdventSolution


def next_secret_number(secret_number: int) -> int:
    val = ((64 * secret_number) ^ secret_number) % 16777216
    val = ((val // 32) ^ val) % 16777216
    val = ((val * 2048) ^ val) % 16777216
    return val


def find_maximum_sequence(sequences: list[list[int]]) -> int:
    found_sequences = [{} for _ in range(len(sequences))]
    total_by_sequence = {}
    max_so_far = 0
    max_sequence = None

    differences = []
    for seq in sequences:
        differences.append([])
        for x, y in pairwise(seq):
            differences[-1].append(y - x)

    for pos, seq in enumerate(sequences):
        for index in range(4, len(seq)):
            subseq = tuple(differences[pos][index - 4 : index])
            if subseq not in found_sequences[pos]:
                found_sequences[pos][subseq] = True
                total_by_sequence[subseq] = (
                    total_by_sequence.get(subseq, 0) + sequences[pos][index]
                )
                if max_sequence is None or total_by_sequence[subseq] > max_so_far:
                    max_sequence = subseq
                    max_so_far = total_by_sequence[subseq]

    print(max_sequence, max_so_far)
    return max_so_far


class Day22(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            total = 0
            for line in file.readlines():
                secret_number = int(line.strip())

                for _ in range(2000):
                    secret_number = next_secret_number(secret_number)
                total += secret_number
            print(total)

    @classmethod
    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            sequences = []
            for line in file.readlines():
                sequences.append([])
                secret_number = int(line.strip())
                sequences[-1].append(secret_number % 10)
                for _ in range(2000):
                    secret_number = next_secret_number(secret_number)
                    sequences[-1].append(secret_number % 10)

            print(find_maximum_sequence(sequences))
