import random
import copy
import time
import math
import cost_plotter

UNEVEN_PENALTY = 5

# Simulated annealing variables. These can be tweaked to change the performance of the algorithm
CONTROL_PARAM_DECREASE_RATE = 0.92
INIT_CONTROL_PARAM_MULTIPLIER = 2
GRAPH_SIZE_ITERATION_MULTIPLIER = 5

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

    consecutive_solutions_unchanged_max = graph_size * graph_size

    (component_group_A, component_group_B) = get_initial_component_groups(graph_size)

    control_param = get_initial_control_parameter(adjacency_matrix, component_group_A, component_group_B)
    initial_cost = calculate_cost(adjacency_matrix, component_group_A, component_group_B)

    best_solution = AlgorithmSolution(\
        copy.deepcopy(component_group_A),\
        copy.deepcopy(component_group_B),\
        initial_cost)
    
    solution_list = []
    iteration = 1
    consecutive_solutions_unchanged = 0
    new_solution = True
    start_time = time.time()
    
    while consecutive_solutions_unchanged < consecutive_solutions_unchanged_max:
        # Edge case: stop running when cost is zero
        if best_solution.cost.connection_cost == 0:
            break
        
        for i in range(0, graph_size * GRAPH_SIZE_ITERATION_MULTIPLIER):
            swap_one_item_between_groups(component_group_A, component_group_B)

            current_cost = calculate_cost(adjacency_matrix, component_group_A, component_group_B)

            # Simulated annealing
            delta = best_solution.cost.connection_cost - current_cost.connection_cost
            probability_to_take = math.exp(delta / control_param)
            random_num = random.random()
            take_solution = (random_num < probability_to_take)
            
            #print("kT: {:.4f}, DELTA: {}, PROB: {:.4f}, RAND: {:.4}, TAKE: {}".format(\
            #    control_param, delta, probability_to_take, random_num, take_solution))

            # Take better solution unconditionally
            # - OR -
            # Take worse solution with some probability
            if take_solution:
                solution_list.append(current_cost.connection_cost)
                new_solution = True
                consecutive_solutions_unchanged = 0
                best_solution = AlgorithmSolution(\
                    copy.deepcopy(component_group_A),\
                    copy.deepcopy(component_group_B),\
                    current_cost)

            else:
                new_solution = False
                consecutive_solutions_unchanged += 1

            if new_solution:
                print("Iteration {}".format(iteration))
                print("Cost due to unevenness: {}\nConnection cost: {}\n".format(current_cost.uneven_cost, current_cost.connection_cost))

            iteration += 1
        # end for

        # Decrease control parameter geometrically
        control_param = control_param * CONTROL_PARAM_DECREASE_RATE

    # end while

    print("> Finished running after {} iterations.".format(iteration))
    print("> Finished in {:.5f} seconds".format(time.time() - start_time))
    print("> Initial cost: {}".format(initial_cost.connection_cost))
    print("> Final cost: {}\n".format(best_solution.cost.connection_cost))
    print_final_solution(best_solution)
    show_cost_plot(solution_list)

def get_initial_control_parameter(adjacency_matrix, node_group_A, node_group_B):
    initial_cost = calculate_cost(adjacency_matrix, node_group_A, node_group_B)
    number_iterations = int((len(node_group_A) **2) / 2) # Experimentally derived
    delta_cost_sum = 0

    node_group_A_copy = copy.deepcopy(node_group_A)
    node_group_B_copy = copy.deepcopy(node_group_B)

    for i in range(0, number_iterations):
        swap_one_item_between_groups(node_group_A_copy, node_group_B_copy)
        current_cost = calculate_cost(adjacency_matrix, node_group_A_copy, node_group_B_copy)
        delta_value = abs(initial_cost.connection_cost - current_cost.connection_cost)
        delta_cost_sum += delta_value

    return (INIT_CONTROL_PARAM_MULTIPLIER * (delta_cost_sum / number_iterations))

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
    solution.group_a.sort()
    solution.group_b.sort()
    group_a = list(map(lambda x: x + 1, solution.group_a))
    group_b = list(map(lambda x: x + 1, solution.group_b))
    print("> Final groups of nodes:")
    print("> Group A: {}".format(group_a))
    print("> Group B: {}\n".format(group_b))

def show_cost_plot(cost_list):
    user_input = input("> Do you want to plot the costs changing over time? (Y/N): ").strip().lower()
    if user_input == "y":
        cost_plotter.plot_costs(cost_list)