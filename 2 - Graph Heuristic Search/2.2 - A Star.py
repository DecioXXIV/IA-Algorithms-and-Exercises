import numpy as np

class Node:
    def __init__(self, state, parent, children, cost_from_parent, h, g, f):
        self.state = state
        self.parent = parent
        self.children = list()
        self.cost_from_parent = cost_from_parent
        self.heuristic = h
        self.cost_so_far = g
        self.priority = f
    
    def solution_dump(self, iteration):
        solution_path = list()
        total_cost = self.cost_so_far
        while self is not None:
            solution_path.append(self.state)
            self = self.parent

        solution_path.reverse()
        print("*** FINAL ITERATION: %d" % iteration) 
        print("*** SOLUTION = " + str(solution_path))
        print("*** TOTAL COST: %d\n" % total_cost)


class Graph:
    def __init__(self, graph_infos, heuristics):
        self.heuristics = heuristics
        self.graph_nodes = list(graph_infos.keys())
        self.graph_arcs = np.zeros((len(self.graph_nodes),len(self.graph_nodes)), dtype=np.int)
    
        arcs_list = list()
        for node in self.graph_nodes:
            for neighbor in graph_infos[node]:
                arcs_list.append((node,neighbor))
    
        for arc in arcs_list:
# An Highlight of the "arc" structure:
# - arc[0] contains a Node
# - arc[1] is a Tuple which contains the informations about the arc[0]'s Neighbor
    # - arc[1][0] contains a Node
    # - arc[1][1] specifies the cost to move between arc[0] and arc[1][0]
            node_idx = self.graph_nodes.index(arc[0])
            neighbor_idx = self.graph_nodes.index(arc[1][0])
            cost = arc[1][1]
            self.graph_arcs[node_idx][neighbor_idx] = cost
        
    def print_graph_description(self):
        print("\n***GRAPH DESCRIPTION***")
        for node in self.graph_nodes:
            node_idx = self.graph_nodes.index(node)
            print("%s" % node + " -> " + str(self.graph_arcs[node_idx]))
    
# *** ********************** ***
# *** A* ALGORITHM FUNCTIONS ***
# *** ********************** ***

    def a_star_tree_mode(self):
        print("*******************************")
        print("*** A* ALGORITHM, TREE MODE ***")
        print("*******************************\n")
        starting_state = None
        # The Search begins from a Starting Node, which must be in the Graph.
        while (starting_state is None):
            print("Starting State: ", end="")
            state = input()
            if state in self.graph_nodes:
                starting_state = state
            else:
                print("This State is not in the Graph!\n")

# ALGORITHM'S EXPLANATION: this version exploits the "Tree Search" model, in which the Fringe contains all the Children of the Expanded Node
# even if they contain an "already-visited" state. 
        print("\n*** STARTING THE SEARCH... ***")
        fringe = list()

        solution_node = None

# STEP 1: We decide to expand the first Node in the Fringe, which is the Fringe's Node with the lowest value of the Evalutation Function "f".
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_state, parent=None, children=list(), cost_from_parent=0, h=self.heuristics[starting_state], g=0, f=self.heuristics[starting_state])
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

# STEP 2: For the "current_node" we execute the Goal Test: if it succeeds we have found the Solution and the Algorithm ends, otherwise we retrieve all the Neighbors.            
            current_node_idx = self.graph_nodes.index(current_node.state)
            
            if int(current_node.heuristic) == 0:
                iterate = False
                solution_node = current_node
                print("*** SOLUTION FOUND! END OF THE SEARCH ***\n")
                break

            for i in range(len(self.graph_arcs[current_node_idx])):
                cost_from_parent = self.graph_arcs[current_node_idx][i]
                if cost_from_parent != 0:
                    state = self.graph_nodes[i]

                    new_neighbor = Node(state=state, parent=current_node, children=list(), cost_from_parent=cost_from_parent, h=self.heuristics[state], g=0, f=0)
                    new_neighbor.cost_so_far = new_neighbor.cost_from_parent + new_neighbor.parent.cost_so_far
                    new_neighbor.priority = new_neighbor.heuristic + new_neighbor.cost_so_far

                    current_node.children.append(new_neighbor)

