import re
from functools import cache
import pandas as pd
from tabulate import tabulate
from collections import defaultdict
inputToImport = "input.txt"


class Robot:
    def __init__(self, X, Y, Vx, Vy):
        self.initPosX = X
        self.initPosY = Y
        self.velX = Vx
        self.velY = Vy
        self.curPosX = X
        self.curPosY = Y
        self._curTime = 0

    @property
    def curTime(self):
        return self._curTime

    @curTime.setter
    def curTime(self,value):
        self._curTime = value
        self.curPosX, self.curPosY = calculateMovement(self.initPosX, self.initPosY,
                                                       self.velX, self.velY, value)

    def __str__(self):
        return f"{self.curPosX}, {self.curPosY}"


robotList = []
with open(inputToImport, 'r') as infile:
    for jj in infile.readlines():
        exp = re.compile("p=(.*),(.*) v=(.*),(.*)")
        vals = exp.findall(jj.rstrip())
        x, y, Vx, Vy = [int(ii) for ii in vals[0]]
        robot = Robot(x, y, Vx, Vy)
        robotList.append(robot)



## Bounds
xLower = 0
yLower = 0
xHigher = 101
# xHigher = 11
yHigher = 103
# yHigher = 7


@cache
def calculateMovement(iX, iY, vX, vY, time):
    calculatedX = iX + (vX * time)
    calculatedY = iY + (vY * time)
    gridx = divmod(calculatedX, xHigher)[1]
    gridY = divmod(calculatedY, yHigher)[1]
    return gridx, gridY


quadx = (xHigher - 1)/2
quady = (yHigher - 1)/2

def calculateSF(listOfrobots):
    quad1 = []
    quad2 = []
    quad3 = []
    quad4 = []
    for rb in listOfrobots:
        if rb.curPosX < quadx and rb.curPosY > quady:  # Quadrant 1
            quad1.append([rb.curPosX, rb.curPosY])
        elif rb.curPosX > quadx and rb.curPosY > quady:  # Quadrant 2
            quad2.append([rb.curPosX, rb.curPosY])
        elif rb.curPosX < quadx and rb.curPosY < quady:  # Quadrant 3
            quad3.append([rb.curPosX, rb.curPosY])
        elif rb.curPosX > quadx and rb.curPosY < quady:  # Quadrant 4
            quad4.append([rb.curPosX, rb.curPosY])

    sf = len(quad1) * len(quad2) * len(quad3) * len(quad4)
    return sf


for ii in robotList:
    # set curTime for all robots to 100 seconds
    ii.curTime = 100

sf = calculateSF(robotList)
print(f"{sf = }")

def areTheyAllTogether(listOfRobots):
    together = False
    getcurLocs = []
    for rb in listOfRobots:
        getcurLocs.append([rb.curPosX, rb.curPosY])

    totalInGroup = 0
    xFreqList = defaultdict(int)
    yFreqList = defaultdict(int)
    for ii in getcurLocs:
        x, y = ii
        xFreqList[x] += 1
        yFreqList[y] += 1
    xSort = sorted(xFreqList.items(), key=lambda ff: ff[1], reverse=True)
    ySort = sorted(yFreqList.items(), key=lambda ss: ss[1], reverse=True)

    densityToCheck = 50
    newX = []
    newY = []
    sumX = 0
    sumY = 0
    for ii in xSort:
        if sumX < densityToCheck:
            newX.append(ii[0])
            sumX += ii[1]
        else:
            break
    for ii in ySort:
        if sumY < densityToCheck:
            newY.append(ii[0])
            sumY += ii[1]
        else:
            break

    togetherNessX = max(newX) - min(newX)
    togetherNessY = max(newY) - min(newY)
    togetherNess = togetherNessX * togetherNessY
    if togetherNess <= 50:
        together = True



    return together



def isSymmetricalY(dataF):
    vertical = True
    N, M = dataF.shape
    i = 0
    k = M - 1
    while i < M // 2:

        # Checking each cell of a row.
        for j in range(N):

            # check if every cell is identical
            if dataF[i][j] != dataF[k][j]:
                vertical = False
                break
        i += 1
        k -= 1
    return vertical


def createGrid(listfRobots, time):
    gridLine = [['' for kk in range(xHigher)] for jj in range(yHigher)]
    for rb in listfRobots:
        rb.curTime = time
        gridLine[rb.curPosY][rb.curPosX] = '1'
    df = pd.DataFrame(gridLine)
    print(tabulate(df, tablefmt="psq1"))


sflist = []
for ii in range(1, 5000):
    for rb in robotList:
        rb.curTime = ii
    sf = calculateSF(robotList)
    sflist.append({'index': ii,
                   'sf': sf})


sortedSF = sorted(sflist, key=lambda x: x['sf'])


print("done")



