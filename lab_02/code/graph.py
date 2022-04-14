from matplotlib import pyplot

class Graph():
    def __init__(self):
        pass

    def plot_main_graphs(self, main_params):
        names = ["U", "F"]
        z = main_params[0]; F = main_params[1]
        u = main_params[2]; Up = main_params[3]
        pyplot.subplots(1, 1,figsize=(15,9))
        pyplot.subplot(1, 2, 1)
        pyplot.plot(z, F)
        pyplot.xlabel('z')
        pyplot.ylabel('F')
        pyplot.title('Зависимость F(z)')

        pyplot.subplot(1, 2, 2)
        pyplot.plot(z, u, label = 'u')
        pyplot.plot(z, Up, label = 'Up')
        pyplot.xlabel('z')
        pyplot.ylabel('u, up')
        pyplot.title('Зависимости u(z), up(z)')
        pyplot.legend()

        pyplot.show()

    def plot_dependence_graps(self, dependences):
        u_k0 = dependences[0]; u_T0 = dependences[1]
        u_Tw = dependences[2]; 
        u_p = dependences[3]
        u_R = dependences[4]

        pyplot.subplots(1, 1,figsize=(15,9))
        pyplot.subplot(2, 3, 1)
        pyplot.plot(u_k0[0], u_k0[1])
        pyplot.xlabel('k0')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(k0)")        

        pyplot.subplot(2, 3, 2)
        pyplot.plot(u_T0[0], u_T0[1])
        pyplot.xlabel('T0')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(T0)")

        pyplot.subplot(2, 3, 3)
        pyplot.plot(u_Tw[0], u_Tw[1])
        pyplot.xlabel('Tw')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(Tw)")

        pyplot.subplot(2, 3, 4)
        pyplot.plot(u_p[0], u_p[1])
        pyplot.xlabel('p')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(p)")

        pyplot.subplot(2, 3, 5)
        pyplot.plot(u_R[0], u_R[1])
        pyplot.xlabel('R')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(R)")

        pyplot.show()