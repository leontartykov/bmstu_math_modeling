from matplotlib import pyplot

class Graph():
    def __init__(self, z, u, F):
        self.z = z
        self.u = u
        self.F = F

    def plot_graph(self):
        names = ["U", "F"]
        pyplot.subplots(1, 1,figsize=(15,9))
        pyplot.subplot(1, 2, 1)
        pyplot.plot(self.z, self.u)
        pyplot.subplot(1, 2, 2)
        pyplot.plot(self.z, self.F)

        #ax.set_title('Зависимость результата от метода.')
        #ax.legend(names, bbox_to_anchor=(1, 0.6))
        #ax.set_xlabel('X')
        #ax.set_ylabel('Значение')
        #ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        pyplot.show()