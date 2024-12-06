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

# For future me:
# There are two base cases to consider based on the first spring in a config.
# a unkown spring is working. i consider it as working
# -> therefore i just ignore it. because i am only interesed in damaged groups. recursive call count again without first spring
#
# a unkown spring is damaged. i consider it as damaged and the first spring of the first damaged group
# -> a group is valid if there are enough springs left in the configuration
# -> and in the next n springs (size of damaged group) there is no working spring
# -> and the length of the config is equal to the size of damaged group or the next spring after this one is not damaged
# this means i found a valid broken group. i remove the group from the config and from groups and call count again
#
# this opens up like a binary tree for every spring in the config until all possible configurations are considered
# until the config and the groups are empty -> this means this branch is valid and returns 1 otherwise is invalid and returns 0
# or until there are no groups left and there are no damaged springs left in the config. -> return 1 otherwise is invalid and returns 0
#
# Caching
# because there are so many options to consider configurations and groups will show up multiple times
# therefor if i ever find a config+group i have seen before i return the cached value otherwise i cache the value for future reference


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
