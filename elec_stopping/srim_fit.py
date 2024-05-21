import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#def fn(x, c1, c2):
#    return c1 * x + c2 * x**2
def fn(x, l):
    return l * x**0.5

with open('Srim_UMoXe.es', 'r') as f:
    jar = f.readlines()
jar = jar[3:55]

x = []; U = []
Mo = []; Xe = []
for line in jar:
    tmp = line.split()
    x.append(float(tmp[0]))
    U.append(float(tmp[1]))
    Mo.append(float(tmp[2]))
    Xe.append(float(tmp[3]))

p1, c1 = curve_fit(fn, x, U)
print(p1)
p2, c2 = curve_fit(fn, x, Mo)
print(p2)
p3, c3 = curve_fit(fn, x, Xe)
print(p3)

plt.scatter(x, U , s=1)
plt.scatter(x, Mo, s=1)
plt.scatter(x, Xe, s=1)

plt.plot(x, [fn(i, *p1) for i in x])
plt.plot(x, [fn(i, *p2) for i in x])
plt.plot(x, [fn(i, *p3) for i in x])

plt.show()
