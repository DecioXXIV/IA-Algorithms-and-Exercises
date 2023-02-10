import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# nQueens Problem: we got a Chessboard ("N" rows and "N" columns) and we want to place "N" Queens on it in order to have none of them putting the others in check.
# We decide to exploit a Genetic Algorithm.

# Each state is represented by a vector of "N" values: each index represents a column, each value represents a row.
# This means that if we have "vector[2] = 5", we have a queen on the "(5,2)" cell.

# Each state is evaluated in terms fo the number of conflicts between the queens: we want to reach "0" for this value.


# FUNCTION: creates the initial population. In few words, it creates "n_population" differents chessboards.
def create_population(n_population, n_queens):
    population = list()

    for i in range(n_population):
        sample = np.random.randint(low = 0, high = n_queens, size = n_queens).tolist()
        population.append(sample)
        # Warning! In this version we admit to different Queens to have the same row index.
        # This fact has obivous implications on the threat's number.

    return population

# FUNCTION: given a populated chessboard, it counts and returns the number of threats.
# Our goal is to minimize this value.
def count_threats(sample):
    tot_threats = 0

    for column in range(0, len(sample)-1):
        current_queen = [column, sample[column]]
        # Observation: each Queen is describes as a couple of coordinates, [column, row]
            # - queen[0] = column_index
            # - queen[1] = row_index

        for previous_column in range(column+1, len(sample)):
            previous_queen = [previous_column, sample[previous_column]]

            slope = (current_queen[1] - previous_queen[1]) / (current_queen[0] - previous_queen[0])

            # Orizzontal Threats
            if slope == 0:
                # Observation: "slope == 0" only if the two Queens observed share the same "row_index".
                tot_threats += 1
            
            # Diagonal Threats
            elif slope == 1 or slope == -1:
                tot_threats += 1
    
    return tot_threats

# FUNCTION: prints the Chessboard
def print_board(sample, n_queens):
    board = list()
    for r in range(0, n_queens):
        row = list()
        for c in range(0, n_queens):
            if r == sample[c]:
                row.append('Q')
            else:
                row.append('-')
        board.append(row)
    
    print(np.matrix(board))

# FUNCTION: sorts the population. 
# The first sample of the ordered population is related to the minimum value of the objective function "count_threats".
def sort_population(population):
    population.sort(key = count_threats)
    return population


# FUNCTION: executes the 1-Point-Crossover.
def crossover(population, crossover_count):
    length = len(population[0])

    for i in range(0, crossover_count):
        # We select two random samples of the population: parents
        parent1 = population[np.random.randint(0, len(population))]
        parent2 = population[np.random.randint(0, len(population))]

        crossover_point = np.random.randint(1, length-1)

        child1 = list()
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = list()
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
        population.append(child1)
        population.append(child2)
        # Warning! The children don't replace the parents: they become part of the population.
    
    return population


# FUNCTION: executes the Mutation.
def mutation(population, mutation_count):
    length = len(population[0])

    for i in range(0, mutation_count):
        parent = population[np.random.randint(0, len(population))]

        mutation_point = np.random.randint(0, length)
        mutation_gene = np.random.randint(0, length)

        mutated_parent = parent.copy()
        mutated_parent[mutation_point] = mutation_gene

        population.append(mutated_parent)
        # Warning! The "mutated_parent" doesn't replace the parents: it becomes part of the population.
    
    return population


def genetic_algorithm(count_threats, n_population, n_queens, n_iterations, crossover_count, mutation_count):
    print("*** *********************************** ***")
    print("*** Genetic Algorithm x nQueens Problem ***")
    print("*** *********************************** ***\n")
    # Getting the Initial Population
    population = create_population(n_population, n_queens)
    population = sort_population(population)

    # Initializing "Best"
    best = population[0]
    best_eval = count_threats(best)

    print("Starting State:")
    print_board(best, n_queens)
    print("n° Threats = %d\n" % best_eval)

    # Iterations: the Algorithm stops if it founds a "global best" or if it completes "n_iterations" cycles.
    for iteration in range(0, n_iterations):
        # Observation: at this point, "len(population) == n_population"

        population = crossover(population, crossover_count)     # Now: "len(population) == n_population + 2*crossover_count"
        population = mutation(population, mutation_count)       # Now: "len(population) == n_population + 2*crossover_count + mutation_count"
        
        # The new population gets sorted again...
        population = sort_population(population)
        # ...and gets "cut": the best samples are the first ones.
        population = population[:n_population]

        top_sample = population[0]
        top_sample_eval = count_threats(top_sample)

        if top_sample_eval < best_eval:
            print("Improvement Found at Iteration: " + str(iteration+1))
            print("n° Threats: " + str(best_eval) + " -> " + str(top_sample_eval) + "\n")
            
            best = top_sample
            best_eval = top_sample_eval

        if best_eval == 0:
            break

    print("*** SEARCH IS OVER! ***")
    print("Iteration: " + str(iteration+1))
    print("Final Best State:")
    print_board(best, n_queens)
    print("n° Threats = %d" % best_eval)


# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
n_population = 10
n_queens = 8
n_iterations = 10000
crossover_count = 5
mutation_count = 5

genetic_algorithm(count_threats, n_population, n_queens, n_iterations, crossover_count, mutation_count)