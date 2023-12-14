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

def mirror(field: List[str]) -> int:
    rows = len(field)

    for i in range(0, rows-1):
        mirrors = True

        size = 0

        while size < rows:
            lower = i - size
            higher = i + 1 + size
            size += 1
            if lower < 0 or higher >= rows:
                break

            if field[lower] != field[higher]:
                mirrors = False
                break


        if mirrors:
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



print("result : " + str(result)) #37113
