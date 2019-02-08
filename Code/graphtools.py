import random
import numpy

def create_symmetric_graph(_size, sparseness):
    """
    Creates and returns a symmetric 2D numpy array of N x N size.

    _size: Dimension N
    sparseness: Value from 0 to 100 determining the percent chance that a node has no connection
        to another node. 100 means that a node will have a 100% chance of having no connection to
        another node (no nodes will be connected). 0 means that a node will have a 0% chance of
        not being connected to another node (the graph will be complete).
    """
    if _size < 2:
        raise ValueError('_size must not be less than two')
    
    if sparseness < 0 or sparseness > 100:
        raise ValueError('Sparseness must be between 0 and 100 (inclusive)')

    # Create a matrix of random integers from 1 to 9
    graph = numpy.random.random_integers(1, 9, size=(_size, _size))

    # Apply sparseness
    chance_of_sparseness = numpy.ones(100)
    chance_of_sparseness[0: sparseness] = 0

    for i in range(0, _size):
        for j in range(0, _size):
            graph[i][j] = graph[i][j] * random.choice(chance_of_sparseness)

    # Get the lower triangle of the random matrix (also ensures diagonal is all zeros)
    symmetric_graph = numpy.tril(graph, k=-1)

    # Symmetrize the matrix
    for i in range(0, _size):
        for j in range(0, _size):
            symmetric_graph[i][j] = symmetric_graph[j][i]

    return symmetric_graph


def create_symmetric_half_connected_graph(_size, sparseness):
    """
    Creates and returns a symmetric 2D numpy array of N x N size, where the nodes are split into
    two disjoint groups.

    _size: Dimension N
    sparseness: Value from 0 to 100 determining the percent chance that a node has no connection
        to another node. 100 means that a node will have a 100% chance of having no connection to
        another node (no nodes will be connected). 0 means that a node will have a 0% chance of
        not being connected to another node (the graph will be complete).
    """
    # Get a symmetric graph
    half_connected_graph = create_symmetric_graph(_size, sparseness)

    # Create two disjoint sets of nodes
    num_nodes_group_1 = int(_size / 2)
    for i in range(0, num_nodes_group_1):
        for j in range(num_nodes_group_1, _size):
            half_connected_graph[i][j] = 0
            half_connected_graph[j][i] = 0

    return half_connected_graph


def convert_text_matrix_to_graph(filepath):
    """
    Converts and returns a 2D numpy array from a text representation of an adjacency matrix.

    filepath: Path to text file
    """
    filelines = []
    with open(filepath, 'r') as f:
        filelines = f.readlines()

    rows_of_numbers = []
    for line in filelines:
        formatted_line = line.replace(' ', '').replace('\n', '')
        numbers = []

        for number in formatted_line:
            numbers.append(int(number))

        rows_of_numbers.append(numbers)

    numpy_array = numpy.array(rows_of_numbers)

    return numpy_array
