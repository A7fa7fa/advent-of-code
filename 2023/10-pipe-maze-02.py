from typing import Dict, List, Tuple
import sys

# TODO fix this by iteratetive instead of recursive
print(sys.getrecursionlimit())
sys.setrecursionlimit(50000)
print(sys.getrecursionlimit())


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


def __setNeigh(y, x, extendedMap, pipe) -> None:
    if ouOfBound(x, y, extendedMap):
        return
    extendedMap[y][x] = pipe

def setNeighs(y, x, extendedMap, pipe) -> None:
    posX = x * 2
    posY = y * 2
    extendedMap[posY][posX] = pipe

    neighs = MOVES[pipe]

    if pipe == "|":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "|")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "|")
    elif pipe == "-":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "-")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "-")
    elif pipe == "L":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "|")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "-")
    elif pipe == "J":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "|")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "-")
    elif pipe == "7":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "|")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "-")
    elif pipe == "F":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "|")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "-")
    elif pipe == "S":
        __setNeigh(posY + neighs[0][0], posX + neighs[0][1], extendedMap, "|")
        __setNeigh(posY + neighs[1][0], posX + neighs[1][1], extendedMap, "-")

def expandPipeToExtendedMap(maze, extendedMap) -> None:

    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char in MOVES:
                setNeighs(y, x, extendedMap, char)


def getPipeTiles(maze: List[str],  start: Tuple[int, int])-> Dict[str, str]:
    pipeTiles = dict()
    currentPos = list(start[:])
    lastPos = [-1,-1]
    posChar = ""

    while posChar != "S":
        currentPipe = maze[currentPos[0]][currentPos[1]]
        pipeTiles[toKey(currentPos[1], currentPos[0])] = currentPipe

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

    return pipeTiles

SEPERATOR = "~"
def toKey(x, y) -> str:
    return f"{x}{SEPERATOR}{y}"

def fromKey(key: str) -> List[int]:
    pos = key.split(SEPERATOR)
    return [pos[1], pos[0]]

def isBorder(x, y, maze) -> bool:
    return x == 0 or x == len(maze[0]) - 1 or y == 0 or y == len(maze) -1

def ouOfBound(x,y, maze) -> bool:
    return x < 0 or x >= len(maze[0]) or y < 0 or  y >= len(maze)

def updateMaze(y, x, maze) -> None:
    mazeY = y//2
    mazeX = x//2
    if maze[mazeY][mazeX] == ".":
        maze[mazeY] = maze[mazeY][:mazeX] + "X" + maze[mazeY][mazeX+1:]



def dfs(maze: List[str], visited: Dict[str, bool], x, y, extendedMap) -> int:

    steps = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0],
    ]

    if toKey(x, y) in visited:
        return 0
    visited[toKey(x, y)] = True

    if ouOfBound(x, y, extendedMap):
        return 0
    if extendedMap[y][x] != "0":
        return 0

    updateMaze(y, x, maze)
    extendedMap[y][x] = "1"

    tiles = 1

    for step in steps:
        nextX = x+step[1]
        nextY = y+step[0]
        # if toKey(nextX, nextY) in visited:
        #     tiles += 0
        # else:
        # visited[toKey(nextX, nextY)] = True
        tiles += dfs(maze, visited, nextX, nextY, extendedMap)

    return tiles

def tilesAccessabelFromBorder(maze: List[str], extendedMap) -> int:
    visited = dict()
    accessableTiles = 0
    for y, row in enumerate(extendedMap):
        for x, char in enumerate(row):
            if not isBorder(x, y, extendedMap):
                continue
            if toKey(x, y) in visited:
                continue
            if char == "0":
                accessableTiles += dfs(maze, visited, x, y, extendedMap)

    return accessableTiles

def removeUnconnectedPipeTiles(maze, pipeTiles: Dict[str, str]) -> None:
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if toKey(x, y) in pipeTiles:
                continue
            maze[y] = maze[y][:x] + "." + maze[y][x+1:]


lines = readFile()
maze = parseRawInput(lines)
start = getStartingPosition(maze)

extendedMap = [list("0"*((len(maze[0])*2)-1)) for _ in range((len(maze)*2)-1)]

pipeTiles = getPipeTiles(maze, start)
removeUnconnectedPipeTiles(maze, pipeTiles)
expandPipeToExtendedMap(maze, extendedMap)

# print("Cleaned extended")
# for row in extendedMap:
#     print("".join(row))

accessableTiles = tilesAccessabelFromBorder(maze, extendedMap)

# print("\nComputed extended")
# for row in extendedMap:
#     print("".join(row))

print("\nComputed maze")
res = 0
for row in maze:
    res += row.count(".")
    print(row, row.count("."))

print("result : " + str(res) ) # 451
