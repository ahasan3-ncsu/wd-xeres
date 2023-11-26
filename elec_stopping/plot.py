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

U = []
with open('elec_stopping_U', 'r') as f:
    jar = f.readlines()
    for line in jar[9:]:
        U.append(float(line.split()[3]))

Mo = []
with open('elec_stopping_Mo', 'r') as f:
    jar = f.readlines()
    for line in jar[9:]:
        Mo.append(float(line.split()[3]))

# unit conversion needed
xdim = list(range(1, 10000))
xdim = [x/1000 for x in xdim]
Sr = [x/1e10 for x in Sr]
Xe = [x/1e10 for x in Xe]
U = [x/1e10 for x in U]
Mo = [x/1e10 for x in Mo]

plt.scatter(xdim, Sr, s=1, marker='o', label='Sr-94, 101.1 MeV')
plt.scatter(xdim, Xe, s=1, marker='*', label='Xe-140, 69.4 MeV')
plt.scatter(xdim, U, s=1, marker='*', label='U-238, 69.4 MeV')
plt.scatter(xdim, Mo, s=1, marker='*', label='Mo-96, 69.4 MeV')

p1, c1 = curve_fit(func, xdim, Sr, bounds=((0), (50)))
print('Sr: ', p1)
fit1 = [func(x, *p1) for x in xdim]
plt.plot(xdim, fit1, c='k')

p2, c2 = curve_fit(func, xdim, Xe, bounds=((0), (50)))
print('Xe: ', p2)
fit2 = [func(x, *p2) for x in xdim]
plt.plot(xdim, fit2, c='k')

p3, c3 = curve_fit(func, xdim, U, bounds=((0), (50)))
print('U: ', p3)
fit3 = [func(x, *p3) for x in xdim]
plt.plot(xdim, fit3, c='k')

p4, c4 = curve_fit(func, xdim, Mo, bounds=((0), (50)))
print('Mo: ', p4)
fit4 = [func(x, *p4) for x in xdim]
plt.plot(xdim, fit4, c='k')

plt.xlabel(r'Distance ($\mu$m)')
plt.ylabel(r'Electronic Stopping Power, $S_e$ (keV/nm)')
plt.legend()
plt.show()
