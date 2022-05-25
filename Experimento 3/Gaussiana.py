import scipy.odr.odrpack as odr
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv
import os
import glob


def GaussH(b, t):
    return b[1] / (np.sqrt(2 * np.pi) * b[0]) * np.e ** (- (((t - b[2]) / (np.sqrt(2) * b[0])) ** 2))


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
    print(beta[0])

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
    Datos_x *= 0.05
    Datos_y = Datos_y / max(Datos_y)
    gauss = [[0.2, 1, 12]]
    a = np.linspace(Datos_x[0], Datos_x[-1], 5000)
    FitAndGraph(Datos_x, Datos_y, gauss)
    plt.scatter(Datos_x, Datos_y, s=2.5, color="#236417", zorder=3, label="Datos Co")
    plt.plot(a, GaussH(gauss[0], a), color="#750303", zorder=2, label="Ajuste Gaussiano")
    plt.xlabel("tiempo (ms)")
    plt.ylabel("Cuentas normalizado")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()