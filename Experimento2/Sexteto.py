import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def Lorentz(b, t):
    return 2 * (b[2] / np.pi) * (b[1] / (4 * (t - b[0]) ** 2 + b[1] ** 2))


def Sextet(fix, t, t_param, j):
    ans = 96630
    temporal = list(t_param[j])  # Valor temporal para cambiarlo al momento de ajuste y despues volver
    t_param[j] = list(fix)
    current = t_param[0][0]
    for i in range(0, 6):
        if i != 0:
            current += t_param[1][(i - 1) % 3]
        if i == 0 or i == 5:
            c_height = t_param[2][0] * 2 * t_param[3][i] / t_param[3][0]
        elif i == 1 or i == 4:
            c_height = t_param[2][1] * t_param[3][i] / t_param[3][1]
        else:
            c_height = t_param[2][0] * t_param[3][i] / t_param[3][0]
        local = [current, t_param[3][i], c_height]
        ans += Lorentz(local, t)
    t_param[j] = list(temporal)
    return ans


def FitAndGraph(x_dat, y_dat, beta, j):
    # Desviacion de los datos
    sigma_x = 0.008
    sigma_y = 0.0002
    lineal = odr.Model(Sextet, extra_args=[beta, j])
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, lineal, beta0=beta[j])

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[j] = output.beta

    return beta


def ReadData(x, y, name):
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, name))
    i = -1
    for f in csv_files:
        i += 1
        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                x.append(float(row[0]))
                y.append(float(row[1]))


def main():
    name = input("Introduce name of the file: ")
    resolution = int(input("introduce resolution: "))
    v0 = [362]
    deltas = [65, 65, 48]
    height = [-142280, -215000]
    width = [8.49, 7.48, 7.11, 7.11, 7.56, 8.38]
    t_param = [v0, deltas, height, width]

    x = []
    y = []
    ReadData(x, y, name)
    x = np.array(x)
    y = np.array(y)
    plt.plot(x, y)
    continuo = np.linspace(x[0], x[-1], 1000)
    plt.plot(continuo, Sextet(t_param[0], continuo, t_param, 0))

    plt.show()
    for i in range(0, resolution):
        for j in range(0, 4):
            FitAndGraph(x, y, t_param, j)
    continuo = np.linspace(x[0], x[-1], 5000)

    plt.plot((continuo - 516) / 29, Sextet(t_param[0], continuo, t_param, 0), label="Ajuste sexteto")
    x = (x - 516) / 29
    plt.plot(x, y, label="Datos experimentales")
    plt.margins(x=0)
    plt.xlabel("Velocidad (mm/s)", fontsize=15)
    plt.ylabel("Cuentas", fontsize=15)
    print(t_param)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
