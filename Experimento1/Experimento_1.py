import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def Gaussian(t, b):
    return b[0] * np.e ** (-(t - b[1]) ** 2 / b[2])


def Exponential(t, b):
    return b[0] * np.e ** (-t * b[1])


# This is the predicted function.
def CompleteFunc(b, t, extra, j):
    ans = 0
    if j == 0:
        ans += Exponential(t, b)
    else:
        ans += Exponential(t, extra[0])
    for i in range(1, len(extra)):
        if j == i:
            ans += Gaussian(t, b)
        else:
            ans += Gaussian(t, extra[i])
    return ans


def FitAndGraph(x_dat, y_dat, beta, j, errors):
    # Desviacion de los datos
    sigma_x = 0.08
    sigma_y = 0.2
    Complete = odr.Model(CompleteFunc, extra_args=[beta, j])
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, Complete, beta0=beta[j])

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    betas[j] = output.beta
    errors[j] = output.sd_beta

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


name = "Co/"
name += input("introduce name of the file: ")
betas = [[1000, 0], [802, 676, 100], [573, 782, 70]]  # Valores iniciales (
# primero exponencial y desp las Gausseanas).
errors = []
for i in range(0, len(betas)):
    errors.append([])
x = []
y = []
Predicted = []
ReadData(x, y, name)
x = np.array(x)
y = np.array(y)
plt.xlabel("prueba", fontsize=15)
plt.ylabel("ejey", fontsize=15)

plt.plot(x, y, "r")
plt.legend()
plt.show()
real = int(input("Introduce real time of the instrument: "))
resolution = int(input("introduce the resolution of the model: "))
begin = int(input("Where should the data start? "))
final = int(input("Cual es el final? "))
for i in range(0, resolution):
    for j in range(len(betas) - 1, -1, -1):
        FitAndGraph(x[begin:final], y[begin:final], betas, j, errors)
print("Estos son los errores de los ajustes: ")
for i in range(0, len(betas)):
    print(errors[i])
print("Estos son los ajustes:")
for i in range(0, len(betas)):
    print(betas[i])
print("Las areas son:")
for i in range(1, len(betas)):
    print("El area de la Gausseana " + str(i) + " normalizada es : " + str(
        betas[i][0] * 2.506628 * (betas[i][2] ** (1 / 2)) / real) + " +- "
          + str(errors[i][0] / betas[i][0] * betas[i][0] * 2.506628 * (betas[i][2] ** (1 / 2)) / real))
plt.plot(x[:final], y[:final])
plt.plot(x[begin:final], CompleteFunc(betas, x[begin:final], betas, -1), label="Ajuste de 60Co, 0mm")
plt.margins(x=0)
plt.xlabel("Canal", fontsize=15)
plt.ylabel("Cantidad de cuentas", fontsize=15)
plt.legend()
plt.show()
