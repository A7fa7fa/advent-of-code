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

def traverse(tree: Dict[str, Dict[str, str]], start: str,  directions: str) -> int:
    steps = 0
    i = 0
    pos = start

    while i < len(directions):
        step = directions[i]
        pos = tree[pos][step]
        steps += 1
        if pos == "ZZZ":
            return steps
        i += 1
        if i == len(directions):
            i = 0

    pass

lines = readFile()
directions = parseRawInput(lines)

result = traverse(directions["map"], "AAA", directions["directions"])

print("result : " + str(result))
