from typing import List


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

def validateGames(games: List[List[str]], rules: dict[str, int]) -> int:

    possibleGames = 0

    for i, game in enumerate(games):
        gameRoundResult = True
        for gameRound in game:
            for item in gameRound:
                item = item.split(" ")
                count = item[0]
                color = item[1]
                if int(count) > rules[color]:
                    gameRoundResult = False
                    break
            if not gameRoundResult:
                break

        if gameRoundResult:
            possibleGames += (i+1)
    return possibleGames


maxItems = {
    "red": 12,
    "green": 13,
    "blue": 14
}

lines = readFile()
games = prepareInput(lines)
possibleGames = validateGames(games, maxItems)

print(possibleGames)