import itertools
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

markers = itertools.cycle(('o','s','p','v','x','+'))
tints = itertools.cycle((0.2,0.8,0.4,0.6,0.0,1.0))
plt.figure(figsize=(5,4))

radii = np.linspace(1, 41, 25)
#radii = np.linspace(1, 101, 25)

for zeta in [0.55, 0.7, 0.85, 1]:
    bhet = []

    for rb in radii:
        xe = quad(sat_Xe, 0, 8, args=(rb, zeta))[0]
        sr = quad(sat_Sr, 0, 8, args=(rb, zeta))[0]
        b = 0.225 * np.pi * (rb+R_spk)**2 * (xe+sr)/2 * 1e-20 * 1e14
        bhet.append(b)

    plt.plot(radii, bhet, color=plt.cm.jet(next(tints)),
             marker=next(markers), ms=3, label=r'$\zeta$'+f'={zeta}')

def bdart(r):
    if r <= 50:
        G = 1
    else:
        G = 1 - ((r-0.03)/r)**3
    return 2e-18 * G * 1e14

yd = [bdart(x) for x in radii]
plt.plot(radii, yd, color=plt.cm.jet(next(tints)),
         marker=next(markers), label='DART')

plt.xlabel(r'Bubble radius, $R_{bubble}$ ($\AA$)')
plt.ylabel(r'Re-solution rate, $b_{het}$ ($s^{-1}$)')
plt.ylim([1e-4, 1e-2])
#plt.ylim([1e-7, 1e-2])
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('resRate.pdf')
