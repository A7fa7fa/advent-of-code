import collections
from dataclasses import dataclass
import time
from typing import Dict, List, Set, Tuple
from unicodedata import category

@dataclass
class Part():
    x: int
    m: int
    a: int
    s: int

    def get(self, prop: str) -> int:
        return getattr(self, prop)

    def sum(self) -> int:
        return self.x + self.m + self.a + self.s

@dataclass
class PartRange():
    x: List[int]
    m: List[int]
    a: List[int]
    s: List[int]

    @staticmethod
    def createBase() -> "PartRange":
        min = 1
        max = 4000
        return PartRange(x=[min, max], m=[min, max], a=[min, max], s=[min, max])

    def inside(self, prop, other) -> bool:
        return self.getMin(prop) <= other.getMin(prop) <= self.getMax(prop)and self.getMin(prop) <= other.getMax(prop) <= self.getMax(prop)

    def overlapping(self, other) -> None:
        notInside = ""
        for prop in "xmas":
            if not self.inside(prop, other):
                notInside += prop

        for prop in notInside:
            if self.getMin(prop) <= other.getMin(prop) <= self.getMax(prop) and self.getMax(prop) < other.getMax(prop):
                other.setMin(prop, self.getMax(prop)+1)
                return
            if self.getMin(prop) <= other.getMax(prop) <= self.getMax(prop) and self.getMin(prop) > other.getMin(prop):
                other.setMax(prop, self.getMin(prop)-1)
                return

    def adjustRange(self, prop: str, value: int, operator: str) -> None:
        if operator == "<":
            self.setMax(prop, value-1)
            return
        else:
            self.setMin(prop, value+1)
        if self.get(prop)[0] > self.get(prop)[0]:
            raise Exception("WHAT!")

    def get(self, prop: str) -> List[int]:
        return getattr(self, prop)

    def set(self, prop: str, value: int) -> None:
        return setattr(self, prop, value)

    def setMin(self, prop: str, value: int) -> None:
        v = self.get(prop)
        v[0] = value
        return self.set(prop, v)

    def setMax(self, prop: str, value: int) -> None:
        v = self.get(prop)
        v[1] = value
        return self.set(prop, v)

    def getMin(self, prop: str) -> int:
        return self.get(prop)[0]

    def getMax(self, prop: str) -> int:
        return self.get(prop)[1]

    def sum(self) -> int:
        return self.x + self.m + self.a + self.s

    def distinctPossibleRatings(self) -> int:
        return (self.x[1] - self.x[0]) * (self.m[1] - self.m[0]) * (self.a[1] - self.a[0]) * (self.s[1] - self.s[0])


@dataclass
class Rule():
    categorie: str
    operator: str
    value: int
    followWorkflow: str

    def isApplicable(self, part: Part) -> bool:

        if self.operator == "<":
            if part.get(self.categorie) < self.value:
                return True
        if self.operator == ">":
            if part.get(self.categorie) > self.value:
                return True
        if self.operator == "else":
            return True
        return False


def readFile() -> List[str]:
    with open('src/19-input-debug.txt') as f:
        lines : List[str] = f.readlines()
        return [line.strip() for line in lines]

def parse(rawInput: List[str]) -> Tuple[Dict[str, List[Rule]], List[Part]]:
    workflows = collections.defaultdict(list)
    parts = []
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
                newRule = Rule(categorie=rule[0], operator=rule[1], value=int(rule.split(":")[0][2:]), followWorkflow=rule.split(":")[1])
                workflows[workflowName].append(newRule)
            elseRule = Rule(categorie="", operator="else", value=-1, followWorkflow=lastRule)
            workflows[workflowName].append(elseRule)
        else:
            x, m , a, s = line[1:-1].split(",")
            part = Part(x=int(x.split("=")[1]), m=int(m.split("=")[1]), a=int(a.split("=")[1]), s=int(s.split("=")[1]))
            parts.append(part)

    return workflows, parts


def processDfs(validPaths: List[List[int]], currPath: List[int], workflows: Dict[str, List[Rule]] , nextWorkflowName: str) -> bool:

    wf = nextWorkflowName
    for i, rule in enumerate(workflows[wf]):
        if rule.followWorkflow == "R":
            continue
        if rule.followWorkflow == "A":
            currPath.append(i)
            validPaths.append(currPath[:])
            currPath.pop()
            continue

        currPath.append(i)
        processDfs(validPaths, currPath, workflows, rule.followWorkflow)
        currPath.pop()

def followPath(workflows: Dict[str, List[Rule]] , path: List[int], part: PartRange) -> None:

    wfName = "in"
    for ruleI in path:
        rule = workflows[wfName][ruleI]
        if rule.operator != "else":
            part.adjustRange(rule.categorie, rule.value, rule.operator)

        if rule.followWorkflow == "A":
            #end
            break
        wfName = rule.followWorkflow


rawInput = readFile()
workflows, parts = parse(rawInput)

startWorkflow = "in"
validPaths = []
processDfs(validPaths, [], workflows, startWorkflow)

parts: List[PartRange] = []
for path in validPaths:
    other = PartRange.createBase()
    followPath(workflows, path, other)
    parts.append(other)


maxI = -1
maxSum = -1
for i, other in enumerate(parts):
    if other.distinctPossibleRatings() > maxSum:
        maxSum = other.distinctPossibleRatings()
        maxI = i



total = sum([part.distinctPossibleRatings() for part in parts])
part = parts.pop(maxI)

while True:
    overlappRanges = []

    for i, other in enumerate(parts):
        if (part.x[0] <= other.x[0] <= part.x[1] and part.x[0] <= other.x[1] <= part.x[1]
            and part.m[0] <= other.m[0] <= part.m[1] and part.m[0] <= other.m[1] <= part.m[1]
            and part.a[0] <= other.a[0] <= part.a[1] and part.a[0] <= other.a[1] <= part.a[1]
            and part.s[0] <= other.s[0] <= part.s[1] and part.s[0] <= other.s[1] <= part.s[1]):
            print("Inside : ", other)
            overlappRanges.append(i)
            break

        part.overlapping(other)


    for i in overlappRanges[::-1]:
        parts.pop(i)
        print("remove", i)

    if total == sum([part.distinctPossibleRatings() for part in parts]):
        break


total = [part.distinctPossibleRatings() for part in parts]



print("result : " + str(sum(total))) #

#167409079868000
#156232926233442

