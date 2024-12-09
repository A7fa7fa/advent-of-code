
from typing import List


def readFile() -> List[str]:
    with open('2024/02-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines


def run() -> int:
    lines = readFile()

    unsafe_lines = 0

    for line in lines:
        nums: list[int] = list(map(lambda x: int(x),line.strip().split(" ")))

        try_unsafe = 0
        for remove in range(len(nums)):
            new_nums = nums[0:remove] + nums[remove + 1:]

            if sorted(new_nums) == new_nums or sorted(new_nums, reverse=True) == new_nums:
                for i in range(1, len(new_nums)):
                    diff = abs(new_nums[i-1] - new_nums[i])
                    if 1 <= diff <= 3:
                        continue
                    else:
                        try_unsafe += 1
                        break
            else:
                try_unsafe += 1
        if try_unsafe == len(nums):
            unsafe_lines += 1


    return len(lines) - unsafe_lines


if __name__ == '__main__':
    result = run()
    print(result)