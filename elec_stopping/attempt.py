import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline
from scipy.integrate import quad

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

Xe = []
with open('elec_stopping_Xe', 'r') as f:
    jar = f.readlines()
    for line in jar[9:]:
        Xe.append(float(line.split()[3]))

# unit conversion needed
xdim = list(range(1, 10000))
xdim = [x*10 for x in xdim]
U  = [x/1e8 for x in U]
Mo = [x/1e8 for x in Mo]
Xe = [x/1e8 for x in Xe]

#plt.scatter(xdim, U,  s=1, marker='*', label='U-238, 69.4 MeV')
#plt.scatter(xdim, Mo, s=1, marker='*', label='Mo-96, 69.4 MeV')
#plt.scatter(xdim, Xe, s=1, marker='*', label='Xe-140, 69.4 MeV')
#plt.legend()
#plt.show()

y_U  = savgol_filter(U,  1000, 2)
y_Mo = savgol_filter(Mo, 1000, 2)
y_Xe = savgol_filter(Xe, 1000, 2)

#plt.plot(xdim, y_U,  label='U savgol_filter')
#plt.plot(xdim, y_Mo, label='Mo savgol_filter')
#plt.plot(xdim, y_Xe, label='Xe savgol_filter')
#
#plt.legend()
#plt.show()

cs_U  = CubicSpline(xdim, y_U)
cs_Mo = CubicSpline(xdim, y_Mo)
cs_Xe = CubicSpline(xdim, y_Xe)

#plt.plot(xdim, cs_U(xdim), label='U CubicSpline')
#plt.plot(xdim, cs_Mo(xdim), label='Mo CubicSpline')
#plt.plot(xdim, cs_Xe(xdim), label='Xe CubicSpline')
#
#plt.legend()
#plt.show()

xs = np.linspace(0, 1e5, num=2000)

# wacking unit conversion follows
E0_U = cs_U.integrate(0, 1e5)
E_U = [(E0_U - cs_U.integrate(0, i)) for i in xs]

E0_Mo = cs_Mo.integrate(0, 1e5)
E_Mo = [(E0_Mo - cs_Mo.integrate(0, i)) for i in xs]

E0_Xe = cs_Xe.integrate(0, 1e5)
E_Xe = [(E0_Xe - cs_Xe.integrate(0, i)) for i in xs]

plt.plot(E_U,  cs_U(xs),  label='U')
plt.plot(E_Mo, cs_Mo(xs), label='Mo')
plt.plot(E_Xe, cs_Xe(xs), label='Xe')
plt.legend()
plt.show()

Ua = []; Ub = []
for i, j in zip(E_U, cs_U(xs)):
    if i > 0 and i < 1e6:
        Ua.append(i)
        Ub.append(j)

zU = np.polyfit(Ua, Ub, 2)
print('U: ', zU)

plt.plot(E_U,  cs_U(xs),  label='U')
qU = [zU[0] * x**2 + zU[1] * x + zU[2] for x in E_U]
plt.plot(E_U, qU)
plt.show()

Moa = []; Mob = []
for i, j in zip(E_Mo, cs_Mo(xs)):
    if i > 0 and i < 1e6:
        Moa.append(i)
        Mob.append(j)

zMo = np.polyfit(Moa, Mob, 2)
print('Mo: ', zMo)

plt.plot(E_Mo,  cs_Mo(xs),  label='Mo')
qMo = [zMo[0] * x**2 + zMo[1] * x + zMo[2] for x in E_Mo]
plt.plot(E_Mo, qMo)
plt.show()

Xea = []; Xeb = []
for i, j in zip(E_Xe, cs_Xe(xs)):
    if i > 0 and i < 1e6:
        Xea.append(i)
        Xeb.append(j)

zXe = np.polyfit(Xea, Xeb, 2)
print('Xe: ', zXe)

plt.plot(E_Xe,  cs_Xe(xs),  label='Xe')
qXe = [zXe[0] * x**2 + zXe[1] * x + zXe[2] for x in E_Xe]
plt.plot(E_Xe, qXe)
plt.show()
