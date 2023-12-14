from typing import Dict, Generator, List, Tuple

DAMAGED = "#"
WORKING = "."
UNKOWN = "?"

def readFile() -> List[str]:
    with open('src/12-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parsSprings(rawInput: List[str]) -> List[Dict[str, str|Tuple[int]]]:
    springs = []

    for line in rawInput:
        [config, groups] = line.split(" ")
        springs.append({
            "config": config,
            "damagedSpringGroups": tuple(map(int, groups.split(",")))
        })

    return springs

MEMO = dict()

def count(config : str, groups: Tuple[int]) -> int:

    if config == "":
        noExpectedBlocksLeft = groups == ()
        if noExpectedBlocksLeft:
            return 1
        else: # expect more blocks of brocken strings, ut config is empty so return 0
            return 0

    if groups == ():
        blocksOfBrockeStringsLeft = DAMAGED in config
        if blocksOfBrockeStringsLeft:
            return 0
        else:
            return 1

    key = (config, groups)

    if key in MEMO:
        return MEMO[key]

    result = 0

    if config[0] in [WORKING, UNKOWN]:
        result += count(config[1:], groups)

    if config[0] in [DAMAGED, UNKOWN]:

        isEnoughSpringsLeft = groups[0] <= len(config)
        notOperationalSpringsInBlock = WORKING not in config[:groups[0]]
        # cant have two operational springs next to each other. otherwise they would not ba a separate grop
        nextSpringAfterIsOperational = isEnoughSpringsLeft and (groups[0] == len(config) or config[groups[0]] != DAMAGED)
        if isEnoughSpringsLeft and notOperationalSpringsInBlock and nextSpringAfterIsOperational:
            # there must be a gap. so i slice of the next element of the next config
            result += count(config[groups[0] + 1:], groups[1:])

    MEMO[key] = result
    return result



def totalArrangments(springs: List[Dict[str, str|Tuple[int]]]) -> int:
    total = 0
    for line in springs:
        total += count("?".join([line["config"]] * 5), line["damagedSpringGroups"] * 5)

    return total

def calc(springs):

    for line in springs:
        start = 0
        end = 0
        while end < len(line["config"]):
            charAtStart = line["config"][start]
            charAtEnd = line["config"][end]
            if start == end:
                if charAtEnd == DAMAGED or charAtEnd == WORKING:
                    start += 1
                    end += 1
                else:
                    end +=1
            else:
                if charAtEnd == UNKOWN:
                    end += 1
                else:
                    print("len of unkown group is", start, end - start)
                    end += 1
                    start = end
        print("len of unkown group is", start, end - start)


rawInput = readFile()
springs = parsSprings(rawInput)
result = totalArrangments(springs)




print("result : " + str(result)) #
