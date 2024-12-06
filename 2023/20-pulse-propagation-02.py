import collections
import math
from typing import Dict, List, Set, Tuple


FLIP_FLOP = "%"
CONJUNCTION = "&"

class Module():
    def __init__(self, type, name, targets) -> None:
        self.type = type
        self.name = name
        self.targets = targets

class Memory():
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name
        self.memory = []


def readFile() -> List[str]:
    with open('src/20-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> Dict[str, Module]:
    modules = dict()
    for line in rawInput:
        [module, targets] = line.replace(" ", "").split("->")
        type = module[0]
        name = module[1:]

        if module == "broadcaster":
            type = "start"
            name = "broadcaster"


        modules[name] = Module(type, name, targets.split(","))

    return modules



rawInput = readFile()
MODULES = parse(rawInput)



def createInitStatus(memo: Dict, moduleName: str, originName: str ) -> None:
    if moduleName not in MODULES:
        return
    if MODULES[moduleName].type == FLIP_FLOP:
        if moduleName in memo:
            return
        memo[moduleName] = "off"

    if MODULES[moduleName].type == CONJUNCTION:
        if moduleName in memo:
            if originName in memo[moduleName]:
                return
            memo[moduleName][originName] = "low"
        else:
            memo[moduleName] = {originName: "low"}
    for target in MODULES[moduleName].targets:
        createInitStatus(memo, target, moduleName)

def buildInitMemo() -> Dict:
    memo = dict()
    for target in MODULES["broadcaster"].targets:
        createInitStatus(memo, target, "broadcaster")
    return memo

def flip(pulse: str) -> str:
    if pulse == "on":
        return "off"
    return "on"

def getPulseAfterFlip(flipStatus: str) -> str:
    if flipStatus == "on":
        return "high"
    return "low"

def allConjuncionAreHigh(conn: Dict[str, str]) -> bool:
    return all(status == "high" for status in conn.values())


def propagate(currMemo, endFeed, pressCount, endFeedCycleLength) -> None:

    qu = collections.deque()
    for target in MODULES["broadcaster"].targets:
        qu.append((target, "low", None,))

    while qu:

        quLen = len(qu)

        while quLen > 0:
            quLen -= 1

            moduleName, pulse, originName = qu.popleft()

            if moduleName not in MODULES:
                continue

            module = MODULES[moduleName]

            if module.type == FLIP_FLOP:
                if pulse == "high":
                    # ignore and nothing happens
                    pass
                if pulse == "low":
                    currMemo[moduleName] = flip(currMemo[moduleName])
                    nextPulse = getPulseAfterFlip(currMemo[moduleName])
                    for target in module.targets:
                        qu.append((target, nextPulse, moduleName))

            elif module.type == CONJUNCTION:
                currMemo[moduleName][originName] = pulse
                nextPulse = "high"

                if moduleName == endFeed and pulse == "high" and originName not in endFeedCycleLength:
                    endFeedCycleLength[originName] = pressCount
                    if len(endFeedCycleLength.values()) == 4:
                        print("Found all")
                        return endFeedCycleLength


                if allConjuncionAreHigh(currMemo[moduleName]):
                    nextPulse = "low"
                for target in module.targets:
                    qu.append((target, nextPulse, moduleName))
    return None

currMemo = buildInitMemo()

(endFeed,) = [module.name for module in MODULES.values() if "rx" in module.targets]

endFeedCycleLength = collections.defaultdict(int)

for pressCount in range(1, 10000):
    res = propagate(currMemo, endFeed, pressCount, endFeedCycleLength)
    if res:
        break

print("result : " + str(math.lcm(*list(endFeedCycleLength.values())))) #246006621493687
