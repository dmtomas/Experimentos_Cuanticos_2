import scipy.odr.odrpack as odr
import numpy as np
import matplotlib.pyplot as plt


# This is the predicted function.
def Recta(b, t):
    return b[0] * t + b[1]


def FitAndGraph(x_dat, y_dat, beta, errors):
    # Desviacion de los datos
    sigma_x = 0.00008
    sigma_y = 0.002
    lineal = odr.Model(Recta)
    mydata = odr.RealData(x_dat, y_dat, sx=sigma_x, sy=sigma_y)

    myodr = odr.ODR(mydata, lineal, beta0=beta)

    # Corremos el ajuste y guardamos los resultados en la variable output
    output = myodr.run()
    beta[0] = output.beta
    errors[0] = output.sd_beta

    return output.beta


# -------------------Ba_0----------------------------
# x = [0, 0.38, 2.89, 3.85, 4.485]
# y = [1136, 861, 206, 118, 108]
# error = [1, 2, 1, 1, 1]
# ---------------------------------------------------

# -------------------Ba_1----------------------------
# x = [0, 0.38, 2.89, 3.85, 4.485]
# y = [559, 534, 398, 392, 382]
# error = [10, 10, 7.6, 7, 7]
# ---------------------------------------------------

# -------------------Ba_2----------------------------
# x = [0, 0.38, 2.89, 3.85, 4.485]
# y = [1230, 1166, 967, 913, 877]
# error = [17, 16, 14, 12, 11]
# ---------------------------------------------------

# ----------------- Na------------------------------
# x = [0, 0.44, 0.88, 3.3, 4.44]
# y = [306, 306, 296, 271, 256.4]
# error = [3.08, 3.3, 2.38, 2, 2.3]
# --------------------------------------------------

# ----------------- Na_2------------------------------
# x = [0, 0.88, 4.44]
# y = [1525, 1460, 1188]
# error = [3, 3.5, 2]
# --------------------------------------------------

# ----------------- Co_1----------------------------
# x = [0, 0.39, 1.115, 2.4, 5]
# y = [193, 191.17, 183.24, 177.8, 158.72]
# error = [2.43, 2.2, 2.23, 1.95, 1.9]
# --------------------------------------------------

# ----------------- Co_2----------------------------
# x = [0, 0.39, 1.115, 2.4, 5]
# y = [151.68, 154, 142, 134.4, 124.1]
# error = [2.36, 1.95, 2.1, 1.97, 1.8]
# --------------------------------------------------

# ----------------- Cs ----------------------------
# x = [0, 0.38, 2.35, 3.195, 4.465]
# y = [2161, 2134, 1962, 1903, 1764]
# error = [7, 3, 2, 4.5, 4]
# --------------------------------------------------

# -------------------Calibración------------------
x = [-5.31, -3.08, -0.82, 0.82, 3.08, 5.31]
y = [362.46, 425.27, 492.08, 540.88, 605.69, 670.5]
error = [0.293, 0.214, 0.076, 0.076, 0.21, 0.29]
# ------------------------------------------------

betas = [0, 0]
errors = [0, 0]
x = np.array(x)
y = np.array(y)
# y = np.log(y / y0)
# for i in range(0, len(error)):
#    error[i] = ((y0_e / y0) ** 2 + (y[i] / error[i]) ** 2) ** (1 / 2)
continuo = np.linspace(x[0], x[-1], 200)
plt.margins(x=0.01)
plt.errorbar(x, y, error, x * 0.01, marker='o', linestyle='None')
plt.plot(continuo, Recta(FitAndGraph(x, y, betas, errors), continuo), label="Ajuste Lineal")
plt.xlabel("Velocidad (mm)", fontsize=15)
plt.ylabel("Canales", fontsize=15)
print(str(betas[0]) + " +- " + str(errors[0]))
plt.legend()
plt.show()
