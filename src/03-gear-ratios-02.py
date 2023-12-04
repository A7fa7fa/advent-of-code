import collections
from typing import List


def readFile() -> List[str]:
    with open('src/03-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def prepareInput(rawInput: List[str]) -> List[List[str]]:
    input = []

    for line in rawInput:
        newLine = []
        for char in line.strip():
            newLine.append(char)
        input.append(newLine)

    return input

def setGearFields(validMap: List[List[bool]], rowNum: int, charNum: int) -> None:
    gear = [rowNum, charNum]
    minRowNum = max(0, rowNum - 1)
    maxRowNum = min(len(validMap) - 1, rowNum + 1)

    minCharNum = max(0, charNum - 1)
    maxCharNum = min(len(validMap[0]) - 1, charNum + 1)

    validMap[minRowNum][minCharNum].append(gear)
    validMap[minRowNum][charNum].append(gear)
    validMap[minRowNum][maxCharNum].append(gear)

    validMap[rowNum][minCharNum].append(gear)
    validMap[rowNum][charNum].append(gear)
    validMap[rowNum][maxCharNum].append(gear)

    validMap[maxRowNum][minCharNum].append(gear)
    validMap[maxRowNum][charNum].append(gear)
    validMap[maxRowNum][maxCharNum].append(gear)


def createGearMap(input: List[List[str]]) -> List[List[bool]]:
    validMap = [[[] for _ in range(len(input[0]))] for _ in range(len(input))]

    for rowNum, line in enumerate(input):
        for charNum, char in enumerate(line):
            isGear = char == "*"
            if isGear:
                setGearFields(validMap, rowNum, charNum)
    return validMap


def extractPartnumbersForGearPosition(input: List[List[str]], validMap: List[List[bool]]) -> dict[str, List[int]]:
    gears = collections.defaultdict(list)
    for rowNum, line in enumerate(input):
        digits = ""
        gearpos = set()
        for charNum, char in enumerate(line):
            if char.isdigit():
                digits += str(char)
                if len(validMap[rowNum][charNum]) >= 0:
                    for g in validMap[rowNum][charNum]:
                        gearpos.add(tuple(g))
            else:
                if len(gearpos) > 0:
                    for gear in gearpos:
                        gears[f"{gear[0]}_{gear[1]}"].append(int(digits))
                digits = ""
                gearpos = set()
        if len(gearpos) > 0:
            for gear in gearpos:
                gears[f"{gear[0]}_{gear[1]}"].append(int(digits))
    return gears

def sumAllGearRatio(gearParts: dict[str, List[int]]) -> int:
    rationSum = 0
    for parts in gearParts.values():
        if len(parts) == 2:
            rationSum += (parts[0] * parts[1])
    return rationSum



lines = readFile()
input = prepareInput(lines)
gearMap = createGearMap(input)

gearParts = extractPartnumbersForGearPosition(input, gearMap)

res = sumAllGearRatio(gearParts)

print(res)