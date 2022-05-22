import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def Polinom(b, t):
    return 2 * (b[2] / np.pi) * (0.28 / ((t - b[0]) ** 2 + 0.28 ** 2)) \
           + 2 * (b[2] / (np.pi * 1.71)) * (0.25 / ((t - b[1]) ** 2 + 0.25 ** 2))


def Lorents(b, t):
    return 2 * (b[2] / np.pi) * (b[1] / ((t - b[0]) ** 2 + b[1] ** 2))


def FitAndGraph(x_dat, y_dat, beta):
    # Desviacion de los datos
    sigma_x = 0.008
    sigma_y = 0.0002
    lineal = odr.Model(Polinom)
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, lineal, beta0=beta[0])

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[0] = output.beta

    return output.beta


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
    beta = [[-5, -4.9, 62916]]
    intervalo = [-6, -4]
    name = input("introduce name of the file: ")
    x = []
    y = []
    x_l = []
    y_l = []
    ReadData(x, y, name)
    for i in range(0, len(y)):
        x[i] -= 516
        x[i] /= 29
    i = 0
    plt.plot(x, y)
    plt.show()
    while intervalo[1] > x[i]:
        i += 1
        if x[i] > intervalo[0]:
            y_l.append(y[i])
            x_l.append(x[i])
    x_l = np.array(x_l)
    y_l = np.array(y_l)
    continuo = np.linspace(x_l[0], x_l[-1], 500)
    FitAndGraph(x_l, y_l, beta)
    plt.plot(continuo, Polinom(beta[0], continuo))
    l1 = [beta[0][0], 0.28, beta[0][2]]
    l2 = [beta[0][1], 0.25, beta[0][2] / 1.7]
    plt.plot(continuo, Lorents(l1, continuo))
    plt.plot(continuo, Lorents(l2, continuo))
    print(beta)
    plt.errorbar(x_l, y_l, np.sqrt(y_l), marker='o', linestyle='None', fmt='none')
    plt.scatter(x_l, y_l, s=10)
    plt.show()


if __name__ == "__main__":
    main()
