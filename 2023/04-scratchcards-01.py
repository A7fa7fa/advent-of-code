from typing import List


def readFile() -> List[str]:
    with open('src/04-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseScratchCards(rawInput: List[str]) -> List[List[str]]:
    input = []

    for line in rawInput:
        cardNum = line.replace("  ", " ").strip().split(":")[0].replace("  ", " ").split(" ")[1].strip()
        winningNums = set(line.replace("  ", " ").strip().split(":")[1].strip().split("|")[0].strip().split(" "))
        myNums = set(line.replace("  ", " ").strip().split(":")[1].strip().split("|")[1].strip().split(" "))
        input.append({"cardNum": cardNum, "winningNums": winningNums, "myNums": myNums})

    return input


lines = readFile()
scratchcards = parseScratchCards(lines)


points = 0
for card in scratchcards:
    intersection = card["myNums"] & card["winningNums"] # intersection between both sets
    matchingNum = len(intersection)

    if matchingNum > 0:
        cardValue = int(1)
        cardValue = cardValue << (matchingNum - 1)
        points += cardValue

print(points) # 17782