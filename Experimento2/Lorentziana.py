import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def Polinom(b, t):
    return b[3] + b[2] * b[0] / (np.pi * ((t - b[1]) ** 2 + b[0] ** 2))


def FitAndGraph(x_dat, y_dat, beta):
    # Desviacion de los datos
    sigma_x = 0.0008
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
    beta = [[0.1, 3.12, 6634, 790]]
    intervalo = [2.46, 3.86]
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
    print(beta)
    plt.plot(x_l, y_l)
    plt.show()


if __name__ == "__main__":
    main()
