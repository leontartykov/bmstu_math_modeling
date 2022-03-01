class DifferEquation:
    """
    Однородные дифференциальные уравнения
    """
    def __init__(self, left_board: float, right_board: float, count_nodes: int):
        self.left_board = left_board
        self.right_board = right_board
        self.count_nodes = count_nodes
        self.step = (right_board - left_board) / count_nodes

    def output_data(self):
        print("Текущее состояние объекта:")
        print(f"Левая граница: {self.left_board}")
        print(f"Правая граница: {self.right_board}")
        print(f"Количество узлов сетки: {self.count_nodes}")
        print(f"Шаг: {self.step}")

    def euler_method(self):
        """
        Метод Эйлера
        """
        pass

    def picard_method(self):
        """
        Метод Пикара
        """
        pass

    def runge_kutta_method(self):
        """
        Метод Рунге-Кутта
        """
        pass
        