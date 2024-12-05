import re

with open(r"E:\AdventOfCode\pythonProject1\Puzzle3\input.txt", 'r') as infile:
    data = infile.read()

summa = 0

searchTerm = re.compile("mul\(\s*\+?(-?\d+)\s*,\s*\+?(-?\d+)\s*\)")
returnList = list(searchTerm.findall(data))
for int1, int2 in returnList:
    summa += int(int1) * int(int2)

finddontdo = re.compile(r"don't\(\)(.*?)do\(\)")
newline = ''

findBetween = finddontdo.findall(data)
newString = re.sub(r'|'.join(map(re.escape, findBetween)), '', data)
finddontdont = re.compile(r"don't\(\)(.*?)don't\(\)")
findBetweendont = finddontdont.findall(newString)
newString2 = re.sub(r'|'.join(map(re.escape, findBetweendont)), '', newString)
newSum = 0
returnList2 = list(searchTerm.findall(newString2))
for int3, int4 in returnList2:
    newSum += int(int3) *int(int4)


pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
matches = re.findall(pattern, data)

result = 0
flag = True
for match in matches:
    if match == "do()":
        flag = True
    elif match == "don't()":
        flag = False
    else:
        if flag:
            x, y  = map(int, match[4:-1].split(','))
            result += x * y

print(newSum)
