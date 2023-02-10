import numpy as np
import pandas as pd

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# Particle Swarm Optimization: it's given a particular Objective Function to optimize. The function is "f(x,y) = x^2 + y^2", which has its global best in "f(0,0) = 0".

# CLASS "Particle": contains all the salient informations about a Particle of the Swarm.
class Particle:
    def __init__(self, id, bounds):
        self.id = id

        self.positions = list()
        start_x = np.random.uniform(low=bounds[0][0], high=bounds[0][1])
        start_y = np.random.uniform(low=bounds[1][0], high=bounds[1][1])
        self.positions.append([start_x,start_y])

        self.velocities = list()
        start_vx = np.random.uniform(low=bounds[0][0], high=bounds[0][1])
        start_vy = np.random.uniform(low=bounds[1][0], high=bounds[1][1])
        self.velocities.append([start_vx,start_vy])

        self.best_value = np.inf
        self.best_idx = None

        self.values = list()
        eval_function(self)

# FUNCTION: executes a move for a Particle.
def move_particle(p, omega, l1, l2, p_best, g_best, bounds):
    p_best = np.array(p_best)
    g_best = np.array(g_best)

    s0 = np.array(p.positions[len(p.positions)-1])
    v0 = np.array(p.velocities[len(p.velocities)-1])

    v1 = omega*v0 + l1*(p_best - s0) + l2*(g_best - s0)
    p.velocities.append(v1)

    s1 = list(v1 + s0)

    # Observation: if the particle exceeds the problem's bounds, his position is resetted to a random position within the bounds.
    if not (bounds[0][0] <= s1[0] <= bounds[0][1]):
        s1[0] = np.random.uniform(low=bounds[0][0], high=bounds[0][1])
        

    if not (bounds[1][0] <= s1[1] <= bounds[1][1]):
        s1[1] = np.random.uniform(low=bounds[1][0], high=bounds[1][1])
    
    p.positions.append(s1)


# FUNCTION: evaluates the last position reached by the Particle.
def eval_function(p):
    last = len(p.positions)-1
    x = p.positions[last][0]
    y = p.positions[last][1]

    value = x**2 + y**2
    p.values.append(value)

    # Observation: for each Particle we memorize its "Personal Best Value" yet reached.
    # If we found a new "Personal Best", it gets updated.
    if value < p.best_value:
        p.best_value = value
        p.best_idx = last


def particle_swarm_optimization(bounds, n_particles, n_iterations, omega):
    print("*** *************************** ***")
    print("*** PARTICLE SWARM OPTIMIZATION ***")
    print("*** *************************** ***\n")
    # Initializing the Swarm
    particle_swarm = list()
    for i in range(0, n_particles):
        p = Particle(i, bounds)
        particle_swarm.append(p)
    
    # Initializing the "Global Best" Informations
    g_best_value = np.inf
    g_best = None
    chief_particle = None
    
    # Principal Cycle
    for it in range(0, n_iterations):
        particles_best = list()
        
        # (If necesssary) update the "Global Best".
        for p in particle_swarm:
            particles_best.append(p.positions[p.best_idx])
            value = p.best_value
            if value < g_best_value:
                g_best_value = value
                g_best = p.positions[p.best_idx]
                chief_particle = p.id
        
        # Actual Iteration's salient Informations.
        print("ITERATION: " + str(it+1) + " -> Global Best Value = " + str(g_best_value))
        data = pd.DataFrame(index = ["Particle %d" % i for i in range(0, n_particles)],
                            columns=['atm_position', 'atm_value', 'personal_best', 'chief'])
        
        for p in particle_swarm:
            row = "Particle " + str(p.id)
            if p.id == chief_particle:
                data.loc[row] = [p.positions[len(p.positions)-1], p.values[len(p.values)-1], p.best_value, "CHIEF"]
            else:
                data.loc[row] = [p.positions[len(p.positions)-1], p.values[len(p.values)-1], p.best_value, "X"]  
        print(data)
        print()

        # Time to move for the Particles!
        l1 = np.random.rand()
        l2 = np.random.rand()
        for i in range(0, len(particle_swarm)):
            particle = particle_swarm[i]
            p_best = particles_best[i]

            move_particle(particle, omega, l1, l2, p_best, g_best, bounds)
            eval_function(particle)
    
    print("*** SEARCH IS OVER! ***")


# *** **** ***
# *** MAIN ***
# *** **** ***

# Parameters Settings
bounds = [[-10.0, 10.0], [-10.0, 10.0]]     # x in [-10, 10], y in [-10, 10]
n_particles = 10
n_iterations = 25
omega = 0.7

particle_swarm_optimization(bounds, n_particles, n_iterations, omega)