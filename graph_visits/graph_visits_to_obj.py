import numpy as np

class GraphSearchNode:
    pass
    def __init__(self, state, parent, cost_from_parent):
        self.state = state
        self.parent = parent
        self.cost_from_parent = cost_from_parent

class Graph:
    def __init__(self, graph, objectives):
        self.objectives = objectives
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

    def breadth_search_to_obj(self):
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

        graph_search_nodes = list()

        solution_node = None

# STEP 1: We decide to expand the first Node in the Fringe, which gets removed from it and gets appended to the Closed List.
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_search_node = GraphSearchNode(state=starting_node, parent=None, cost_from_parent=0)
                graph_search_nodes.append(current_search_node)
            else:
                current_node = fringe.pop(0)
                current_search_node = None
                for search_node in graph_search_nodes:
                    if search_node.state == current_node:
                        current_search_node = search_node
                        break
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_search_node.state)

            if current_search_node.state not in closed_list:
                closed_list.append(current_search_node.state)

# STEP 2: For the "current_node" we retrieve all the Neighbors.
            current_node_idx = self.graph_nodes.index(current_search_node.state)

            current_node_neighbors = list()
            for i in range(len(self.graph_arcs[current_node_idx])):
                if self.graph_arcs[current_node_idx][i] != 0:
                    current_node_neighbors.append(self.graph_nodes[i])

# STEP 3: The Neighbors of the "current_node" are added to the Fringe, but only if they are "not-yet-expanded" Nodes.
# Insight: in this version of the Algorithm, we decide to order the Neighbors following the Lexicographic Rules. 
            current_node_neighbors.sort()
            for neighbor in current_node_neighbors:
                if neighbor not in closed_list:
                    fringe.append(neighbor)

                    neighbor_idx = self.graph_nodes.index(neighbor)
                    cost_from_parent = self.graph_arcs[current_node_idx][neighbor_idx]
                    graph_search_nodes.append(GraphSearchNode(neighbor, current_search_node, cost_from_parent))
            
# The Algorithm ends when it founds the Solution or when the Fringe is empty.
            print("Fringe: " + str(fringe))

            if self.objectives[current_node_idx] == 1:
                iterate = False
                solution_node = current_search_node
                print("\n*** SOLUTION FOUND! END OF THE SEARCH ***")
                break
            
            if len(fringe) == 0:
                iterate = False
                print("\n*** EMPTY FRINGE! END OF THE SEARCH ***")
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
     
# *** ************ ***
# *** DEPTH SEARCH ***
# *** ************ ***

    def depth_search_to_obj(self):
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

        graph_search_nodes = list()

        solution_node = None

# STEP 1: We decide to expand the first Node in the Fringe, which gets removed from it and gets appended to the Closed List.
        iterate = True
        iteration = 1
        while iterate == True:
            if iteration == 1:
                current_search_node = GraphSearchNode(state=starting_node, parent=None, cost_from_parent=0)
                graph_search_nodes.append(current_search_node)
            else:
                current_node = fringe.pop(0)
                current_search_node = None
                for search_node in graph_search_nodes:
                    if search_node.state == current_node and search_node:
                        current_search_node = search_node
                        break
            
            print("ITERATION: %d" % iteration)
            print("Expanded Node: %s" % current_search_node.state)

            if current_search_node.state not in closed_list:
                closed_list.append(current_search_node.state)

# STEP 2: For the "current_node" we retrieve all the Neighbors.
            current_node_idx = self.graph_nodes.index(current_search_node.state)

            current_node_neighbors = list()
            for i in range(len(self.graph_arcs[current_node_idx])):
                if self.graph_arcs[current_node_idx][i] != 0:
                    current_node_neighbors.append(self.graph_nodes[i])

# STEP 3: The Neighbors of the "current_node" are added to the Fringe, but only if they are "not-yet-expanded" Nodes.
# Insight: in this version of the Algorithm, we decide to order the Neighbors following the Lexicographic Rules. 
            current_node_neighbors.sort(reverse=True)
            for neighbor in current_node_neighbors:
                if neighbor not in closed_list:
                    fringe.insert(0,neighbor)

                    neighbor_idx = self.graph_nodes.index(neighbor)
                    cost_from_parent = self.graph_arcs[current_node_idx][neighbor_idx]
                    graph_search_nodes.insert(0,GraphSearchNode(neighbor, current_search_node, cost_from_parent))
            
# The Algorithm ends when the Fringe is empty.
            print("Fringe: " + str(fringe))

            if self.objectives[current_node_idx] == 1:
                iterate = False
                solution_node = current_search_node
                print("\n*** SOLUTION FOUND! END OF THE SEARCH ***")
                break
            
            if len(fringe) == 0:
                iterate = False
                print("\n*** EMPTY FRINGE! END OF THE SEARCH ***")
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

# Insert your Graph below

# graph_infos = dict()
# graph_infos[''] = [('',)]
# objectives = []
# graph = Graph(graph_infos, objectives)

# graph.breadth_search_to_obj()
# graph.depth_search_to_obj()

graph_infos = dict()
graph_infos['AQ'] = [('RM',11),('AN',19),('PG',17)]
graph_infos['AN'] = [('BO',21),('AQ',19),('BA',46),('PG',16)]
graph_infos['BA'] = [('RM',46),('AN',45)]
graph_infos['BO'] = [('AN',21),('MI',21),('FI',10)]
graph_infos['FI'] = [('BO',10),('RM',28),('PG',15),('PI',9),('GE',22)]
graph_infos['GE'] = [('FI',22),('PI',16),('MI',14)]
graph_infos['MI'] = [('TO',14),('GE',14),('BO',21)]
graph_infos['NA'] = [('RM',22)]
graph_infos['PG'] = [('RM',17),('FI',15),('AN',16),('AQ',17)]
graph_infos['PI'] = [('FI',9),('GE',16),('RM',37)]
graph_infos['RM'] = [('NA',22),('AQ',11),('BA',45),('PI',17),('PG',37),('FI',28)]
graph_infos['TO'] = [('MI',14)]

objectives = [0,0,1,0,0,0,0,0,0,0,0,0]

graph = Graph(graph_infos,objectives)

graph.depth_search_to_obj()



