import numpy as np
from sympy import symbols, Eq, solve, core
import re
from decimal import Decimal
inputToImport = "input.txt"

class Button(object):
    def __init__(self, x, y):
        self.xInc = x
        self.yInc = y


class ClawMachine(object):
    def __init__(self):
        self.prizeX = None
        self.prizeY = None
        self.buttonA = None
        self.buttonB = None


    def calculateResult(self):
        # x, y = symbols('x,y')
        # eq1 = Eq((self.buttonA.xInc*x + self.buttonB.xInc*y), self.prizeX)
        # eq2 = Eq((self.buttonA.yInc*x + self.buttonB.yInc*y), self.prizeY)
        # res = solve((eq1, eq2), (x, y))
        A = np.array([[self.buttonA.xInc, self.buttonB.xInc],
                      [self.buttonA.yInc, self.buttonB.yInc]])
        rhs = np.array([self.prizeX, self.prizeY])

        # a_inv = np.linalg.inv(A)
        res = np.linalg.solve(A, rhs)
        return res

counter = 0
clawMachines = []
claw = None
with open(inputToImport, 'r') as infile:
    for jj in infile.readlines():
        if jj == '\n':
            clawMachines.append(claw)
            counter += 1
            claw = ClawMachine()
            continue
        else:
            if claw is None:
                claw = ClawMachine()
            exp = re.compile("Button (.*): X\+(.*), Y\+(.*)")
            prizeExp = re.compile("Prize: X=(.*), Y=(.*)")
            button = exp.findall(jj.rstrip())
            prizeLoc = prizeExp.findall(jj.rstrip())
            if button:
                butt, x, y = button[0]
                if butt == 'A':
                    butA = Button(int(x), int(y))
                    claw.buttonA = butA
                else:
                    butB = Button(int(x), int(y))
                    claw.buttonB = butB
            elif prizeLoc:
                prX, prY = prizeLoc[0]
                prX = int(prX) + 10000000000000
                prY = int(prY) + 10000000000000
                claw.prizeX = int(prX)
                claw.prizeY = int(prY)

    # add the last claw machine
    clawMachines.append(claw)

sumCalculation = 0
for ii in clawMachines:
    res = ii.calculateResult()
    # xTimes, yTimes = list(res.values())
    xTimes, yTimes = res
    xInt = round(xTimes)
    yInt = round(yTimes)
    xAbsDif = abs(xTimes - xInt)
    yAbsDif = abs(yTimes - yInt)
    # xCorrect = isinstance(xTimes, core.numbers.Integer)
    # yCorrect = isinstance(yTimes, core.numbers.Integer)
    # if not xCorrect or not yCorrect or xTimes < 0 and yTimes < 0:
    #     continue
    if xAbsDif > 1e-4 or yAbsDif > 1e-4 or xTimes < 0 or yTimes < 0:
        continue
    else:
        sumCalculation += (int(xTimes) * 3) + (int(yTimes) * 1)

print(f"{sumCalculation = }")
