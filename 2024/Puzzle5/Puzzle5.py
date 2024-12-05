rules = []
order = []
with open(r"input.txt", 'r') as infile:
    collectRule = True
    for ii in infile.readlines():
        if ii == "\n":
            collectRule = False
            continue
        if collectRule:
            rules.append([int(jj) for jj in ii.split('|')])
        else:
            order.append([int(jj) for jj in ii.split(',')])

rules2 = []
order2 = []
with open(r"smallInput.txt", 'r') as infile:
    collectRule = True
    for ii in infile.readlines():
        if ii == "\n":
            collectRule = False
            continue
        if collectRule:
            rules2.append([int(jj) for jj in ii.split('|')])
        else:
            order2.append([int(jj) for jj in ii.split(',')])


ruleToCheck = rules
orderToCheck = order


def listSorter(numList, rulesOfOrder):
    sortedlist = [0 for jj in numList]
    for number in numList:
        indexGet = 0
        subOrder = [ff for ff in numList if ff != number]
        for subNum in subOrder:
            if [number, subNum] not in rulesOfOrder:
                indexGet += 1
        sortedlist[indexGet] = number

    return sortedlist


middleSum = 0
incMiddleSum = 0
for rowId, ii in enumerate(orderToCheck):
    inCorrectRow = ii.copy()
    breakFlag = False
    rowLength = len(ii)
    for indexJ in range(rowLength):
        subrow = ii[indexJ + 1: rowLength]
        for indexK, kk in enumerate(subrow):
            if [ii[indexJ], kk] not in ruleToCheck:
                breakFlag = True

    middleIndex = int((rowLength - 1) / 2)
    if breakFlag:
        sortedStuff = listSorter(inCorrectRow, ruleToCheck)
        incMiddleSum += sortedStuff[middleIndex]
    else:
        middleSum += ii[middleIndex]

print(f"{middleSum}")
print(f"{incMiddleSum}")


# Part 2



