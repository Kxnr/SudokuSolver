# number of variables is puzzle_width**2,
# assuming square puzzles, staring at 1
# var: row col val

# many thanks to Matt Zucker for his solution to a much more complicated
# problem in the same way
# https://github.com/mzucker/flow_solver/blob/master/pyflowsolver.py


# and to this stack overflow for saving me from thinking too hard
# https://stackoverflow.com/questions/2489435/python-check-if-a-number-is-a-perfect-square

import pycosat as sat
import numpy as np
import itertools
import sys

# please forgive the use of globals
puzzle_width = 9
grid_width = 3 

def pairs(sat_vars):
    return itertools.combinations(sat_vars, 2)

def no_two(sat_vars):
    return ((-a, -b) for (a, b) in pairs(sat_vars))

def exactly_one(sat_vars):
    clauses = []
    sat_vars = list(sat_vars)

    clauses = [sat_vars]
    clauses.extend(no_two(sat_vars))
    return clauses

def cell_var(row, col, val):
    return row*puzzle_width**2 + col*puzzle_width + val + 1

def unpack_satvar(sat_var):
    # consume from the right, zeroes as separators
    sat_var = sat_var - 1
    row = sat_var // 81
    sat_var = sat_var - 81*row

    col = sat_var // 9
    sat_var = sat_var - 9*col

    val = sat_var + 1
    return row, col, val

def cell_clauses(row, col, value=0):
    clauses = []
    sat_vars = list(cell_var(row, col, i) for i in range(puzzle_width))
    if value == 0:
        # cell can have only one value
        clauses.extend(exactly_one(sat_vars))
        
    else:
        # only value is true
        clauses.extend(((-cell_var(row, col, i),) for i in range(puzzle_width) if i+1 != value))
        clauses.append((cell_var(row, col, value-1),))

    return clauses

def row_clauses(row):
    # only one element in each row can have a given value
    clauses = []
    for i in range(puzzle_width):
        sat_vars = (cell_var(row, c, i) for c in range(puzzle_width))
        clauses.extend(exactly_one(sat_vars))
    return clauses

def col_clauses(col):
    # only one element in each column can have a given value
    clauses = []
    for i in range(puzzle_width):
        sat_vars = (cell_var(r, col, i) for r in range(puzzle_width))
        clauses.extend(exactly_one(sat_vars))
    return clauses

def grid_clauses(row, col):
    # only one element in each small grid can have a given value
    # takes top left corner of grid
    sat_vars = []
    clauses = []
    for i in range(puzzle_width):
        sat_vars = (cell_var(row+r, col+c, i) for c in range(grid_width) for r in range(grid_width))
        clauses.extend(exactly_one(sat_vars))
    return clauses

def parse_puzzle(puzzle_file):
    '''
    takes filename of puzzle and transforms it into an array

    blank squares are represented by 0
    '''

    puzzle = open(filename).read().splitlines()
    puzzle = [[int(a) for a in row.split()] for row in puzzle if not row == '']
    assert len(puzzle) == puzzle_width
    for row in puzzle:
        assert len(row) == puzzle_width

    return puzzle

def solve_puzzle(puzzle):
    '''
    '''
    clauses = []
    for r in range(puzzle_width):
        clauses.extend(row_clauses(r))
        clauses.extend(col_clauses(r))

        for c in range(puzzle_width):
            clauses.extend(cell_clauses(r, c, puzzle[r][c]))

            if r % grid_width == 0 and c % grid_width == 0:
                clauses.extend(grid_clauses(r, c))

    return sat.solve(clauses)

def parse_solution(solution):
    puzzle = np.zeros((puzzle_width, puzzle_width)).astype(int)

    if isinstance(solution, str):
        return solution

    solution = np.array(solution)
    mask = solution >= 0
    solution = solution[mask]

    #assert len(solution) == int(puzzle_width**2)

    for a in solution:
        r, c, v = unpack_satvar(a)
        puzzle[r][c] = v

    return puzzle

def pretty(puzzle):
    out = ""
    if isinstance(puzzle, str):
        print(puzzle)

    for r in range(len(puzzle)):
        if r % 3 == 0:
            out = out + '\n     '
        for c in range(len(puzzle[r])):
            if c % 3 == 0:
                out = out + ' '
            out = out + str(int(puzzle[r][c])) + ' '
        out = out + '\n     '
        
    return out

def check_solution(puzzle):
    correct = True
    
    for r in range(len(puzzle)):
        for c in range(len(puzzle[r])):
                # check  rows
                for i in range(c+1, puzzle_width):
                    if puzzle[r][c] == puzzle[r][i]:
                        print("row error at {},{} and {},{}".format(r, c, r, i))
                        correct = False
                
                # check columns
                for j in range(r+1, puzzle_width):
                    if r != j and puzzle[r][c] == puzzle[j][c]:
                        print("column error at {},{} and {},{}".format(r, c, j, c))
                        correct = False

                # check grids
                if r % grid_width == 0 and c % grid_width == 0:    
                    cells = ((r+i, c+j) for i in range(grid_width) for j in range(grid_width)) 
                    for pair in pairs(cells):
                        if puzzle[pair[0]] == puzzle[pair[1]]:
                            print("grid error at {},{} and {},{}".format(*pair[0], *pair[1]))
                            correct = False

    if correct:
        print("Solution is correct!")

if __name__ == "__main__":
    filename = sys.argv[1]
    puzzle = parse_puzzle(filename)
    solution = solve_puzzle(puzzle)
    solved = parse_solution(solution)

    print("###########  puzzle  ###########")
    print(pretty(puzzle))
    print()
    print("########### solution ###########")
    print(pretty(solved))

    check_solution(solved)