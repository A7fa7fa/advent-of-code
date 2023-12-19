import collections
from dataclasses import dataclass
import time
from typing import Dict, List, Set, Tuple

def readFile() -> List[str]:
    with open('src/18-input-debug.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> List[str]:
    result = []
    for line in rawInput:
        [direction, length, color] = line.split(" ")
        result.append({
            "direction": direction,
            "length": int(length),
            "color": color.replace("(", "").replace(")", "")
        })
    return result

def outOfBounds(floor, row, column) -> bool:
    return row < 0 or row >= len(floor) or column < 0 or column >= len(floor[0])


DIRECTIONS = {
    "D": [1, 0],
    "U": [-1, 0],
    "L": [0, -1],
    "R": [0, 1],
}

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


def digTrench(diggingInstructions: Dict[str, str|int], floor: List[List[str]], start: List[int]) -> None:
    for instruction in diggingInstructions:
        floor[start[0]][start[1]] = "#"
        for i in range(instruction["length"]):
            off = DIRECTIONS[instruction["direction"]]
            start[0] += off[0]
            start[1] += off[1]
            floor[start[0]][start[1]] = "#"

def bfs(floor: List[List[str]], pos: List[int]) -> None:
    positions = []
    positions.append(pos)
    while positions:
        pos = positions[0]
        positions = positions[1:]
        for key, step in DIRECTIONS.items():
            newPos = [pos[0] + step[0], pos[1] + step[1]]
            if outOfBounds(floor, *newPos):
                continue
            if floor[newPos[0]][newPos[1]] == "#":
                continue
            if floor[newPos[0]][newPos[1]] == "0":
                continue
            if floor[newPos[0]][newPos[1]] == ".":
                floor[newPos[0]][newPos[1]] = "0"
                positions.append(newPos[:])

def markOutsideFloor(floor: List[List[str]]) -> None:

    for c, char in enumerate(floor[0]):
        if char == ".":
            bfs(floor, [0, c] )
    for c, char in enumerate(floor[-1]):
        if char == ".":
            bfs(floor, [len(floor) - 1, c] )

    for r, row in enumerate(floor):
        if row[0] == ".":
            bfs(floor, [r, 0] )

    for r, row in enumerate(floor):
        if row[-1] == ".":
            bfs(floor, [r, len(floor[0]) - 1] )


def interiorSize(floor: List[List[str]]) -> int:
    return sum(list(map(lambda row: row.count("#") + row.count("."), floor)))


rawInput = readFile()
diggingInstructions = parse(rawInput)
[floorSizeStart, floorSizeEnd] = size(diggingInstructions)

rows = floorSizeEnd[0] - floorSizeStart[0] + 1
collumns = floorSizeEnd[1] - floorSizeStart[1] + 1

floor = [["."]*collumns for _ in range(rows)]

digTrench(diggingInstructions, floor, [abs(floorSizeStart[0]), abs(floorSizeStart[1])])
markOutsideFloor(floor)

result = interiorSize(floor)

print("result : " + str(result)) #

