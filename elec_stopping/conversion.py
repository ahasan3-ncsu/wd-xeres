import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

def integrand_U(x):
    return 10.3 * np.exp(-2.36e-7 * x**10.7) + 14.6 * np.exp(-0.629 * x**1.27)

def integrand_Mo(x):
    return 6.21 * np.exp(-0.663 * x**1.29) + 18.3 * np.exp(-0.0219 * x**2.97)

def integrand_Xe(x):
    return 21.3 * np.exp(-0.239 * x**1.78) + 5.23 * np.exp(-4.67e-8 * x**11)

# Watch out for multiplication by 100 and 1e6
# They are for converting keV/nm to eV/Ang and MeV to eV

x = [i for i in np.linspace(0, 10, num=250)] # in microns
y_U = [100*integrand_U(i) for i in np.linspace(0, 10, num=250)]
y_Mo = [100*integrand_Mo(i) for i in np.linspace(0, 10, num=250)]
y_Xe = [100*integrand_Xe(i) for i in np.linspace(0, 10, num=250)]
#plt.plot(x, y_U)
#plt.plot(x, y_Mo)
#plt.plot(x, y_Xe)
#plt.show()

E0_U = quad(integrand_U, 0, 10)
E_U = [1e6*(E0_U[0] - quad(integrand_U, 0, i)[0])
    for i in np.linspace(0, 10, num=250)]

E0_Mo = quad(integrand_Mo, 0, 10)
E_Mo = [1e6*(E0_Mo[0] - quad(integrand_Mo, 0, i)[0])
    for i in np.linspace(0, 10, num=250)]

E0_Xe = quad(integrand_Xe, 0, 10)
E_Xe = [1e6*(E0_Xe[0] - quad(integrand_Xe, 0, i)[0])
    for i in np.linspace(0, 10, num=250)]

#plt.plot(E_U, y_U, label='U')
#plt.plot(E_Mo, y_Mo, label='Mo')
#plt.plot(E_Xe, y_Xe, label='Xe')
#plt.legend()
#plt.show()

base_E = np.linspace(0, 50e6, num=250)
U_interp = np.interp(base_E, E_U[::-1], y_U[::-1])
Mo_interp = np.interp(base_E, E_Mo[::-1], y_Mo[::-1])
Xe_interp = np.interp(base_E, E_Xe[::-1], y_Xe[::-1])

#plt.plot(base_E, U_interp, label='U')
#plt.plot(base_E, Mo_interp, label='Mo')
#plt.plot(base_E, Xe_interp, label='Xe')
#plt.legend()
#plt.show()

with open('Iradina_UMoXe.es', 'w') as f:
    for i, j, k, l in zip(base_E, U_interp, Mo_interp, Xe_interp):
        f.write(f'{round(i)}\t{round(j)}\t{round(k)}\t{round(l)}\n')
