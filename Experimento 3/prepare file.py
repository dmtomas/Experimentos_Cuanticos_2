import scipy.odr.odrpack as odr
from scipy.fft import rfftfreq, rfft, irfft
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob


def ReadData(name):
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, name))
    data = ""
    with open(name, 'r') as file:
        data = file.read().replace(',', '.').replace(' ', ',')
    with open("Niquel.csv", "w") as out_file:
        out_file.write(data)


name = input("Introduce name of the file: ")
ReadData(name)
