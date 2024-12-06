from typing import Dict, List, Tuple

def readFile() -> List[str]:
    with open('src/14-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def getLoad(firstRockRowLoad: int, rockCount: int) -> int:
    res = 0
    for i in range(firstRockRowLoad, firstRockRowLoad - rockCount, -1):
        res += i
    return res

def tilt(rawInput: List[str]) -> List[List[str]]:
    cube = "#"
    rock = "O"
    rowLen = len(rawInput[0])

    totalLoad = 0

    for collumnI in range(rowLen):
        lastCube = -1
        countRockSinceCube = 0
        for rowI in range(len(rawInput)):
            char = rawInput[rowI][collumnI]
            if char == rock:
                countRockSinceCube += 1
            if char == cube:
                totalLoad += getLoad(rowLen - (lastCube + 1), countRockSinceCube)
                lastCube = rowI
                countRockSinceCube = 0
        totalLoad += getLoad(rowLen - (lastCube + 1), countRockSinceCube)
    return totalLoad


rawInput = readFile()
totalLoad = tilt(rawInput)

print("result : " + str(totalLoad)) #107951
