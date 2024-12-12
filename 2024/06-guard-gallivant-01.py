
from typing import List


def readFile(file_name: str) -> List[str]:
    with open(f'2024/{file_name}') as f:
        lines : List[str] = f.readlines()
        return lines

def in_bound(pos: tuple[int, int], table: list[str]) -> bool:
    return pos[0] < len(table) and pos[1] < len(table[0]) and pos[0] >= 0 and pos[1] >= 0

def turn_right(direction: tuple[int, int]) -> tuple[int, int]:
    row, col = direction
    if row == -1:
        return (0, 1)
    if row == 1:
        return (0, -1)
    if col == 1:
        return (1, 0)
    if col == -1:
        return (-1, 0)
    assert False

def move(pos: tuple[int, int], direction: tuple[int, int], table: list[str], path: list[tuple[int, int]]):
    next_pos = (pos[0] -1, pos[1])
    while in_bound(next_pos, table):
        char = table[next_pos[0]][next_pos[1]]
        if char == "#":
            direction = turn_right(direction)
            next_pos = (path[-1][0] + direction[0], path[-1][1] + direction[1])
            continue
        path.append(next_pos)
        next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])



def run(file_name: str) -> int:
    lines = readFile(file_name)
    lines = [line.strip() for line in lines]

    start_pos: list[int] = [0, 0]
    for row, line in enumerate(lines):
        found = line.find("^")
        if found > -1:
            start_pos[0] = row
            start_pos[1] = found

    path: list[tuple[int, int]] = []
    path.append((start_pos[0], start_pos[1],))
    move(path[-1], (-1, 0), lines, path)


    return len(set(path))



if __name__ == '__main__':

    result = run("06-input-test.txt")
    assert result == 41, result
    print("test", result)

    result = run("06-input.txt")
    assert result == 5329, result
    print("result", result)