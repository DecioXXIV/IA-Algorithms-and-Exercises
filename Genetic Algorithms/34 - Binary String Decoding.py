import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# It is given the Objective Function "f(x,y) = x^2 + y^2" and it's asked to minimize it. This function has a global minimum in (0,0), where f(0,0) = 0.

def create_population(n_bits, n_population, bounds):
    population = list()
    for n in range(n_population):
        sample = np.random.randint(0, 2, n_bits*len(bounds)).tolist()
        population.append(sample)
    
    # Observation: each sample of the population is a 32-Bit-Binary String in which the First 16 Bits describe the "X" and the Last 16 Bits describe the "Y".
    return population

def objective(x):
    return (x[0]**2.0 + x[1]**2.0)


def decode(bounds, n_bits, sample):
    decoded = list()
    max_value = 2**n_bits - 1
    
    for i in range(len(bounds)):
        # Substring Extraction
        start = i * n_bits              # i=0 -> start = 0, i=1 -> start = 16
        end = (i * n_bits) + n_bits     # i=0 -> end = 16, i=1 -> end = 32 

        substring = sample[start:end]

        chars = ''.join([str(s) for s in substring])
        integer = int(chars, 2)         # Transforms the Binary Number in a Decimal Number

        value = bounds[i][0] + (integer/max_value) * (bounds[i][1] - bounds[i][0]) 
        # What happens here? If i=0 we work on the "X", else, if i=1, we work on the "Y"
            # 1) bounds[i][0] = Lower Bound for the Variable
            # 2) Mapping of the "integer" value in the "bounds" interval
        
        decoded.append(value)
    
    return decoded


def selection(population, scores, k=3):
    selected_idx = np.random.randint(len(population))

    for idx in np.random.randint(0, len(population), k-1):
        if scores[idx] < scores[selected_idx]:
            selected_idx = idx
    
    return population[selected_idx]


def crossover(p1, p2, r_crossover):
    c1 = p1.copy()
    c2 = p2.copy()

    execute_crossover = np.random.rand()
    
    if execute_crossover < r_crossover:
        point = np.random.randint(1, len(p1)-2)

        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
    
    return [c1, c2]


def mutation(sample, r_mutation):
    for i in range(len(sample)):
        execute_mutation = np.random.rand()

        if execute_mutation < r_mutation:
            sample[i] = 1 - sample[i]


def genetic_algorithm(objective, bounds, n_bits, n_iterations, n_population, r_crossover, r_mutation):
    # Create the Starting Population
    population = create_population(n_bits, n_population, bounds)
    
    # Initialize "Best"
    best = population[0]
    best_eval = objective(decode(bounds, n_bits, best))

    # Iterate over "n_iterations" Generations
    iteration = 1
    for gen in range(n_iterations):
        decoded_samples = list()
        for sample in population:
            decoded_samples.append(decode(bounds, n_bits, sample))
        
        scores = list()
        for sample in decoded_samples:
            scores.append(objective(sample))
        
        # (Eventually) Update the Best
        new_best_found = False
        for i in range(n_population):
            if scores[i] < best_eval:
                new_best_found = True
                best = population[i]
                best_eval = scores[i]
        
        if new_best_found == True:
            print("New \'Best\' found at Iteration %d" % iteration)
            print("New Best: " + str(best))
            print("New Best Eval: %.9f\n" % best_eval)
        
        # Create the Next Generation
        parents = list()
        children = list()

        for sample in population:
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

# Parameters Setting
bounds = [[-5.0, 5.0], [-5.0, 5.0]]
n_iterations = 100
n_bits = 16
n_population = 100
r_crossover = 0.9
r_mutation = 1.0 / (float(n_bits) * len(bounds))

genetic_algorithm(objective, bounds, n_bits, n_iterations, n_population, r_crossover, r_mutation)