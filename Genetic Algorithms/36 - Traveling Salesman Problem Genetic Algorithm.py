import numpy as np
import random
import math

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Traveling Salesman Problem: we got "n" cities and a Traveling Salesman, who has to visit each city only once and go back to the starting city.
# Every move between two cities implies a cost, and we want this cost to be the lowest possible.

# Each state is represented by a sequence of indexes (each index is related to a city), representing the cycle travelled by the salesman.

# Each state has its own neighborhood and each neighbor is obtained by "swapping" two cities into the sequence.
# Each state is then evaluated by a function that calculates the total cost "payed" by the Traveling Salesman: obviously, the goal is to minimize this cost.


# FUNCTION: creates the Search State.
# Each City is represented by a pair of coordinates (x,y).
def create_search_space(n_cities):
    city_coordinates = list()
    
    for i in range(n_cities):
        city = np.random.randint(low=1, high=150, size=2).tolist()
        # Each city is represented by a 2-values-vector: in few words, the coordinates "x" and "y".
        city_coordinates.append(city)
    
    return city_coordinates


# FUNCTION: creates a Random Starting Population from the Search State.
# Each sample is a vector of cities: each vectory represents the cycle travelled by the Salesman.
def create_population(n_population, city_coordinates):
    n_cities = len(city_coordinates)
    population = list()

    for n in range(n_population):
        indexes = [i for i in range(0, n_cities)]
        random.shuffle(indexes)
        sample = list()

        for idx in indexes:
            sample.append(city_coordinates[idx])
        
        population.append(sample)

    return population


# FUNCTION: evaluates a sample.
def eval_function(sample):
    n_cities = len(sample)
    total_distance = 0.0
    
    for c in range(0, n_cities-1):
        src = sample[c]
        dst = sample[c+1]
        total_distance += math.sqrt(((src[0] - dst[0])**2) + ((src[1] - dst[1])**2))

    src = sample[n_cities-1]
    dst = sample[0]

    total_distance += math.sqrt((src[0] - dst[0])**2 + (src[1] - dst[1])**2)

    return total_distance


# FUNCTION: executes the "Tournament Selection" on 3 randomely-selected samples of the current population.
# The "winnner" is the sample with best fitness value.
def selection(population, scores, k=3):
    n_population = len(population)
    selected = None

    # Tournament Selection
    first_idx = np.random.randint(0, n_population)
        
    second_idx = np.random.randint(0, n_population)
    while second_idx == first_idx:
        second_idx = np.random.randint(0, n_population)

    third_idx = np.random.randint(0, n_population)
    while (third_idx == first_idx) or (third_idx == second_idx):
        third_idx = np.random.randint(0, n_population)

    selected_scores = np.array([scores[first_idx], scores[second_idx], scores[third_idx]])
    top_score = selected_scores.max()
    parent_idx = scores.index(top_score)

    selected = population[parent_idx]
    
    return selected


