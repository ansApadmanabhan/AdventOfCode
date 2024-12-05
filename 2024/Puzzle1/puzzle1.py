from collections import Counter

def readInput(filename, delimiter, forceFormat: type):

    with open(filename) as infile:
        data = infile.readlines()
    numberOfColumns = len(data[0].split("   "))
    masterList = [[] for ii in range(numberOfColumns)]
    for line in data:
        ss = line.split("   ")
        for ii in range(numberOfColumns):
            masterList[ii].append(forceFormat(ss[ii]))
    return masterList


checkData = readInput(filename="input.txt",
                      delimiter="   ", forceFormat=int)

firstList = checkData[0]
secondList = checkData[1]

firstList.sort()
secondList.sort()

summ = 0
for ii in range(len(firstList)):
    summ += abs(firstList[ii] - secondList[ii])

print(summ)

similarity = 0
countedDict = Counter(secondList)
for ii in range(len(firstList)):
    similarityCheck = 0 if firstList[ii] not in countedDict.keys() else firstList[ii]*countedDict[firstList[ii]]

    similarity += similarityCheck

print(similarity)