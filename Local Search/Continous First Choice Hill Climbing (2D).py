import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Given an Objective Function, f(x) = x^2, we execute the "First Choice Hill Climbing".
# We start from a random state and we want to move to the optimal state, x = 0.

def objective_function(x):
    return x[0]**2.0
# Observation: type(x) == numpy.array

def first_choice_hill_climbing_with_scores(objective_function, bounds, n_iterations, step_size):
    current = bounds[:, 0] + np.random.rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])    # Generation of a Random Starting State
# Observations:
    # - bounds[:, 0] -> Lower Bound of the imposed observation interval: "5" for the default execution.
    # - np.random.rand(n) -> creates an array of the given shape and populates it with random samples from a Uniform Distribution over [0,1).
    # - (bounds[:, 1] - bounds[:, 0]) -> Dimension of the imposed observation interval -> "10" for the default execution.
    # - type(current) == numpy.ndarray
    # - current.shape == (1,)

# Starting State Evalutation
    current_eval = objective_function(current)

# Scores Memory
    scores = list()
    scores.append(current_eval)

# Hill Climbing execution
    for i in range(n_iterations):
        next = current + np.random.randn(len(bounds)) * step_size   # Generation of a Random Next State
# Observations:
    # - len(bounds) == 1
    # - np.random.randn(d0, d1, ..., dn) -> returns an array of the given shape and populated with samples from a Standard Normal Distribution
    # - step_size -> Standard Normal Distribution's Standard Deviation

# Next State Evalutation
        next_eval = objective_function(next)

        if next_eval <= current_eval:
            print("Improvement Found at Iteration %d!" % (i+1))
            print("Old State: f(%s) = %.5f" %(current, current_eval))
            print("New State: f(%s) = %.5f\n" %(next, next_eval))
            
            current = next
            current_eval = next_eval
            scores.append(current_eval)
    
    print("*** END OF THE SEARCH! ***")
    return scores


# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
np.random.seed(5)
bounds = np.asarray([[-5.0, 5.0]])
n_iterations = 1000
step_size = 0.1

first_choice_hill_climbing_with_scores(objective_function, bounds, n_iterations, step_size)