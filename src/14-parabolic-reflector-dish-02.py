import time
from typing import Dict, List, Tuple

def readFile() -> List[str]:
    with open('src/14-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> Tuple[Tuple[str]]:
    return tuple([tuple([*line]) for line in rawInput])

def getLoad(field: List[List[str]]) -> int:
    loadAmount = len(field)
    total = 0
    for line in field:
        total += line.count("O") * loadAmount
        loadAmount -= 1
    return total


def tilt(field: List[List[str]]) -> None:
    for collumnI in range(len(field[0])):

        lastFreeSpace = 0
        for rowI in range(len(field)):
            char = field[rowI][collumnI]

            if char == ".":
                lastFreeSpace = min(rowI, lastFreeSpace)

            elif char == "#":
                lastFreeSpace = rowI + 1

            elif char == "O":
                if lastFreeSpace != rowI:
                    field[lastFreeSpace][collumnI], field[rowI][collumnI] = field[rowI][collumnI], field[lastFreeSpace][collumnI]
                lastFreeSpace += 1

def cycle(field: Tuple[Tuple[str]]) -> Tuple[Tuple[str]]:
    def rotate(field):
        return list(map(list, zip(*field[::-1])))

    field = list(map(list, field))
    for _ in range(4):
        tilt(field)
        field = rotate(field)


    return tuple(map(tuple, field))

rawInput = readFile()
field = parse(rawInput)

seen = set()
seenFields = list()
iter = 0
seenFields.append(field)

for _ in range(1_000_000_000):
    iter += 1
    field = cycle(field)

    if field in seen:
        break

    seen.add(field)
    seenFields.append(field)

start = seenFields.index(field)

print("start of cycle : ", start)
print("end of cycle : ", iter)
print("cycle len : ", iter - start)

GOAL = 1_000_000_000

cycleLen = iter - start

cyclePosAtGoal = (GOAL - start) % cycleLen

fieldAtGoal = seenFields[start + cyclePosAtGoal]

totalLoad = getLoad(fieldAtGoal)
print("result : " + str(totalLoad)) #95736
