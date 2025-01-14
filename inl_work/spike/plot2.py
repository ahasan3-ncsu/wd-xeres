import matplotlib.pyplot as plt
from statistics import mean, stdev

energ = [0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1, \
         1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, \
         10, 15, 20, 25, 30, 35, 40]

xe_res = [[5, 2, 3], [8, 6, 7], [4, 4, 7], [20, 5, 11], \
          [7, 11, 3], [7, 6, 6], [8, 13, 8], [10, 20, 12], \
          [32, 13, 22], [33, 10, 14], [14, 11, 15], [18, 15, 13], \
          [16, 19, 17], [15, 8, 19], [25, 19, 19], [46, 33, 58], \
          [65, 52, 59], [62, 75, 77], [92, 107, 83], [132, 89, 86], \
          [99, 107, 100], [101, 122, 94]]

xe_mean = [mean(x)/200 for x in xe_res]
xe_stdev = [stdev(x)/200 for x in xe_res]

plt.errorbar(energ, xe_mean, xe_stdev, capsize=3, marker='o', label='200 atoms')

energ2 = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, \
         2.5, 2.75, 3, 3.25, 3.5, 10, 15, 20, 25, 30, 35, 40]

xe_res2 = [[5, 14, 4], [9, 3, 3], [18, 15, 9], [12, 25, 12], \
          [14, 19, 13], [13, 16, 28], [12, 28, 19], [26, 16, 28], \
          [11, 23, 21], [15, 24, 26], [10, 25, 32], [32, 25, 24], \
          [27, 28, 19], [90, 74, 63], [105, 116, 144], [135, 163, 146], \
          [188, 129, 140], [178, 182, 168], [182, 249, 229], [190, 209, 224]]

xe_mean2 = [mean(x)/400 for x in xe_res2]
xe_stdev2 = [stdev(x)/400 for x in xe_res2]

plt.errorbar(energ2, xe_mean2, xe_stdev2, capsize=3, marker='o', label='400 atoms')

plt.xlabel('Energy (MeV)')
plt.ylabel('Fraction of resolved Xe atoms')
plt.legend()
plt.show()
