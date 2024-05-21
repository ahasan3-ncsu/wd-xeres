#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def fun(xevac):
    T = 400
    v = 11.86 / xevac # dependent on T

    A = 1
    B = 14.625 + 54597.728 / T - 386.344 / T**2
    C = 2968.616 + 2938.01 / T - 84.545 / T**2
    D = 705527.001 + 53.609 / T + 421.138 / T**2
    p = 8.3145 * T / v * (A + B/v + C/v**2 + D/v**3)

    return p

x = np.arange(0.05, 1, 0.05)
y = [fun(i) for i in x]

z = np.polyfit(x, y, 4)
pp = np.poly1d(z)
fit = [pp(i) for i in x]

def ill(x, a, b):
    return a * x**2 + b * x**4

p, c = curve_fit(ill, x, y)
print(p)
fit2 = [ill(i, *p) for i in x]

plt.scatter(x, y)
plt.plot(x, fit, 'k')
plt.plot(x, fit2, 'r')
plt.show()
