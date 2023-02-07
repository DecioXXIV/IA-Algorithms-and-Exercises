import random 

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# "Monty Hall" Problem: we have got 3 closed doors (Door 1, Door 2 and Door 3). Only one door hides a Supercar, the others hide a goat.
# The Algorithm, who knows where is hidden the car, asks us to choose a Door to open.

# After receiving our input, he decides to open one of the two remaining doors. This door surely hides a goat.

# After this event, the Algorithm asks us whether we want to change our choice: we can accept or deny.
# Finally, the chosen door gets opened and out prize gets revealed...hopefully the Supercar!

class Door:
    def __init__(self, prize):
        self.prize = prize

def play_game_always_change(doors, MAX_ITERATIONS):
    victories = list()

    for i in range(0, MAX_ITERATIONS):
        random.shuffle(doors)
        
        doors_indexes = [0,1,2]
        chosen_door_idx = random.randint(0,2)
        final_door_idx = None

        doors_indexes.remove(chosen_door_idx)

        nc_door1 = doors[doors_indexes[0]]
        nc_door2 = doors[doors_indexes[1]]

        if nc_door1.prize == nc_door2.prize:                                # The "not-chosen" doors both hide a Goat
            random_value = random.random()
            if random_value > 0.5:
                final_door_idx = doors.index(nc_door2)                      # "nc_door1" opened, the Player moves from "chosen_door" to "nc_door2"
            else:
                final_door_idx = doors.index(nc_door1)                      # "nc_door2" opened, the Player moves from "chosen_door" to "nc_door1"
            
        if nc_door1.prize == 'Supercar' and nc_door2.prize == 'Goat':      
            final_door_idx = doors.index(nc_door1)                          # "nc_door2" hides a Goat and gets opened, the Player moves from "chosen_door" to "nc_door1"
        
        if nc_door1.prize == 'Goat' and nc_door2.prize == 'Supercar':
            final_door_idx = doors.index(nc_door2)                          # "nc_door1" hides a Goat and gets opened, the Player moves from "chosen_door" to "nc_door2"
        

        final_door = doors[final_door_idx]
        if final_door.prize == 'Supercar':
            victories.append(i)

    ratio = len(victories) / MAX_ITERATIONS
    perc_ratio = ratio*100

    print("\'Turnin' Tables\' Policy results:")
    print("Total Victories (on 10000) = %d" % len(victories))
    print("Percentual Ratio of Victory = %.2f\n" % perc_ratio)

def play_game_never_change(doors, MAX_ITERATIONS):
    victories = list()

    for i in range(0, MAX_ITERATIONS):
        random.shuffle(doors)
        chosen_door_idx = random.randint(0,2)

        chosen_door = doors[chosen_door_idx]
        if chosen_door.prize == "Supercar":
            victories.append(i)
    
    ratio = len(victories) / MAX_ITERATIONS
    perc_ratio = ratio*100

    print("\'Once Chosen, Never Change!\' Policy results:")
    print("Total Victories (on 10000) = %d" % len(victories))
    print("Percentual Ratio of Victory = %.2f" % perc_ratio)    

# *** **** ***
# *** MAIN ***
# *** **** ***

# Problem's Setup
MAX_ITERATIONS = 10000

doors = list()
doors.append(Door("Supercar"))
doors.append(Door("Goat"))
doors.append(Door("Goat"))

# Test Execution
play_game_always_change(doors, MAX_ITERATIONS)
play_game_never_change(doors, MAX_ITERATIONS)