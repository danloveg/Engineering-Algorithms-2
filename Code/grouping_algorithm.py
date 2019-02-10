import random
import copy
import time

UNEVEN_PENALTY = 5

class Cost:
    """Defines the cost of a solution"""
    def __init__(self, connection_cost, uneven_cost):
        self.connection_cost = connection_cost
        self.uneven_cost = uneven_cost

class AlgorithmSolution:
    """Contains all of the data associated with a solution to the problem"""
    def __init__(self, group_a, group_b, cost: Cost):
        self.group_a = group_a
        self.group_b = group_b
        self.cost = cost

def split_into_groups(adjacency_matrix):
    """
    Splits a matrix into two groups with minimal connection between groups.

    adjacency_matrix: A numpy N x N array representing a symmetric adjacency matrix
    """
    print('Using simulated annealing to split matrix into two groups with minimal connections.')
    print('Press CTRL-C at any point to stop.\n')

    graph_size = len(adjacency_matrix)

    # Number of tries to find a better solution without finding a better one is proportional to graph size
    consecutive_worse_cost_max = graph_size * graph_size

    # Initially, separate graph into two non-optimized groups
    (component_group_A, component_group_B) = get_initial_component_groups(graph_size)

    control_param = get_initial_control_parameter(adjacency_matrix, component_group_A, component_group_B)

    # Make the best solution really bad at first (very high cost)
    best_solution = AlgorithmSolution([], [], Cost(9 * (graph_size ^ 2), 9 * (graph_size ^ 2)))
    iteration = 1
    consecutive_worse_cost = 0
    better_solution_found = True
    start_time = time.time()
    
    while consecutive_worse_cost < consecutive_worse_cost_max:
        # Swap two nodes between group A and B (except on first iteration)
        if iteration != 1:
            indexA = random.choice(range(0, len(component_group_A)))
            indexB = random.choice(range(0, len(component_group_B)))
            temp = component_group_A[indexA]
            component_group_A[indexA] = component_group_B[indexB]
            component_group_B[indexB] = temp

        # Get the cost for this iteration
        current_cost = calculate_cost(adjacency_matrix, component_group_A, component_group_B)

        # If the new solution is better than the best one so far, make it the new best
        if current_cost.connection_cost < best_solution.cost.connection_cost:
            better_solution_found = True
            consecutive_worse_cost = 0
            best_solution = AlgorithmSolution(copy.deepcopy(component_group_A), copy.deepcopy(component_group_B), current_cost)

        # Else the new solution is no better than the current one
        else:
            better_solution_found = False
            consecutive_worse_cost += 1

        # Only print cost of new solution if we found a new best
        if better_solution_found:
            print("Iteration {}".format(iteration))
            print("Cost due to unevenness: {}\nConnection cost: {}\n".format(current_cost.uneven_cost, current_cost.connection_cost))

        # Don't keep running if cost is zero
        if best_solution.cost.connection_cost == 0:
            break

        iteration += 1

    print("> Finished running after {} iterations.".format(iteration))
    print("> Finished in {:.5f} seconds\n".format(time.time() - start_time))
    print_final_solution(best_solution)

def get_initial_control_parameter(adjacency_matrix, node_group_A, node_group_B):
    initial_cost = calculate_cost(adjacency_matrix, node_group_A, node_group_B)
    delta_multiplier = 5
    number_iterations = len(node_group_A) # This is arbitrary
    delta_cost_sum = 0

    node_group_A_copy = copy.deepcopy(node_group_A)
    node_group_B_copy = copy.deepcopy(node_group_B)

    for i in range(0, number_iterations):
        swap_one_item_between_groups(node_group_A_copy, node_group_B_copy)
        current_cost = calculate_cost(adjacency_matrix, node_group_A_copy, node_group_B_copy)
        delta_value = abs(initial_cost.connection_cost - current_cost.connection_cost)
        delta_cost_sum += delta_value

    return (delta_multiplier * (delta_cost_sum / number_iterations))

def swap_one_item_between_groups(node_group_A, node_group_B):
    indexA = random.choice(range(0, len(node_group_A)))
    indexB = random.choice(range(0, len(node_group_B)))
    temp = node_group_A[indexA]
    node_group_A[indexA] =node_group_B[indexB]
    node_group_B[indexB] = temp

def get_initial_component_groups(graph_size):
    # Shuffle component list
    all_components = list(range(0, graph_size))
    random.shuffle(all_components)

    # Put half of the components in one array, the other half in the other
    half_size = int(graph_size / 2)
    component_group_A = all_components[0: half_size]
    component_group_B = all_components[half_size:]

    return (component_group_A, component_group_B)

def calculate_cost(adjacency_matrix, node_group_A, node_group_B):
    # Get the number of connections between groups
    connection_cost = 0
    for i in node_group_A:
        for j in node_group_B:
            connection_cost += adjacency_matrix[i][j]

    # Get uneven penalty
    uneven_cost = UNEVEN_PENALTY * abs(len(node_group_A) - len(node_group_B))

    return Cost(connection_cost, uneven_cost)

def print_final_solution(solution: AlgorithmSolution):
    user_input = input("Do you want to print the final groups of components? (Y/N): ").strip().lower()
    if user_input == "y":
        solution.group_a.sort()
        solution.group_b.sort()
        group_a = list(map(lambda x: x + 1, solution.group_a))
        group_b = list(map(lambda x: x + 1, solution.group_b))
        print("Group A: {}".format(group_a))
        print("Group B: {}\n".format(group_b))
