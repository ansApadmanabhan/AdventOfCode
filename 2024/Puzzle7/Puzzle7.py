import math
import operator
import sys
import time

import pandas as pd
import itertools


def progressbar(it, prefix="", size=60, out=sys.stdout):  # Python3.6+
    count = len(it)
    start = time.time()  # time estimate start

    def show(j):
        x = int(size * j / count)
        # time estimate calculation and string
        remaining = ((time.time() - start) / j) * (count - j)
        mins, sec = divmod(remaining, 60)  # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        print(f"{prefix}[{u'█' * x}{('.' * (size - x))}] {j}/{count} Est wait {time_str}", end='\r', file=out,
              flush=True)

    show(0.1)  # avoid div/0
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("\n", flush=True, file=out)


with open(r"input.txt", 'r') as infile:
    data = []
    for ii in infile.readlines():
        options = ii.split(':')
        total = options[0]
        nums = options[1].lstrip(' ').rstrip().split(' ')
        data.append([int(total)] + [int(jj) for jj in nums if jj.isdigit()])


with open(r"smallInput.txt", 'r') as infile:
    data2 = []
    for ii in infile.readlines():
        options = ii.split(':')
        total = options[0]
        nums = options[1].lstrip(' ').rstrip().split(' ')
        data2.append([int(total)] + [int(jj) for jj in nums if jj.isdigit()])


def isThereAWay(totalStuff, otherDigits):
    IsWay = False
    if math.prod(otherDigits) < totalStuff and 0 not in otherDigits and 1 not in otherDigits:
        return False
    if sum(otherDigits) > totalStuff and 1 not in otherDigits:
        return False
    # Get Quotient, remainder and difference between total and last Digit
    lastDigit = otherDigits[-1]
    otherDigitsExceptLastDigit = otherDigits[:len(otherDigits) -1]
    quotient, remainder = divmod(totalStuff, lastDigit)
    difference = totalStuff - lastDigit

    if len(otherDigitsExceptLastDigit) == 1:
        # If we reach end of line stop iterating
        if remainder == 0 and quotient == otherDigitsExceptLastDigit[0]:
            IsWay = True
        elif difference == otherDigitsExceptLastDigit[0]:
            IsWay = True
    else:
        # Keep iterating till we reach the end
        if lastDigit == 1:
            # Try first with quotient
            IsWay = isThereAWay(quotient, otherDigitsExceptLastDigit)
            if not IsWay:
                # If not try with difference
                IsWay = isThereAWay(difference, otherDigitsExceptLastDigit)
        else:
            if remainder == 0:
                # The digits except last one would be a multiple
                IsWay = isThereAWay(quotient, otherDigitsExceptLastDigit)
                if not IsWay:
                    # If not try with difference
                    IsWay = isThereAWay(difference, otherDigitsExceptLastDigit)
            else:
                IsWay = isThereAWay(difference, otherDigitsExceptLastDigit)

    return IsWay


dataToCheck = data
summa = []
badda = []
goodList = []
badList = []
start1 = time.time()
for ii in progressbar(dataToCheck, "Checking.."):
    productSum = ii[0]
    restOfDigits = ii[1:]
    if isThereAWay(productSum, restOfDigits):
        summa.append(productSum)
        goodString = f"{productSum}:{restOfDigits}"
        goodList.append(goodString)
    else:
        badString = f"{productSum}:{restOfDigits}"
        badList.append(badString)
        badda.append(ii)
end1 = time.time()
df = pd.DataFrame(goodList)
badDF = pd.DataFrame(badList)

print(f"Part1: Sum of all good row: {sum(summa)}")
print(f"Time taken = {round((end1 - start1), 2)}")


# Part 2
def isThereAWay2(totalStuff, otherDigits):
    IsWay = False
    # if math.prod(otherDigits) < totalStuff and 0 not in otherDigits and 1 not in otherDigits:
    #     return False
    # if sum(otherDigits) > totalStuff and 1 not in otherDigits:
    #     return False
    # Get Quotient, remainder and difference between total and last Digit
    lastDigit = otherDigits[-1]
    otherDigitsExceptLastDigit = otherDigits[:len(otherDigits) -1]
    quotient, remainder = divmod(totalStuff, lastDigit)
    difference = totalStuff - lastDigit
    diffCat = str(totalStuff)[len(str(totalStuff)) - len(str(lastDigit)):]
    canConCat = str(lastDigit) == diffCat
    if len(str(totalStuff)) <= len(str(lastDigit)):
        difConCat = 0
    else:
        difConCat = int(str(totalStuff)[0:len(str(totalStuff)) - len(str(lastDigit))])

    if len(otherDigitsExceptLastDigit) == 1:
        # If we reach end of line stop iterating
        if remainder == 0 and quotient == otherDigitsExceptLastDigit[0]:
            IsWay = True
        elif difference == otherDigitsExceptLastDigit[0]:
            IsWay = True
        elif difConCat == otherDigitsExceptLastDigit[0] and diffCat == str(lastDigit):
            IsWay = True
    else:
        # Keep iterating till we reach the end
        if lastDigit == 1:
            # Try first with quotient
            IsWay = isThereAWay2(quotient, otherDigitsExceptLastDigit)
            if not IsWay:
                # If not try with difference
                IsWay = isThereAWay2(difference, otherDigitsExceptLastDigit)
                if not IsWay and canConCat:
                    IsWay = isThereAWay2(difConCat, otherDigitsExceptLastDigit)
        else:
            if remainder == 0:
                # The digits except last one would be a multiple
                IsWay = isThereAWay2(quotient, otherDigitsExceptLastDigit)
                if not IsWay:
                    # If not try with difference
                    IsWay = isThereAWay2(difference, otherDigitsExceptLastDigit)
                    # If not try with concatenation
                    if not IsWay and canConCat:
                        IsWay = isThereAWay2(difConCat, otherDigitsExceptLastDigit)
            elif canConCat:
                IsWay = isThereAWay2(difConCat, otherDigitsExceptLastDigit)
                if not IsWay:
                    # If not try with difference
                    IsWay = isThereAWay2(difference, otherDigitsExceptLastDigit)
            else:
                IsWay = isThereAWay2(difference, otherDigitsExceptLastDigit)

    return IsWay

dataToCheck2 = badda
summa2 = []
badda2 = []
goodList2 = []
badList2 = []
start2 = time.time()
for ii in progressbar(dataToCheck2, "Checking.."):
    productSum = ii[0]
    restOfDigits = ii[1:]
    if isThereAWay2(productSum, restOfDigits):
        summa2.append(productSum)
        goodString = f"{productSum}:{restOfDigits}"
        goodList2.append(goodString)
    else:
        badString = f"{productSum}:{restOfDigits}"
        badList2.append(badString)
        badda2.append(ii)

end2 = time.time()

df2 = pd.DataFrame(goodList2)
badDF2 = pd.DataFrame(badList2)


print(f"Part2: Sum of all good row: {sum(summa) + sum(summa2)}")
print(f"Time taken = {round((end2 - start2), 2)}")
