
def readFile(file_name: str) -> list[str]:
    with open(f'2024/{file_name}') as f:
        lines : list[str] = f.readlines()
        return lines

def out_of_bound(x: int, y: int, last_x: int, last_y: int) -> bool:
    return x < 0 or x > last_x or y < 0 or  y > last_y


def run(file_name: str) -> int:
    lines = readFile(file_name)
    lines = [line.strip() for line in lines]

    antennas: dict[str, list[tuple[int, int]]] = dict()

    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == ".":
                continue
            if char in antennas:
                antennas[char].append((r, c))
            else:
                antennas[char] = [(r, c)]

    print(antennas)

    last_x, last_y = len(lines) - 1, len(lines[0]) - 1

    valid_antennas: set[tuple[int, int]] = set()

    for antenna_type in antennas.keys():
        for antenna in antennas[antenna_type]:
            for other in antennas[antenna_type]:
                if antenna == other:
                    continue

                diff = (antenna[0] - other[0], antenna[1] - other[1])

                new_pos = (antenna[0] + diff[0], antenna[1] + diff[1])
                if out_of_bound(new_pos[0], new_pos[1], last_x, last_y):
                    continue
                valid_antennas.add(new_pos)



    return len(valid_antennas)



if __name__ == '__main__':

    result = run("08-input-test.txt")
    assert result == 14, result
    print("test", result)

    result = run("08-input.txt")
    assert result == 392, result
    print("result", result)
