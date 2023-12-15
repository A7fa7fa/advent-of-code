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

rawInput = readFile()
input = parse(rawInput)

result = sum(list(map(hash, input)))

print("result : " + str(result)) #
