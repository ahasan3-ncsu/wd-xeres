import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b, c, d, e, f):
    return a * np.exp(-b * x**c) + d * np.exp(-e * x**f)

Sr = []
with open('elec_stopping_Sr', 'r') as f:
    jar = f.readlines()
    for line in jar[9:]:
        Sr.append(float(line.split()[3]))

Xe = []
with open('elec_stopping_Xe', 'r') as f:
    jar = f.readlines()
    for line in jar[9:]:
        Xe.append(float(line.split()[3]))

# unit conversion needed
xdim = list(range(1, 10000))
xdim = [x/1000 for x in xdim]
Sr = [x/1e10 for x in Sr]
Xe = [x/1e10 for x in Xe]

def avg_contiguous(data, window_size):
    avg_data = []
    for i in range(0, len(data), window_size):
        chunk = data[i:i+window_size]
        avg = sum(chunk)/len(chunk)
        avg_data.append(avg)
    return avg_data

plt.figure(figsize=(5,4))

plt.scatter(avg_contiguous(xdim, 100), avg_contiguous(Sr, 100), s=15,
            marker='^', color=plt.cm.jet(0.8), label='Sr-94, 101.1 MeV')
p1, c1 = curve_fit(func, xdim, Sr, bounds=((0), (50)))
print('Sr: ', p1)
fit1 = [func(x, *p1) for x in xdim]
plt.plot(xdim, fit1, ls='solid',
         c=plt.cm.jet(0.7), label=r'Fit to Sr-94 $S_e$')

plt.scatter(avg_contiguous(xdim, 100), avg_contiguous(Xe, 100), s=15,
            marker='s', color=plt.cm.jet(0.2), label='Xe-140, 69.4 MeV')
p2, c2 = curve_fit(func, xdim, Xe, bounds=((0), (50)))
print('Xe: ', p2)
fit2 = [func(x, *p2) for x in xdim]
plt.plot(xdim, fit2, ls='dashed',
         c=plt.cm.jet(0.3), label=r'Fit to Xe-140 $S_e$')

plt.xlabel(r'Distance ($\mu$m)')
plt.ylabel(r'Electronic Stopping Power, $S_e$ (keV/nm)')
plt.legend()
plt.tight_layout()
plt.savefig('elec_stopping.pdf')
