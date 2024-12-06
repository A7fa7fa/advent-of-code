from ast import Dict
import collections
from typing import List, Tuple


def readFile() -> List[str]:
    with open('src/06-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> Tuple[int, int]:

    time = rawInput[0].strip().replace(" ", "").split(":")[1].strip()
    distance = rawInput[1].strip().replace(" ", "").split(":")[1].strip()
    return (int(time), int(distance),)

def race(data: Tuple[int, int]):
    # TODO refactor to binary search upper and lower boundaries
    maxTime = data[0]
    possibleWins = []
    for buttonHold in range(1, maxTime + 1):
        speed = buttonHold
        timeLeftToRace = maxTime - buttonHold
        distance = speed * timeLeftToRace

        if distance > int(data[1]):
            possibleWins.append(buttonHold)

    return possibleWins


lines = readFile()

data = parseRawInput(lines)
countRacesWon  = race(data)


print("result : " + str(len(countRacesWon)))
