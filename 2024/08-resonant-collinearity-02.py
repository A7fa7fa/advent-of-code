
def read_file(file_name: str) -> list[str]:
    file_path = f'2024/{file_name}'
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines : list[str] = f.readlines()
            return lines

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.")
    except OSError as e:
        print(f"Error: An OS error occurred: {e}")
    return []

def out_of_bound(x: int, y: int, last_x: int, last_y: int) -> bool:
    return x < 0 or x > last_x or y < 0 or  y > last_y


def run(file_name: str) -> int:
    lines = read_file(file_name)
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


    last_x, last_y = len(lines) - 1, len(lines[0]) - 1

    valid_antinodes: set[tuple[int, int]] = set()

    for antenna_type in antennas.keys():
        if len(antennas[antenna_type]) == 1:
            continue
        valid_antinodes.update(set(antennas[antenna_type]))
        for antenna in antennas[antenna_type]:
            for other in antennas[antenna_type]:
                if antenna == other:
                    continue

                diff = (antenna[0] - other[0], antenna[1] - other[1])
                new_pos = (antenna[0] + diff[0], antenna[1] + diff[1])

                while not out_of_bound(new_pos[0], new_pos[1], last_x, last_y):
                    valid_antinodes.add(new_pos)
                    new_pos = (new_pos[0] + diff[0], new_pos[1] + diff[1])


    for x, y in valid_antinodes:
        lines[x] = lines[x][:y] + "#" + lines[x][y+1:]

    for line in lines:
        print(line)

    return len(valid_antinodes)



if __name__ == '__main__':

    result = run("08-input-test.txt")
    assert result == 34, result
    print("test", result)

    result = run("08-input.txt")
    assert result == 1235, result
    print("result", result)
