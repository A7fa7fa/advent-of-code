
from typing import List


digitsAsWords = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

maxDigiWordtLen = max([len(str(key)) for key in digitsAsWords])

digitWordChars = set("".join(list(digitsAsWords.keys())))

def run() -> None:
    with open('01-input.txt') as f:
        lines : List[str] = f.readlines()
        res = 0
        for line in lines:
            lineDigits = ""
            for i, char in enumerate(line.strip()):
                if char.isdigit():
                    lineDigits += str(char)
                else:
                    for n in range(1, maxDigiWordtLen + 1):
                        if i + n == len(line):
                            break
                        if line[i+n] not in digitWordChars:
                            break
                        if line[i:i+n+1] in digitsAsWords:
                            lineDigits += str(digitsAsWords[line[i:i+n+1]])
                            break

            res += int(f"{lineDigits[0]}{lineDigits[-1]}")
    print(res)

# 54676

if __name__ == '__main__':
    run()