from math import exp, fabs

class DifferEquation:
    EPS = 1e-4
    LEFT_KSI = 1e-2
    RIGHT_KSI = 1
    def __init__(self, left_board, right_board, step):
        self.k_0 = 8e-4
        self.R = 0.35
        self.T_w = 2e3
        self.T_0 = 1e4
        self.p = 4
        self.c = 3e10
        self.left_board = left_board
        self.right_board = right_board
        self.step = step

    def __calc_du(self, z, u, last_F):
        """
        Вычисление du/dz
        """
        k = self.__calc_k(z)

        du = -last_F * 3 * self.R * k / self.c
        return du

    def __calc_Up(self, z):
        """
        Вычисление Up
        """
        T = self.__calc_T(z)
        return 3.084e-4 / (exp(4.799e4 / T) - 1)

    def __calc_T(self, z):
        """
        Вычисление T
        """
        return (self.T_w - self.T_0) * (z ** self.p) + self.T_0

    def __calc_psi(self, last_u, last_F):
        """
        Вычисление функции пси
        """
        return last_F - 0.393 * self.c * last_u

    def __calc_dF(self, z, u=None, last_F=None):
        """
        Вычисление dF/dz
        """
        # левая граница равна нулю => F = 0
        if z == 0:
            return 0
        
        k = self.__calc_k(z)
        Up = self.__calc_Up(z)
        return self.c * self.R * k * (Up - u) - last_F / z

    def __calc_k(self, z):
        """
        Вычисление параметра k
        """
        T = self.__calc_T(z)
        return self.k_0 * pow(T / 300, 2)

    def __calc_runge_cutta_iv(self, last_z, last_u, last_F):
        """
        Метод Рунге-Кутта IV порядка
        """
        half_step = self.step / 2

        k1 = self.step * self.__calc_du(last_z, None, last_F)
        q1 = self.step * self.__calc_dF(last_z, last_u, last_F)

        k2 = self.step * self.__calc_du(last_z + half_step, None, last_F + q1 / 2)
        q2 = self.step * self.__calc_dF(last_z + half_step, last_u + k1 / 2, last_F + q1 / 2)

        k3 = self.step * self.__calc_du(last_z + half_step, None, last_F + q2 / 2)
        q3 = self.step * self.__calc_dF(last_z + half_step, last_u + k2 / 2, last_F + q2 / 2)

        k4 = self.step * self.__calc_du(last_z + self.step, None, last_F + q3)
        q4 = self.step * self.__calc_dF(last_z + self.step, last_u + k3, last_F + q3)

        u_next = last_u + (k1 + 2*k2 + 2*k3 + k4) / 6
        F_next = last_F + (q1 + 2*q2 + 2*q3 + q4) / 6

        return (u_next, F_next)

    def get_solution(self):
        """
        Получить решение
        """
        z, F, u, Up = self.__get_graph()
        return (z, F, u, Up)  

    def __find_suitable_ksi(self, psi):
        """
        Метод половинного деления в сочетании с Рунге-Куттом IV порядка
        (нахождение подходящего кси)
        """
        left = self.LEFT_KSI; right = self.RIGHT_KSI
        middle = (left + right) / 2
        #вычисление начальных значений F, u
        last_du, last_dF = self.__shooting_method(self.left_board, self.right_board, middle)
        u_middle = last_du

        while fabs(psi(u_middle, last_dF)) > self.EPS:
            if psi(u_middle, last_dF) < 0:
                right = middle
            else:
                left = middle
            middle = (left + right) / 2

            last_du, last_dF = self.__shooting_method(self.left_board, self.right_board, middle)
            u_middle = last_du

        return middle

    def __shooting_method(self, min_z, max_z, ksi):
        last_dF = 0
        current_z = min_z
        Up = self.__calc_Up(current_z)
        last_du = ksi * Up

        current_z += self.step
        
        while current_z < max_z:
            next = self.__calc_runge_cutta_iv(current_z, last_du, last_dF)
            last_du = next[0]; last_dF = next[1]
            current_z += self.step
            
        return last_du, last_dF        

    def __get_graph(self):
        """
        Получить данные для вывода графика
        """
        print(f'Программа выполняется. Ожидайте.')
        left_board = self.left_board
        right_board = self.right_board
        z_array = []; F_array = []; u_array = []; Up_array = []
        current_z = left_board
        
        ksi = self.__find_suitable_ksi(self.__calc_psi)
        print(f'Найденный параметр ksi = {ksi}. Выполняются вычисления. Ожидайте.')
        
        #вычисление начальных условий
        last_dF = 0
        max_dF = last_dF
        Up = self.__calc_Up(current_z)
        last_du = ksi * Up

        z_array.append(current_z)
        F_array.append(last_dF)
        u_array.append(last_du)
        Up_array.append(Up)
        current_z += self.step

        while current_z < right_board:
            next = self.__calc_runge_cutta_iv(current_z, last_du, last_dF)
            last_du = next[0]; last_dF = next[1]
            if last_dF > max_dF:
                max_dF = last_dF
            Up = self.__calc_Up(current_z)
            current_z += self.step

            z_array.append(current_z)
            F_array.append(last_dF)
            u_array.append(last_du)
            Up_array.append(Up)

        return z_array, F_array, u_array, Up_array

    def define_dependence_u_k0(self):
        """
        Зависимость u(0) от k0
        """
        print(f'Выполняются вычисления зависимости u(0) от k0. Ожидайте.')
        u_k0_array = []
        k0_array = []
        Up = self.__calc_Up(0)
        for k0 in range(1, 30, 1):
            self.k_0 = k0 / 10000
            k0_array.append(k0)
            ksi = self.__find_suitable_ksi(self.__calc_psi)
            u_k0 = ksi * Up
            u_k0_array.append(u_k0)

        print(f'Вычисления зависимости u(0) от k0 завершены.')
        return (k0_array, u_k0_array)

    def define_dependence_u_Tw(self):
        """
        Зависимость u(0) от Tw
        """
        print(f'Выполняются вычисления зависимости u(0) от Tw. Ожидайте.')
        u_Tw_array = []
        T_w_array = []
        Up = self.__calc_Up(0)
        self.k_0 = 8e-4
        self.R = 0.35
        self.T_w = 2e3
        self.T_0 = 1e4
        self.p = 4
        for T_w in range(1000, 3000, 100):
            self.T_w = T_w
            T_w_array.append(T_w)
            ksi = self.__find_suitable_ksi(self.__calc_psi)
            u_Tw = ksi * Up
            u_Tw_array.append(u_Tw)

        print(f'Вычисления зависимости u(0) от Tw завершены.')
        return (T_w_array, u_Tw_array)

    def define_dependence_u_T0(self):
        """
        Зависимость u(0) от T0
        """
        print(f'Выполняются вычисления зависимости u(0) от T0. Ожидайте.')
        u_T0_array = []
        T_0_array = []
        Up = self.__calc_Up(0)
        self.k_0 = 8e-4
        self.R = 0.35
        self.T_w = 2e3
        self.T_0 = 1e4
        self.p = 4
        for T_0 in range(4000, 16000, 300):
            self.T_0 = T_0
            T_0_array.append(T_0)
            ksi = self.__find_suitable_ksi(self.__calc_psi)
            u_T0 = ksi * Up
            u_T0_array.append(u_T0)

        print(f'Вычисления зависимости u(0) от T0 завершены.')
        return (T_0_array, u_T0_array)

    def define_dependence_u_p(self):
        """
        Зависимость u от p
        """
        print(f'Выполняются вычисления зависимости u(0) от p. Ожидайте.')
        u_p_array = []
        p_array = []
        Up = self.__calc_Up(0)
        self.k_0 = 8e-4
        self.R = 0.35
        self.T_w = 2e3
        self.T_0 = 1e4
        self.p = 4
        for p in range(1, 16, 1):
            self.p = p
            p_array.append(p)
            ksi = self.__find_suitable_ksi(self.__calc_psi)
            u_p = ksi * Up
            u_p_array.append(u_p)

        print(f'Вычисления зависимости u(0) от p завершены.')
        return (p_array, u_p_array)

    def define_dependence_u_R(self):
        """
        Зависимость u от R
        """
        print(f'Выполняются вычисления зависимости u(0) от R. Ожидайте.')
        u_R_array = []
        R_array = []
        Up = self.__calc_Up(0)
        self.k_0 = 8e-4
        self.R = 0.35
        self.T_w = 2e3
        self.T_0 = 1e4
        self.p = 4
        for R in range(5, 70, 2):
            self.R = R / 100
            R_array.append(R)
            ksi = self.__find_suitable_ksi(self.__calc_psi)
            u_R = ksi * Up
            u_R_array.append(u_R)
        print(f'Вычисления зависимости u(0) от R завершены.')

        return (R_array, u_R_array)
