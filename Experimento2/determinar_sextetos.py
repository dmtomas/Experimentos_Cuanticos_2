import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def Lorentz(b, t):
    return 2 * (b[2] / np.pi) * (b[1] / (4 * (t - b[0]) ** 2 + b[1] ** 2))


def Sextet(fix, t, param, j):
    ans = 0
    temporal = list(param[j])  # Valor temporal para cambiarlo al momento de ajuste y despues volver
    param[j] = list(fix)
    current = param[0][0]
    for i in range(0, 6):
        if i != 0:
            if i != 3:
                current += param[1][0]
            else:
                current += param[1][1]
        if i == 0 or i == 5:
            c_height = param[2][0] * 2 * param[3][i] / param[3][0]
        elif i == 1 or i == 4:
            c_height = param[2][1] * param[3][i] / param[3][1]
        else:
            c_height = param[2][0] * param[3][i] / param[3][0]
        local = [current, param[3][i], c_height]
        ans += Lorentz(local, t)
    param[j] = list(temporal)
    return ans


def Double(fix, t, t_param, j, i):
    ans = 3807088
    for k in range(0, 2):
        if k == i:
            ans += Sextet(fix, t, t_param[k], j)
        else:
            ans += Sextet(t_param[k][j], t, t_param[k], j)
    return ans


def FitAndGraph(x_dat, y_dat, beta, j, i, function):
    # Desviacion de los datos
    sigma_x = 0.008
    sigma_y = 0.0002
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)
    myodr = odr.ODR(mydata, function, beta0=beta[i][j])

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[i][j] = list(output.beta)

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
    v0 = [[-8.12], [-8.28]]
    deltas = [[3.05, 2.31], [3.28, 2.47]]
    height = [[-31797, -35472], [-18260, -30000]]
    width = [[0.26, 0.24, 0.27, 0.27, 0.24, 0.26], [0.38, 0.24, 0.27, 0.27, 0.24, 0.38]]
    t2_param = []
    for i in range(0, len(v0)):
        t2_param.append([v0[i], deltas[i], height[i], width[i]])

    x = []
    y = []

    ReadData(x, y, name)
    x = np.array(x)
    y = np.array(y)
    x = x * 0.034 - 17.77  # Calibración del instrumento.
    plt.plot(x, y, label="Datos")
    continuo = np.linspace(x[0], x[-1], 1000)
    plt.plot(continuo, Double(t2_param[0][0], continuo, t2_param, 0, 0), label="prediccion")
    plt.legend()
    plt.show()
    for i in range(0, resolution):
        for k in range(0, len(t2_param)):
            for j in range(0, 4):
                lineal = odr.Model(Double, extra_args=[t2_param, j, k])
                FitAndGraph(x, y, t2_param, j, k, lineal)
    continuo = np.linspace(x[0], x[-1], 5000)
    plt.plot(continuo, Sextet(t2_param[0][0], continuo, t2_param[0], 0) + 3807088, linestyle='--', label="Sexteto 1")
    plt.plot(continuo, Sextet(t2_param[1][0], continuo, t2_param[1], 0) + 3807088, linestyle='--', label="Sexteto 2")
    plt.plot(continuo, Double(t2_param[0], continuo, t2_param, 0, 0), label="Suma de Sextetos", color="#870404")
    plt.scatter(x, y, label="Datos Experimentales", s=0.8, color="green")
    plt.margins(x=0)
    plt.xlabel("Velocidad (mm/s)", fontsize=15)
    plt.ylabel("Cuentas", fontsize=15)
    print(t2_param)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
