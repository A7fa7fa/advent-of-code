
from dataclasses import dataclass, field
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
    operators: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.result} = {' '.join(self.operators).strip('+ ')}"


def mult(val1:int | None, val2:int) -> int:
    if val1 is None:
        return val2
    return val1 * val2

def add(val1:int | None, val2:int) -> int:
    if val1 is None:
        return val2
    return val1 + val2

def combine(val1:int | None, val2:int) -> int:
    if val1 is None:
        return val2
    return int(str(val1) + str(val2))

def apply_iterative(equation: Equation):
    from itertools import product

    # Generate all operator combinations
    ops = ["+", "*", "||"]
    for op_combination in product(ops, repeat=len(equation.values) - 1):
        res = equation.values[0]
        operators: list[str] = []
        operators.append(f"+ {equation.values[0]}")
        for i, op in enumerate(op_combination):
            next_value = equation.values[i + 1]
            if op == "+":
                res = add(res, next_value)
            elif op == "*":
                res = mult(res, next_value)
            elif op == "||":
                res = combine(res, next_value)
            operators.append(f"{op} {next_value}")

        if res == equation.result:
            equation.solvable = True
            equation.operators = operators[:]
            return


def validated(equ: Equation):
    total = 0
    for value in equ.operators:
        if value.startswith("+"):
            total = add(total, int(value.split(" ")[1]))
        elif value.startswith("*"):
            total = mult(total, int(value.split(" ")[1]))
        elif value.startswith("||"):
            total = combine(total, int(value.split(" ")[1]))
    assert total == equ.result
    return total


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
        apply_iterative(equa)
        if equa.solvable:
            total_solvable += validated(equa)
            print(equa)
        else:
            print("NOT")

    return total_solvable



if __name__ == '__main__':

    test_result = run("07-input-test.txt")
    assert test_result == 11387, test_result
    print("test", test_result)

    result = run("07-input.txt")
    assert result == 456565678667482, result # this is too high
    print("result", result)
