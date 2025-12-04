import pathlib
import collections

def read_input(filename):
    pathToText = f"{pathlib.Path(__file__).parent}/{filename}"
    with open(pathToText) as infile:
        data = infile.readlines()
    
    masterList = []
    for ii in data:
        masterList.append(ii.rstrip('\n'))
    return masterList

inputText = read_input(filename="2025_3.txt")

def get_max_val(inputLine):
    digit_list = list(inputLine)
    sorted_list= digit_list.copy()
    sorted_list.sort(key=lambda x: int(x), reverse=True)
    max_val = sorted_list[0]
    second_max_val = sorted_list[1]
    index_of_max = digit_list.index(max_val)
    index_of_second_max = digit_list.index(second_max_val)

    if index_of_max > index_of_second_max:
        if index_of_max == len(digit_list) - 1: # if it is the last digit
            return int(second_max_val + max_val)
        else:
            smaller_list = digit_list[index_of_max+1:]
            for ii in range(2, len(sorted_list)):
                val_to_check = sorted_list[ii]
                if val_to_check in smaller_list:
                    return int(max_val + val_to_check)
    else:
        return int(max_val+second_max_val)
    


    
def get_max_val2(input_line, search_limit=12):
    if len(input_line) == search_limit:
        return input_line
    digit_list = list(input_line)
    sorted_list= digit_list.copy()
    sorted_list.sort(key=lambda x: int(x), reverse=True)
    max_val = sorted_list[0]
    index_of_max = digit_list.index(max_val)
    search_limit_to_send = search_limit - 1
    if search_limit_to_send == 0:
        return max_val
    left_list = digit_list[:index_of_max]
    right_list = digit_list[index_of_max+1:]
    if len(right_list) >= search_limit_to_send:
        input_string = ''.join(right_list)
        newVal = max_val + get_max_val2(input_string, search_limit_to_send)
        return newVal
    search_limit_to_send_left = search_limit_to_send - len(right_list)
    newVal = get_max_val2(''.join(left_list), search_limit_to_send_left) + max_val
    search_limit_to_send_right = search_limit_to_send - search_limit_to_send_left
    if search_limit_to_send_right != 0:
        newVal = newVal + get_max_val2(''.join(right_list), search_limit_to_send_right)
    
    return newVal
    


def solve_p1(inputLines):
    total_sum = 0
    for ii in inputLines:
        total_sum += get_max_val(ii)
    return total_sum

def solve_p2(input_lines):
    total_sum = 0
    for ii in input_lines:
        total_sum += int(get_max_val2(ii))
    return total_sum

print(solve_p2(inputText))
        