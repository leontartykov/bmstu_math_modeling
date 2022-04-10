from math import exp, fabs
from turtle import right

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

    def __calc_u(self, z, ksi):
        """
        Вычисление u
        """
        Up = self.__calc_Up(z)
        return ksi * Up

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
        return (self.T_w - self.T_0) * pow(z, self.p) + self.T_0

    def __calc_psi(self, last_u, last_F):
        """
        Вычисление функции пси
        """
        #print(f'last_F = {last_F}, last_u = {last_u}')
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
        z, F, u = self.__get_graph()
        return (z, F, u)

    def __find_suitable_ksi(self):
        """
        Нахождение подходящего параметра кси
        """
        left_ksi = self.LEFT_KSI
        right_ksi = self.RIGHT_KSI
        current_z = self.left_board

        suitable_ksi = self.__dichotomy_method(left_ksi, right_ksi, self.__calc_psi, current_z)

        return suitable_ksi        

    def __dichotomy_method(self, left, right, psi, current_z):
        """
        Метод половинного деления в сочетании с Рунге-Куттом IV порядка
        (нахождение подходящего кси)
        """
        middle = (left + right) / 2
        print(f'current_z = {current_z}')
        #вычисление начальных значений F, u
        last_dF = self.__calc_dF(current_z)
        last_du = self.__calc_u(current_z, middle)
        print(f'last_dF = {last_dF}, last_du = {last_du}')

        u_middle = last_du
        Up = self.__calc_Up(current_z)
        u_left = left * Up
        print(f'u_middle = {u_middle}, u_left = {u_left}')

        while fabs((left - right) / middle) > self.EPS:
            print(f'left = {left}, right = {right}, current_z = {current_z}')
            #print(f'Up = {Up}')
            #print(f'psi_left = {psi(u_left, last_F)}, psi_middle = {psi(u_middle, last_F)}')
            #print(f'psi(u_left, last_dF) * psi(u_middle, last_dF) = {psi(u_left, last_dF) * psi(u_middle, last_dF)}')
            if psi(u_left, last_dF) * psi(u_middle, last_dF) < 0:
                right = middle
            else:
                left = middle

            middle = (left + right) / 2
            current_z += self.step
            Up = self.__calc_Up(current_z)
            u_left = left * Up

            next = self.__calc_runge_cutta_iv(current_z, last_du, last_dF)
            #print(f'next = {next}')
            last_du = next[0]; last_dF = next[1]
            #print(f'last_du = {last_du}, last_dF = {last_dF}')
            u_middle = last_du
        #print('end Половинное деление')
        return middle    

    def __get_graph(self):
        """
        Получить данные для вывода графика
        """
        left_board = self.left_board
        right_board = self.right_board
        step = self.step
        z_array = []; F_array = []; u_array = []
        current_z = left_board
        
        ksi = self.__find_suitable_ksi()
        print(f'ksi = {ksi}')
        
        #добавление первых значений
        last_dF = self.__calc_dF(current_z)
        last_du = self.__calc_u(current_z, ksi)
        
        while (current_z < right_board):
            z_array.append(current_z)
            F_array.append(last_dF)
            u_array.append(last_du)
            print(f'last_dF = {last_dF}, last_du = {last_du}')

            next = self.__calc_runge_cutta_iv(current_z, last_du, last_dF)
            last_du = next[0]; last_dF = next[1]
            current_z += step

        #добавление последних значений
        z_array.append(current_z)
        F_array.append(last_dF)
        u_array.append(last_du)
        
        return z_array, F_array, u_array
