from dataclasses import dataclass
from heapq import heappop, heappush
from typing import List, Tuple

@dataclass
class Position():
    pos: Tuple[int, int]
    lastMove: str
    minHeat: int = 0

    def val(self) -> Tuple[int, int]:
        return self.pos

    def __eq__(self, other) -> bool:
        return self.val() == other.val()

    def __lt__(self, other) -> bool:
        return self.val() < other.val()

def readFile() -> List[str]:
    with open('src/17-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> List[str]:
    return rawInput

def outOfBounds(floor, row, column) -> bool:
    return row < 0 or row >= len(floor) or column < 0 or column >= len(floor[0])

def isReverse(lastMove: str, nextMove: str) -> bool:
    return ((lastMove == "down" and nextMove == "up") or
    (lastMove == "up" and nextMove == "down") or
    (lastMove == "left" and nextMove == "right") or
    (lastMove == "right" and nextMove == "left"))


DIRECTIONS = {
    "down": [1, 0],
    "up": [-1, 0],
    "left": [0, -1],
    "right": [0, 1],
}

def dijkstra(floor: List[str], start: Position, goal: Tuple[int, int])  -> int:

    qu = []
    seen = set()
    seen.add((tuple(start.pos), (1,1,), ))

    heappush(qu, (start.minHeat, start,) )

    while qu:

        heapPos = heappop(qu)
        pos: Position = heapPos[1]

        for key, value in DIRECTIONS.items():
            if isReverse(pos.lastMove, key):
                continue
            if key == pos.lastMove:
                continue

            newHeat = pos.minHeat
            for stepSize in range(1, 4):
                off = [value[0] * stepSize, value[1] * stepSize, ]
                newTile = (pos.pos[0] + off[0], pos.pos[1] + off[1],)
                if outOfBounds(floor, newTile[0], newTile[1]):
                    break

                newHeat += int(floor[newTile[0]][newTile[1]])


            for stepSize in range(4, 11):

                off = [value[0] * stepSize, value[1] * stepSize, ]
                newTile = (pos.pos[0] + off[0], pos.pos[1] + off[1],)
                if outOfBounds(floor, newTile[0], newTile[1]):
                    break

                newHeat += int(floor[newTile[0]][newTile[1]])
                seenKey = (newTile, tuple(off),)
                if seenKey in seen:
                    continue
                seen.add(seenKey)

                newPos = Position(pos=newTile, lastMove=key, minHeat=newHeat)

                heappush(qu, (newPos.minHeat, newPos,) )

                if newPos.pos == goal:
                    return newPos.minHeat

    raise Exception("not found")


rawInput = readFile()
floor = parse(rawInput)
start = Position(pos=[0,0], lastMove="")
goal = (len(floor)-1, len(floor[0])-1)
pos = dijkstra(floor, start, goal)
print("result : " + str(pos)) #1367

