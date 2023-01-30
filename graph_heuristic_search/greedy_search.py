import numpy as np

class Node:
    def __init__(self, state, children, parent, cost_from_parent, h):
        self.state = state
        self.children = list()
        self.parent = parent
        self.cost_from_parent = cost_from_parent
        self.h = h

    def print_path(self):
        total_cost = 0
        solution_path = list()
        current_node = self
        while current_node is not None:
            total_cost += current_node.cost_from_parent
            current_node = current_node.parent
            solution_path.insert(0, current_node.state)
        
        print("*** SOLUZIONE: " + str(solution_path))
        print("*** TOTAL COST = %d" % total_cost)

class Graph:
    def __init__(self, graph_infos, objectives, heuristics):
        self.objectives = objectives
        self.heuristics = heuristics
        self.graph_nodes = list(graph_infos.keys())
        self.graph_arcs = np.zeros((len(self.graph_nodes),len(self.graph_nodes)), dtype=np.int)
    
        arcs_list = list()

        for node in self.graph_nodes:
            for neighbor in self.graph_nodes[node]:
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
    
    def greedy_search_tree_mode(self):
        starting_state = None

        while (starting_state is None):
            print("Starting State: ", end="")
            state = input()
            if state in self.graph_nodes:
                starting_state = state
            else:
                print("This State is not in the Graph!\n")
        
        print("\n*** STARTING: BREADTH FIRST SEARCH ***")
        fringe = list()

        solution_node = None

        iterate = True
        iteration = 1

        while iterate == True:
            if iteration == 1:
                current_node = Node(state=starting_state, parent=None, cost_from_parent=0, h=self.heuristics[starting_state])
            else:
                current_node = fringe.pop(0)
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_node.state)

            current_node_idx = self.graph_nodes.index(current_node.state)
            for i in range(len(self.graph_arcs[current_node_idx])):
                cost_from_parent = self.graph_arcs[current_node_idx][i]
                if cost_from_parent != 0:
                    state = self.graph_nodes[i]
                    new_neighbor = Node(state=state, parent=current_node, cost_from_parent=cost_from_parent, h=self.heuristics[state])
                    current_node.children.append(new_neighbor)

            for node in current_node.children:
                if len(fringe) == 0:
                    fringe.append(node)
                else:
                    for fringe_idx in range(len(fringe)):
                        if fringe[fringe_idx].h > node:
                            fringe.insert(fringe_idx,node)
                            break




    def greedy_search_graph_mode(self):
        pass
    




        