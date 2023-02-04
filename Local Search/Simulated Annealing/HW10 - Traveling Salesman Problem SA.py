import math
import random
import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Traveling Salesman Problem: we got "n" cities and a Traveling Salesman, who has to visit each city only once and go back to the starting city.
# Every move between two cities implies a cost, and we want this cost to be the lowest possible.

# Each state is represented by a sequence of indexes (each index is related to a city), representing the cycle travelled by the salesman.
# Each state has its own neighborhood and each neighbor is obtained by "swapping" two cities into the sequence.
# Each state is then evaluated by a function that calculates the total cost "payed" by the Traveling Salesman: obviously, the goal is to minimize this cost.

# FUNCTION: moving from the Current State to the Next State
def tweak(state):
    state_copy = np.copy(state)
    N = len(state_copy)

# Swapping two cities in the sequence
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    while x == y:
        y = random.randint(0, N-1)
    
    temp = state_copy[x]
    state_copy[x] = state_copy[y]
    state_copy[y] = temp

    return state_copy


# FUNCTION: Evaluating Function (Energy)
def eval_function(state, graph_arcs):
    total_distance = 0

    for i in range(len(state)-1):
        current_city_idx = state[i]
        next_city_idx = state[i+1]
        total_distance += graph_arcs[current_city_idx][next_city_idx]
    
# Last Distance = Distance "Last City-First City"
    current_city_idx = state[len(state)-1]
    next_city_idx = state[0]
    total_distance += graph_arcs[current_city_idx][next_city_idx]

    return total_distance


# FUNCTION: Getting the Initial State
def get_initial_state(state):
    for c in range(len(state)):
        state = tweak(state)
    return state


# FUNCTION: we have the Space of States' information as a List of Adiacency Lists.
# This function translates the List of Adiacency Lists into an Adiacency Matrix.
def build_graph(graph_infos):
    graph_nodes = list(graph_infos.keys())
    N = len(graph_nodes)

    graph_arcs = np.zeros((N,N), dtype=np.int)
    
    for city in graph_nodes:
        city_idx = graph_nodes.index(city)
        for adiacency in graph_infos[city]:
            neighbor = adiacency[0]
            neigh_idx = graph_nodes.index(neighbor)
            distance = adiacency[1]
            graph_arcs[city_idx][neigh_idx] = distance
    
    return graph_nodes, graph_arcs


# SIMULATED ANNEALING ALGORITHM
def simulated_annealing(graph_infos, T_START, T_END, n_iterations, ALPHA):
    print("*** ************************************************ ***")
    print("*** Simulated Annealing x Traveling Salesman Problem ***")
    print("*** ************************************************ ***\n")

# Graph Building
    graph_nodes, graph_arcs = build_graph(graph_infos)
    N = len(graph_nodes)

    print("Cities: " + str(graph_nodes))
    print("Traveling Costs:")
    print(graph_arcs)

# Starting State
    current = get_initial_state(range(0, N))
    current_eval = eval_function(current, graph_arcs)

# Best Inizialization
    best = current
    best_eval = current_eval

    temperature = T_START
    iteration = 1
    
    print("\n*** STARTING THE SEARCH... ***\n")

    while temperature > T_END:

# Dumping the informations about the current iteration
        print("ITERATION: %d" % iteration)

        current_best_cities = list()
        for index in best:
            current_best_cities.append(graph_nodes[index])

        if iteration == 1:
            print("Starting State = %s" % str(current_best_cities))
            print("Starting Cost = %d" % best_eval)
        else:
            print("Actual State = %s" % str(current_best_cities))
            print("Actual Cost = %d" % best_eval)
        
        print("Temperature = %.3f\n\n" % temperature)

        for i in range(n_iterations):
            next = tweak(current)
            next_eval = eval_function(next, graph_arcs)

            if next_eval < current_eval:
                current = next
                current_eval = next_eval
                if next_eval < best_eval:
                    best = next
                    best_eval = next_eval

            else:
                delta_eval = next_eval - current_eval
                metropolis = math.exp(-delta_eval/temperature)
                test = random.random()
                if test < metropolis:
                    current = next
                    current_eval = next_eval
            
        temperature *= ALPHA
        iteration += 1
    
    final_cities = list()
    for index in best:
        final_cities.append(graph_nodes[index])
    
    print("*** SEARCH IS OVER! ***")
    print("Final State = %s" % str(final_cities))
    print("Final Cost = %d" % best_eval)

# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
T_START = 30
T_END = 0.1
n_iterations = 15
ALPHA = 0.8

# Search State Settings
graph_infos = dict()
graph_infos['Milano'] = [('Torino',126),('Genova',119),('Bologna',201),('Firenze',250),('Roma',478),('Napoli',658),('Palermo',887)]
graph_infos['Torino'] = [('Milano',126),('Genova',123),('Bologna',296),('Firenze',318),('Roma',525),('Napoli',712),('Palermo',906)]
graph_infos['Genova'] = [('Milano',119),('Torino',123),('Bologna',192),('Firenze',199),('Roma',402),('Napoli',589),('Palermo',791)]
graph_infos['Bologna'] = [('Milano',201),('Torino',296),('Genova',192),('Firenze',81),('Roma',304),('Napoli',471),('Palermo',729)]
graph_infos['Firenze'] = [('Milano',250),('Torino',318),('Genova',199),('Bologna',81),('Roma',232),('Napoli',408),('Palermo',653)]
graph_infos['Roma'] = [('Milano',478),('Torino',525),('Genova',402),('Bologna',304),('Firenze',232),('Napoli',188),('Palermo',426)]
graph_infos['Napoli'] = [('Milano',658),('Torino',712),('Genova',589),('Bologna',471),('Firenze',408),('Roma',188),('Palermo',313)]
graph_infos['Palermo'] = [('Milano',887),('Torino',906),('Genova',791),('Bologna',729),('Firenze',653),('Roma',426),('Napoli',313)]

simulated_annealing(graph_infos, T_START, T_END, n_iterations, ALPHA)