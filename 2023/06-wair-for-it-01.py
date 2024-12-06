from ast import Dict
import collections
from typing import List, Tuple


def readFile() -> List[str]:
    with open('src/06-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> Tuple[List[str], List[str]]:

    time = rawInput[0].strip().replace("  ", " ").split(":")[1].strip().split(" ")
    distance = rawInput[1].strip().replace("  ", " ").split(":")[1].strip().split(" ")
    fileredTime = list(filter(lambda entry: entry != "", time))
    fileredDistance = list(filter(lambda entry: entry != "", distance))
    return (fileredTime, fileredDistance,)

def race(data: Tuple[List[str], List[str]]):
    races = len(data[0])

    racesWon = []
    for raceNo in range(races):

        maxTime = int(data[0][raceNo])
        possibleWins = []
        for buttonHold in range(1, maxTime + 1):
            speed = buttonHold
            timeLeftToRace = maxTime - buttonHold
            distance = speed * timeLeftToRace

            if distance > int(data[1][raceNo]):
                possibleWins.append(buttonHold)
        racesWon.append(len(possibleWins))

    return racesWon


lines = readFile()

data = parseRawInput(lines)
countRacesWon  = race(data)

result = 1
for count in countRacesWon:
    result *= count


print("result : " + str(result))
