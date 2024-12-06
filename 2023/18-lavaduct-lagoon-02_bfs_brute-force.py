import collections
from dataclasses import dataclass
import time
from typing import Dict, List, Set, Tuple

def readFile() -> List[str]:
    with open('src/18-input-debug.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

NUM_DIRECTION = ["R", "D", "L", "U"]

DIRECTIONS = {
    "D": [1, 0],
    "U": [-1, 0],
    "L": [0, -1],
    "R": [0, 1],
}
def parse(rawInput: List[str]) -> List[str]:
    result = []
    for line in rawInput:
        [direction, length, color] = line.split(" ")
        result.append({
            "direction": NUM_DIRECTION[int(color.replace("(", "").replace(")", "")[-1])],
            "off": DIRECTIONS[NUM_DIRECTION[int(color.replace("(", "").replace(")", "")[-1])]],
            "length": int(color.replace("(", "").replace(")", "")[1:-1], 16),
            "color": color.replace("(", "").replace(")", ""),
            "start": -1,
            "end": -1,
        })
    return result

def outOfBounds(floor, row, column) -> bool:
    return row < 0 or row >= len(floor) or column < 0 or column >= len(floor[0])



def getDelta(direction: str, length: int) -> Tuple[int, int]:
        direction = DIRECTIONS[direction]
        return (direction[0] * length, direction[1] * length)


def size(diggingInstructions: Dict[str, str|int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    maxRow = 0
    maxColumn = 0
    minRow = 0
    minColumn = 0
    curr = [0, 0]
    for instruction in diggingInstructions:
        off = getDelta(instruction["direction"], instruction["length"])
        curr[0] += off[0]
        curr[1] += off[1]
        maxRow = max(curr[0], maxRow)
        maxColumn = max(curr[1], maxColumn)
        minRow = min(curr[0], minRow)
        minColumn =min(curr[1], minColumn)

    return ((minRow, minColumn,), (maxRow, maxColumn,),)


def digTrench(diggingInstructions: Dict[str, str|int], start: List[int]) -> None:
    for instruction in diggingInstructions:
        instruction["start"] = tuple(start)
        off = DIRECTIONS[instruction["direction"]]
        end = [start[0] + (off[0] * instruction["length"]), start[1] + (off[1] * instruction["length"])]
        instruction["end"] = tuple(end)
        start = end

def inRange(start, r, point) -> bool:
    pass

def isOnTrenchLine(diggingInstructions: Dict[str, str|int], point) -> bool:
    for instruction in diggingInstructions:
        if instruction["direction"] in "RL":
            if instruction["start"][0] == point[0] and min(instruction["start"][1],instruction["end"][1]) <= point[1] <= max(instruction["start"][1],instruction["end"][1]):
                return True
        if instruction["direction"] in "UD":
            if instruction["start"][1] == point[1] and min(instruction["start"][0],instruction["end"][0]) <= point[0] <= max(instruction["start"][0],instruction["end"][0]):
                return True
    return False

def bfs(diggingInstructions: Dict[str, str|int], pos: List[int], boundary: Tuple[int, int], seen: Set[Tuple[int, int]]) -> None:
    positions = []
    positions.append(pos)
    total = 0
    while positions:
        pos = positions.pop()
        total += 1
        for key, step in DIRECTIONS.items():
            newPos = [pos[0] + step[0], pos[1] + step[1]]
            if tuple(newPos) in seen:
                continue
            seen.add(tuple(newPos))
            if newPos[0] < 0 or newPos[0] >= boundary[0] or newPos[1] < 0 or newPos[1] >= boundary[1]:
                continue
            if isOnTrenchLine(diggingInstructions, newPos):
                continue
            positions.append(newPos[:])
    return total


def totalOutsideFloor(rows: int, collumns: int, diggingInstructions: Dict[str, str|int]) -> None:
    seen = set()
    totalOutside = 0
    for c in range(collumns):
        if (0, c,) in seen:
            continue
        seen.add((0, c,))
        if not isOnTrenchLine(diggingInstructions, [0, c]):
            totalOutside += bfs(diggingInstructions, [0, c], (rows, collumns,), seen )

    for c in range(collumns):
        if (rows - 1, c,) in seen:
            continue
        seen.add((rows - 1, c,))
        if not isOnTrenchLine(diggingInstructions, [rows - 1, c]):
            totalOutside += bfs(diggingInstructions, [rows - 1, c], (rows, collumns,), seen)

    for r in range(rows):
        if (r, 0,) in seen:
            continue
        seen.add((r, 0,) )
        if not isOnTrenchLine(diggingInstructions, [r, 0,]):
            totalOutside += bfs(diggingInstructions, [r, 0,], (rows, collumns,), seen)

    for r in range(rows):
        if ( r, collumns - 1,) in seen:
            continue
        seen.add(( r, collumns - 1,) )
        if not isOnTrenchLine(diggingInstructions, [ r,collumns - 1]):
            totalOutside += bfs(diggingInstructions, [ r, collumns - 1], (rows, collumns,), seen)
    return totalOutside


rawInput = readFile()
diggingInstructions = parse(rawInput)
[floorSizeStart, floorSizeEnd] = size(diggingInstructions)

rows = floorSizeEnd[0] - floorSizeStart[0] + 1
collumns = floorSizeEnd[1] - floorSizeStart[1] + 1

digTrench(diggingInstructions, [abs(floorSizeStart[0]), abs(floorSizeStart[1])])

totalOutside = totalOutsideFloor(rows, collumns, diggingInstructions)

print("result : " + str((rows * collumns) - totalOutside)) #
