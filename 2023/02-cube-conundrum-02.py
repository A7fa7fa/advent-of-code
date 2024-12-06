from typing import List
from unittest import result


def readFile() -> List[str]:
    with open('src/02-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def prepareInput(rawInput: List[str]) -> List[List[str]]:
    games = []

    for line in rawInput:
        gameNum = line.split(":")[0].split(" ")[1]
        gamesRaw = line.split(":")[1].split(";")
        gameParsed = []
        for game in gamesRaw:
            draws = game.split(",")
            for i, _ in enumerate(draws):
                draws[i] = draws[i].strip()
            gameParsed.append(draws)
        games.append(gameParsed)
    return games

def sumPowerOfLeastCubes(games: List[List[str]]) -> int:

    result = 0

    for i, game in enumerate(games):
        leastCubes = {
            "red": 1,
            "green": 1,
            "blue": 1
        }
        for gameRound in game:
            for item in gameRound:
                item = item.split(" ")
                count = item[0]
                color = item[1]
                leastCubes[color] = max(leastCubes[color], int(count))

        powerOfValue = 1
        for value in leastCubes.values():
            powerOfValue *= value
        result += powerOfValue


    return result


lines = readFile()
games = prepareInput(lines)
possibleGames = sumPowerOfLeastCubes(games)

print(possibleGames)