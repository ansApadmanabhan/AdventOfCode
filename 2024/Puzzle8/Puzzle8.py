from collections import defaultdict
import itertools

import pandas as pd
import sys
import time

with open(r"input.txt", 'r') as infile:
    data = infile.readlines()

with open(r"smallInput.txt", 'r') as infile:
    data2 = infile.readlines()

df = pd.DataFrame(data)
orig_set = df.values.astype(str).view('U1')
set_without_newline = orig_set[:, :-1]
n_rows, n_cols = set_without_newline.shape

xLowerBound = 0
xUpperBound = n_rows - 1
yLowerBound = 0
yUpperBound = n_cols - 1


def isInBounds(point, xlower=xLowerBound, xhigher=xUpperBound, ylower=yLowerBound, yhigher=yUpperBound):
    x,y = point
    if xlower <= x <= xhigher and ylower <= y <= yhigher:
        return True
    return False

# Create a lookup tabl
lookUp = defaultdict(list)
for indexR, row in enumerate(set_without_newline):
    for indexC, col in enumerate(row):
        if col != '.':
            lookUp[col].append([indexR, indexC])


antiNodeLocations = []
for key,values in lookUp.items():
    # Get Combinations
    combs = list(itertools.combinations(values, 2))
    for line in combs:
        ((x1, y1), (x2, y2)) = line
        xDist = x2 - x1
        yDist = y2 - y1
        antiX1, antiY1 = x1 - xDist, y1 - yDist
        antiX2, antiY2 = x2 + xDist, y2 + yDist
        if xLowerBound <= antiX1 <= xUpperBound and yLowerBound <= antiY1 <= yUpperBound:
            if [antiX1, antiY1] not in antiNodeLocations:
                antiNodeLocations.append([antiX1, antiY1])
        if xLowerBound <= antiX2 <= xUpperBound and yLowerBound <= antiY2 <= yUpperBound:
            if [antiX2, antiY2] not in antiNodeLocations:
                antiNodeLocations.append([antiX2, antiY2])

print(f"Part1: Number of antinodes :{len(antiNodeLocations)}")

# Part 2

antiNodeLocations2 = []
for key,values in lookUp.items():
    # Get Combinations
    combs = list(itertools.combinations(values, 2))
    for line in combs:
        inBoundFirstDir = True
        inBoundSecondDir = True
        counterDir1 = 1
        counterDir2 = 1
        ((x1, y1), (x2, y2)) = line
        xDist = x2 - x1
        yDist = y2 - y1
        if [x1, y1] not in antiNodeLocations2:
            antiNodeLocations2.append([x1, y1])
        if [x2, y2] not in antiNodeLocations2:
            antiNodeLocations2.append([x2, y2])
        while inBoundFirstDir:
            antiX1, antiY1 = x1 - (xDist * counterDir1), y1 - (yDist * counterDir1)
            boundStill = isInBounds([antiX1, antiY1])
            if boundStill and [antiX1, antiY1] not in antiNodeLocations2:
                antiNodeLocations2.append([antiX1, antiY1])
            counterDir1 += 1
            if not boundStill:
                inBoundFirstDir = False
        while inBoundSecondDir:
            antiX2, antiY2 = x2 + (xDist * counterDir2), y2 + (yDist * counterDir2)
            boundStill = isInBounds([antiX2, antiY2])
            if boundStill and [antiX2, antiY2] not in antiNodeLocations2:
                antiNodeLocations2.append([antiX2, antiY2])
            counterDir2 += 1
            if not boundStill:
                inBoundSecondDir = False

print(f"Part2: Number of antinodes :{len(antiNodeLocations2)}")

