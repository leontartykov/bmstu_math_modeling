from matplotlib import pyplot

class Graph():
    def plot_main_graphs(self, main_params):
        names = ["U", "F"]
        z = main_params[0]; y = main_params[1]
        F_derivative = main_params[2]; F_integral = main_params[3]
        z_dep = main_params[4]; up_z = main_params[5]
        
        cur_step = 0.05
        step = 0
        flag_step = 1
        print(f'len_up = {len(up_z)}, len_u = {len(y)}')
        for i in range(len(up_z)):
            #print(f'here')
            if z[i] >= step :
                print(f"up={up_z[i]}")
                flag_step = 0
                step += cur_step

        print(f'y[-1] = {y[-1]}')
        print(f'y[-2] = {y[-2]}')
        print(f'y[-3] = {y[-3]}')
        print(f'y[-4] = {y[-4]}')
        print(f'y[1] = {y[1]}')
        print(f'y[2] = {y[2]}')
        print(f'y[3] = {y[3]}')
        print(f'y[4] = {y[4]}')
        
        pyplot.subplots(1, 1,figsize=(15,9))
        pyplot.subplot(1, 2, 1)
        pyplot.plot(z, y)
        pyplot.plot(z_dep, up_z)
        pyplot.xlabel('u')
        pyplot.ylabel('u')
        pyplot.title('Зависимость u(z)')

        pyplot.subplot(1, 2, 2)
        pyplot.plot(z, F_derivative, label = 'F_derivative')
        pyplot.plot(z, F_integral, label = 'F_integral')
        pyplot.xlabel('z')
        pyplot.ylabel('F_derivative, F_integral')
        pyplot.title('Зависимости F_der(z), F_integral(z)')
        pyplot.legend()

        pyplot.show()
        

    def plot_dependence_graphs(self, dependences):
        u_k0 = dependences[0]; u_T0 = dependences[1]
        u_Tw = dependences[2]; 
        u_p = dependences[3]
        u_R = dependences[4]

        pyplot.subplots(1, 1,figsize=(15,9))
        pyplot.subplot(2, 3, 1)
        pyplot.plot(u_k0[0], u_k0[1])
        pyplot.xlabel('k0')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(k0)")        

        pyplot.subplot(2, 3, 2)
        pyplot.plot(u_T0[0], u_T0[1])
        pyplot.xlabel('T0')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(T0)")

        pyplot.subplot(2, 3, 3)
        pyplot.plot(u_Tw[0], u_Tw[1])
        pyplot.xlabel('Tw')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(Tw)")

        pyplot.subplot(2, 3, 4)
        pyplot.plot(u_p[0], u_p[1])
        pyplot.xlabel('p')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(p)")

        pyplot.subplot(2, 3, 5)
        pyplot.plot(u_R[0], u_R[1])
        pyplot.xlabel('R')
        pyplot.ylabel('u')
        pyplot.title("Зависимость u(R)")

        pyplot.show()