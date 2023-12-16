import sys
import time
from typing import Dict, List, Tuple

sys.setrecursionlimit(50000)

def readFile() -> List[str]:
    with open('src/16-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> List[str]:
    return rawInput

def outOfBounds(floor, row, column) -> bool:
    return row < 0 or row >= len(floor) or column < 0 or column >= len(floor[0])

empty = "."
mirror1 = "/"
mirror2 = "\\"
splitterHor = "-"
splitterVert = "|"
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
directions = {
    "down": [1, 0],
    "up": [-1, 0],
    "left": [0, -1],
    "right": [0, 1],
}

regularMoves = [empty, mirror1, mirror2]

def light(floor: List[str]) -> List[List[int]]:
    lights = []
    # top
    for collI in range(len(floor[0])):
        startPos = [0, collI]
        startMove = "down"

        seen = set()
        floorLight = set()

        lights.append(traverse(startPos, startMove, seen, floorLight))
    # down
    for collI in range(len(floor[0])):
        startPos = [len(floor) - 1, collI]
        startMove = "up"

        seen = set()
        floorLight = set()

        lights.append(traverse(startPos, startMove, seen, floorLight))

    # left
    for rowI in range(len(floor)):
        startPos = [rowI, 0]
        startMove = "right"

        seen = set()
        floorLight = set()

        lights.append(traverse(startPos, startMove, seen, floorLight))

    # right
    for rowI in range(len(floor)):
        startPos = [rowI, len(floor[0])-1]
        startMove = "left"

        seen = set()
        floorLight = set()

        lights.append(traverse(startPos, startMove, seen, floorLight))
    return lights



globalCache = dict()

def buildKey(pos: List[int], move: str) -> tuple[tuple[int, int], str]:
     return (tuple(pos), move,)

def traverse(pos, move, seen, floorLight) -> int:
    key = buildKey(pos, move)
    # if globalCache.get(key, None):
    #     return globalCache[key]
    if outOfBounds(floor, pos[0], pos[1]):
        return 0
    if key in seen:
        return 0
    seen.add(key)

    totalTileLight = 0
    if tuple(pos) not in floorLight:
        totalTileLight = +1
    floorLight.add(tuple(pos))

    floorTile = floor[pos[0]][pos[1]]

    rawNextMovesFromThisPosition = possibleMoves[floorTile][move]
    nextMovesFromThisPosition = []
    if floorTile in regularMoves:
        nextMovesFromThisPosition = [rawNextMovesFromThisPosition]
    else:
        nextMovesFromThisPosition = rawNextMovesFromThisPosition.split(" ")

    for nxt in nextMovesFromThisPosition:
        newPos = [pos[0] + directions[nxt][0], pos[1] + directions[nxt][1]]
        totalTileLight += traverse(newPos, nxt, seen, floorLight)

    globalCache[key] = totalTileLight
    return totalTileLight


rawInput = readFile()
floor = parse(rawInput)
lightedTiles = light(floor)

print("result : " + str(max(lightedTiles))) #6701
