from typing import Dict, Generator, List, Tuple
from unittest import result


def readFile() -> List[str]:
    with open('src/10-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> List[str]:
    result = []

    for line in rawInput:
        result.append(line.strip())
    return result

def getStartingPosition(maze: List[str]) -> Tuple[int, int]:
    for y, rowNum in enumerate(maze):
        for x, char in enumerate(rowNum):
            if char == "S":
                return (y, x,)

MOVES = {
    "|": [(-1 , 0,), (1, 0,)],
    "-": [(0 , -1,), (0, 1,)],
    "L": [(-1, 0,), (0, 1,)],
    "J": [(-1, 0,), (0, -1,)],
    "7": [(1, 0,), (0, -1,)],
    "F": [(1, 0,), (0, 1,)],
    "S": [(1, 0,), (0, 1,)],
}

def step(pos, move) -> Tuple[int, int]:
    return (pos[0] + move[0], pos[1] + move[1])


def followPipe(maze: List[str],  start: Tuple[int, int])-> int:
    currentPos = list(start[:])
    lastPos = [-1,-1]
    posChar = ""
    pipeLength = 0

    while posChar != "S":
        currentPipe = maze[currentPos[0]][currentPos[1]]
        nextMoves = MOVES[currentPipe]

        possibleNextPosition1 = step(currentPos, nextMoves[0])
        possibleNextPosition2 = step(currentPos, nextMoves[1])

        if possibleNextPosition1[0] == lastPos[0] and possibleNextPosition1[1] == lastPos[1]:
            lastPos = currentPos[:]
            currentPos = possibleNextPosition2[:]
        else:
            lastPos = currentPos[:]
            currentPos = possibleNextPosition1[:]

        posChar = maze[currentPos[0]][currentPos[1]]
        print(currentPipe, posChar)
        pipeLength += 1

    return pipeLength


lines = readFile()
maze = parseRawInput(lines)
start = getStartingPosition(maze)
pipeLength = followPipe(maze, start)

print("result : " + str(pipeLength//2)) #6838
