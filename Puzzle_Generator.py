import Sudoku_Solver
import numpy as np
import pycosat as sat
import itertools


def generate_seed():
    seed = np.random.choice(range(9), 9, replace=False) + 1

    puzzle =   [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    row = seed[0] // 3
    col = seed[0] - 3*row

    for i in range(3):
        for j in range(3):
            puzzle[row+i][col+j] = int(seed[3*i + j])

    clauses = Sudoku_Solver.get_clauses(puzzle)
    
    seed = sat.solve(clauses)

    return Sudoku_Solver.parse_solution(seed)

def generate_puzzle(seed):
    unique = True

    puzzle = np.array(seed)
    seed = seed.flatten()

    elements = list(range(81))
    while unique:
        # remove some stuff
        ind = np.random.choice(elements)
        elements.remove(ind)

        seed[ind] = int(0)

        # check if unique
        puzzle = list(np.reshape(seed, (9,9)))
        clauses = Sudoku_Solver.get_clauses(puzzle)
        solutions = len(list(sat.itersolve(clauses)))
        
        if solutions > 1:
            unique = False

    return puzzle

if __name__ == "__main__":
    seed = generate_seed()

    print("###########   seed   ###########")
    print(Sudoku_Solver.pretty(seed))

    # TODO: write to file
    puzzle = generate_puzzle(seed)
    print("###########  puzzle  ###########")
    print(Sudoku_Solver.pretty(puzzle))

    solution = Sudoku_Solver.solve_puzzle(puzzle)
    print("########### solution ###########")
    print(Sudoku_Solver.pretty(solution))

    Sudoku_Solver.check_solution(solution)

