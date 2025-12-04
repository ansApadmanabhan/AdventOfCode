import pathlib
import re
def read_input(filename):
    pathToText = f"{pathlib.Path(__file__).parent}/{filename}"
    with open(pathToText) as infile:
        data = infile.readlines()
    return data

inputText = read_input(filename="2025_2.txt")

def find_valid_ids(range_start, range_end):
    start_digits = len(range_start)
    end_digits = len(range_end)
    valid_ids = []
    if start_digits % 2 and end_digits % 2 and (start_digits == end_digits): # both have same odd number of digits
        return valid_ids
    
    split_start_digits = ''.join(range_start[:int(start_digits/2)])
    split_start_int = int(split_start_digits) if split_start_digits != '' else 0
    to_check = str(split_start_int)*2
    while int(to_check) <= int(range_end):
        if int(to_check) < int(range_start):
            pass
        else:
            valid_ids.append(to_check)
        split_start_int += 1
        to_check = str(split_start_int)*2

    return valid_ids


def find_valid_ids_2(range_start, range_end):
    valid_ids = []
    search_term = re.compile(r"\b(\d+)\1+\b")
    int_range_start = int(range_start) if range_start != '' else 0
    int_range_end = int(range_end) if range_end != '' else 0
    for ii in range(int_range_start, int_range_end+1):
        if search_term.search(str(ii)):
            valid_ids.append(str(ii))

    return valid_ids


        
    
    
    
    

def solve_p1(input):
    # clean input
    input= input[0]
    ranges = input.split(",")
    valid_ids = []
    for ii in ranges:
        range_split = ii.split("-")
        range_start = range_split[0]
        range_end = range_split[1]
        valid_ids.extend(find_valid_ids(range_start, range_end))

    sum_ids = sum(int(ii) for ii in valid_ids)

        

    return sum_ids

def solve_p2(input):
    input= input[0]
    ranges = input.split(",")
    valid_ids = []
    for ii in ranges:
        range_split = ii.split("-")
        range_start = range_split[0]
        range_end = range_split[1]
        valid_ids.extend(find_valid_ids_2(range_start, range_end))

    sum_ids = sum(int(ii) for ii in valid_ids)

        

    return sum_ids



print(solve_p2(inputText))