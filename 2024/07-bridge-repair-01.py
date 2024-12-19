
from dataclasses import dataclass
from typing import List


def readFile(file_name: str) -> List[str]:
    with open(f'2024/{file_name}') as f:
        lines : List[str] = f.readlines()
        return lines

@dataclass
class Equation:
    result: int
    values: list[int]
    solvable: bool = False


def mult(val1:int, val2:int) -> int:
    return val1 * val2

def add(val1:int, val2:int) -> int:
    return val1 + val2

def apply(equa: Equation, start:int = 0, res:int = 0):
    i = start
    added, multiplied = 0,0
    while i < len(equa.values):
        added = add(res, equa.values[i])
        apply(equa, i+1, added)

        multiplied = mult(res, equa.values[i])
        apply(equa, i+1, multiplied)
        i += 1


    if added == equa.result or multiplied == equa.result:
        equa.solvable = True


def run(file_name: str) -> int:
    lines = readFile(file_name)
    lines = [line.strip() for line in lines]

    equas: list[Equation] = []
    for line in lines:
        res = int(line.split(":")[0].strip(""))
        val = list(map(int, line.split(":")[1].strip(" ").split(" ")))
        equas.append(Equation(res, val))

    total_solvable = 0
    for equa in equas:
        apply(equa)
        if equa.solvable:
            total_solvable += equa.result

    return total_solvable



if __name__ == '__main__':

    result = run("07-input-test.txt")
    assert result == 3749, result
    print("test", result)

    result = run("07-input.txt")
    assert result == 1430271835320, result
    print("result", result)
