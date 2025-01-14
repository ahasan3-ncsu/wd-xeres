import matplotlib.pyplot as plt
from statistics import mean, stdev

rad = [15, 20, 25, 30, 35, 40]
xe = [138, 328, 641, 1107, 1758, 2624]

plt.plot(rad, xe, marker='o')

plt.xlabel(r'Bubble radius ($\AA$)')
plt.ylabel('Number of Xe atoms in the bubble')
plt.show()
