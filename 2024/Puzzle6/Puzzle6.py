import pandas as pd
import sys
import time

global GuardDirection, guard_location, distinct_positions, turning_locations, loop_checker

with open(r"input.txt", 'r') as infile:
    data = infile.readlines()

with open(r"smallInput.txt", 'r') as infile:
    data2 = infile.readlines()

df = pd.DataFrame(data)
orig_set = df.values.astype(str).view('U1')
set_without_newline = orig_set[:, :-1]

n_rows, n_cols = set_without_newline.shape

direction_Set = ['^', '>', 'v', '<']


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

def rotateGuardBy90():
    global GuardDirection
    indexOfDirection = direction_Set.index(GuardDirection)
    if indexOfDirection == 3:
        GuardDirection = '^'
    else:
        GuardDirection = direction_Set[indexOfDirection + 1]


def rotateGuardBy90Local(direction):
    indexOfDirection = direction_Set.index(direction)
    if indexOfDirection == 3:
        newdir = '^'
    else:
        newdir = direction_Set[indexOfDirection + 1]
    return newdir

def updatePositionTillGetsOut(direction, matrix):
    global guard_location, distinct_positions
    getsOut = False
    x, y = guard_location
    try:
        while str(matrix[x][y]) != '#':
            guard_location = [x, y]
            if [x, y] not in distinct_positions:
                distinct_positions.append([x, y])

            if x == 0 or y == 0:
                getsOut = True
                break
            if direction == '^':
                x -= 1
            elif direction == '>':
                y += 1
            elif direction == 'v':
                x += 1
            else:
                y -= 1

    except IndexError:
        print("Guard got out")
        getsOut = True

    return getsOut

def checkIfGuardIsStuck(direction, matrix, guardloc1, getsOut=False):
    global loop_checker
    if getsOut: return False
    x, y = guardloc1
    locLoop = []

    try:
        while str(matrix[x][y]) != '#':
            guardloc1 = [x, y]
            if [x, y] not in locLoop:
                locLoop.append([x, y])

            if x == 0 or y == 0:
                return True
            if direction == '^':
                x -= 1
            elif direction == '>':
                y += 1
            elif direction == 'v':
                x += 1
            else:
                y -= 1
        newDirection = rotateGuardBy90Local(direction)
        if locLoop in loop_checker:
            return False
        else:
            loop_checker.append(locLoop)
        getsOut = checkIfGuardIsStuck(newDirection, matrix, guardloc1, getsOut)

    except IndexError:
        getsOut = True

    return getsOut


def countRectangles(pointToCheck, points):
    numRects = 0
    x1, y1 = pointToCheck
    # Check  for diagonals
    for ii in range(len(points)):
        x2, y2 = points[ii]
        if x1 != x2 and y1 != y2:
            if [x1, y2] in points and [x2, y1] in points:
                numRects += 1

    return numRects

# Find the guard
for row in range(n_rows):
    for col in range(n_cols):
        if set_without_newline[row][col] in direction_Set:
            guard_location = [row, col]
            start_loc = [row, col]
            distinct_positions = [[row, col]]
            GuardDirection = set_without_newline[row][col]
            startDir = set_without_newline[row][col]

guarding = True
turning_locations = []
while guarding:
    gotOut = updatePositionTillGetsOut(GuardDirection, set_without_newline)
    if gotOut:
        guarding = False
    else:
        turning_locations.append(guard_location)
        rotateGuardBy90()

print(f"Number of distinct positions for guard: {len(distinct_positions)}")

stuck_location = []
g_locatoin = start_loc

timeStart = time.time()
for index in progressbar(range(len(distinct_positions) - 2),"Checking..."):
    guarding = True
    gdir = startDir
    newposition = distinct_positions[index + 2]
    if newposition[0] == start_loc[0] and newposition[1] == start_loc[1]:
        print("can't place here")
    else:
        loop_checker = []
        x,y = newposition
        oldVal = set_without_newline[x][y]
        set_without_newline[x][y] = '#'
        gotOut = checkIfGuardIsStuck(gdir,set_without_newline, g_locatoin)
        if gotOut:
            pass
        else:
            stuck_location.append([x, y])
        set_without_newline[x][y] = oldVal
timeEnd = time.time()

print(f"Number of loops possible for guard: {len(stuck_location)} and took {round((timeEnd - timeStart), 2)}s")

