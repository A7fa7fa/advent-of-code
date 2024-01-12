import collections
import sys
from typing import Dict, List, Set, Tuple
sys.setrecursionlimit(50000000)


def readFile() -> List[str]:
    with open('src/21-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def getStartingPosition(rawInput: List[str]) -> Tuple[int, int]:
    for rowI, row in enumerate(rawInput):
        for collI, _ in enumerate(row):
            if rawInput[rowI][collI] == "S":
                return (rowI, collI,)

rawInput = readFile()
start = getStartingPosition(rawInput)

assert len(rawInput) == len(rawInput[0])
size = len(rawInput)
assert start[0] == start[1] == size // 2

steps = 26501365

assert steps % size == size // 2

print(f"multi = {steps // size}")
print(f"{steps = }")

gardenWidth = steps // size - 1
print(f"{gardenWidth = }")

MAX_STEP = size
print(f"{MAX_STEP = }")

ROCK = "#"

seen: Dict[Tuple, int] = dict()

evenStepReach = set()

def outOfBounds(garden, pos) -> bool:
    return pos[0] < 0 or pos[0] >= len(garden) or pos[1] < 0 or pos[1] >= len(garden[1])

def rowWrap(garden, rowI) -> int:
    rowI = rowI % len(garden)

    if 0 <= rowI < len(garden):
        return rowI
    if rowI < 0:
        return len(garden) - 1
    else:
        return 0

def colWrap(garden, collI) -> int:
    collI = collI % len(garden[0])
    if 0 <= collI < len(garden[0]):
        return collI
    if collI < 0:
        return len(garden[0]) - 1
    else:
        return 0

def dfs(garden, lastPos, newPos, path: List[List[int]], multiplier: List[int]):
    if lastPos == newPos:
        return

    if outOfBounds(garden, newPos):
        return

    if garden[newPos[0]][newPos[1]] == ROCK:
        return

    actualPos = (newPos[0] + (len(garden) * multiplier[0]), newPos[1] + (len(garden[0]) * multiplier[1]),)

    if len(path) % 2 == 0:
        evenStepReach.add(actualPos)

    if len(path) == MAX_STEP:
        return

    if actualPos in seen and len(path) >= seen[actualPos]:
        return

    seen[actualPos] = len(path)

    STEPS = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    for step in STEPS:
        nextStep = (newPos[0] + step[0], newPos[1] + step[1],)
        newMulti = multiplier[:]
        if outOfBounds(garden, nextStep):
            newRow = rowWrap(garden, nextStep[0])
            newCol = colWrap(garden, nextStep[1])
            if nextStep[0] < newRow:
                newMulti[0] -= 1
            if nextStep[0] > newRow:
                newMulti[0] += 1
            if nextStep[1] < newCol:
                newMulti[1] -= 1
            if nextStep[1] > newCol:
                newMulti[1] += 1
            nextStep = (newRow, newCol,)
        path.append(nextStep)
        dfs(garden, actualPos, nextStep, path, newMulti)
        path.pop()

start = getStartingPosition(rawInput)

dfs(rawInput, (-1, -1,), start, [], [0,0])

res = len(evenStepReach)
print("result : " + str(res)) #

# TODO finish day 21
