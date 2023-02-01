import numpy as np

class Node:
    pass
    def __init__(self, state, parent, cost_from_parent):
        self.state = state
        self.parent = parent
        self.cost_from_parent = cost_from_parent
    
    def solution_dump(self, iteration):
        solution_path = list()
        total_cost = 0
        while self is not None:
            solution_path.append(self.state)
            total_cost += self.cost_from_parent
            self = self.parent
        solution_path.reverse()
        print("*** FINAL ITERATION: %d" % iteration) 
        print("*** SOLUTION = " + str(solution_path))
        print("*** TOTAL COST: %d\n" % total_cost)


class Graph:
    def __init__(self, graph, objectives):
        self.objectives = objectives
        self.graph_nodes = list(graph.keys())
        rows = columns = len(self.graph_nodes)

        self.graph_arcs = np.zeros((rows,columns), dtype=np.int)

        arcs_list = list()
        for node in self.graph_nodes:
            for neighbor in graph[node]:
                arcs_list.append((node,neighbor))

        for arc in arcs_list:
# An Highlight of the "arc" structure:
# - arc[0] contains a Node
# - arc[1] is a Tuple which contains the informations about the arc[0]'s Neighbor
    # - arc[1][0] contains a Node
    # - arc[1][1] specifies the cost to move between arc[0] and arc[1][0]

            first_idx = self.graph_nodes.index(arc[0])
            second_idx = self.graph_nodes.index(arc[1][0])
            cost = arc[1][1]
            self.graph_arcs[first_idx][second_idx] = cost

    def print_graph_description(self):
        print("\n***GRAPH DESCRIPTION***")
        for node in self.graph_nodes:
            node_idx = self.graph_nodes.index(node)
            print("%s" % node + " -> " + str(self.graph_arcs[node_idx]))


# *** ************** ***
# *** BREADTH SEARCH ***
# *** ************** ***

    def breadth_search_to_obj(self):
        print("**********************************")
        print("*** BREADTH SEARCH, GRAPH MODE ***")
        print("**********************************\n")
        starting_node = None

# The Search begins from a Starting Node, which must be in the Graph.
        while(starting_node is None):
            print("Starting Node: ", end="")
            node = input()
            if node in self.graph_nodes:
                starting_node = node
            else:
                print("This Node is not in the Graph!\n")

# ALGORITHM'S EXPLANATION: this version exploits the "Graph Search" model, in which the Fringe contains only the "not-yet-expanded" Nodes.        
        print("\n*** STARTING THE SEARCH... ***")
        closed_list = list()
        fringe = list()

        solution_node = None

# STEP 1: We decide to expand the first Node in the Fringe, which gets removed from it and gets appended to the Closed List.
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_node, parent=None, cost_from_parent=0)
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

            if current_node.state not in closed_list:
                closed_list.append(current_node.state)

# STEP 2: For the "current_node" we execute the Goal Test: if it succeeds we have found the Solution and the Algorithm ends, otherwise we retrieve all the Neighbors.
            current_node_idx = self.graph_nodes.index(current_node.state)

            if self.objectives[current_node_idx] == 1:
                iterate = False
                solution_node = current_node
                print("*** SOLUTION FOUND! END OF THE SEARCH ***\n")
                break

            current_node_neighbors = list()
            for i in range(len(self.graph_arcs[current_node_idx])):
                if self.graph_arcs[current_node_idx][i] != 0:
                    current_node_neighbors.append(self.graph_nodes[i])

# STEP 3: The Neighbors of the "current_node" are added to the Fringe, but only if they are "not-yet-expanded" Nodes.
# Insight: in this version of the Algorithm, we decide to order the Neighbors following the Lexicographic Rules. 
            current_node_neighbors.sort()
            for neighbor in current_node_neighbors:
                if neighbor not in closed_list:
                    neighbor_idx = self.graph_nodes.index(neighbor)
                    cost_from_parent = self.graph_arcs[current_node_idx][neighbor_idx]

                    new_neighbor = Node(state=self.graph_nodes[neighbor_idx], parent=current_node, cost_from_parent=cost_from_parent)
                    fringe.append(new_neighbor)
            
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
            print("*** THERE IS NOT AN OBJECTIVE NODE IN THE GRAPH! ***\n")
     
# *** ************ ***
# *** DEPTH SEARCH ***
# *** ************ ***

    def depth_search_to_obj(self):
        print("********************************")
        print("*** DEPTH SEARCH, GRAPH MODE ***")
        print("********************************\n")
        starting_node = None

# The Search begins from a Starting Node, which must be in the Graph.
        while(starting_node is None):
            print("Starting Node: ", end="")
            node = input()
            if node in self.graph_nodes:
                starting_node = node
            else:
                print("This Node is not in the Graph!\n")

# ALGORITHM'S EXPLANATION: this version exploits the "Graph Search" model, in which the Fringe contains only the "not-yet-expanded" Nodes.        
        print("\n*** STARTING THE SEARCH... ***")
        closed_list = list()
        fringe = list()

        solution_node = None

# STEP 1: We decide to expand the first Node in the Fringe, which gets removed from it and gets appended to the Closed List.
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_node, parent=None, cost_from_parent=0)
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

            if current_node.state not in closed_list:
                closed_list.append(current_node.state)

# STEP 2: For the "current_node" we execute the Goal Test: if it succeeds we have found the Solution and the Algorithm ends, otherwise we retrieve all the Neighbors.
            current_node_idx = self.graph_nodes.index(current_node.state)

            if self.objectives[current_node_idx] == 1:
                iterate = False
                solution_node = current_node
                print("*** SOLUTION FOUND! END OF THE SEARCH ***\n")
                break

            current_node_neighbors = list()
            for i in range(len(self.graph_arcs[current_node_idx])):
                if self.graph_arcs[current_node_idx][i] != 0:
                    current_node_neighbors.append(self.graph_nodes[i])

# STEP 3: The Neighbors of the "current_node" are added to the Fringe, but only if they are "not-yet-expanded" Nodes.
# Insight: in this version of the Algorithm, we decide to order the Neighbors following the Lexicographic Rules. 
            current_node_neighbors.sort(reverse=True)
            for neighbor in current_node_neighbors:
                if neighbor not in closed_list:
                    neighbor_idx = self.graph_nodes.index(neighbor)
                    cost_from_parent = self.graph_arcs[current_node_idx][neighbor_idx]

                    new_neighbor = Node(state=neighbor, parent=current_node, cost_from_parent=cost_from_parent)
                    fringe.insert(0,new_neighbor)
            
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
            print("*** THERE IS NOT AN OBJECTIVE NODE IN THE GRAPH! ***\n")


# *** **** ***
# *** MAIN ***
# *** **** ***

# Insert your Graph below

# graph_infos = dict()
# graph_infos[''] = [('',)]
# objectives = []
# graph = Graph(graph_infos, objectives)

# graph.breadth_search_to_obj()
# graph.depth_search_to_obj()