from point import *

class DifferEquation:
    """
    Однородные дифференциальные уравнения
    """
    def __init__(self, left_board: float, right_board: float, count_nodes: int):
        self.left_board = left_board
        self.right_board = right_board
        self.count_nodes = count_nodes
        self.step = (right_board - left_board) / count_nodes

        self.nodes_x = []; self.nodes_u = []
        
    def info(self):
        print("Текущее состояние объекта:")
        print(f"Левая граница: {self.left_board}")
        print(f"Правая граница: {self.right_board}")
        print(f"Количество узлов сетки: {self.count_nodes}")
        print(f"Шаг: {self.step}")

    def f(self, x, y):
        return x * x + y * y

    def euler_method(self):
        """
        Метод Эйлера
        """
        x = self.left_board; x_end = self.right_board
        x += self.step
        self.nodes_x.append(0); self.nodes_u.append(0)

        i = 1
        while (x <= x_end):
            self.nodes_x.append(x)
            self.nodes_u.append(self.nodes_u[i-1] + 
                                self.step * self.f(self.nodes_x[i-1], self.nodes_u[i-1]))
            x += self.step
            i += 1
        #print(f"self_nodes_x = {self.nodes_x}")
        #print(f"self_nodes_u = {self.nodes_u}")
        return

    def picard_method(self):
        """
        Метод Пикара
        """
        pass

    def runge_kutta_method(self):
        """
        Метод Рунге-Кутта
        при значении alpha = 1
        """
        self.nodes_u.clear(); self.nodes_x.clear()
        x = self.left_board; x_end = self.right_board
        x += self.step
        self.nodes_x.append(0); self.nodes_u.append(0)

        i = 1
        while x <= x_end:
            self.nodes_x.append(x)
            self.nodes_u.append(self.nodes_u[i-1] + self.step *
                                self.f(self.nodes_x[i-1] + self.step / 2, 
                                       self.nodes_u[i-1] + self.step / 2 
                                            * self.f(self.nodes_x[i-1], self.nodes_u[i-1])))
            x += self.step
            i += 1

        #print("Рунге-Кутта")
        #print(f"self_nodes_x = {self.nodes_x}")
        #print(f"self_nodes_u = {self.nodes_u}")
        return
        
        