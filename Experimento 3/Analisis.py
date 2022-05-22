import scipy.odr.odrpack as odr
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


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
    # Definir bloqueos para los valores
    if 0.1 > b[0] or b[0] > 0.5 or b[0] > b[1] or b[1] > 0.5 or 0 > b[2] or b[2] > 1:
        return np.ones(len(t)) * 50000
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


def FitAndGraph(x_dat, y_dat, beta, lineal, errors):
    # Desviacion de los datos
    sigma_x = 0.00008
    sigma_y = 0.0002
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, lineal, beta0=beta[0])

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[0] = output.beta
    errors[0] = output.sd_beta
    print(errors[0])
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
    name = input('Introducir nombre del archivo: ')
    # Co = input('Introducir nombre de la Gausseana: ')
    # error = input('Nombre del ruido de fondo')
    taus = [[0.195, 0.4, 0.9]]
    errors = [[0, 0, 0, 0, 0]]
    x = []
    y = []
    err_x = []
    err_y = []
    Ruido_x = []
    Ruido_y = []
    ReadData(x, y, name)
    # ReadData(err_x, err_y, Co)
    # ReadData(Ruido_x, Ruido_y, error)
    Gauss = [0.47, 0.5, 0.59]

    # --------------------------------Proximamente Ajustar tamb la Gausseana--------------------------------
    # for i in range(0, len(y)):
    #    y[i] -= Ruido_y[i]
    # Aj_gauss = odr.Model(FuncGauss)
    # FitAndGraph(err_x, err_y, Gauss, Aj_gauss)
    # ------------------------------------------------------------------------------------------------------
    x = np.array(x)
    x *= 0.001
    y = np.array(y)
    a = np.linspace(x[0], x[-1], 5000)
    Aj_fin = odr.Model(Ajustar, extra_args=[Gauss])
    FitAndGraph(x, y, taus, Aj_fin, errors)
    plt.scatter(x, y, label="Medidas", s=1.5, color="#236417", zorder=3)
    plt.plot(a, Ajustar(taus[0], a, Gauss), label="Ajuste", color="#FF8585", zorder=1)
    plt.xlabel("Canales")
    plt.ylabel("Cuentas")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
