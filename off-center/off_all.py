import numpy as np
from statistics import mean, stdev
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

dis1 = [0, 10, 20, 30, 40] # 50]
off1 = [[3, 3, 4, 4, 4], [4, 4, 4, 3, 4], [3, 4, 3, 3, 2],
        [1, 4, 3, 4, 4], [2, 4, 2, 0, 4]] # [0, 0, 0, 0, 0]]

dis2 = [0, 10, 20, 30, 40, 50] # 60]
off2 = [[55, 25, 32, 9, 29], [22, 16, 23, 21, 17], [13, 11, 15, 19, 16],
        [5, 7, 5, 3, 9], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0]] # [0, 0, 0, 0, 0]]

dis3 = [0, 10, 20, 30, 40, 50, 60] # 70]
off3 = [[18, 20, 16, 15, 30], [11, 38, 16, 27, 21],
        [11, 6, 18, 14, 15], [9, 10, 9, 7, 5], [1, 2, 4, 3, 0],
        [0, 1, 0, 1, 0], [0, 0, 0, 0, 0]] # [0, 0, 0, 0, 0]]

dis4 = [0, 10, 20, 30, 40, 50, 60, 70] # 80]
off4 = [[21, 20, 21, 17, 16], [18, 14, 25, 25, 16], [15, 16, 21, 4, 19],
        [5, 11, 11, 16, 8], [3, 5, 2, 4, 4], [1, 0, 0, 3, 3],
        [0, 0, 0, 2, 0], [0, 0, 0, 0, 0]] # [0, 0, 0, 0, 0]]

radii = [5, 15, 25, 35]
xe_num = [5, 138, 641, 1758]

averages = []; std_devs = []
for i, off in enumerate([off1, off2, off3, off4]):
    averages.append([mean(x)/xe_num[i] for x in off])
    std_devs.append([stdev(x)/xe_num[i] for x in off])

#for i, j, k in zip([dis2, dis3, dis4], averages[1:], std_devs[1:]):
#    plt.errorbar(i, j, k)
#plt.show()

fractions = []; devs = []
for avg, dev in zip(averages, std_devs):
    fractions.append([x/avg[0] for x in avg])
    devs.append([x/avg[0] for x in dev])

Xs = []; Ys = []
for i, (r, dis) in enumerate(zip(radii[1:], [dis2, dis3, dis4])):
    norm_dis = [x/dis[-1] for x in dis]
    plt.errorbar(norm_dis, fractions[i+1], devs[i+1], marker='o',
                 ls='', capsize=3, label=f'{r} ang radius')
    Xs.extend(norm_dis)
    Ys.extend(fractions[i+1])

X = [x for x, y in sorted(zip(Xs, Ys))]
Y = [y for x, y in sorted(zip(Xs, Ys))]
#plt.scatter(X, Y)

def logistic(x, l, k, c):
    return l / (1 + np.exp(k * x - c))

p, c = curve_fit(logistic, X, Y, p0=[1, 8, 3])
print(*p)
xs = np.linspace(0, 1, 100)
plt.plot(xs, logistic(xs, *p), c='k', label='Logistic fit')

plt.legend()
plt.show()
