import collections
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

def propagate(currMemo, pulseCount: Dict) -> None:

    qu = collections.deque()
    pulseCount["low"] += 1
    for target in MODULES["broadcaster"].targets:
        pulseCount["low"] += 1
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
                        pulseCount[nextPulse] += 1
                        qu.append((target, nextPulse, moduleName))

            elif module.type == CONJUNCTION:
                currMemo[moduleName][originName] = pulse
                nextPulse = "high"
                if allConjuncionAreHigh(currMemo[moduleName]):
                    nextPulse = "low"
                for target in module.targets:
                    pulseCount[nextPulse] += 1
                    qu.append((target, nextPulse, moduleName))

currMemo = buildInitMemo()
total = { "low": 0,  "high": 0 }

for i in range(1000):
    propagate(currMemo, total)


print("result : " + str(total["low"] * total["high"])) # 841763884
