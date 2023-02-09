import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# "OneMax" Problem: this problem aims to transform a random Binary String in a Binary one, which contains only "1".
# To achieve this objective, we decide to exploit a Genetic Algorithm.

# FUNCTION: create a population of cardinality "n_bits", composed by Binary Strings with "len(bin_string) == n_bits"
def create_population(n_population, n_bits):
    population = list()
    for n in range(n_population):
        sample = np.random.randint(0, 2, n_bits).tolist()
        population.append(sample)

    # Faster Version
    # population = [np.random.randint(0, 2, n_bits).tolist() for _ in range(n_population)]

    return population


# FUNCTION: evaluates a Binary String with the sum of his values. The "-" sign is related to the aiming of minimizing the Fitness Function
def onemax(bin_string):
    return -sum(bin_string)


# FUNCTION: Tournament Selection. We randomely select and compare "k" samples from the population: the best one is returned as "parent".
def selection(population, scores, k=3):
    selected_idx = np.random.randint((len(population)))

    for idx in np.random.randint(0, len(population), k-1):
        if scores[idx] < scores[selected_idx]:
            selected_idx = idx
    
    return population[selected_idx]


# FUNCTION: Crossover. We execute de "1-Point Crossover" between the Parents.
def crossover(p1, p2, r_crossover):
    c1, c2 = p1.copy(), p2.copy()

    execute_crossover = np.random.rand()
    
    if execute_crossover < r_crossover:
        point = np.random.randint(1, len(p1)-2)

        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
    
    return [c1, c2]


# FUNCTION: Mutation.
def mutation(children, r_mutation):
    for i in range(len(children)):
        execute_mutation = np.random.rand()
        if execute_mutation < r_mutation:
            children[i] = 1 - children[i]


# FUNCTION: the Genetic Algorithm itself
def genetic_algorithm(objective, n_bits, n_iterations, n_population, r_crossover, r_mutation):
    print("*** ********************************** ***")
    print("*** Genetic Algorithm x OneMax Problem ***")
    print("*** ********************************** ***\n")
    # Getting the Starting Population
    population = create_population(n_population, n_bits)
    
    # Initializing "Best"
    best = population[0]
    best_eval = objective(best)

    # Iterate over "n_iterations" Generations
    iteration = 1
    for gen in range(n_iterations):
        scores = list()
        for sample in population:
            scores.append(objective(sample))
        
        # (Eventually) Update the Best Solution
        new_best_found = False
        for i in range(n_population):
            if scores[i] < best_eval:
                new_best_found = True
                best = population[i]
                best_eval = scores[i]

        if (new_best_found == True):
            print("New \'Best\' found at Iteration %d" % iteration)
            print("New Best = " + str(best))
            print("New Best Eval = %d\n" % best_eval)
        
        # Time to Create the New Generation
        parents = list()
        children = list()

        for i in range(n_population):
            parents.append(selection(population, scores))
        
        for i in range(0, n_population, 2):
            p1 = parents[i]
            p2 = parents[i+1]

            for c in crossover(p1, p2, r_crossover):
                mutation(c, r_mutation)
                children.append(c)
        
        population = children
        iteration += 1
    

# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
np.random.seed(4)

n_iterations = 100
n_bits = 25
n_population = 100
r_crossover = 0.9
r_mutation = 1.0 / float(n_bits)

genetic_algorithm(onemax, n_bits, n_iterations, n_population, r_crossover, r_mutation)