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
        input.append({"cardNum": cardNum, "winningNums": winningNums, "myNums": myNums, "amount": 1})

    return input


lines = readFile()
# lines = [
#     "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
#     "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
#     "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
#     "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
#     "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
#     "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
# ]
scratchcards = parseScratchCards(lines)


for i, card in enumerate(scratchcards):
    intersection = card["myNums"] & card["winningNums"] # intersection between both sets
    matchingNum = len(intersection)
    print(matchingNum)

    for n in range(1, matchingNum + 1):
        scratchcards[i+n]["amount"] += card["amount"] # add as much cards to the next cards, as much cards we have ( for every card we add one)

points = 0
for i in range(0, len(scratchcards)):
    points += scratchcards[i]["amount"]


print(points) # 8477787
