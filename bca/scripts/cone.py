import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

points = np.array([
    [0.0, 0.0],
    [0.5, 0.0],
    [1.0, 0.0],
    [1.0, 0.5],
    [1.0, 1.0],
    [0.5, 0.5]
])
values = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])

grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]

grid_z = griddata(points, values, (grid_x, grid_y), method='linear')

mask = grid_y > grid_x
grid_z = np.ma.masked_where(mask, grid_z)

# colormap
plt.figure(figsize=(6, 6))
plt.pcolormesh(grid_x, grid_y, grid_z, shading='auto', cmap='viridis')
plt.colorbar(label='Interpolated Value')

# boundary
plt.plot([0, 1], [0, 0], 'k-', linewidth=2)
plt.plot([1, 1], [0, 1], 'k-', linewidth=2)
plt.plot([1, 0], [1, 0], 'k-', linewidth=2)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Colormap with Interpolation')
plt.xlim(0, 1)
plt.ylim(0, 1)

plt.show()
