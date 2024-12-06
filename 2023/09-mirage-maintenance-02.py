from typing import Dict, Generator, List
from unittest import result


def readFile() -> List[str]:
    with open('src/09-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> List[List[int]]:
    result = []

    for line in rawInput:
        result.append([int(i) for i in line.strip().split(" ")])
    return result

def reduce(data: List[List[int]]) -> Generator[List[List[int]], None, None]:

    for line in data:
        res = []
        res.append(line[:])
        while True:
            newLineLen = len(res[-1])
            temp = []
            allZero = True
            for i in range(1, newLineLen):
                diff = res[-1][i] - res[-1][i-1]
                if diff != 0:
                    allZero = False
                temp.append(diff)
            res.append(temp)
            if allZero:
                break
        yield res


def extrapolateStart(data: List[List[int]]) -> int:
    lastExtrapolatedValue = data[-1][0]
    for i in range(len(data)-2, -1, -1):
        lastExtrapolatedValue = data[i][0] - lastExtrapolatedValue
    return lastExtrapolatedValue



lines = readFile()
histories = parseRawInput(lines)

result = 0
for history in reduce(histories):
    result += extrapolateStart(history)

print("result : " + str(result)) # 21022
