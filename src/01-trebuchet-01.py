
from typing import List


def run() -> None:
    with open('01-input.txt') as f:
        lines : List[str] = f.readlines()
        res = 0
        for line in lines:
            lineDigits = ""
            for char in line:
                if char.isdigit():
                    lineDigits += char
            res += int(f"{lineDigits[0]}{lineDigits[-1]}")
    print(res)



if __name__ == '__main__':
    run()