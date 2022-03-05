from point import *

class DifferEquation:
    """
    Однородные дифференциальные уравнения
    """
    def __init__(self, left_board: float, right_board: float, step:float):
        self.left_board = left_board
        self.right_board = right_board
        self.step = step
        
    def info(self):
        print("Текущее состояние объекта:")
        print(f"Левая граница: {self.left_board}")
        print(f"Правая граница: {self.right_board}")
        print(f"Шаг: {self.step}")

    def f(self, x, y):
        return x * x + y * y

    def euler_method(self, last_x, last_u) -> None:
        """
        Метод Эйлера
        """
        return last_u + self.step * self.f(last_x, last_u)

    def picard_1(self, x):
        """
        Метод Пикара I порядка точности
        """
        return pow(x, 3) / 3

    def picard_2(self, x):
        """
        Метод Пикара II порядка точности
        """
        return self.picard_1(x) + pow(x, 7) / 63

    def picard_3(self, x):
        """
        Метод Пикара III порядка точности
        """
        return self.picard_2(x) + 2 * pow(x, 11) / 2079 + \
               pow(x, 15) / 59535

    def picard_4(self, x):
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
               self.picard_2(x)

    def runge_kutta_method(self, last_x, last_u):
        """
        Метод Рунге-Кутта
        при значении alpha = 1
        """ 
        return last_u + self.step * self.f(last_x + self.step / 2, 
                                           last_u + self.step / 2 * self.f(last_x, last_u))
        
    def get_table(self):
        print("x     |Пикар I порядка │ Пикар II порядка │ Пикар III порядка │ Пикар IV порядка │ ЭЙлер │ Ругге-Кутт\n" + \
              "─────────────────────────────────────────────────────────────────────────────────────────────────────")
        start = self.left_board; end = self.right_board
        last_x_runge_kutta = 0; current_x_runge_kutta = 0
        last_u_runge_kutta = 0; current_u_runge_kutta = 0
        last_x_euler = 0; current_x_euler = 0
        last_u_euler = 0; current_u_euler = 0

        while start <= end:
            last_x_euler = current_x_euler; 
            current_x_euler = start
            last_u_euler = current_u_euler
            current_u_euler = self.euler_method(last_x_euler, last_u_euler)

            last_x_runge_kutta = current_x_runge_kutta
            current_x_runge_kutta = start
            last_u_runge_kutta = current_u_runge_kutta
            current_u_runge_kutta = self.runge_kutta_method(last_x_runge_kutta, last_u_runge_kutta)

            print(f"{start:4.3f} |{self.picard_1(start):15.6f} | {self.picard_2(start):16.6f}" + 
                  f"| {self.picard_3(start):17.6f} | {self.picard_4(start):16.6f}" +
                  f"| {current_u_euler:16.6f} | {current_u_runge_kutta:16.6f}")
            start += self.step 

        