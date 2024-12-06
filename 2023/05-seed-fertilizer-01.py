from ast import Dict
import collections
from typing import List


def readFile() -> List[str]:
    with open('src/05-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines

def parseRawInput(rawInput: List[str]) -> List[List[str]]:
    section = 0
    curr = {
        "mapName": "",
        "values": collections.defaultdict(list),
        "child": dict()
    }
    mapName = ""
    result = curr
    for line in rawInput:
        if line.strip() == "":
            section += 1
            newMap = {
                "values": list(),
                "child": dict()
            }
            curr["child"] = newMap
            curr = newMap
            continue
        if "-" in line:
            mapName = line.strip().split(" ")[0]
            continue
        if section == 0:
            seeds = line.strip().replace("  ", " ").split(":")[1].strip().split(" ")
            curr["mapName"] = "seeds"
            curr["values"] = seeds
            continue
        if section > 0:
            map = line.strip().replace("  ", " ").split(" ")
            curr["values"].append({"dest": int(map[0]), "source": int(map[1]), "rang": int(map[2])})
            curr["mapName"] = mapName
            continue

    return result

def traverse(tree) -> int:
    seeds = tree["values"]
    lowestLocation = float("inf")
    for seed in seeds:
        curr = tree["child"]
        pointer = int(seed)
        while curr:
            found = False
            for map in curr["values"]:
                if map["source"] <= pointer < map["source"] + map["rang"]:
                    diff = pointer - map["source"]
                    pointer = map["dest"] + diff
                    curr = curr["child"]
                    found = True
                    break
            if not found:
                curr = curr["child"]
            if not curr:
                print("location " + str(pointer))
                lowestLocation = min(lowestLocation, int(pointer))
    return lowestLocation


lines = readFile()

maps = parseRawInput(lines)
res  = traverse(maps)

print("lowest : " + str(res)) #
