from collections import defaultdict

data = []
with open(r"input.txt", 'r') as infile:
    for ii in infile.readlines():
        nl = ii.rsplit()[0]
        line = [int(jj) for jj in nl]
        data.append(line)


locationLookUpMap = defaultdict(list)
for indexi, ii in enumerate(data):
    for indexj, jj in enumerate(ii):
        locationLookUpMap[jj].append([indexi, indexj])


def isThereAGoodContinuation(currentLocation, currentValue, path=None,subCounter=0):
    if path is None:
        path = []
    continuation = False
    if currentValue == 9:
        return True, path
    x,y = currentLocation
    locationsToMatch1 = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]

    locationsOfNextVal = locationLookUpMap[currentValue + 1]
    matchedLocation = []
    for ii in locationsOfNextVal:
        if ii in locationsToMatch1:
            matchedLocation.append(ii)

    if len(matchedLocation) == 0:
        return False, path
    else:
        # Create branching dicts

        for kk in matchedLocation:
            continuation, path = isThereAGoodContinuation(kk, currentValue + 1, path)
            if continuation:
                path += [{currentValue + 1: kk}]

    return continuation, path


# Possible Trails
totalTrails = []
trailEnd = locationLookUpMap[0]
for endLoc in trailEnd:
    startPath = [{0: endLoc}]
    goodTrail, path = isThereAGoodContinuation(endLoc, 0, startPath)
    totalTrails.append(path)

# Count how many times 9 comes up.
# Unique Nines
summa = 0
for trail in totalTrails:
    loc9 = []
    for loc in trail:
        for key, value in loc.items():
            if key == 9 and value not in loc9:
                loc9.append(value)
                summa += 1




summa2 = 0
for jj in totalTrails:
    numNines = len([kk for kk in jj if list(kk.keys())[0] == 9])
    summa2 += numNines
print(f"Part 1: {summa}")
print(f"Part 2: {summa2}")