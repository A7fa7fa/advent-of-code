
from typing import List


def readFile() -> List[str]:
    with open('2024/04-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines



def step(current_pos: list[int], lines: list[str]) -> list[int]:
    coord = (current_pos[0] * len(lines[0])) + current_pos[1]
    coord += 1
    pos_row = coord // len(lines[0])
    pos_col = coord - (pos_row * len(lines[0]))
    if pos_col == 0:
        pos_col += 1
    if pos_col == len(lines[0]) - 1:
        pos_row += 1
        pos_col = 1
    return [pos_row, pos_col]

def run() -> int:
    lines = readFile()
    lines = [line.strip() for line in lines]

    current_pos = [1, 1]

    total = 0
    while current_pos[0] < len(lines) - 1:

        char = lines[current_pos[0]][current_pos[1]]
        if char != "A":
            current_pos = step(current_pos, lines)
            continue


        top_left = lines[current_pos[0] -1][current_pos[1] -1]
        top_right = lines[current_pos[0] -1][current_pos[1] +1]
        bottom_left = lines[current_pos[0] +1][current_pos[1] -1]
        bottom_right = lines[current_pos[0] +1][current_pos[1] +1]

        # print("found", current_pos)
        # print(top_left, " ", top_right)
        # print(" ", char, " ")
        # print(bottom_left, " ", bottom_right)

        option1 = top_left == "M" and bottom_right == "S" or top_left == "S" and bottom_right == "M"
        option2 = top_right == "M" and bottom_left == "S" or top_right == "S" and bottom_left == "M"

        if option1 and option2:
            total += 1

        current_pos = step(current_pos, lines)

    return total


if __name__ == '__main__':
    check: list[tuple[int, int]] = []


    result = run()


    assert result == 1866, result
    print(result)