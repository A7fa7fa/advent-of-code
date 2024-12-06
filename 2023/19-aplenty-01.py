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
    with open('src/19-input.txt') as f:
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

def process(part: Part, workflows: Dict[str, List[Rule]] , startWorkflow: str) -> bool:

    wf = startWorkflow
    while wf != None:
        rules = workflows[wf]

        for rule in rules:
            if rule.isApplicable(part):
                wf = rule.followWorkflow
                break
        if wf == "A":
            return True
        if wf == "R":
            return False
    raise Exception("Fail!")

rawInput = readFile()
workflows, parts = parse(rawInput)

startWorkflow = "in"
result = []
for part in parts:
    if process(part, workflows, startWorkflow):
        result.append(part)

totalSum = sum([part.sum() for part in result])


print("result : " + str(totalSum)) #446935

