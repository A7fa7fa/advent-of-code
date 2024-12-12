
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

def have_seen(curr_position: tuple[int, int], direction: tuple[int, int], path_dir: set[tuple[int, int, int, int]], table: list[str],) -> bool:
    if (curr_position[0], curr_position[1], direction[0], direction[1]) in path_dir:
        return True
    return False

def is_looping(direction: tuple[int, int], table: list[str], path: list[tuple[int, int]], path_dir: set[tuple[int, int, int, int]], new_blocker: tuple[int, int]) -> bool:
    next_pos = (new_blocker[0], new_blocker[1])
    is_loop = False
    while in_bound(next_pos, table):

        char = table[next_pos[0]][next_pos[1]]
        if char == "#" or new_blocker == next_pos:
            direction = turn_right(direction)
            next_pos = (path[-1][0] + direction[0], path[-1][1] + direction[1])
            continue


        if have_seen(next_pos, direction, path_dir, table):
            is_loop = True
            break

        path.append(next_pos)
        path_dir.add((next_pos[0], next_pos[1], direction[0], direction[1]))
        next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])
    return is_loop


def move(pos: tuple[int, int], direction: tuple[int, int], table: list[str], path: list[tuple[int, int]], path_dir: set[tuple[int, int, int, int]]) -> int:
    next_pos = (pos[0] + direction[0], pos[1] + direction[1])
    loops = 0
    path_lookup: set[tuple[int, int]] = set()
    path_lookup.add(pos)
    path_lookup: set[tuple[int, int]] = set()
    while in_bound(next_pos, table):

        char = table[next_pos[0]][next_pos[1]]

        if char == "#":
            direction = turn_right(direction)
            next_pos = (path[-1][0] + direction[0], path[-1][1] + direction[1])
            continue

        if next_pos not in path_lookup:
            if is_looping(direction, table, path[:], path_dir.copy(), next_pos):
                loops += 1
        else:
            print("in path")

        path.append(next_pos)
        path_lookup.add(next_pos)
        path_dir.add((next_pos[0], next_pos[1], direction[0], direction[1]))
        next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])

    return loops

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
    path_dir: set[tuple[int, int, int, int]] = set()
    path.append((start_pos[0], start_pos[1],))
    path_dir.add((start_pos[0], start_pos[1], -1, 0))
    total_looping = move(path[-1], (-1, 0), lines, path, path_dir)

    return total_looping




if __name__ == '__main__':

    result = run("06-input-test.txt")
    assert result == 6, result
    print("test", result)

    result = run("06-input.txt")
    assert result == 2162, result
    print("result", result)