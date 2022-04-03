from math import exp

class DifferEquation:
    def __init__(self):
        self.k_0 = 8e-4
        self.m = 0.786
        self.R = 0.35
        self.T_w = 2000
        self.T_0 = 10e3
        self.p = 4
        self.c = 3e10

    def calc_T(self, z):
        return (self.T_w - self.T_0) * pow(z, self.p) + self.T_0

    def calc_k(self):
        return self.k_0 * pow(self.calc_T / 300, 2)

    def calc_u_p(self):
        T = self.calc_T()
        return 3.084e-4 / (exp(4.709e4 / T) - 1)

    def calc_u(self):
        pass

    def _calc_f(self):
        return -F * (3 * self.R * k) / c

    def calc_phi(self, z):
        u_p = self.calc_u_p()
        u = self.calc_u()
        return self.c * k * (u_p - u) - (1 / self.R) * (F / z)

    def calc_runge_cutta_iv(self, yn, zn, f, phi):
        k1 = h * self.calc_f(xn, yn, zn)
        q1 = h * self.calc_phi(xn, yn, zn)

        k2 = h * self.calc_f(xn + h / 2, yn + k1 / 2, zn + q1 / 2)
        q2 = h * self.calc_phi(xn + h / 2, yn + k1 / 2, zn + q1 / 2)

        k3 = h * self.calc_f(xn + h / 2, yn + k2 / 2, zn + q2 / 2)
        q3 = h * self.calc_phi(xn + h / 2, yn + k2 / 2, zn + q2 / 2)

        k4 = h * self.calc_f(xn + h, yn + k3, zn + q3)
        q4 = h * self.calc_f(xn + h, yn + k3, zn + q3)

        y_next = yn + (k1 + k2 + k3 + k4) / 6
        z_next = zn + (q1 + q2 + q3 + q4) / 6

        return (y_next, z_next)