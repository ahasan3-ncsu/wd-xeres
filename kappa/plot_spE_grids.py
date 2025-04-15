import matplotlib.pyplot as plt

grid = [50, 100, 250]
spE = [0.0046, 0.0096, 0.027]

plt.plot(grid, spE, marker='o')

plt.xlabel('Number of grids')
plt.ylabel('Avg. spurious energy per timestep')

#plt.legend()
plt.show()
