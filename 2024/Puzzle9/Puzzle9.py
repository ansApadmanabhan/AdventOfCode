# First spread out the input

digitList = []
chunkList = []
fileTocheck = "input.txt"
with open(fileTocheck) as infile:
    input1 = infile.readlines()[0]  # There is only one line
    longStr = ''
    counter = 0
    spaceCounter = 0
    for index, ii in enumerate(input1):
        if index == 0 or index % 2 == 0:  # Even index
            if int(ii):
                inp = str(counter)*int(ii)
                digitList.extend([counter for jj in range(int(ii))])
                chunkList.append([counter for jj in range(int(ii))])
                counter += 1
        else:
            inp = str('.')*int(ii)
            digitList.extend([None for kk in range(int(ii))])
            if int(ii):  # If ii is not 0
                chunkList.append([None for kk in range(int(ii))])
        longStr += inp


# Part 1
# Convert to list of str
strList = [ii for ii in longStr]
copyList = list(reversed(digitList.copy()))
newList = [0 for ii in range(len(digitList))]

numberOfDigits = sum([1 for ii in digitList if ii is not None])


def findInCopyList(listToCheck, startIt):
    for ii in range(startIt, len(listToCheck)):
        if listToCheck[ii] is not None:
            return listToCheck[ii], ii+1


index2 = 0
for ii2 in range(numberOfDigits):
    if digitList[ii2] is None:
        newList[ii2], index2 = findInCopyList(copyList, index2)
    else:
        newList[ii2] = digitList[ii2]

# print(f"{''.join(newList)}")

# Add up index * number
summa = sum([ii*index for index, ii in enumerate(newList) if ii is not None])

print(f"Part 1: Product Sum = {summa}")


def isChunkNone(chunk):
    for ii in chunk:
        if ii is None:
            return True
        return False


# Part 2
def findIndexWhereChunkCanFit(chunk, masterList:list):
    space = len(chunk)
    indexForChange = None
    for index, element in enumerate(masterList):
        if isChunkNone(element):
            sizeOfChunk = len(element)
            if space <= sizeOfChunk:
                indexForChange = index
                break
    return indexForChange


def compressNones(copyList):
    newList = []
    collectNones = []
    for ii in copyList:
        if isChunkNone(ii):
            collectNones += ii
        else:
            newList.append(collectNones)
            newList.append(ii)
            collectNones = []
    if len(collectNones) > 0: newList.append(collectNones)
    # Remove empties
    returnList = [ii for ii in newList if len(ii) != 0]
    return returnList


reverseChunkList = list(reversed(chunkList.copy()))
reverseChunkListClean = [ii for ii in reverseChunkList if not isChunkNone(ii)]
copyDigit = chunkList.copy()
for index, chunk in enumerate(reverseChunkListClean):
    indexToChange = findIndexWhereChunkCanFit(chunk, copyDigit)
    if indexToChange is None:
        continue
    else:
        indexToPad = copyDigit.index(chunk)
        if indexToChange > indexToPad:  # only look to fill spots to the left
            continue
        else:
            emptySpaceLen = len(copyDigit[indexToChange])
            diff = emptySpaceLen - len(chunk)
            copyDigit[indexToChange] = chunk
            rightPadNone = [None for ee in range(len(chunk))]
            copyDigit[indexToPad] = rightPadNone

        if diff:
            newNone = [None for dd in range(diff)]
            copyDigit = copyDigit[:indexToChange+1] + [newNone] + copyDigit[indexToChange+1:]
        copyDigit = compressNones(copyDigit)
unchunkify = []
for ii in copyDigit:
    unchunkify += ii

summa2 = sum([ii*index for index, ii in enumerate(unchunkify) if ii is not None])
print(f"Part 2: Sum of stuff is {summa2}")