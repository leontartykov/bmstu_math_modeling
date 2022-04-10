from input_output import *
from differ_equation import *
from graph import *

def main():
    input_data = input_values()
    solution = DifferEquation(input_data[0], input_data[1], input_data[2])
    result_graph = solution.get_solution()
    graph = Graph(result_graph[0], result_graph[1], result_graph[2])
    graph.plot_graph()

if __name__ == "__main__":
    main()