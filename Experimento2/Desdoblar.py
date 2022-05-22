import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def Polinom(b, t):
    return b[0] + b[1] * t + b[2] * t ** 2 + b[3] * t ** 3


def FitAndGraph(x_dat, y_dat, beta):
    # Desviacion de los datos
    sigma_x = 0.08
    sigma_y = 0.2
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
    beta = [[1895000, 0, 0, 0]]
    newBeta = [[1895000, 0, 0, 0]]
    centros = [502, 1547]
    name = "Data/"
    name += input("introduce name of the file: ")
    fit = int(input("introduce where the noise starts: "))
    x = []
    y = []
    Noise1_x = []
    Noise1_y = []
    Noise2_x = []
    Noise2_y = []
    ReadData(x, y, name)
    plt.scatter(x, y, s=2, color="#176600")
    plt.margins(x=0)
    plt.xlabel("Canales", fontsize=15)
    plt.ylabel("Cuentas", fontsize=15)
    plt.show()
    tope1 = 1898000
    tope2 = 1892000
    for i in range(0, len(x)):
        if x[i] > fit and y[i] > tope2:
            Noise2_x.append(x[i])
            Noise2_y.append(y[i])
        elif x[i] < fit and y[i] > tope1:
            Noise1_x.append(x[i])
            Noise1_y.append(y[i])
    Noise1_x = np.array(Noise1_x)
    Noise1_y = np.array(Noise1_y)
    continuo = np.linspace(Noise1_x[0], Noise1_x[-1], 500)
    continuo2 = np.linspace(Noise2_x[0], Noise2_x[-1], 500)
    plt.scatter(Noise1_x, Noise1_y, color="#176600", s=1.5)
    plt.scatter(Noise2_x, Noise2_y, label="Ruido de fondo de la función", color="#176600", s=1.5)
    FitAndGraph(Noise1_x, Noise1_y, beta)
    FitAndGraph(Noise2_x, Noise2_y, newBeta)
    beta[0][0] = Polinom(newBeta[0], Noise2_x[0])
    beta[0][1] = 0
    beta[0][2] = 0
    beta[0][3] = 0
    plt.plot(continuo, Polinom(beta[0], continuo), color="#FF0000")
    plt.plot(continuo2, Polinom(newBeta[0], continuo2), label="Ajuste polinomial", color="#FF0000")
    plt.margins(x=0)
    plt.xlabel("Canales", fontsize=15)
    plt.ylabel("Cuentas", fontsize=15)
    print(beta)
    plt.legend()
    plt.show()
    plt.plot(x, y)
    plt.show()
    ancho = 300
    finales_x = [i for i in range(int(centros[0] - ancho), int(centros[0] + ancho))]
    finales_y = []
    for i in range(finales_x[0], finales_x[-1] + 1):
        finales_y.append(y[i] + y[i + int(centros[1] - centros[1])])
    for i in range(0, len(finales_x)):
        finales_x[i] = finales_x[i] * 0.034 - 17.77
    plt.margins(x=0)
    plt.xlabel("Velocidad (mm/s)", fontsize=15)
    plt.ylabel("Cuentas", fontsize=15)
    plt.errorbar(finales_x, finales_y, yerr=np.sqrt(finales_y), ecolor='#FF8585', linestyle='', zorder=0)
    plt.scatter(finales_x, finales_y, s=2, color="#176600", label="Datos experimentales desdoblados", zorder=10)
    plt.legend()
    plt.show()
    save = input("Do you want to save the file? y/n: ")
    if save.lower() == "y":
        guardar = input("Ingresar el nombre: ")
        with open(guardar, 'w', encoding='UTF8', newline='\n') as f:
            for i in range(0, len(finales_x)):
                row = [finales_x[i], finales_y[i]]
                # create the csv writer
                writer = csv.writer(f)

                # write a row to the csv file
                writer.writerow(row)


if __name__ == "__main__":
    main()
