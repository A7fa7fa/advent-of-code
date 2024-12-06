import collections
from typing import Dict, List, Set, Tuple


def readFile() -> List[str]:
    with open('src/21-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def getStartingPosition(rawInput: List[str]) -> Tuple[int, int]:
    for rowI, row in enumerate(rawInput):
        for collI, _ in enumerate(row):
            if rawInput[rowI][collI] == "S":
                return (rowI, collI,)



ROCK = "#"
MAX_STEP = 64
seen: Dict[Tuple, int] = dict()

evenStepReach = set()

def outOfBounds(garden, pos) -> bool:
    return pos[0] < 0 or pos[0] >= len(garden) or pos[1] < 0 or pos[1] >= len(garden[1])

def dfs(garden, lastPos, newPos, path: List[List[int]]):
    if lastPos == newPos:
        return

    if outOfBounds(garden, newPos):
        return

    if garden[newPos[0]][newPos[1]] == ROCK:
        return

    if len(path) % 2 == 0:
        evenStepReach.add(newPos)

    if len(path) == MAX_STEP:
        return

    if newPos in seen and len(path) >= seen[newPos]:
        return

    seen[newPos] = len(path)

    STEPS = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    for step in STEPS:
        nextStep = (newPos[0] + step[0], newPos[1] + step[1],)
        path.append(nextStep)
        dfs(garden, newPos, nextStep, path)
        path.pop()

rawInput = readFile()
start = getStartingPosition(rawInput)

dfs(rawInput, (-1, -1,), start, [])

res = len(evenStepReach)
print("result : " + str(res)) #3660
