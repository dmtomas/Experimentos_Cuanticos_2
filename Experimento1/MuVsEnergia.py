import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt


def Sigmoid(t, b):
    return 1 / (1 + np.e ** ((t + b[0]) / b[1]))


def Cubic(t, b):
    return b / (t ** 3)


def linear(t, b):
    return b / t


def logaritmic(t, b):
    return b * np.log(t)


# This is the predicted function.
def Completa(b, t):
    return Cubic(t, b[0]) + linear(t, b[1]) + Sigmoid(t, [-1.1, -0.01]) * logaritmic(t, b[2])


def FitAndGraph(x_dat, y_dat, beta, errors):
    # Desviacion de los datos
    sigma_x = 0.08
    sigma_y = 0.2
    lineal = odr.Model(Completa)
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, lineal, beta0=beta)

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[0] = output.beta
    errors[0] = output.sd_beta

    return output.beta


x = [0.081, 0.276, 0.302, 0.511, 0.661, 1.173, 1.274, 1.332]
y = [0.56, 0.098, 0.077, 0.056, 0.043, 0.038, 0.038, 0.042]
error = [0.02, 0.04, 0.002, 0.001, 0.001, 0.001, 0.001, 0.003]

betas = [1, 1, 1]
errors = [0, 0, 0]
y0 = y[0]
y0_e = error[0]
x = np.array(x)
y = np.array(y)
continuo = np.linspace(x[0], x[-1], 1000)
plt.errorbar(x, y, error, x * 0.01, marker='o', linestyle='None')
plt.plot(continuo, Completa(FitAndGraph(x, y, betas, errors), continuo), label="Predicción del modelo")
plt.plot(continuo, Sigmoid(continuo, [-1.1, -0.01]) * logaritmic(continuo, betas[0][2]), "--", label="Producción de Pares")
plt.plot(continuo, linear(continuo, betas[0][1]), "--", label="Dispersión Compton")
plt.plot(continuo, Cubic(continuo, betas[0][0]), "--", label="Absorción fotoelectrica")
plt.legend()
plt.margins(x=0.01)
plt.xlabel("Energia (MeV)", fontsize=15)
plt.ylabel("Absorbencia (1/mm)", fontsize=15)
print(str(betas[0]) + " +- " + str(errors[0]))
plt.show()
