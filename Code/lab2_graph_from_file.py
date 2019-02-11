import graphtools
import grouping_algorithm_anneal
import plac
from pathlib import Path

def main(filename: "Path to file containing adjacency matrix"):
    filepath = Path(filename)

    if filepath.is_file():
        graph = graphtools.convert_text_matrix_to_graph(filepath)
        grouping_algorithm.split_into_groups(graph)
    else:
        print('"{}" does not exist.'.format(filename))

if __name__ == '__main__':
    try:
        plac.call(main)
    except KeyboardInterrupt:
        print('Exiting.')
