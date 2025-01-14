import matplotlib.pyplot as plt
from statistics import mean, stdev

rad = [15, 20, 25, 30, 35, 40]
xe = [138, 328, 641, 1107, 1758, 2624]

xe_res = [[4, 3, 3, 4, 4], [7, 5, 10, 7, 9], [6, 15, 4, 24, 5],
          [11, 13, 10, 10, 13], [16, 22, 19, 15, 14], [49, 11, 59, 13, 35]]

xe_mean = [mean(x)/f for x, f in zip(xe_res, xe)]
xe_stdev = [stdev(x)/f for x, f in zip(xe_res, xe)]

plt.errorbar(rad, xe_mean, xe_stdev, capsize=3, marker='o')

plt.xlabel(r'Bubble radius ($\AA$)')
plt.ylabel('Fraction of resolved Xe atoms')
plt.show()
