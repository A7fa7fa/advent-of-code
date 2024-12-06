
import collections
from typing import List


def readFile() -> List[str]:
    with open('2024/01-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def run() -> int:
    lines = readFile()
    first_list: list[int] = []
    second_list: list[int] = []
    for line in lines:
        contents = line.strip().replace("  ", "").split(" ")
        first_list.append(int(contents[0].strip()))
        second_list.append(int(contents[1].strip()))
    counter = collections.Counter(second_list)
    assert len(first_list) == len(second_list)

    total = 0
    for i in range(len(first_list)):
        total += counter.get(first_list[i], 0) * first_list[i]
    return total



if __name__ == '__main__':
    result = run()
    print(result)