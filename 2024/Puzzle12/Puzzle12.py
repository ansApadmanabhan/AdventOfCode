from collections import defaultdict
from functools import cache

import numpy as np
import pandas as pd
import sys
import time

inputToCheck = "input.txt"

dataToPass = []
with open(inputToCheck, 'r') as infile:
    data = infile.readlines()
    for index, row in enumerate(data):
        rLine = row.rstrip()
        newLine = []
        for jj in rLine:
            newLine += ['.', jj]
        newLine += ['.']
        emptyRow = ['.' for kk in range(len(newLine))]
        dataToPass.append(emptyRow)
        dataToPass.append(newLine)
dataToPass.append(emptyRow)

df = pd.DataFrame(dataToPass)
anotherDF = pd.DataFrame(data)
orig_set = anotherDF.values.astype(str).view('U1')
set_without_newline = orig_set[:, :-1]
n_rows, n_cols = df.shape

# bounds
xLower = 1
yLower = 1
xHigher = n_rows - 1
yHigher = n_cols - 1

valDict = {}
counter = 1


def updateDF(x, y, val):
    getVal = df[x][y]
    if getVal.isdigit():
        setVal = f"{getVal}|{val}"
    else:
        setVal = f"{val}"
    df.loc[y, x] = setVal


def getPerimeter(x, y, val):
    lpm, rpm, upm, bpm = True, True, True, True
    LIndex, rIndex, uIndex, bIndex = [x - 2, y], [x + 2, y], [x, y + 2], [x, y - 2]
    x1, y1 = LIndex
    x2, y2 = rIndex
    x3, y3 = uIndex
    x4, y4 = bIndex
    if 0 < x1 < xHigher and 0 < y1 < yHigher:
        valToCheck = df[x1][y1]
        if val == valToCheck:
            lpm = False
    if 0 < x2 < xHigher and 0 < y2 < yHigher:
        valToCheck = df[x2][y2]
        if val == valToCheck:
            rpm = False
    if 0 < x3 < xHigher and 0 < y3 < yHigher:
        valToCheck = df[x3][y3]
        if val == valToCheck:
            bpm = False
    if 0 < x4 < xHigher and 0 < y4 < yHigher:
        valToCheck = df[x4][y4]
        if val == valToCheck:
            upm = False
    return lpm, rpm, upm, bpm


perimeterTracker = defaultdict(int)
perimeterCounter = 0
areaTracker = defaultdict(list)
areaCounter = 0


def getRelevantAreaKey(listOfKeys, row, col):
    keyToReturn = None
    countToReturn = 0
    x, y = row, col

    for key in listOfKeys:
        countToReturn += 1
        CurrentAreaMap = areaTracker[key]
        if [x + 2, y] in CurrentAreaMap or [x - 2, y] in CurrentAreaMap or [x, y + 2] in CurrentAreaMap or [x,
                                                                                                            y - 2] in CurrentAreaMap:
            return key, countToReturn
        # Try next element on the right to find till the end
        # See if the next element is the same letter
    if y == yHigher - 1:
        return None, 0
    # if df.loc[y + 2, x] == df.loc[y, x]:
    #     keyToReturn, countToReturn = getRelevantAreaKey(listOfKeys, row, col + 2)

    return keyToReturn, countToReturn


for row in range(n_rows):
    if row == 0 or row % 2 == 0:
        continue
    for col in range(n_cols):
        if col == 0 or col % 2 == 0:
            continue
        valToCheck = df[row][col]
        if valToCheck in valDict.keys():
            pass
        else:
            valDict.update({valToCheck: str(counter)})
            counter += 1
        # Are there any area trackers with the letter
        relevantKey = [key for key, value in areaTracker.items() if valToCheck in key]
        if relevantKey:  # There are area trackers with similar letters
            # Check for keys where the current row column can extend
            keyTracker, keycounter = getRelevantAreaKey(relevantKey, row, col)
            if keyTracker is None:
                keyTracker = f"{valToCheck}{keycounter}"
        else:
            keyTracker = f"{valToCheck}0"
        pLeft, pRight, pUp, pDown = getPerimeter(row, col, valToCheck)

        if pLeft:
            updateDF(row - 1, col, valDict[valToCheck])
            perimeterTracker[keyTracker] += 1
        if pRight:
            updateDF(row + 1, col, valDict[valToCheck])
            perimeterTracker[keyTracker] += 1
        if pUp:
            updateDF(row, col - 1, valDict[valToCheck])
            perimeterTracker[keyTracker] += 1
        if pDown:
            updateDF(row, col + 1, valDict[valToCheck])
            perimeterTracker[keyTracker] += 1
        areaTracker[keyTracker].append([row, col])

newAreaDict = defaultdict(list)
newPerimeterDict = defaultdict(int)


def MergeDict(keyName):
    countToReturn = 0
    relevantKeyMaster = [key for key, value in areaTracker.items() if keyName in key]
    for keyMaster in relevantKeyMaster:
        setToMain = False
        valueT = areaTracker[keyMaster]
        perimT = perimeterTracker[keyMaster]
        relevantKeyFollower = [key for key, value in newAreaDict.items() if keyName in key]
        if not relevantKeyFollower:
            keyTracker = f"{keyName}{countToReturn}"
            currentAreaMap = areaTracker[keyTracker]
            currentPerimeter = perimeterTracker[keyTracker]
            countToReturn += 1
            newAreaDict[keyTracker] += currentAreaMap
            newPerimeterDict[keyTracker] += currentPerimeter
        else:
            for keyT in relevantKeyFollower:
                extAreaMap = newAreaDict[keyT]
                for co_ord in valueT:
                    xC, yC = co_ord
                    if [xC + 2, yC] in extAreaMap or [xC - 2, yC] in extAreaMap or [xC, yC + 2] in extAreaMap or [
                        xC, yC - 2] in extAreaMap:
                        newAreaDict[keyT] += valueT
                        newPerimeterDict[keyT] += perimT
                        setToMain = True
                        break
            if not setToMain:
                newAreaDict[f"{keyName}{countToReturn}"] += valueT
                newPerimeterDict[f"{keyName}{countToReturn}"] += perimT
                countToReturn += 1


# Resolve the ones that did not convert properly
for key, value in valDict.items():
    MergeDict(key)

cost = 0
for key, value in newAreaDict.items():
    perimeter = newPerimeterDict[key]
    area = len(newAreaDict[key])
    cost += perimeter * area
print(f"{cost = }")
