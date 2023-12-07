from typing import List

CARDS = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2",)

def readFile() -> List[str]:
    with open('src/07-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> List[List[str]]:
    result = []
    for line in rawInput:
        [hand, bid] = line.strip().split(" ")
        result.append([hand, int(bid)])

    return result


def setHandType(hand: str, differentCards: List[str]) -> int:
    if len(differentCards) == 1:
        ## five of a kind
        return 7
    elif (len(differentCards) == 2 and
        (hand.count(differentCards[0]) == 4 or hand.count(differentCards[1]) == 4)):
        ## four of a kind
        return 6
    elif (len(differentCards) == 2 and
        (hand.count(differentCards[0]) == 3 or hand.count(differentCards[1]) == 3)):
        ## full house
        return 5
    elif (len(differentCards) == 3 and
        (hand.count(differentCards[0]) == 3 or hand.count(differentCards[1]) == 3 or hand.count(differentCards[2]) == 3)):
        ## three of a kind
        return 4
    elif len(differentCards) == 3:
        ## two pair
        return 3
    elif len(differentCards) == 4:
        ## one pair
        return 2
    elif len(differentCards) == 5:
        ## one pair
        return 1
    else:
        raise Exception("could not determine hand type")


def evaluateHandTypes(hands: List[List[str]]) -> None:
    for handNum in range(len(hands)):
        hands[handNum].append(-1)
        differentCards = set(hands[handNum][0])
        hands[handNum][2] = setHandType(hands[handNum][0], list(differentCards))

def getValueFromCard(card: str) -> int:

    value = 0
    for poossibleCard in CARDS:
        value += 1
        if poossibleCard == card:
            return len(CARDS) - value

    raise Exception("Card does not exist")


def evaluateHands(hands: List[List[str]]) -> None:

    for hand in hands:

        handValue = []
        for char in hand[0]:
            handValue.append(getValueFromCard(char))
        hand.append(handValue)



def calculaTotalWinnings(hands: List[List[str]]) -> int:
    totalWinnings = 0
    rank = 0
    for i in range(len(hands) -1, -1, -1):
        rank += 1
        totalWinnings += (hands[i][1] * rank)

    return totalWinnings

def sortHands(hands: List[List[str]]) -> None:
    hands.sort(key = lambda hand : (hand[2], hand[3][0], hand[3][1], hand[3][2], hand[3][3], hand[3][4]), reverse = True)


lines = readFile()
hands = parseRawInput(lines)

evaluateHandTypes(hands)
evaluateHands(hands)
sortHands(hands)

result = calculaTotalWinnings(hands)

print("result : " + str(result))
