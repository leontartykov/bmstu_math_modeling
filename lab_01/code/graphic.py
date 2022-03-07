from matplotlib import pyplot

class GraphicLinear:
    def __init__(self, cauchy_methods_values):
        self.x = cauchy_methods_values[0]
        self.picard_1 = cauchy_methods_values[1]
        self.picard_2 = cauchy_methods_values[2]
        self.picard_3 = cauchy_methods_values[3]
        self.picard_4 = cauchy_methods_values[4]
        self.euler = cauchy_methods_values[5]
        self.runge_kutt = cauchy_methods_values[6]

        #print(self.x)
        #print(self.picard_1)
        #print(self.picard_2)
        #print(self.picard_3)
        #print(self.picard_4)
        #print(self.euler)
        #print(self.runge_kutt)

    def plot_graph(self):
        names = ["Пикар I", "Пикар II", "Пикар III", "Пикар IV", "Эйлер", "Рунге-Кутт"]
        fig, ax = pyplot.subplots(1, 1,figsize=(15,9))
        ax.plot(self.x, self.picard_1)
        ax.plot(self.x, self.picard_2)
        ax.plot(self.x, self.picard_3)
        ax.plot(self.x, self.picard_4)
        ax.plot(self.x, self.euler)
        ax.plot(self.x, self.runge_kutt)

        ax.set_title('Зависимость результата от метода.')
        ax.legend(names, bbox_to_anchor=(1, 0.6))
        ax.set_xlabel('X')
        ax.set_ylabel('Значение')
        ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        pyplot.show()
