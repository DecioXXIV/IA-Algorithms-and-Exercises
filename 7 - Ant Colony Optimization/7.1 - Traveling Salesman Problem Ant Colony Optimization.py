import numpy as np
import math

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Traveling Salesman Problem: we got "n" cities and a Traveling Salesman, who has to visit each city only once and go back to the starting city.
# Every move between two cities implies a cost, and we want this cost to be the lowest possible.

# Each state is represented by a sequence of indexes (each index is related to a city), representing the cycle travelled by the salesman.

# Each state is then evaluated by a function that calculates the total cost "payed" by the Traveling Salesman: obviously, the goal is to minimize this cost.

# CLASS: it represents one Ant used to explore the Search Space.
class Ant:
    def __init__(self, id, graph):
        self.id = id
        self.graph = graph
        self.start_node = np.random.randint(low=0, high=len(graph))
        self.path = [self.start_node]
        self.path_cost = 0
    
    # METHOD: it builds the paths travelled by the Ant, also updating the variable "path_cost".
    def gen_path(self, pheromone):
        n_cities = len(self.graph)
        prev = self.start_node

        # The Ant travels until she visites all the cities in the Search Space.
        while len(self.path) != n_cities:
            # The New City is picked depending on the pheromone set in the previous iterations (by other Ants).
            next = self.pick_next(pheromone[prev], self.graph[prev], self.path)
            self.path.append(next)
        
        self.path_cost = eval_path(self.graph, self.path)

        return self.path

    # METHOD: it picks a new city to add to the Ant's Exploration Path.
    def pick_next(self, pheromone, distances, path):
        pheromone = np.copy(pheromone)
        
        # We want to exclude the already-visited-cities: we set their pheromone to 0.
        for city in path:
            pheromone[city] = 0

        
        row = pheromone ** alpha * ((1.0 / distances) ** beta)
        norm_row = row / row.sum()
        # The "norm_row" contains all the "travel probabilities" which affect the Ant's choice.
            # Observation: norm_row.shape == (1, n_cities). The values related to the "already-visited-cities" are 0.


        next = np.random.choice([i for i in range(0, n_cities)], 1, p=norm_row)[0]
        # This step extracts an integer in [0, ..., n_cities-1] but basing on the "norm_row" probabilities.
        
        return next
    
    # METHOD: it spreads the pheromone. 
    def spread_pheromone(self, pheromone, all_paths):
        n_cities = len(all_paths[0])
        for path in all_paths:
            for i in range(0, n_cities-1):
                src = path[i]
                dst = path[i+1]

                # If the Ant chose a good arc (short), the spreaded pheromone will be higher.
                # In this way it suggests to the "future Ants" a good way to travel.
                pheromone[src][dst] += 1.0 / self.graph[src][dst]
            
            last = path[-1]
            first = path[0]

            pheromone[last][first] += 1.0 / self.graph[last][first]


# FUNCTION: creates a Random Search State and produces the Graph related to it.
def create_search_state(n_cities):
    city_coordinates = list()

    for i in range(0, n_cities):
        city = np.random.randint(low=-100, high=100, size=2).tolist()
        # Each City is represented by a 2-values-vector: the first value is the "x" (interval = [-20,20]), the second is the "y" (interval = [-20,20]).
        city_coordinates.append(city)
    
    graph_matrix = np.zeros((n_cities, n_cities), dtype=np.float32)
    for i in range(0, n_cities):
        graph_matrix[i][i] = np.inf

    for i in range(0, n_cities-1):
        for j in range(i+1, n_cities):
            d = distance(city_coordinates[i], city_coordinates[j])
            d = round(d, 3)
            graph_matrix[i][j] = d
            graph_matrix[j][i] = d
    
    return [city_coordinates, graph_matrix]


# FUNCTION: calculates and returns the distance between two cities of the Search State.
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# FUNCTION: evaluates a path in terms of the costs held moving through all the cities (first to last + last to first).
def eval_path(graph, path):
    total_cost = 0
    n_cities = len(path)

    for i in range(0, n_cities-1):
        src = path[i]
        dst = path[i+1]
        total_cost += graph[src][dst]
    
    last = path[-1]
    first = path[0]

    total_cost += graph[last][first]

    return total_cost


def ant_colony_optimization(graph, n_ants, n_iterations, decay, alpha, beta):
    print("*** **************************************************** ***")
    print("*** Ant Colony Optimization x Traveling Salesman Problem ***")
    print("*** **************************************************** ***\n")

    best_path = None
    best_path_cost = np.inf
    best_ant = None
    best_update = False

    n_cities = len(graph)
    pheromone = np.ones((n_cities,n_cities)) / n_cities

    for iteration in range(0, n_iterations):
        all_paths = list()
        ants = list()
        for i in range(0, n_ants):
            ant = Ant(i, graph)
            ants.append(ant)
            
            found_path = ant.gen_path(pheromone)
            all_paths.append(found_path)

        for ant in ants:
            ant.spread_pheromone(pheromone, all_paths)
        pheromone = pheromone * decay

        for ant in ants:
            if ant.path_cost < best_path_cost:
                best_path = ant.path
                best_path_cost = ant.path_cost
                best_ant = ant.id
                best_update = True

        if best_update == True:
            print("Iteration: " + str(iteration+1))
            if iteration == 0:
                print("Starting Best Path = " + str(best_path))
            else:
                print("New Best Path = " + str(best_path))
            print("Found by Ant %d" % best_ant)
            print("Cost = %.3f\n" % best_path_cost)
        
        best_update = False
    
    print("\n*** SEARCH IS OVER! ***")
    print("Final Best Path = " + str(best_path))
    print("Found by Ant %d" % best_ant)
    print("Cost = %.3f" % best_path_cost)

# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
np.random.seed(0)
n_cities = 8
n_ants = 10
n_iterations = 500
alpha = 1.0
beta = 1.0
decay = 0.7

cities, graph = create_search_state(n_cities)

ant_colony_optimization(graph, n_ants, n_iterations, decay, alpha, beta)