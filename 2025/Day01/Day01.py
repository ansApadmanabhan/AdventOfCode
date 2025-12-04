import pathlib
import re
# from Lib import regex
def read_input(filename):
    pathToText = f"{pathlib.Path(__file__).parent}/{filename}"
    with open(pathToText) as infile:
        data = infile.readlines()
    
    masterList = []
    for ii in data:
        masterList.append(ii.rstrip('\n'))
    return masterList

inputText = read_input(filename="2025_1.txt")

def solve_p1(input):
    start = 50
    stringMatcher = re.compile(r"([A-Z])(\d+)")
    count = 0
    for ii in input:
        matchGroup = stringMatcher.search(ii)
        if matchGroup is None:
            print(f"Did not find {ii}")
        if matchGroup[1] == "L":
            start = (start - int(matchGroup[2])) % 100
        else:
            start = (start + int(matchGroup[2])) % 100
        
        if start == 0:
            count += 1
    return count

def solve_p2(input):
    start = 50
    stringMatcher = re.compile(r"([A-Z])(\d+)")
    count = 0
    for ii in input:
        previousStart = start
        matchGroup = stringMatcher.search(ii)
        if matchGroup is None:
            print(f"Did not find {ii}")
        if matchGroup[1] == "L":
            currentStep = start - int(matchGroup[2])
            start = (currentStep) % 100
        else:
            currentStep = start + int(matchGroup[2])
            start = (start + int(matchGroup[2])) % 100
        
        if previousStart == 0:
            count += abs(currentStep)//100
            
            continue
            

        if 0 < abs(currentStep) < 100:
            # Check if it crosses
            if currentStep != start:
                count += 1
        else:
            if abs(currentStep) == 0:
                count+=1
            else:
                count += abs(currentStep)// 100
                if currentStep < 0:
                    count += 1
        
        
    return count


# print(solve_p1(inputText))
print(solve_p2(inputText))
    

