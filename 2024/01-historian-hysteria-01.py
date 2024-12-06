
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
    first_list.sort()
    second_list.sort()
    assert len(first_list) == len(second_list)
    total = 0
    for i in range(len(first_list)):
        total += abs(first_list[i]-second_list[i])

    return total



if __name__ == '__main__':
    result = run()
    print(result)