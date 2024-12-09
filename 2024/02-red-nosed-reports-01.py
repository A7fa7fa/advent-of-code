
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
        if sorted(nums) == nums or sorted(nums, reverse=True) == nums:
            for i in range(1, len(nums)):
                diff = abs(nums[i-1] - nums[i])
                if 1 <= diff <= 3:
                    continue
                else:
                    unsafe_lines += 1
                    break
        else:
            unsafe_lines += 1


    return len(lines) - unsafe_lines


if __name__ == '__main__':
    result = run()
    print(result)