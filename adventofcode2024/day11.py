from common import AdventSolution


def run_sequence_naive(nums: list[int], iters: int) -> int:
    next_nums = nums
    for _ in range(iters):
        cur_nums = next_nums
        next_nums: list[int] = []
        for num in cur_nums:
            strnum = str(num)
            if num == 0:
                next_nums.append(1)
            elif (len(strnum) % 2) == 0:
                mid = len(strnum) // 2
                next_nums.append(int(strnum[0:mid]))
                next_nums.append(int(strnum[mid:]))
            else:
                next_nums.append(num * 2024)
        # print(next_nums)

    return len(next_nums)


def run_sequence_memoize(
    num: int, rem_iters: int, memory: dict[int, dict[int, int]]
) -> int:
    if rem_iters == 0:
        return 1

    if num in memory:
        if rem_iters in memory[num]:
            return memory[num][rem_iters]
    else:
        memory[num] = {}

    if num == 0:
        val = run_sequence_memoize(1, rem_iters - 1, memory)
    else:
        strnum = str(num)
        mid = len(strnum) // 2
        if (len(strnum) % 2) == 0:
            val1 = run_sequence_memoize(int(strnum[0:mid]), rem_iters - 1, memory)
            val2 = run_sequence_memoize(int(strnum[mid:]), rem_iters - 1, memory)
            val = val1 + val2
        else:
            val = run_sequence_memoize(2024 * num, rem_iters - 1, memory)

    memory[num][rem_iters] = val
    return val


class Day11(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            print(
                run_sequence_naive(
                    [int(x) for x in file.readline().strip().split()], 25
                )
            )

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            total_length = 0
            memory = {}
            for x in file.readline().strip().split():
                total_length += run_sequence_memoize(int(x), 75, memory)
            print(total_length)
