
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

    return len(start_lit)-1


def run() -> int:
    lines = readFile()

    full_text = "".join(lines)

    result: list[list[str]] = []

    i = 0
    is_do = True
    out_of_bound = len(full_text) + 1
    while i < len(full_text):
        next_do = full_text[i:].find("do()")
        next_dont = full_text[i:].find("don't()")
        next_mul = full_text[i:].find("mul(")
        if next_mul == -1:
            break
        if next_do == -1:
            next_do = out_of_bound
        if next_dont == -1:
            next_dont = out_of_bound

        if next_dont < next_mul and next_dont < next_do: # next flag is dont
            is_do = False
        if next_do < next_mul and next_do < next_dont:  # next flag is do
            is_do = True

        if next_do < next_mul or next_dont < next_mul: # skip to next flag
            i += min(next_do, next_dont) + 1
            continue

        if is_do:
            skip = process(full_text[i+next_mul:], result)
            result[-1][2] = str(i+next_mul)
            i += skip + next_mul
        else:
            i += 1

    total = 0
    for first, second, _ in result:
        total += (int(first) * int(second))

    return total




if __name__ == '__main__':
    result = run()
    print(result) # 100_189_366

