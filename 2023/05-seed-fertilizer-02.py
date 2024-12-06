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


def processNextRanges(inputRange: List[int], node) -> None:
    result = []
    inputRanges = []
    inputRanges.append(inputRange)
    while inputRanges:
        iR = inputRanges[0]
        # print(f"Now : {iR}")
        inputRanges = inputRanges[1:]

        foundSome = False

        for mapping in node:

            if (mapping["source"] <= iR[0] <= mapping["source"] + mapping["rang"] and
                mapping["source"] <= iR[1] <= mapping["source"] + mapping["rang"]):

                inputDiff = iR[1] - iR[0]

                mappingdiff = iR[0] - mapping["source"]
                nextMinPointer = mapping["dest"] + mappingdiff
                nextMaxPointer = nextMinPointer + inputDiff

                result.append([nextMinPointer, nextMaxPointer])

                foundSome = True
                # print(f"FOUND {nextMinPointer}, {nextMaxPointer}")

                break

            if (mapping["source"] <= iR[0] <= mapping["source"] + mapping["rang"] and
                iR[1] > mapping["source"] + mapping["rang"]):

                mappingdiff = iR[0] - mapping["source"]
                nextMinPointer = mapping["dest"] + mappingdiff
                nextMaxPointer = mapping["dest"] + mapping["rang"]

                result.append([nextMinPointer, nextMaxPointer])

                newRange = [mapping["source"] + mapping["rang"] + 1, iR[1]]
                inputRanges.append(newRange)
                # print(f"next range - higher clip {newRange}")

                foundSome = True


            if (mapping["source"] <= iR[1] <= mapping["source"] + mapping["rang"] and
                iR[0] <= mapping["source"]):

                inputDiff = iR[1] - iR[0]

                nextMinPointer = mapping["dest"]
                nextMaxPointer = (iR[0] - mapping["source"]) + mapping["dest"]  + inputDiff

                result.append([nextMinPointer, nextMaxPointer])

                newRange = [iR[0], mapping["source"] - 1]
                inputRanges.append(newRange)
                # print(f"next range - lower clip {newRange}")
                foundSome = True

            if (mapping["source"] > iR[0] and
                mapping["source"] + mapping["rang"] < iR[1]):

                inputDiff = iR[1] - iR[0]

                nextMinPointer = mapping["dest"]
                nextMaxPointer = mapping["dest"] + mapping["rang"]

                result.append([nextMinPointer, nextMaxPointer])

                newRangeSmall = [iR[0], mapping["source"] - 1]
                inputRanges.append(newRangeSmall)
                newRangeBig = [mapping["source"] + mapping["rang"] + 1, iR[1]]
                inputRanges.append(newRangeBig)
                # print(f"next range - both {newRangeSmall}  {newRangeBig}")

                foundSome = True

        if not foundSome:
             result.append(iR[:])
    return result

def findLowestLocation(seed, node) -> int:
    currentNode = node

    lowestLocation = float("inf")

    inputRanges = [seed[:]]

    while currentNode:
        nextRanges = []
        for inputRange in inputRanges:
            nextRanges.extend(processNextRanges(inputRange, currentNode["values"]))

        inputRanges = nextRanges[:]

        currentNode = currentNode["child"]
    for location in inputRanges:
        lowestLocation = min(lowestLocation, int(location[0]))

    return lowestLocation

def traverse(tree) -> int:
    lowestLocation = float("inf")
    for i in range(0, len(tree["values"]), 2):
        minSeed = int(tree["values"][i])
        maxSeed = int(tree["values"][i]) + int(tree["values"][i+1])
        seed = [minSeed, maxSeed]
        print(f"seed range {minSeed}.{maxSeed}")

        location = findLowestLocation(seed, tree["child"])
        print(f"location {location}")
        lowestLocation = min(lowestLocation, int(location))

    return lowestLocation


lines = readFile()

maps = parseRawInput(lines)
res  = traverse(maps)

print("lowest : " + str(res)) #
