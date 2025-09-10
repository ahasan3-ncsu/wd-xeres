import numpy as np
import matplotlib.pyplot as plt

N = 1000
u = np.random.uniform(0, 1, N)
v = np.random.uniform(0, 1, N)

theta = 2 * np.pi * u
phi = np.arccos(2 * v - 1)

x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

fig, axs  = plt.subplots(1, 2)

axs[0].scatter(x, y, s=5)
axs[0].set_xlabel('x')
axs[0].set_ylabel('y')

axs[1].scatter(x, z, s=5)
axs[1].set_xlabel('x')
axs[1].set_ylabel('z')

circle1 = plt.Circle((0, 0), 1, color='dimgray', alpha=0.2)
axs[0].add_patch(circle1)

circle2 = plt.Circle((0, 0), 1, color='dimgray', alpha=0.2)
axs[1].add_patch(circle2)

axs[0].axis('equal')
axs[1].axis('equal')

plt.show()
