import math
from typing import Dict, List


def readFile() -> List[str]:
    with open('src/08-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> List[List[str]]:
    result = {
        "map": dict()
    }
    for i, line in enumerate(rawInput):
        if line.strip() == "":
            continue
        if i == 0:
            result["directions"] = line.strip()
        else:
            pos = line.strip().replace("  ", " ").split(" = ")[0].strip()
            childs = line.strip().replace("  ", " ").split(" = ")[1].replace("(", "").replace(")", "").split(", ")
            result["map"][pos] = {"L": childs[0], "R": childs[1] }


    return result

def getStartingNodes(tree: Dict[str, Dict[str, str]]) -> List[str]:
    return list(filter(lambda entry: entry[-1] == "A", list(tree.keys())))

def traverse(tree: Dict[str, Dict[str, str]], start: List[str],  directions: str) -> int:
    steps = 0
    i = 0
    positions = start

    while i < len(directions):
        step = directions[i]

        steps += 1
        found = 0
        for posI in range(len(positions)):
            position = positions[posI]
            newPosition = tree[position][step]
            positions[posI] = newPosition

            if newPosition[-1] == "Z":
                found += 1
        if found == len(start):
            return steps
        i += 1
        if i == len(directions):
            # print(steps)
            i = 0


lines = readFile()
directions = parseRawInput(lines)
startingNodes = getStartingNodes(directions["map"])

result = []
for node in startingNodes:
    result.append(traverse(directions["map"], [node], directions["directions"]))
    # cycles are all divisible by the length of the directions and we not offset within the directions (e.g. you could imagine that a cycle would be of the same length as the directions but not start and end at the start of the directions, which would make things much much more complicated)
    print(str(result[-1]/len(directions["directions"])))

print("result : " + str(math.lcm(*result)))


