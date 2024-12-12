
from typing import List


def readFile() -> List[str]:
    with open('2024/05-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines



def traverse(offset:int, qu: list[int], rules: dict[int, list[int]]) -> None:
    if len(qu) == 1:
        return
    must_print_before = set(rules.get(qu[offset], []))
    i = offset + 1
    while i < len(qu):
        if len(must_print_before) == 0:
            break
        if qu[i] in must_print_before:
            old_qu = qu[:]
            qu[offset] = old_qu[i]
            for entry in range(offset, i):
                qu[entry+1] = old_qu[entry]

            must_print_before = set(rules.get(qu[offset], []))
            i = offset + 1
        else:
            i += 1

def is_correct(offset:int, qu: list[int], rules: dict[int, list[int]]) -> bool:
    if len(qu) == 1:
        return True

    must_print_before = set(rules.get(qu[offset], []))
    for page in qu[offset+1:]:
        if page in must_print_before:
            return False
    return True



def run() -> int:
    lines = readFile()
    rules: dict[int, list[int]] = {}
    queues: list[list[int]] = []

    queue_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            queue_start = i
            break
        nums = line.strip().split("|")
        assert len(nums) == 2

        # after - before
        if int(nums[1]) not in rules:
            rules[int(nums[1])] = []
        rules[int(nums[1])].append(int(nums[0]))

    for line in lines[queue_start+1:]:
        nums = line.strip().split(",")
        queues.append(list(map(int, nums)))


    all_qu: list[list[int]] = [que[:] for que in queues]

    for qu in queues:
        for i in range(len(qu)):
            traverse(i, qu, rules)


    assert len(all_qu) == len(queues)

    for qu in queues:
        for i in range(len(qu)):
            assert is_correct(i, qu, rules), qu

    updated_qu: list[list[int]] = []
    for i in range(len(queues)):
        if all_qu[i] != queues[i]:
            updated_qu.append(queues[i])

    middle_pages: list[int] = []
    for qu in updated_qu:
        middle_pages.append(qu[len(qu) // 2])


    return sum(middle_pages)


if __name__ == '__main__':

    result = run()

    assert result == 5273, result
    print(result)