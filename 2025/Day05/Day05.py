import pathlib

def read_input(filename):
    pathToText = f"{pathlib.Path(__file__).parent}/{filename}"
    with open(pathToText) as infile:
        data = infile.readlines()
    
    ranges_limit = []
    item_ids = []
    indexOfNL = data.index('\n')

    for idx, ii in enumerate(data):
        if idx < indexOfNL:
            ranges_limit.append([jj.rstrip() for jj in list(ii.split('-'))])
        elif idx == indexOfNL:
            continue
        else:
            item_ids.append(int(ii.rstrip()))

    
    return ranges_limit, item_ids


ranges, itemList = read_input("2025_5.txt")

def solve_p1(ranges, items):
    int_ranges = []
    for idx, ii in enumerate(ranges):
        num1,num2 = int(ii[0]), int(ii[1])
        int_ranges.append([num1, num2])
        max_of = max([num1, num2])
        min_of = min([num1, num2])
        if idx == 0:
            min_ = min_of
            max_ = max_of
        else:
            if max_of > max_:
                max_ = max_of
            if min_of < min_:
                min_ = min_of

        int_ranges.append([min_of, max_of])

    total = 0
    for jj in items:
        if jj < min_ or jj > max_:
            continue
        for kk in int_ranges:
            if kk[0] <= jj <= kk[1]:
                total += 1
                break

    return total

def solve_p2(rangesList):
    int_ranges = []
    for ii in rangesList:
        ii.sort(key=lambda x: int(x)) 
        int_ranges.append([int(ii[0]), int(ii[1])])
    
    total = 0
    int_ranges.sort(key=lambda x: x[0])
    for idx, jj in enumerate(int_ranges):
        x,y = jj
        if idx == 0:
            total += y-x + 1
            xp, yp = x, y
        else:
            if (x > yp and y > yp): # no overlap
                total += y - x + 1
                xp, yp = x, y
            elif x == xp and y == yp: # complete overlap
                continue
            elif y > yp:
                total += (y - yp)
                yp = y
            elif y < yp:
                continue

    return total



print(solve_p2(ranges))

        

