import graphtools
import grouping_algorithm
import plac

def str_to_int(string):
    try:
        return int(string)
    except ValueError:
        raise ValueError('Value "{}" could not be converted to an integer'.format(string))

def main(size: "Size of graph", sparseness: "Percentage of graph that is sparse"):
    graph = graphtools.create_symmetric_graph(str_to_int(size), str_to_int(sparseness))
    grouping_algorithm.split_into_groups(graph)

if __name__ == '__main__':
    try:
        plac.call(main)
    except KeyboardInterrupt:
        print('Exiting.')
