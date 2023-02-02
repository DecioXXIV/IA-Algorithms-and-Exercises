import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Given the Ackley's Objective Function, we execute the "First Choice Hill Climbing".
# We start from a random state and we want to move to the optimal state, x = 0 -> f(0) = 0

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

def first_choice_hill_climbing_with_scores(ackley_function, bounds, n_iterations, step_size):
# Generation of a Random Starting State...which has to respect the bounds
    current = None
    
    while current is None or not in_bounds(current, bounds):
        current = bounds[:, 0] + np.random.rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
# Observations:
    # - bounds[:, 0] -> Lower Bound of the imposed observation interval: "5" for the default execution.
    # - np.random.rand(n) -> creates an array of the given shape and populates it with random samples from a Uniform Distribution over [0,1).
    # - (bounds[:, 1] - bounds[:, 0]) -> Dimension of the imposed observation interval -> "10" for the default execution.
    # - type(current) == numpy.ndarray
    # - current.shape == (2,)

    current_eval = ackley_function(current)

# Scores Memory
    scores = list()
    scores.append(current_eval)

# Hill Climbing execution
    for i in range(n_iterations):
        next = None

        while next is None or not in_bounds(next, bounds):
            next = current + np.random.randn(len(bounds)) * step_size
# Observations:
    # - len(bounds) == 1
    # - np.random.randn(d0, d1, ..., dn) -> returns an array of the given shape and populated with samples from a Standard Normal Distribution
    # - step_size -> Standard Normal Distribution's Standard Deviation
        
        next_eval = ackley_function(next)

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
bounds = np.asarray([[-5.0, 5.0],[-5.0, 5.0]])
n_iterations = 1000
step_size = 0.1

first_choice_hill_climbing_with_scores(ackley_function, bounds, n_iterations, step_size)