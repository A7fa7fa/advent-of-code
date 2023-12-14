from typing import Dict, List, Tuple


def readFile() -> List[str]:
    with open('src/13-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parsInput(rawInput: List[str]) -> List[List[str]]:
    result = []
    field = []
    for line in rawInput:
        if line == "":
            result.append(field[:])
            field = []
            continue
        field.append(line)

    result.append(field)
    return result

def countDifferences(line1, line2) -> int:
    differCount = 0
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            differCount += 1
    return differCount

def mirror(field: List[str]) -> int:
    rows = len(field)

    for i in range(0, rows-1):
        differences = 0
        size = 0

        while size < rows:
            lower = i - size
            higher = i + 1 + size
            size += 1

            if lower < 0 or higher >= rows:
                break

            differences += countDifferences(field[lower], field[higher])

        if differences == 1:
            return i + 1
    return -1


def getRefelctions(fields: List[List[str]]) -> int:

    total = 0

    for field in fields:
        horizontal = mirror(field) * 100
        vertical = mirror(list(zip(*field)))

        total += max(horizontal, vertical)


    return total

rawInput = readFile()
fields = parsInput(rawInput)
result = getRefelctions(fields)



print("result : " + str(result)) #30449
