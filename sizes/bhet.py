import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

R_spk = 35

def S_Xe(x):
    return 21.3 * np.exp(-0.238 * x**1.78) + 5.23 * np.exp(-4.67e-8 * x**11)

def S_Sr(x):
    return 19.7 * np.exp(-0.00273 * x**3.71) + 6.8 * np.exp(-0.424 * x**1.45)

def alpha(r):
    return 5.069 / r**2.202

def sat_Xe(x, r=20):
    return 1 - np.exp(-alpha(r) * S_Xe(x) * 0.7)

def sat_Sr(x, r=20):
    return 1 - np.exp(-alpha(r) * S_Sr(x) * 0.7)

radii = np.linspace(4, 44, 100)
bhet = []

for rb in radii:
    xe = quad(sat_Xe, 0, 8, args=(rb))[0]
    sr = quad(sat_Sr, 0, 8, args=(rb))[0]
    b = 0.225 * np.pi * (rb+R_spk)**2 * (xe+sr)/2 * 1e-20
    bhet.append(b)

plt.figure(figsize=(5,4))
plt.scatter(radii, bhet, s=1, color=plt.cm.jet(0.2))
plt.plot(radii, bhet, color=plt.cm.jet(0.8), label=r'$\xi$=0.7')

plt.xlabel(r'Bubble radius, $R_{bubble}$ ($\AA$)')
plt.ylabel(r'Re-solution rate, $b_{het}$ ($s^{-1}$)')
plt.legend()
plt.tight_layout()
plt.savefig('resRate.pdf')
#plt.show()
