from typing import Dict, Generator, List, Tuple

def readFile() -> List[str]:
    with open('src/11-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def __linesWithoutGalaxies(universe: List[str]) -> List[int]:
    lineIndex = []
    for i, row in enumerate(universe):
        if "#" not in row:
            lineIndex.append(i)
    return lineIndex

def rowsWithoutGalaxies(universe: List[str]) -> List[int]:
    return __linesWithoutGalaxies(universe)

def collumnsWithoutGalaxies(universe: List[str]) -> List[int]:
    return __linesWithoutGalaxies(zip(*universe))

def getGalaxies(universe: List[str]) -> List[Tuple[int, int]]:
    galaxies = []
    for y, line in enumerate(universe):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((y, x,))
    return galaxies

def calculateTotalDistance(galaxies: List[Tuple[int, int]], emptyRows: List[int], emptyCollumns: List[int]) -> int:
    totalDistance = 0
    scale = 1_000_000
    for i, galaxy in enumerate(galaxies):
        for other in galaxies[i+1:]:
            for row in range(min(galaxy[0], other[0]), max(galaxy[0], other[0])):
                if row in emptyRows:
                    totalDistance += scale
                else:
                    totalDistance += 1
            for collumn in range(min(galaxy[1], other[1]), max(galaxy[1], other[1])):
                if collumn in emptyCollumns:
                    totalDistance += scale
                else:
                    totalDistance += 1
    return totalDistance



universe = readFile()
emptyRows = rowsWithoutGalaxies(universe)
emptyCollumns = collumnsWithoutGalaxies(universe)
galaxies = getGalaxies(universe)

distance = calculateTotalDistance(galaxies, emptyRows, emptyCollumns)


print("result : " + str(distance)) #447744640566
