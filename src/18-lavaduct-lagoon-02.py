import collections
from dataclasses import dataclass
import time
from typing import Dict, List, Set, Tuple

def readFile() -> List[str]:
    with open('src/18-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

NUM_DIRECTION = "RDLU"

DIRECTIONS = {
    "D": [1, 0],
    "U": [-1, 0],
    "L": [0, -1],
    "R": [0, 1],
}

def parse(rawInput: List[str]) -> Dict[str, str|int]:
    result = []
    for line in rawInput:
        [_, _, color] = line.split(" ")
        color = color[2: -1]
        scale = color[:-1]
        dir = color[-1]
        result.append({
            "off": DIRECTIONS[NUM_DIRECTION[int(dir)]],
            "distance": int(scale, 16),
        })
    return result

def getPoints(diggingInstructions: Dict[str, str|int]) -> List[Tuple[int, int]]:
    result = []
    result.append((0,0,))
    for instruction in diggingInstructions:
        lastRow, lastCol = result[-1]
        rowOff, colOff = instruction["off"]
        point = (lastRow + (rowOff * instruction["distance"]), lastCol + (colOff * instruction["distance"]),)
        result.append(point)
    return result

def getBoundaryPoints(diggingInstructions: Dict[str, str|int]) -> List[Tuple[int, int]]:
    totalBoundary = 0
    for instr in diggingInstructions:
        totalBoundary += instr["distance"]
    return totalBoundary

# https://en.wikipedia.org/wiki/Shoelace_formula
def getShoulaceArea(points: List[Tuple[int, int]]) -> int:
    A = 0
    for i in range(len(points)):
        prevPoint = points[i - 1]
        currPoint = points[i]
        nextpoint = points[(i + 1) % len(points)]
        A += currPoint[0] * (prevPoint[1] - nextpoint[1])

    return abs(A) // 2


# https://en.wikipedia.org/wiki/Pick%27s_theorem
# A = i + (b/2) - 1
# area = interior + (boundary/2) - 1
# interior = area - (b/2) + 1
def getInteriorArea(area, boundary) -> int:
    interior = area - (boundary / 2) + 1
    return int(interior)

rawInput = readFile()
diggingInstructions = parse(rawInput)
points = getPoints(diggingInstructions)
area = getShoulaceArea(points)
totalBoundary = getBoundaryPoints(diggingInstructions)
interior = getInteriorArea(area, totalBoundary)

print("result : " + str(interior + totalBoundary)) #

