import random
import string

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Given a target string with len(target_string) == n, we start from a random string with len(starting_string) == n.
# We want to transform the "starting_string" into the "target_string" by iterating and modifying only one character at a time in the "starting_string".

def generate_starting_string(length):
    return [random.choice(string.printable) for _ in range(length)]

def eval_function(current, target):
    total_diff = 0

# STRING EVALUTATION: for each pair or corresponding characters we calculate their distance from each other.
# The distance between "current_string" and "target_string" will be the sum of the individual distances, calculated for all the pairs of corresponding characters.
    for i in range(len(target)):
        c = current[i]
        t = target[i]

        diff = abs(ord(c) - ord(t))
        total_diff += diff
    
    return total_diff

def tweak(current):
# STRING TWEAKING: we choose a random charachter in the "current_string" and replace it with a character randomely chosen from the "string.printable" set.
    index = random.randint(0, len(current)-1)
    current[index] = random.choice(string.printable)

def first_choice_hill_climbing(starting_string, target_string):
# We exploit the "First-Choice Hill Climbing" Algorithm: given the current state, we choose one random neighbor which gets accepted
# only if its valutation results to be better than the current state's.
    print("*** ************************** ***")
    print("*** FIRST-CHOICE HILL CLIMBING ***")
    print("*** ************************** ***\n")
    current_state = starting_string
    current_eval = eval_function(current_state, target_string)
    iteration = 1

    print("Starting Score: %d" % current_eval)
    print("Starting String:", "".join(current_state), "\n")

    while True:
    
        if current_eval == 0:
            break

        next_state = list(current_state)
        tweak(next_state)
        next_state_eval = eval_function(next_state, target_string)

        if next_state_eval < current_eval:
            current_state = next_state
            current_eval = next_state_eval

# VISUALIZATION EFFICIENCY: "current_eval" and "current_state" are printed only if the Algorithm actually moves to a next state which is better than the actual state.
            print("Improvement found at Iteration %d!" % iteration)
            print("Current Score: %d" % current_eval)
            print("Current String:", "".join(current_state), "\n")

        iteration += 1
    
    print("*** END OF THE SEARCH ***")
    print("Iterations =", iteration, ", Starting String =", "".join(starting_string), ", Final String =", "".join(current_state))


# *** **** ***
# *** MAIN ***
# *** **** ***

target_string = "DecioXXIV"
starting_string = generate_starting_string(len(target_string))

first_choice_hill_climbing(starting_string, target_string)