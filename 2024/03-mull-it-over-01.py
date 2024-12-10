
from typing import List


def readFile() -> List[str]:
    with open('2024/03-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def process(text: str, res: list[list[str]]) -> int:
    start_lit = "mul("

    next_closing_bracket =  text.find(")")
    if next_closing_bracket == -1:
        return len(start_lit)

    next_comma =  text.find(",")

    if next_comma == -1:
        return len(start_lit)

    if next_comma > next_closing_bracket:
        return len(start_lit)

    params = text[len(start_lit):next_closing_bracket].split(",")
    if len(params) != 2:
        return len(start_lit)

    if params[0].isdigit() and len(params[0]) <= 3 and params[1].isdigit() and len(params[1]) <= 3:
        res.append([params[0], params[1], "0"])
        return next_closing_bracket

    return len(start_lit)


def run() -> int:
    lines = readFile()

    full_text = "".join(lines)

    result: list[list[str]] = []

    i = 0
    while i < len(full_text):
        next_pos = full_text[i:].find("mul(")
        if next_pos == -1:
            break
        skip = process(full_text[i+next_pos:], result)
        result[-1][2] = str(i+next_pos)
        i += skip + next_pos

    total = 0
    for first, second, _ in result:
        total += (int(first) * int(second))

    return total




if __name__ == '__main__':
    result = run()
    assert result == 155955228, result
    print(result)