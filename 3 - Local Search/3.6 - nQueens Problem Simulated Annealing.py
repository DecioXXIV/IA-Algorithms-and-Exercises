import math
import random
import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# nQueens Problem: we got a Chessboard ("N" rows and "N" columns) and we want to place "N" Queens on it in order to have none of them putting the others in check.
# We decide to exploit the "Simulated Annealing" Algorithm.

# To simplify the state definition and the problem itself, we decide to place only one Queen for each column of the board.
# In this way we can easily represent the board with a vector of dimension "N": each index stands for a column index and each value stands for a row index.
# For example, if we have: vector[2] = 5, it means that we have a Queen on the (5,2) cell.

# Each state has his own neighborhood, obtained imposing the "swap" between two columns of the board.
# If we have "N" columns, the neighborhood's cardinality is equal to: N(N-1)/2.
# Each state is evaluated in terms fo the number of conflicts between the queens: we want to reach "0" for this value.

def tweak(solution):
    solution_copy = np.copy(solution)
# We randomely choose two separate column indexes
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    while x == y:
        y = random.randint(0, N-1)
    
# Column Swap
    temp = solution_copy[y]
    solution_copy[y] = solution_copy[x]
    solution_copy[x] = temp

    return solution_copy

def get_starting_state(solution):
    for c in range(0, N):
        solution = tweak(solution)
    return solution

def energy_function(state):
# Chessboard Definition
    board = [[0] * N for i in range(N)]
# Placing the Queens on the Chessboard
    for i in range(0, N):
        board[state[i]][i] = 'Q'

# Possible Moves on the Chessboard: having one Queen on each column/row, we need to count only the conflicts on the diagonals
    dx = [1,1,-1,-1]
    dy = [1,-1,1,-1]
# Observations:
    # - dx == 1, dy == 1: "Bottom-Right" move
    # - dx == 1, dy == -1: "Bottom-Left" move
    # - dx == -1, dy == 1: "Top-Right" move
    # - dx == -1, dy == -1: "Top-Left" move

    conflicts = 0

    for i in range(0, N):
        x = state[i]
        y = i

# Conflicts Count
        for j in range(0,4):
            temp_x = x
            temp_y = y
            while True:
                temp_x += dx[j]
                temp_y += dy[j]

                if (temp_x < 0 or temp_x >= N) or (temp_y < 0 or temp_y >= N):
                    break

                if board[temp_x][temp_y] == 'Q':
                    conflicts += 1
    
    return conflicts

def print_chessboard(state):
# Chessboard Definition
    board = [[0] * N for i in range(N)]
# Placing the Queens on the Chessboard
    for i in range(0, N):
        board[state[i]][i] = 'Q'

    for x in range(0, N):
        for y in range(0, N):
            if board[x][y] == 'Q':
                print("Q    ", end="")
            else:
                print(".    ", end="")
        print("\n")

def simulated_annealing():
    print("*** ***************** ***")
    print("*** %d QUEENS PROBLEM ***" % N)
    print("*** ***************** ***\n")

# Initial State
    current = get_starting_state(range(0, N))
    current_energy = energy_function(current)

# "Best" Inizialization
    best = current
    best_energy = current_energy

    print("STARTING STATE: Conflicts = %d" % best_energy)
    print_chessboard(best)

# Temperature Inizialization
    temperature = T_START
    
    iterations = 1
    print("\n*** SEARCH IS STARTING... ***")
    while (temperature > T_END and best_energy > 0):
        print("ITERATION: %d" % iterations)
        print("Temperature: %.3f" % temperature)
        print("Conflicts = %d\n" % best_energy)
        
        for i in range(0, STEPS_PER_CHANGE):
            update = False

# Getting & Evaluating a New Random State
            next = tweak(current)
            next_energy = energy_function(next)

            if next_energy < current_energy:
                update = True
            else:
                delta_energy = next_energy - current_energy
                metropolis = math.exp(-delta_energy/temperature)
                test = random.random()
                
                if (test < metropolis):
                    update = True
            
            if update:
                current = next
                current_energy = next_energy

                if (current_energy < best_energy):
                    best = current
                    best_energy = current_energy
            
        temperature *= ALPHA
        iterations += 1

    print("\n*** SEARCH IS OVER! ***")
    print("FINAL STATE: Conflicts = %d" % best_energy)
    print_chessboard(best)

# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
N = 8   # "Classic" Chessboard
T_START = 30
T_END = 0.2
ALPHA = 0.8
STEPS_PER_CHANGE = 40

solution = simulated_annealing()