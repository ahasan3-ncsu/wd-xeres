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

def sat_Xe(x, r=20, zeta=0.7):
    return 1 - np.exp(-alpha(r) * S_Xe(x) * zeta)

def sat_Sr(x, r=20, zeta=0.7):
    return 1 - np.exp(-alpha(r) * S_Sr(x) * zeta)

radii = np.linspace(1, 21, 100)
pres = np.linspace(0.1, 0.5, 20)

bhet = []
for rb in radii:
    xe = quad(sat_Xe, 0, 8, args=(rb, 0.01))[0]
    sr = quad(sat_Sr, 0, 8, args=(rb, 0.01))[0]
    b = 0.225 * np.pi * (rb+R_spk)**2 * (xe + sr) * 1e-20 * 1e14
    bhet.append(b)

def pared(r, p):
    delta = (21 - 1) / (100 - 1)
    ind = round((r - 1) / delta)
    return bhet[ind] * 0.2 / p

vpared = np.vectorize(pared)

X, Y = np.meshgrid(radii, pres)
Z = vpared(X, Y)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(projection='3d')

ax.plot_surface(X, Y, Z, cmap=plt.cm.turbo, alpha=1.0,
                linewidth=0, antialiased=False)

ax.view_init(elev=10, azim=-30)
ax.set_xlabel(r'Bubble radius, $R_{bubble}$ ($\AA$)')
ax.set_ylabel(r'Xe/vacancy ratio, $\phi$')
ax.set_zlabel(r'Re-solution rate, $b_{het}$ ($s^{-1}$)')
plt.tight_layout()
plt.savefig('3d.pdf')
