import matplotlib.pyplot as plt

def bei(x):
    return 2e-18 * x

def jahid(x):
    return 8e-19 * x

fr = list(range(int(2e14), int(9e14), int(1e14)))
pred1 = [bei(x) * 1e4 for x in fr]
pred2 = [jahid(x) * 1e4 for x in fr]

plt.plot(fr, pred1, 'co-', label='DART model')
plt.plot(fr, pred2, 'k^--', label='This work')

plt.xlabel(r'Fission rate (fissions/cm$^3$/s)')
plt.ylabel(r'Re-solution rate (10$^{-4}$/s)')
plt.legend()
plt.show()
