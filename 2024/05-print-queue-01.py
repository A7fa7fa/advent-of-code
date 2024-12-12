
from typing import List


def readFile() -> List[str]:
    with open('2024/05-input.txt') as f:
        lines : List[str] = f.readlines()
        return lines



def traverse(offset:int, qu: list[int], rules: dict[int, list[int]]) -> bool:
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

    # print(rules)
    # print(queues)


    correct_ques: list[list[int]] = []
    bad_ques: list[list[int]] = []


    for qu in queues:
        correct = True
        for i in range(1, len(qu)):

            correct = traverse(i-1, qu, rules)
            if not correct:
                bad_ques.append(qu)
                break
        if correct:
            correct_ques.append(qu)

    middle_pages: list[int] = []

    for qu in correct_ques:
        middle_pages.append(qu[len(qu) // 2])

    print(middle_pages)

    return sum(middle_pages)


if __name__ == '__main__':

    result = run()

    assert result == 5639, result
    print(result)