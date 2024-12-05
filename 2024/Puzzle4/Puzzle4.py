import pandas as pd
import numpy as np

with open(r"E:\AdventOfCode\pythonProject1\Puzzle4\input.txt", 'r') as infile:
    data = infile.readlines()

with open(r"E:\AdventOfCode\pythonProject1\Puzzle4\smallInput.txt", 'r') as infile:
    data2 = infile.readlines()


def wordCounter(words, matrix):
    total_count = 0
    for word in words:
        for row in matrix:
            one_word = ''.join(row)
            total_count += one_word.count(word)
    return total_count


wordList = ['XMAS', 'SAMX']
df = pd.DataFrame(data)
orig_set = df.values.astype(str).view('U1')
set_without_newline = orig_set[:, :-1]

n_rows, n_cols = set_without_newline.shape

# search columns
column_transpose = set_without_newline.transpose()


# Search diagonals
# Create a new array of zeros
holder_matrix = np.zeros((n_rows, 2 * n_cols - 1), dtype='U1')
holder_matrix[:, : n_cols] = set_without_newline

# forward and backward diagonal matrices
fdiag_matrix = np.zeros((n_rows, 2 * n_cols - 1), dtype='U1')
bdiag_matrix = np.zeros((n_rows, 2 * n_cols - 1), dtype='U1')


for index, row in enumerate(holder_matrix):
    forward_row = np.roll(row,index)
    backward_row = np.roll(row,n_cols - 1 - index)
    fdiag_matrix[index] = forward_row
    bdiag_matrix[index] = backward_row

fdiag_matrix_tr = fdiag_matrix.transpose()
bdiag_matrix_tr = bdiag_matrix.transpose()

# Search rows, columns, forward diagonals, backward diagonals
XMAS_row_count = wordCounter(wordList, set_without_newline)
XMAS_column_count = wordCounter(wordList, column_transpose)
XMAS_fdiag_count = wordCounter(wordList, fdiag_matrix_tr)
XMAS_bdiag_count = wordCounter(wordList, fdiag_matrix_tr)
print(f"{XMAS_bdiag_count + XMAS_fdiag_count + XMAS_column_count+ XMAS_row_count}")

# Part 2
newWordList = ['MAS', 'SAM']
p2_holder_matrix = np.zeros((2 * n_cols - 1, n_rows), dtype='U1')
new_n_row, new_n_col = p2_holder_matrix.shape
counter = 0
for row_id in range(n_rows):
    for col_id in range(n_cols):
        if row_id == 0 or col_id == 0 or row_id == n_rows -1 or col_id == n_cols -1:
            continue
        else:
            npVal = set_without_newline[row_id][col_id]
            x = row_id
            y = col_id
            if str(npVal) == "A":
                diag1 = ''.join([str(set_without_newline[x-1][y-1]),
                                 str(set_without_newline[x][y]),
                                 str(set_without_newline[x+1][y+1])])
                diag2 = ''.join([str(set_without_newline[x+1][y-1]),
                                 str(set_without_newline[x][y]),
                                 str(set_without_newline[x-1][y+1])])

                if diag1 in newWordList and diag2 in newWordList:
                    counter += 1


print(f"{counter}")