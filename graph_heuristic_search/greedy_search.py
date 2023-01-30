import numpy as np

class Node:
    def __init__(self, state, children, parent, cost_from_parent, h):
        self.state = state
        self.children = list()
        self.parent = parent
        self.cost_from_parent = cost_from_parent
        self.h = h

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

# *** *********************** ***
# *** GREEDY SEARCH FUNCTIONS ***
# *** *********************** ***
    
    def greedy_search_tree_mode(self):
        print("********************************")
        print("*** GREEDY SEARCH, TREE MODE ***")
        print("********************************\n")
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

# STEP 1: We decide to expand the first Node in the Fringe, which is the Fringe's Node with the lowest value of the Heuristic Function "h".
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_state, parent=None, cost_from_parent=0, h=self.heuristics[starting_state], children=list())
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

# STEP 2: For the "current_node" we execute the Goal Test: if it succeeds we have found the Solution and the Algorithm ends, otherwise we retrieve all the Neighbors.            
            current_node_idx = self.graph_nodes.index(current_node.state)
            
            if current_node.h == int(0):
                iterate = False
                solution_node = current_node
                print("*** SOLUTION FOUND! END OF THE SEARCH ***\n")
                break

            for i in range(len(self.graph_arcs[current_node_idx])):
                cost_from_parent = self.graph_arcs[current_node_idx][i]
                if cost_from_parent != 0:
                    state = self.graph_nodes[i]
                    new_neighbor = Node(state=state, parent=current_node, cost_from_parent=cost_from_parent, h=self.heuristics[state], children=list())
                    current_node.children.append(new_neighbor)

# STEP 3: The Neighbors of the "current_node" are added to the Fringe.
# Insight: As said before, the Fringe is ordered with the "Increasing H Value" rule. The first Nodes are estimated to be closer to the Objective.
            for node in current_node.children:
                if len(fringe) == 0:
                    fringe.append(node)
                else:
                    for fringe_idx in range(len(fringe)):
                        if fringe[fringe_idx].h > node.h:
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
            solution_path = list()
            total_cost = 0
            while solution_node is not None:
                solution_path.append(solution_node.state)
                total_cost += solution_node.cost_from_parent
                solution_node = solution_node.parent
            solution_path.reverse()
            print("*** FINAL ITERATION: %d" % iteration) 
            print("*** SOLUTION = " + str(solution_path))
            print("*** TOTAL COST: %d" % total_cost)
        else:
            print("*** THERE IS NOT AN OBJECTIVE NODE IN THE GRAPH! ***")

    def greedy_search_graph_mode(self):
        print("*********************************")
        print("*** GREEDY SEARCH, GRAPH MODE ***")
        print("*********************************\n")
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

# STEP 1: We decide to expand the first Node in the Fringe, which is the Fringe's Node with the lowest value of the Heuristic Function "h".
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_state, parent=None, cost_from_parent=0, h=self.heuristics[starting_state], children=list())
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

            if current_node.state not in closed_list:
                closed_list.append(current_node.state)

# STEP 2: For the "current_node" we execute the Goal Test: if it succeeds we have found the Solution and the Algorithm ends, otherwise we retrieve all the Neighbors.            
            current_node_idx = self.graph_nodes.index(current_node.state)
            
            if current_node.h == int(0):
                iterate = False
                solution_node = current_node
                print("*** SOLUTION FOUND! END OF THE SEARCH ***\n")
                break

            for i in range(len(self.graph_arcs[current_node_idx])):
                cost_from_parent = self.graph_arcs[current_node_idx][i]
                if cost_from_parent != 0:
                    state = self.graph_nodes[i]
                    new_neighbor = Node(state=state, parent=current_node, cost_from_parent=cost_from_parent, h=self.heuristics[state], children=list())
                    current_node.children.append(new_neighbor)

# STEP 3: The Neighbors of the "current_node" are added to the Fringe.
# Insight: As said before, the Fringe is ordered with the "Increasing H Value" rule. The first Nodes are estimated to be closer to the Objective.
            for node in current_node.children:
                if node.state not in closed_list:
                    if len(fringe) == 0:
                        fringe.append(node)
                    else:
                        for fringe_idx in range(len(fringe)):
                            if fringe[fringe_idx].h > node.h:
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
            solution_path = list()
            total_cost = 0
            while solution_node is not None:
                solution_path.append(solution_node.state)
                total_cost += solution_node.cost_from_parent
                solution_node = solution_node.parent
            solution_path.reverse()
            print("*** FINAL ITERATION: %d" % iteration) 
            print("*** SOLUTION = " + str(solution_path))
            print("*** TOTAL COST: %d" % total_cost)
        else:
            print("*** THERE IS NOT AN OBJECTIVE NODE IN THE GRAPH! ***")


# *** **** ***
# *** MAIN ***
# *** **** ***

# Insert your Graph and Heuristic information below

graph_infos = dict()
graph_infos['Arad'] = [('Sibiu',140),('Timisoara',118),('Zerind',75)]
graph_infos['Bucharest'] = [('Fagaras',211),('Giurgiu',90),('Pitesti',101),('Urziceni',85)]
graph_infos['Craiova'] = [('Drobeta',120),('Pitesti',120),('Rimnicu',146)]
graph_infos['Drobeta'] = [('Craiova',120),('Mehadia',75)]
graph_infos['Eforie'] = [('Hirsova',86)]
graph_infos['Fagaras'] = [('Sibiu',99),('Bucharest',211)]
graph_infos['Giurgiu'] = [('Bucharest',90)]
graph_infos['Hirsova'] = [('Eforie',86),('Urziceni',98)]
graph_infos['Iasi'] = [('Neamt',87),('Vaslui',92)]
graph_infos['Lugoj'] = [('Mehadia',70),('Timisoara',111)]
graph_infos['Mehadia'] = [('Drobeta',75),('Lugoj',70)]
graph_infos['Neamt'] = [('Iasi',87)]
graph_infos['Oradea'] = [('Sibiu',151),('Zerind',71)]
graph_infos['Pitesti'] = [('Bucharest',101),('Craiova',120),('Rimnicu',97)]
graph_infos['Rimnicu'] = [('Craiova',146),('Pitesti',97),('Sibiu',80)]
graph_infos['Sibiu'] = [('Arad',140),('Fagaras',99),('Oradea',151),('Rimnicu',80)]
graph_infos['Timisoara'] = [('Arad',118),('Lugoj',111)]
graph_infos['Urziceni'] = [('Bucharest',85),('Hirsova',98),('Vaslui',142)]
graph_infos['Vaslui'] = [('Iasi',92),('Urziceni',142)]
graph_infos['Zerind'] = [('Arad',75),('Oradea',71)]

h = dict() # Distanza in Linea d'Aria da Bucharest (Obbiettivo)
h['Arad'] = 366
h['Bucharest'] = 0
h['Craiova'] = 160
h['Drobeta'] = 242
h['Eforie'] = 161
h['Fagaras'] = 176
h['Giurgiu'] = 77
h['Hirsova'] = 151
h['Iasi'] = 226
h['Lugoj'] = 244
h['Mehadia'] = 241
h['Neamt'] = 234
h['Oradea'] = 380
h['Pitesti'] = 100
h['Rimnicu'] = 193
h['Sibiu'] = 253
h['Timisoara'] = 329
h['Urziceni'] = 80
h['Vaslui'] = 199
h['Zerind'] = 374

graph = Graph(graph_infos,h)
graph.greedy_search_tree_mode()




        