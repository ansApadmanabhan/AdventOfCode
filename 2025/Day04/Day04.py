import pandas as pd
import pathlib
from numpy.lib.stride_tricks import sliding_window_view


def read_input(filename):
    pathToText = f"{pathlib.Path(__file__).parent}/{filename}"
    with open(pathToText) as infile:
        data = infile.readlines()
    
    masterList = []
    for ii in data:
        masterList.append(list(ii.rstrip('\n')))
    return masterList

data = read_input("2025_4.txt")


df = pd.DataFrame(data)
df.replace(to_replace=['.', "@"], value=[0,1], inplace=True)


def get_2d_window(matrix, windowSize):
    window = sliding_window_view(matrix, windowSize)
    return window
    


def solve_p1(input:pd.DataFrame, window_size=1, limit=3, update=False):
    summa = 0
    x,y = input.shape
    for i  in range(x):
        for j in range(y):
            begin_x = i - 1 if i else 0
            end_x = i + 2 if i < input.shape[1] else 0
            begin_y = j - 1 if j else 0
            end_y = j + 2 if j < input.shape[0] else 0

        
            if input.iloc[i,j] == 1:
                slice_window = input.iloc[begin_x: end_x, begin_y:end_y]
                total = slice_window.values.sum() - 1
                if total <= 3:
                    summa += 1
                    if update:
                        input.iloc[i,j] = 0
    return summa

def solve_p2(input:pd.DataFrame):
    output = 1
    summa = 0
    while output != 0:
        output = solve_p1(input, update=True)
        summa += output

    return summa


print(solve_p2(df))
    