# STEP 3: The Neighbors of the "current_node" are added to the Fringe.
# Insight: As said before, the Fringe is ordered with the "Increasing F Value" rule. The first Nodes are estimated to be closer to the Objective.
            for node in current_node.children:
                if len(fringe) == 0:
                    fringe.append(node)
                else:
                    for fringe_idx in range(len(fringe)):
                        if fringe[fringe_idx].priority > node.priority:
                            fringe.insert(fringe_idx,node)
                            break
                if node not in fringe:
                    fringe.append(node)

# The Algorithm ends when it founds the Solution or if the Fringe is empty.            
            print("Fringe: [ ", end="")
            for node in fringe:
                print(node.state + " ", end="")
            print("]")

            if len(fringe) == 0:
                iterate = False
                print("*** EMPTY FRINGE! END OF THE SEARCH ***\n")
                break

            iteration += 1
            print()

        if solution_node is not None:
            solution_node.solution_dump(iteration)
        else:
            print("*** THERE IS NOT AN OBJECTIVE NODE IN THE GRAPH! ***")

    def a_star_graph_mode(self):
        print("********************************")
        print("*** A* ALGORITHM, GRAPH MODE ***")
        print("********************************")
        starting_state = None
        # The Search begins from a Starting Node, which must be in the Graph.
        while (starting_state is None):
            print("Starting State: ", end="")
            state = input()
            if state in self.graph_nodes:
                starting_state = state
            else:
                print("This State is not in the Graph!\n")

# ALGORITHM'S EXPLANATION: this version exploits the "Graph Search" model, in which the Fringe contains only the "not-yet-expanded" Nodes.
        print("\n*** STARTING THE SEARCH... ***")
        fringe = list()
        closed_list = list()

        solution_node = None

# STEP 1: We decide to expand the first Node in the Fringe, which is the Fringe's Node with the lowest value of the Evalutation Function "f".
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_state, parent=None, children=list(), cost_from_parent=0, h=self.heuristics[starting_state], g=0, f=self.heuristics[starting_state])
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

# STEP 2: For the "current_node" we execute the Goal Test: if it succeeds we have found the Solution and the Algorithm ends, otherwise we retrieve all the Neighbors.            
            current_node_idx = self.graph_nodes.index(current_node.state)
            
            if int(current_node.heuristic) == 0:
                iterate = False
                solution_node = current_node
                print("*** SOLUTION FOUND! END OF THE SEARCH ***\n")
                break

            for i in range(len(self.graph_arcs[current_node_idx])):
                cost_from_parent = self.graph_arcs[current_node_idx][i]
                if cost_from_parent != 0:
                    state = self.graph_nodes[i]

                    new_neighbor = Node(state=state, parent=current_node, children=list(), cost_from_parent=cost_from_parent, h=self.heuristics[state], g=0, f=0)
                    new_neighbor.cost_so_far = new_neighbor.cost_from_parent + new_neighbor.parent.cost_so_far
                    new_neighbor.priority = new_neighbor.heuristic + new_neighbor.cost_so_far

                    current_node.children.append(new_neighbor)

# STEP 3: The Neighbors of the "current_node" are added to the Fringe.
# Insight: as said before...
#   - The Fringe is ordered with the "Increasing F Value" rule. The first Nodes are estimated to be closer to the Objective.
#   - The Fringe contains only the Nodes whose stats are "not-yet-visited".
            for node in current_node.children:
                if node.state not in closed_list:
                    if len(fringe) == 0:
                        fringe.append(node)
                    else:
                        for fringe_idx in range(len(fringe)):
                            if fringe[fringe_idx].priority > node.priority:
                                fringe.insert(fringe_idx,node)
                                break
                    if node not in fringe:
                        fringe.append(node)

# The Algorithm ends when it founds the Solution or if the Fringe is empty.            
            print("Fringe: [ ", end="")
            for node in fringe:
                print(node.state + " ", end="")
            print("]")

            if len(fringe) == 0:
                iterate = False
                print("*** EMPTY FRINGE! END OF THE SEARCH ***\n")
                break

            iteration += 1
            print()

        if solution_node is not None:
            solution_node.solution_dump(iteration)
        else:
            print("*** THERE IS NOT AN OBJECTIVE NODE IN THE GRAPH! ***")


# *** **** ***
# *** MAIN ***
# *** **** ***

# Insert your Graph and Heuristic information below

# graph_infos = dict()
# graph_infos[''] = [('',)]

# h = dict()
# h[''] = ...

# graph = Graph(graph_infos,h)
# graph.a_star_tree_mode()
# graph.a_star_graph_mode()