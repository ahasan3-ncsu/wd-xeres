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

plt.figure(figsize=(5,4))

plt.scatter(xdim, Sr, s=1, marker='o', label='Sr-94, 101.1 MeV')
plt.scatter(xdim, Xe, s=1, marker='*', label='Xe-140, 69.4 MeV')

p1, c1 = curve_fit(func, xdim, Sr, bounds=((0), (50)))
print('Sr: ', p1)
fit1 = [func(x, *p1) for x in xdim]
plt.plot(xdim, fit1, c='k')

p2, c2 = curve_fit(func, xdim, Xe, bounds=((0), (50)))
print('Xe: ', p2)
fit2 = [func(x, *p2) for x in xdim]
plt.plot(xdim, fit2, c='k')

plt.xlabel(r'Distance ($\mu$m)')
plt.ylabel(r'Electronic Stopping Power, $S_e$ (keV/nm)')
plt.legend()
plt.savefig('iradina.jpg', dpi=300)
