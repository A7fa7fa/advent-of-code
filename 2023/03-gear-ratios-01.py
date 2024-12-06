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

def validateFields(validMap: List[List[bool]], rowNum: int, charNum: int) -> None:

    minRowNum = max(0, rowNum - 1)
    maxRowNum = min(len(validMap) - 1, rowNum + 1)

    minCharNum = max(0, charNum - 1)
    maxCharNum = min(len(validMap[0]) - 1, charNum + 1)

    validMap[minRowNum][minCharNum] = True
    validMap[minRowNum][charNum] = True
    validMap[minRowNum][maxCharNum] = True

    validMap[rowNum][minCharNum] = True
    validMap[rowNum][charNum] = True
    validMap[rowNum][maxCharNum] = True

    validMap[maxRowNum][minCharNum] = True
    validMap[maxRowNum][charNum] = True
    validMap[maxRowNum][maxCharNum] = True


def createValidMap(input: List[List[str]]) -> List[List[bool]]:
    validMap = [[False for _ in range(len(input[0]))] for _ in range(len(input))]

    for rowNum, line in enumerate(input):
        for charNum, char in enumerate(line):
            isSymbol = not char.isdigit() and char != "."
            if isSymbol:
                validateFields(validMap, rowNum, charNum)
    return validMap


def extractValidPartNumbers(input: List[List[str]], validMap: List[List[bool]]) -> List[int]:
    validParts = []
    for rowNum, line in enumerate(input):
        digits = ""
        isValidPart = False
        for charNum, char in enumerate(line):
            if char.isdigit():
                digits += str(char)
                if not isValidPart:
                    isValidPart = validMap[rowNum][charNum]
            else:
                if isValidPart:
                    validParts.append(int(digits))
                digits = ""
                isValidPart = False
        if isValidPart:
            validParts.append(int(digits))
    return validParts




lines = readFile()
input = prepareInput(lines)
validMap = createValidMap(input)
partNumberSum = extractValidPartNumbers(input, validMap)

print(sum(partNumberSum))