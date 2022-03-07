from math import fabs
from tracemalloc import start
from point import *

class DifferEquation:
    """
    Однородные дифференциальные уравнения
    """
    def __init__(self, left_board: float, right_board: float, step:float):
        self.left_board = left_board
        self.right_board = right_board
        self.step = step

        self.is_data_graph = False
        self.x = []
        self.picard_1 = []
        self.picard_2 = []
        self.picard_3 = []
        self.picard_4 = []
        self.euler = []
        self.runge_kutt = []
        self.default_step = 0.05

    def info(self):
        print("Текущее состояние объекта:")
        print(f"Левая граница: {self.left_board}")
        print(f"Правая граница: {self.right_board}")
        print(f"Шаг: {self.step}")

    def f(self, x, y):
        """
        Исходная функция u(x) = x^2 + u^2
        """
        return x * x + y * y

    def calc_euler_method(self, last_x, last_u) -> None:
        """
        Метод Эйлера
        """
        return last_u + self.step * self.f(last_x, last_u)

    def calc_picard_1_method(self, x):
        """
        Метод Пикара I порядка точности
        """
        return pow(x, 3) / 3

    def calc_picard_2_method(self, x):
        """
        Метод Пикара II порядка точности
        """
        return self.calc_picard_1_method(x) + pow(x, 7) / 63

    def calc_picard_3_method(self, x):
        """
        Метод Пикара III порядка точности
        """
        return self.calc_picard_2_method(x) + 2 * pow(x, 11) / 2079 + \
               pow(x, 15) / 59535

    def calc_picard_4_method(self, x):
        """
        Метод Пикара IV порядка точности
        """
        return pow(x, 31) / 109876902975 + \
               4 * pow(x, 27) / 3341878155 + \
               4 * pow(x, 23) / 99411543 + \
               2 * pow(x, 23) / 86266215 + \
               82 * pow(x, 19) / 37328445 + \
               13 * pow(x, 15) / 218295 + \
               2 * pow(x, 11) / 2079 + \
               self.calc_picard_2_method(x)

    def calc_runge_kutt_method(self, last_x, last_u):
        """
        Метод Рунге-Кутта
        при значении alpha = 1
        """ 
        return last_u + self.step * self.f(last_x + self.step / 2, 
                                           last_u + self.step / 2 * self.f(last_x, last_u))
        
    def get_table(self):
        print("x     |Пикар I порядка │ Пикар II порядка │ Пикар III порядка │ Пикар IV порядка │    Эйлер     │    Рунге-Кутт\n" + \
              "────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        start_x = self.left_board; end_x = self.right_board
        last_x_runge_kutt = self.left_board; current_x_runge_kutt = self.left_board
        last_u_runge_kutt = self.left_board; current_u_runge_kutt = self.left_board
        last_x_euler = self.left_board; current_x_euler = self.left_board
        last_u_euler = self.left_board; current_u_euler = self.left_board
        picard_1_u = self.left_board; picard_2_u = self.left_board
        picard_3_u = self.left_board; picard_4_u = self.left_board

        x_default_step = self.left_board
        diff_start_default_x = 0 
        while start_x < end_x:
            diff_start_default_x = fabs(start_x - x_default_step)
            if self.is_data_graph == False and diff_start_default_x <= 1e-3:
                self.x.append(start_x)
                self.picard_1.append(picard_1_u)
                self.picard_2.append(picard_2_u)
                self.picard_3.append(picard_3_u)
                self.picard_4.append(picard_4_u)
                self.euler.append(current_u_euler)
                self.runge_kutt.append(current_u_runge_kutt)
            
            if start_x >= self.left_board and diff_start_default_x <= 1e-3:
                print(f"{x_default_step:4.3f} |{picard_1_u:16.6f} | {picard_2_u:16.6f}" + 
                    f"| {picard_3_u:18.6f} | {picard_4_u:16.6f}" +
                    f"| {current_u_euler:13.6f} | {current_u_runge_kutt:16.6f}")
                x_default_step += self.default_step

            start_x += self.step

            last_x_euler = current_x_euler; current_x_euler = start_x
            last_u_euler = current_u_euler
            current_u_euler = self.calc_euler_method(last_x_euler, last_u_euler)

            last_x_runge_kutt = current_x_runge_kutt
            current_x_runge_kutt = start_x
            last_u_runge_kutt = current_u_runge_kutt
            current_u_runge_kutt = self.calc_runge_kutt_method(last_x_runge_kutt, last_u_runge_kutt)

            picard_1_u = self.calc_picard_1_method(start_x)
            picard_2_u = self.calc_picard_2_method(start_x)
            picard_3_u = self.calc_picard_3_method(start_x)
            picard_4_u = self.calc_picard_4_method(start_x)

        self.is_data_graph = True

    def get_graph(self):
        """
        Вычисленные значения методов
        """
        return (self.x, self.picard_1, self.picard_2, self.picard_3,
                self.picard_4, self.euler, self.runge_kutt)