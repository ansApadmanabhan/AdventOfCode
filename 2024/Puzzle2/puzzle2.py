import pandas

with open(r"/\\Puzzle2\\input.txt") as infile:
    data = infile.readlines()


masterList = []
for line in data:
    ss = line.split(" ")
    ss = [int(ii) for ii in ss]
    masterList.append(ss)


def difLessThan3(listOfInts):
    for index, ii in enumerate(listOfInts):
        if index != len(listOfInts) - 1:
            if abs(listOfInts[index+1] - ii) > 3:
                return False
    return True


def isValid(listOfInts):
    if listOfInts[-1] == listOfInts[-2]:
        return False
    isIncreasing = True if listOfInts[-1] > listOfInts[-2] else False
    for index, ii in enumerate(listOfInts):
        if index != len(listOfInts) - 1:
            if isIncreasing:
                if listOfInts[index+1] <= ii:
                    return False
            else:
                if listOfInts[index+1] >= ii:
                    return False
    return True


safeList = []
for list1 in masterList:
    if difLessThan3(list1) and isValid(list1):
        safeList.append(list1)
    else:
        for index, ii in enumerate(list1):
            newList = list1.copy()
            newList.pop(index)
            if difLessThan3(newList) and isValid(newList):
                safeList.append(newList)
                break

lessThan3 = list(filter(difLessThan3, masterList))
moreThan3List = [ii for ii in masterList if ii not in lessThan3]
lessThan3New = []
for list1 in moreThan3List:
    for index, ii in enumerate(list1):
        newList = list1.copy()
        newList.pop(index)
        if difLessThan3(newList):
            lessThan3New.append(newList)
            break
        else:
            continue
safe1 = list(filter(isValid, lessThan3))
safe2 = list(filter(isValid, lessThan3New))
unSafeNow = [ii for ii in lessThan3 if ii not in safe1]
for list2 in unSafeNow:
    for index,ii in enumerate(list2):
        newList2 = list2.copy()
        newList2.pop(index)
        if isValid(newList2):
            safe2.append(list2)
            break
        else:
            continue


print(len(safe1 + safe2))