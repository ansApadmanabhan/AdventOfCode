from functools import cache
inputFile = "input.txt"

data = []
with open(inputFile) as infile:
    line = infile.readlines()
    digitList = line[0].split(" ")


@cache
def expandIndexOnce(num):
    if int(num) == 0:
        return '1', None
    elif len(num) % 2 == 0:
        replacer1 = str(int(num[:int(len(num) / 2)]))
        replacer2 = str(int(num[int(len(num) / 2):]))
        return replacer1, replacer2
    else:
        return f'{int(num) * 2024}', None


@cache
def expandStonesToCount(stone, numberOfBlinks):
    stone1, stone2 = expandIndexOnce(stone)
    if numberOfBlinks == 1:
        if stone2 is None:
            return 1
        else:
            return 2

    totalStones = expandStonesToCount(stone1, numberOfBlinks - 1)
    if stone2 is not None:
        totalStones += expandStonesToCount(stone2, numberOfBlinks - 1)

    return totalStones


total = 0
for ii in digitList:
    total += expandStonesToCount(ii, 75)


print(f"Part 2: Answer {total}")
