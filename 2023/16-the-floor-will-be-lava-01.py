import time
from typing import Dict, List, Tuple

def readFile() -> List[str]:
    with open('src/16-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> List[str]:
    return rawInput

def outOfBounds(floor, row, column) -> bool:
    return row < 0 or row >= len(floor) or column < 0 or column >= len(floor[0])

def light(floor: List[str]) -> List[List[int]]:
    empty = "."
    mirror1 = "/"
    mirror2 = "\\"
    splitterHor = "-"
    splitterVert = "|"

    directions = {
        "down": [1, 0],
        "up": [-1, 0],
        "left": [0, -1],
        "right": [0, 1],
    }

    regularMoves = [empty, mirror1, mirror2]

    possibleMoves = {
        empty: {
            "down": "down",
            "up": "up",
            "left": "left",
            "right": "right",
        },
        mirror1: {
            "down": "left",
            "up": "right",
            "left": "down",
            "right": "up",
        },
        mirror2: {
            "down": "right",
            "up": "left",
            "left": "up",
            "right": "down",
        },
        mirror2: {
            "down": "right",
            "up": "left",
            "left": "up",
            "right": "down",
        },
        splitterVert: {
            "down": "down",
            "up": "up",
            "left": "down up",
            "right": "down up",
        },
        splitterHor: {
            "down": "right left",
            "up": "right left",
            "left": "left",
            "right": "right",
        },
    }

    nextMoves = [[[0, 0], "right"]]

    lightedFloor = [[0]*len(row) for row in floor  ]
    seen = set()
    while nextMoves:
        currentMove =  nextMoves[0]
        nextMoves = nextMoves[1:]
        if (tuple(currentMove[0]), currentMove[1],) in seen:
            continue
        seen.add((tuple(currentMove[0]), currentMove[1],))
        if outOfBounds(floor, currentMove[0][0], currentMove[0][1]):
            continue
        lightedFloor[currentMove[0][0]][currentMove[0][1]] = 1

        floorTile = floor[currentMove[0][0]][currentMove[0][1]]
        print(currentMove[0], floorTile)
        rawNextMovesFromThisPosition = possibleMoves[floorTile][currentMove[1]]
        nextMovesFromThisPosition = []
        if floorTile in regularMoves:
            nextMovesFromThisPosition = [rawNextMovesFromThisPosition]
        else:
            nextMovesFromThisPosition = rawNextMovesFromThisPosition.split(" ")

        for nxt in nextMovesFromThisPosition:
            newPos = [currentMove[0][0] + directions[nxt][0], currentMove[0][1] + directions[nxt][1]]

            nextMoves.append([newPos, nxt])
    return lightedFloor


rawInput = readFile()
floor = parse(rawInput)
lightedFloor = light(floor)

result = sum(list(map(sum, lightedFloor)))

print("result : " + str(result)) #6361
