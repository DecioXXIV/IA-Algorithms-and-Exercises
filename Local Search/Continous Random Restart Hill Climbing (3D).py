import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Given the Ackley's Objective Function, we execute the "Random Restart Hill Climbing" in order to move to the Optimal State: x = 0 -> f(0) = 0.
# This version of the "Hill Climbing" Algorithm execute multiple times the "Base Version", but starting every time from a different Starting State (randomely chosen).

def ackley_function(v):
    x, y = v
# Typical Parameters
    a = 20
    b = 0.2
    c = 2 * np.pi

    return -a * np.exp(-b * np.sqrt(0.5*(x**2 + y**2))) - np.exp(0.5 * (np.cos(c*x) + np.cos(c*y))) + np.e + a

def in_bounds(point, bounds):
# For Each Dimension...
    for d in range(len(bounds)):
# ... it's verified if the dimension exceeds its bound
        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
            return False
    return True

def base_hill_climbing(ackley_function, bounds, n_iterations, step_size, starting_state):
    current = starting_state
    current_eval = ackley_function(current)

    for i in range(n_iterations):
        next = None

        while next is None or not in_bounds(next, bounds):
            next = current + np.random.randn(len(bounds)) * step_size

        next_eval = ackley_function(next)

        if next_eval <= current_eval:
            current = next
            current_eval = next_eval
    
    return [current, current_eval]

def random_restart_hill_climbing_with_scores(ackley_function, bounds, n_base_iterations, step_size, n_restarts):
    best = None
    best_eval = np.inf
    scores = list()

    for n in range(n_restarts):
        starting_state = None
        while starting_state is None or not in_bounds(starting_state, bounds):
            starting_state = bounds[:, 0] + np.random.rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
        
        current, current_eval = base_hill_climbing(ackley_function, bounds, n_base_iterations, step_size, starting_state)

        if current_eval < best_eval:
            print("Improvement Found at Restart %d!" % (n+1))
            print("Old Best: f(%s) = %.5f" %(best, best_eval))
            print("New Best: f(%s) = %.5f\n" %(current, current_eval))

            best = current
            best_eval = current_eval
            scores.append(best_eval)
        
    return scores

# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
np.random.seed(1)
bounds = np.asarray([[-5.0, 5.0], [-5.0, 5.0]])
n_base_iterations = 1000
step_size = 0.05
n_restarts = 30

random_restart_hill_climbing_with_scores(ackley_function, bounds, n_base_iterations, step_size, n_restarts)