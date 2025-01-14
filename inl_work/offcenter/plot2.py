import matplotlib.pyplot as plt
from statistics import mean, stdev

dist = [0, 5, 10, 15, 20, 25, 30]

xe_res = [[6, 12, 7, 10, 12], [4, 19, 13, 10, 12], [11, 9, 4, 15, 12], \
          [2, 2, 14, 11, 9], [2, 9, 10, 11, 4], [3, 4, 5, 4, 9], [2, 0, 3, 7, 5]]

xe_mean = [mean(x)/200 for x in xe_res]
xe_stdev = [stdev(x)/200 for x in xe_res]

plt.errorbar(dist, xe_mean, xe_stdev, capsize=3, marker='o', label='200 atoms')

xe_res2 = [[6, 13, 21, 17, 6], [12, 12, 11, 14, 20], [11, 15, 7, 5, 11], \
          [3, 5, 9, 5, 3], [3, 5, 9, 8, 7], [7, 9, 5, 8, 6], [48, 51, 19, 9, 17]]

xe_mean2 = [mean(x)/400 for x in xe_res2]
xe_stdev2 = [stdev(x)/400 for x in xe_res2]

plt.errorbar(dist, xe_mean2, xe_stdev2, capsize=3, marker='o', label='400 atoms')

plt.xlabel(r'Off-center distance ($\AA$)')
plt.ylabel('Fraction of resolved Xe atoms')
plt.legend()
plt.show()
