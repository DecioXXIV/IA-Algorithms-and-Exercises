import numpy as np

class Graph:
    def __init__(self, graph):
        self.graph_nodes = list(graph.keys())
        rows = columns = len(self.graph_nodes)

        self.graph_arcs = np.zeros((rows,columns), dtype=np.int)

        arcs_list = []
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

    def breadth_search(self):
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
        print("\n*** STARTING: BREADTH FIRST SEARCH ***")
        closed_list = list()
        fringe = list()

# STEP 1: We decide to expand the first Node in the Fringe, which gets removed from it and gets appended to the Closed List.
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = starting_node
            else:
                current_node = fringe[0]
                fringe.remove(current_node)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node)
            
            if current_node not in closed_list:
                closed_list.append(current_node)

# STEP 2: For the "current_node" we retrieve all the Neighbors.
            current_node_idx = self.graph_nodes.index(current_node)

            current_node_neighbors = list()
            for i in range(len(self.graph_arcs[current_node_idx])):
                archi = self.graph_arcs[current_node_idx]
                if self.graph_arcs[current_node_idx][i] != 0:
                    current_node_neighbors.append(self.graph_nodes[i])

# STEP 3: The Neighbors of the "current_node" are added to the Fringe, but only if they are "not-yet-expanded" Nodes.
# Insight: in this version of the Algorithm, we decide to order the Neighbors following the Lexicographic Rules. 
            current_node_neighbors.sort()
            for neighbor in current_node_neighbors:
                if neighbor not in closed_list:
                    fringe.append(neighbor)
            
# The Algorithm ends when the Fringe is empty.
            print("Fringe: " + str(fringe))
            if len(fringe) == 0:
                iterate = False
                print("\n*** END OF THE SEARCH ***")
                break

            iteration += 1
            print()

# *** ************ ***
# *** DEPTH SEARCH ***
# *** ************ ***

    def depth_search(self):
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
        print("\n*** STARTING: DEPTH FIRST SEARCH ***")
        closed_list = list()
        fringe = list()

# STEP 1: We decide to expand the first Node in the Fringe, which gets removed from it and gets appended to the Closed List.
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_node = starting_node
            else:
                current_node = fringe[0]
                fringe.remove(current_node)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node)
            
            if current_node not in closed_list:
                closed_list.append(current_node)

# STEP 2: For the "current_node" we retrieve all the Neighbors.
            current_node_idx = self.graph_nodes.index(current_node)

            current_node_neighbors = list()
            for i in range(len(self.graph_arcs[current_node_idx])):
                archi = self.graph_arcs[current_node_idx]
                if self.graph_arcs[current_node_idx][i] != 0:
                    current_node_neighbors.append(self.graph_nodes[i])

# STEP 3: The Neighbors of the "current_node" are added to the Fringe, but only if they are "not-yet-expanded" Nodes.
# Insight: in this version of the Algorithm, we decide to order the Neighbors following the Lexicographic Rules. 
            current_node_neighbors.sort(reverse=True)
            for neighbor in current_node_neighbors:
                if neighbor not in closed_list:
                    fringe.insert(0,neighbor)

# The Algorithm ends when the Fringe is empty.
            print("Fringe: " + str(fringe))
            if len(fringe) == 0:
                iterate = False
                print("\n*** END OF THE SEARCH ***")
                break

            iteration += 1
            print()