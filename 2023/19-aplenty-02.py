import collections
from dataclasses import dataclass
import time
from typing import Dict, List, Set, Tuple
from unicodedata import category

@dataclass
class Rule():
    key: str
    comperator: str
    value: int
    followWorkflow: str

def readFile() -> List[str]:
    with open('src/19-input.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> Dict[str, List[Rule]]:
    workflows = collections.defaultdict(list)
    rules = True
    for line in rawInput:
        if line == "":
            rules = False
            continue

        if rules:
            workflowName = line.split("{")[0]
            rules = line.split("{")[1][:-1].split(",")
            lastRule = rules.pop()
            for rule in rules:
                newRule = Rule(key=rule[0], comperator=rule[1], value=int(rule.split(":")[0][2:]), followWorkflow=rule.split(":")[1])
                workflows[workflowName].append(newRule)
            elseRule = Rule(key="", comperator="else", value=-1, followWorkflow=lastRule)
            workflows[workflowName].append(elseRule)

    return workflows

rawInput = readFile()
WORKFLOWS = parse(rawInput)


def count(ranges: Dict[str, List[int]], name = "in") -> int:
    if name == "R":
        return 0
    if name == "A":
        product = 1
        for low, high in ranges.values():
            product *= high - low + 1
        return product

    rules: List[Rule] = WORKFLOWS[name]
    fallback = rules[-1]
    total = 0

    for rule in rules[:-1]:
        low, high = ranges[rule.key]
        if rule.comperator == "<":
            good = (low, min(rule.value - 1, high))
            bad = (max(rule.value, low), high)
        if rule.comperator == ">":
            good = (max(rule.value + 1, low), high)
            bad = (low, min(rule.value, high))

        if good[0] <= good[1]:
            rangeCopy = dict(ranges)
            rangeCopy[rule.key] = good
            total += count(rangeCopy, rule.followWorkflow)

        if bad[0] <= bad[1]:
            ranges = dict(ranges)
            ranges[rule.key] = bad
        else:
            break
    else:
        total += count(ranges, fallback.followWorkflow)
    return total


ranges = {key: (1, 4000,) for key in "xmas"}
res = count(ranges, "in")

print("result : " + str(res))