# FUNCTION: executes the "Ordered Crossover".
# This is composed of two operations: 2-Point-Crossover + "Child Filling"
def crossover(sample1, sample2, crossover_rate):
    execute_crossover = np.random.rand()

    if execute_crossover > crossover_rate:
        return [sample1, sample2]

    else:
        n_cities = len(sample1)

        child1 = [None for n in range(0, n_cities)]
        child2 = child1.copy()
        
        # 2-Point Crossover on the Children
        start = np.random.randint(low=0, high=int(n_cities/2))
        end = np.random.randint(low=int(n_cities/2), high=n_cities)

        for n in range(start, end+1):
            child1[n] = sample2[n]
            child2[n] = sample1[n]
        
        # Filling "child1"
        none_elements = n_cities - (end - start + 1)
        it_1 = (end+1) % n_cities
        n = it_1
        while none_elements > 0:
            if child1[n] == None:
                while sample1[it_1] in child1:
                    it_1 = (it_1 + 1) % (n_cities)
                child1[n] = sample1[it_1]
                
                n += 1 
                n = n % n_cities

                none_elements -= 1
            
        # Filling "child2"
        none_elements = n_cities - (end - start + 1)
        it_2 = (end+1) % n_cities
        n = it_2
        while none_elements > 0:
            if child2[n] == None:
                while sample2[it_2] in child2:
                    it_2 = (it_2 + 1) % (n_cities)
                child2[n] = sample2[it_2]
                
                n += 1 
                n = n % n_cities
                none_elements -= 1

        # How does this function works? Let's explain with an example:
            # sample1 = [1 2 3 4 5 6]
            # sample2 = [4 2 6 3 1 5]
        
            # Step1 = 2-Point-Crossover: we sort the "start" and the "end" point.
                # Suppose: len = len(sample), half = int(len(sample)/2)
                # "start" belongs to the [0, half) interval -> suppose: start = 2
                # "end" belongs to the [half, len) interval -> suppose: end = 4

                # Crossing-Over:
                # child1 = [None None 6 3 1 None]
                # child2 = [None None 3 4 5 None]
            
            #Step2 = "Child Filling": we have to fill the child with the parent's value that are missing in this moment.
                # child1 = [4 5 6 3 1 2]
                # child2 = [6 1 3 4 5 2]

        return [child1, child2]


# FUNCTION: executed the "Swap Mutation".
def mutation(sample, mutation_rate):
    execute_mutation = np.random.rand()

    if execute_mutation > mutation_rate:
        return sample
    
    else:
        n_cities = len(sample)
        mutated_sample = sample.copy()

        first_idx = np.random.randint(0, n_cities)
        second_idx = np.random.randint(0, n_cities)
        
        temp = mutated_sample[first_idx]
        mutated_sample[first_idx] = mutated_sample[second_idx]
        mutated_sample[second_idx] = temp
    
        return mutated_sample


def genetic_algorithm(n_iterations, n_population, n_cities, crossover_rate, mutation_rate):
    print("*** ********************************************** ***")
    print("*** Genetic Algorithm x Traveling Salesman Problem ***")
    print("*** ********************************************** ***\n")
    # Search Space Inizialization
    city_coordinates = create_search_space(n_cities)

    # Starting Population Inizialization
    population = create_population(n_population, city_coordinates)

    scores = list()
    for sample in population:
        scores.append(eval_function(sample))

    # Best Inizialization
    best_eval = np.array(scores).min()
    best = population[scores.index(best_eval)]

    print("Starting State: " + str(best))
    print("Cost = %.3f\n" % best_eval)

    print("*** SEARCH IS STARTING... ***")
    for iteration in range(0, n_iterations):
        # Creating the New Generation
        children = list()

        # Selection Phase: Tournament Selection
        parents = list()
        for i in range(0, n_population):
            parents.append(selection(population,scores))

        # Crossover & Mutation Phase
        for i in range(0, n_population, 2):
            # Crossover Phase: Tournament Crossover
            parent1 = parents[i]
            parent2 = parents[i+1] 
            child1, child2 = crossover(parent1, parent2, crossover_rate)

            # Mutation Phase: Swap Mutation
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)

            children.append(child1)
            children.append(child2)

        children_scores = list()
        for sample in children:
            children_scores.append(eval_function(sample))

        best_child_eval = np.array(children_scores).min()

        # (Eventually) update the Best
        if best_child_eval < best_eval:
            print("Found new Best at Iteration " + str(iteration+1) + "\n")
            best_eval = best_child_eval
            best_child = children[children_scores.index(best_child_eval)]
            best = best_child

        
        population = children
    
    print("*** SEARCH IS OVER! ***")
    print("Final Best: " + str(best))
    print("Final Cost = %.3f" % best_eval)

# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
n_iterations = 10000
n_population = 10
n_cities = 10
crossover_rate = 0.9
mutation_rate = 0.25

genetic_algorithm(n_iterations, n_population, n_cities, crossover_rate, mutation_rate)