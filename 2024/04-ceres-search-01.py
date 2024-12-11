
from typing import Any, Generator, List


def readFile() -> List[str]:
    with open('2024/04-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines


def in_bound(pos: list[int], maxS: list[int]) -> bool:
    return pos[0] < maxS[0] and pos[1] < maxS[1] and pos[0] >= 0 and pos[1] >= 0

def steps(pos: list[int], maxS: list[int]) -> Generator[list[int], Any, None]:
    for x, y, in[[-1 , -1]
                ,[-1 , 0]
                ,[-1 , 1]
                ,[0 , -1]
                ,[0 , 1]
                ,[1 , -1]
                ,[1 , 0]
                ,[1 , 1]]:
        new_pos = [pos[0]+x, pos[1]+y]
        if in_bound(new_pos, maxS):
            yield [x, y]


next_char = {"XM", "XMA"}

FOUND: list[tuple[int, int, int, int]] = []

def walk(pos: list[int], table: list[str], res: list[str], dir: tuple[int, int]) -> int:
    total = 0
    new_pos = [pos[0] + dir[0], pos[1] +  dir[1]]
    if not in_bound(new_pos, [len(table), len(table[0])]):
        return total
    char = table[new_pos[0]][new_pos[1]]
    new_string = res[-1] + char
    if new_string == "XMAS":
        total += 1
        FOUND.append((new_pos[0], new_pos[1], dir[0], dir[1]))
        return total
    if new_string in next_char:
        res.append(new_string)
        total += walk(new_pos, table, res, dir)
        res.pop()
    return total

def pocess(pos: list[int], table: list[str], res: list[str]) -> int:
    total = 0
    for d_row, d_col in steps(pos, [len(table), len(table[0])]):
        total += walk(pos, table, res, (d_row, d_col,))
    return total


def step(current_pos: list[int], lines: list[str]) -> list[int]:
    coord = (current_pos[0] * len(lines[0])) + current_pos[1]
    coord += 1
    pos_row = coord // len(lines[0])
    pos_col = coord - (pos_row * len(lines[0]))
    return [pos_row, pos_col]

def run() -> int:
    lines = readFile()
    lines = [line.strip() for line in lines]

    current_pos = [0, 0]

    total = 0
    while current_pos[0] < len(lines):

        char = lines[current_pos[0]][current_pos[1]]
        if char != "X":
            print(current_pos)
            current_pos = step(current_pos, lines)
            continue

        print(current_pos, "X found")
        res: list[str] = []
        res.append("X")
        total += pocess(current_pos, lines, res)
        res.pop()
        assert len(res) == 0
        current_pos = step(current_pos, lines)
    return total


_lines = readFile()
_lines = [li.strip() for li in _lines]
_row = ["."] * len(_lines[0])
_new_file = [_row[:] for _ in range(len(_lines))]


flip = {
    0: 0,
    -1: 1,
    1: -1
}



if __name__ == '__main__':
    check: list[tuple[int, int]] = []

    for x, y in steps([0,0], [1, 1]):
        check.append((x, y,))
    assert len(check) == 0
    check.clear()
    for x, y in steps([1,1], [3, 3]):
        check.append((x, y,))
    assert len(check) == 8

    result = run()


    # for f in FOUND:
    #     _new_file[f[0]][f[1]] = "S"
    #     _new_file[f[0] + (flip[f[2]]  * 1) ][f[1] + (flip[f[3]] * 1)] = "A"
    #     _new_file[f[0] + (flip[f[2]]  * 2) ][f[1] + (flip[f[3]] * 2)] = "M"
    #     _new_file[f[0] + (flip[f[2]]  * 3) ][f[1] + (flip[f[3]] * 3)] = "X"

    # with open('2024/04-input-found.txt', "w") as f:
    #     for r in _new_file:
    #         print("".join(r))
    #         f.write("".join(r)+'\n')


    assert result == 2534, result
    print(result)