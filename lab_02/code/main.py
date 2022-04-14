from unittest import result
from input_output import *
from differ_equation import *
from graph import *

def main():
    input_data = input_values()
    solution = DifferEquation(input_data[0], input_data[1], input_data[2])
    result_graph = solution.get_solution()
    u_k0 = solution.define_dependence_u_k0()
    u_T0 = solution.define_dependence_u_T0()
    u_Tw = solution.define_dependence_u_Tw()
    u_p = solution.define_dependence_u_p()
    u_R = solution.define_dependence_u_R()
    dependences = [u_k0, u_T0, u_Tw, u_p, u_R]

    graph = Graph()
    graph.plot_main_graphs(result_graph)
    graph.plot_dependence_graps(dependences)

if __name__ == "__main__":
    main()