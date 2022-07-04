from math import exp

class DifferEquation():
    def __init__(self, left_board, right_board, step):
        self.__k_0 = 8e-4
        self.__R = 0.35
        self.__T_w = 2e3
        self.__T_0 = 1e4
        self.__p = 4
        self.__c = 3e10
        self.__left_board = left_board
        self.__right_board = right_board
        self.__step = step

    def __find_Up(self, z):
        """
        Вычисление Up
        """
        T = self.__find_T(z)
        return 3.084 * 1e-4 / (exp(47990 / T) - 1)

    def __find_T(self, z):
        """
        Вычисление T
        """
        return (self.__T_w - self.__T_0) * (z ** self.__p) + self.__T_0

    def __find_k(self, z):
        """
        Вычисление параметра k
        """
        T = self.__find_T(z)
        return self.__k_0 * pow(T / 300, 2)

    def finite_difference_method(self):
        """
        Точка входа поиска решения
        """
        ksi, eta = self.__find_runthrough_coeffs()
        #print(f'ksi = {ksi}\neta={eta}')
        z, y = self.__find_approx_func(ksi, eta)
        F_derivative = self.__find_F_derivative(z, y)
        F_integral = self.__find_F_integral(z, y)
        z_dep, up_z = self.__find_up_dependence()
        #print(f'F_integral = {F_integral}')
        
        return (z, y, F_derivative, F_integral, z_dep, up_z)

    def __find_runthrough_coeffs(self): 
        """
        Нахождение прогоночных коэффициентов по выведенным формулам
        (прямой ход)
        """
        h = self.__step
        half_h = h / 2  
        current_z = half_h
        max_z = self.__right_board
        ksi = []; eta = []

        M0 = self.__find_M0(current_z, h)
        K0 = self.__find_K0(current_z, h)
        P0 = self.__find_P0(current_z, h)
        print(f'M0 = {M0}, K0 = {K0}, P0 = {P0}')
        ksi.append(-K0/M0)
        eta.append(P0/K0)
        
        print(f'1 / h = {1 / h}')
        while (current_z <= max_z):
            #print(f'current_z = {current_z}')
            #print(f"i = {i}")
            a_n = self.__find_kappa(current_z) * current_z
            current_z += half_h
            b_n = a_n + self.__c * self.__find_k(current_z) * current_z * h * h * self.__R
            f_n = h * h * self.__R * self.__c * current_z * self.__find_k(current_z) * self.__find_Up(current_z)
            current_z += half_h
            c_n = self.__find_kappa(current_z) * current_z
            b_n += c_n

            next_ksi = c_n / (b_n - a_n * ksi[-1])
            next_eta = (f_n + a_n * eta[-1]) / (b_n - a_n * ksi[-1])
            ksi.append(next_ksi)
            eta.append(next_eta)
            #print(f'current_z = {current_z}')
        print(f'current_z = {current_z}')
        print(f'len_ksi = {len(ksi)}')

        return ksi, eta

    def __find_approx_func(self, ksi: list, eta: list):
        """
        Нахождение всех yn (обратный ход)
        """
        y = [0] * len(ksi); z = []
        h = self.__step
        half_h = h / 2  
        current_z = self.__right_board - half_h

        Mn = self.__find_Mn(current_z, h)
        Kn = self.__find_Kn(current_z, h)
        Pn = self.__find_Pn(current_z, h)
        print(f'Mn = {Mn}, Kn = {Kn}, Pn = {Pn}')
        
        y[-1] = (Pn - Mn * eta[-1]) / (Mn * ksi[-1] + Kn)

        for i in range(len(y) - 2, -1, -1):
            y[i] = y[i+1] * ksi[i+1] + eta[i+1]

        print(f'len_y = {len(y)}')
        z = [(0 + i * h) for i in range(len(y))]
        print(f'len_z = {len(z)}')
        return z, y

    def __find_F_derivative(self, z, u):
        """
        Нахождение потока путем дифференцирования
        """
        h = self.__step
        dy = []
        
        dy.append((-3 * u[0] + 4 * u[1] - u[2]) / (2 * h))
        for i in range(1, len(u) - 1):
            dy.append((u[i+1] - u[i-1]) / (2 * h))
        dy.append((3 * u[-1] - 4 * u[-2] + u[-3]) / (2 * h))

        #F = [0]
        #for i in range(1, len(z)):
        #    F.append(-self.__c * dy[i] / (3 * self.__R * self.__find_k(z[i])))

        F = [-self.__c / 3 / self.__R / self.__find_k(z[i]) * dy[i] for i in range(len(z))]
        F[0] = 0

        return F

    def __find_F_integral(self, z, u):
        """
        Нахождение потока путем интегрирования
        """
        F = [0] * len(z)
        h = self.__step; integral_value = 0
        current_z = 0; next_z = h    
        for i in range(1, len(u)):
            integral_value += h / 2 * (self.__find_k(current_z) * (self.__find_Up(current_z) - u[i-1]) * current_z +  \
                              self.__find_k(next_z) * (self.__find_Up(next_z) - u[i]) * next_z)
            F[i] = self.__c * self.__R / next_z * integral_value
            current_z = next_z
            next_z += h

        return F

    def __find_up_dependence(self):
        """
        Нахождение зависимости up(z)
        """
        z_dep = []; up_z = []
        z = 0; h = self.__step

        up = self.__find_Up(z)   
        up_z.append(up)
        z_dep.append(z)    

        while z < self.__right_board:
            z += h
            z_dep.append(z)
            up = self.__find_Up(z)
            up_z.append(up)
        print(f'len_z = {len(z_dep)}; len_up = {len(up_z)}')
        return z_dep, up_z
    
    def __find_kappa(self, z):
        half_step = self.__step
        return self.__c * (self.__find_k(z + half_step) + self.__find_k(z - half_step)) / \
                          (6 * self.__R * self.__find_k(z + half_step) * self.__find_k(z - half_step))
    
    def __find_M0(self, z, h):
        return self.__find_kappa(z) * z + self.__c * self.__R * h * h / 8 * z * self.__find_k(z)

    def __find_K0(self, z, h):
        return -self.__find_kappa(z) * z + h * h / 8 * self.__c * self.__R * self.__find_k(z) * z

    def __find_P0(self, z, h):
        return self.__c * self.__R * h * h / 4 * self.__find_k(z) * self.__find_Up(z) * z    

    def __find_Mn(self, z, h):
        print(f'z = {z}, h = {h}')
        return -self.__find_kappa(z) * z + \
             self.__R * self.__c * h * h / 8 * z * self.__find_k(z)

    def __find_Kn(self, z, h):
        print(f'z = {z}, h = {h}')
        return self.__find_kappa(z) * z + 0.393 * self.__c * h + \
             self.__R * self.__c * h * h / 8 * z * self.__find_k(z) + \
             self.__R * self.__c * h * h / 4 * self.__find_k(1)

    def __find_Pn(self, z, h):
        print(f'z = {z}, h = {h}')
        return self.__c * self.__R * h * h / 4 * (self.__find_k(z) * self.__find_Up(z) * z + \
                                                self.__find_k(1) * self.__find_Up(1))
         

