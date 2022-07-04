from input_output import *
from differ_equation import DifferEquation
from graph import *

def main():
    input_data = input_values()
    solution = DifferEquation(input_data[0], input_data[1], input_data[2])
    result = solution.finite_difference_method()

    graph = Graph()
    graph.plot_main_graphs(result)


if __name__ == "__main__":
    main()