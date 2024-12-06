from os import replace
import time
from typing import Dict, List, Tuple

def readFile() -> List[str]:
    with open('src/15-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> List[str]:
    return "".join(rawInput).strip().split(",")

def hash(base: str) -> int:
    currentValue = 0
    for char in base:
        currentValue += ord(char)
        currentValue *= 17
        currentValue %= 256
    return currentValue

def sortLensesIntoBoxes(boxes: List[List[str]], lenses: List[str] ) -> None:

    for lens in lenses:
        addLens = "=" in lens

        if addLens:
            boxNum = hash(lens.split("=")[0])
            newLens = lens.replace("=", " ")
            newLensName = newLens.split(" ")[0]
            replaced = False
            for i, boxLens in enumerate(boxes[boxNum]):
                if boxLens.startswith(newLensName):
                    boxes[boxNum][i] = newLens
                    replaced = True
                    break
            if not replaced:
                boxes[boxNum].append(lens.replace("=", " "))
        else:
            boxNum = hash(lens.split("-")[0])
            newLensName = lens.replace("-", "")
            pos = None
            for i, boxLens in enumerate(boxes[boxNum]):
                if newLensName == boxLens.split(" ")[0]:
                    pos = i
                    break
            if pos != None:
                boxes[boxNum].pop(pos)


def focusingPowerOfBox(boxNum: int, box: List[str]) -> int:
    power = 0
    for i, lens in enumerate(box):
        power += int(lens.split(" ")[1]) * (i+1) * (boxNum + 1)
    return power


def calcTotalFocusingPower(boxes: List[List[str]]) -> int:
    return sum(list(map(focusingPowerOfBox, list(range(len(boxes))), boxes)))

rawInput = readFile()
lenses = parse(rawInput)

boxes = [[] for _ in range(256)]

sortLensesIntoBoxes(boxes, lenses)
totalFocuingPower = calcTotalFocusingPower(boxes)

print("result : " + str(totalFocuingPower)) #
