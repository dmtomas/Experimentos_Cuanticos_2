import numpy as np
import matplotlib.pyplot as plt

class Detector:
  def __init__(self, eficiencia, tipo, ret):
    self.activo = False
    self.eficiencia = eficiencia
    self.tipo = tipo # Si es el start o el stop
    self.t = 0 # Tiempo propio del sistema.
    self.ret = ret


def dist(t0, delta):
  return np.random.normal(t0, delta)

def Entrelazados(ret):
  return dist(ret + 25/(3*(10**10)), 0.2)

def fondo(ret):
  r1 = 1 # cm
  r2 = 5
  theta = np.random.uniform(0.57, 0.71) 
  aten = np.e ** (-0.16 * r1/np.sin(theta))
  pasa = np.random.uniform(0, 1)
  if pasa > aten:
    t = 15/np.sin(theta)/(3*(10**10))
    return dist(t + ret, 0.2)

def Emitir(t, ret, y, total, canales, ratio_e, ratio_f, medida):
  d_start = Detector(0.9, "start", 0)
  d_stop = Detector(0.6, "stop", 0.3)
  abs = 0.8
  paso = False
  e = 0 # Tiempo restante para que salga un foton entrelazado.
  c = 0 # Tiempo restante para que salga un foton de 511.
  delta = 0 # Tiempo entre start y stop.
  for i in range(0, int(t / total * canales)):
    a = i * total / canales  # Tiempo actual
    e += total / canales
    c += total / canales
    if d_start.activo == True:
      delta += 1 / (t / total * canales)
    if  d_start.activo == False and d_stop.activo == True:
      d_stop.t += 1 / (t / total * canales)
    if d_stop.t > d_stop.ret:
      d_stop.t = 0
      d_stop.activo = False
    if delta > total:
      delta = 0
      d_start.activo = False
      d_stop.activo = False
    if e > ratio_e:
      if np.random.uniform(0, 1) > abs * d_start.eficiencia and d_start.activo == False:
        paso = True
        d_start.activo = True
      if np.random.uniform(0, 1) > abs * d_stop.eficiencia:
        d_stop.activo = True
      else:
        paso = False
      e -= ratio_e

    elif c > ratio_f:
      theta = np.random.uniform(0.57, 0.71)
      if np.random.uniform(0, 1) > np.e ** (-0.16 * 1/np.sin(theta)) * d_start.eficiencia:
        d_start.activo = True
      if np.random.uniform(0, 1) > np.e ** (-0.16 * 1/np.sin(theta)) * d_stop.eficiencia:
        d_stop.activo = True
      c -= ratio_f
    if d_start.activo == True and d_stop.activo == True:
      d_start.activo = False
      d_stop.activo = False
      tiempo = int(dist((delta + ret - d_stop.t), 0.2) / total * (canales - 1)) # A que canal pertenece el tiempo.
      d_stop.t = 0
      if tiempo < canales - 1:
        y[tiempo] += 1 
        if paso == True:
          medida[tiempo] += 1
          paso = False

ret = 15  # Retardo total del instrumento (ns).
total = 50 # Tiempo total (ns).
canales = 2048
ratio_e = 0.1  # Cada cuanto se produce un foton entrelazado.
ratio_f = 0.05 # Cada cuanto se produce un foton de 511.
x = [total / canales * x for x in range(canales)]
y = [0 for i in range(canales)]
medida = [0 for i in range(canales)]

Emitir(50, ret, y, total, canales, ratio_e, ratio_f, medida)
plt.scatter(x[550:670], y[550:670], s=1.5, label="Datos simulados")
plt.scatter(x[550:670], medida[550:670], s=1.5, label="Medidas")
plt.scatter(x[550:670], np.array(y[550:670]) - np.array(medida[550:670]), s=1.5, label="Fondo")
plt.xlabel("Tiempo (ns)")
plt.ylabel("Cuentas")
plt.legend()
plt.show()
