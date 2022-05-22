import scipy.odr.odrpack as odr
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv
import os
import glob


def GaussH(b, t):
    return b[1] / (np.sqrt(2 * np.pi) * b[0]) * np.e ** (- ((t / (np.sqrt(2) * b[0])) ** 2))


def FuncGauss(b, t):
    return b[2] / (np.sqrt(2 * np.pi) * b[0]) * np.e ** (-2 * (((t - b[1]) / b[0]) ** 2))


def Exp(b, t):
    if b[2] == 0:
        return (b[1] / b[0]) * np.e ** (-t / b[0])
    else:
        return ((1 - b[1]) / b[0]) * np.e ** (-t / b[0])


def TauExp(b, t):
    ans = 0
    for i in range(0, len(b) - 1):
        ans += Exp([b[i], b[-1], i], t)
    return ans


def Ajustar(b, t, Gauss):
    # Define la funcion Gausseana y las exponenciales por separado para fft.
    ans = FuncGauss(Gauss, t)
    temporal = TauExp(b, t)

    # Le aplico la transformada de Fourier a las exponenciales.
    temporal = list(rfft(temporal))
    # Aplico transformada de Fourier a la Gausseana y multiplico ambas transformadas.
    ans = list(rfft(ans))
    for i in range(0, len(ans)):
        ans[i] *= temporal[i]
    # Ahora hay que transformar inversa a ans.
    ans = np.array(ans)
    ans = irfft(ans)
    ans = list(ans)
    while len(ans) < len(t):
        ans.append(0)
    b = max(ans)
    ans = np.array(ans) / b
    return ans


def FitAndGraph(x_dat, y_dat, beta):
    # Desviacion de los datos

    sigma_x = 0.008
    sigma_y = 0.02

    Aj_fin = odr.Model(GaussH)
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, Aj_fin, beta0=beta[0])

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[0] = output.beta
    # print(beta[0])

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
    name = input("introducir nombre del archivo de Ajuste: ")
    Datos_x = []
    Datos_y = []
    ReadData(Datos_x, Datos_y, name)
    Datos_x = np.array(Datos_x)
    Datos_y = np.array(Datos_y)
    print(len(Datos_x))
    resolution = 25000
    taus = [0.127, 0.247, 0.86]
    sigma = [0.032, 0.031, 0.003]
    Gauss = [0.47, 0.5, 0.59]
    errors = []
    Datos_x *= 0.001
    x = np.linspace(Datos_x[0], Datos_x[-1], 2048)
    y = Ajustar(taus, x, Gauss)
    # Esto tiene que calcular los errores a cada punto
    for i in range(0, resolution):
        temps = list(taus)
        for j in range(0, len(taus)):
            b = np.random.normal(taus[j], sigma[j])
            if 1 > b > 0:
                temps[j] = b
        Corrida = list(Ajustar(temps, x, Gauss))
        # plt.plot(x, Corrida, color="#939393")
        for j in range(0, len(x)):
            if len(errors) < j + 1:
                errors.append([])
            errors[j].append(y[j] - Corrida[j])
    sigmas = []
    pos = 0
    for i in range(0, len(y)):
        rango = list(np.linspace(min(errors[pos]), max(errors[pos]), 50))
        n, bins, patches = plt.hist(x=errors[pos], bins=rango, rwidth=0.85)
        n = list(n)
        n.append(0)
        n = np.array(n)
        if i > 55:
            gauss = [[y[pos] / 10, resolution / 50]]
        else:
            gauss = [[y[pos] / 10, 1]]
        FitAndGraph(bins, n, gauss)
        a = np.linspace(min(errors[pos]), max(errors[pos]), 2000)
        plt.plot(a, GaussH(gauss[0], a))
        if np.abs(gauss[0][0]) < y[pos]:
            sigmas.append(gauss[0][0])
        else:
            sigmas.append(0)
        pos += 1
    plt.xlabel("Delta de velocidad (mm/s)")
    plt.ylabel("Cuentas")
    plt.legend()
    plt.show()
    x = np.linspace(Datos_x[0], Datos_x[-1], 2048)
    plt.scatter(Datos_x, Datos_y, s=3, color="#236417", zorder=3, label="Medidas experimentales")
    plt.plot(x, Ajustar(taus, x, Gauss), label="Ajuste", color="#750303", zorder=2)
    sigmas = np.array(sigmas)
    plt.errorbar(x, Ajustar(taus, x, Gauss), yerr=sigmas, linestyle='None', color="#FF8585", zorder=1)
    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Cuentas (normalizado)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()