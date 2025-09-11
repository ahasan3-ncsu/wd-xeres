import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.tri as tri

xlo, ylo = -80, -80
xhi, yhi = 80, 80

xc, yc = 0, 0
rad = 40

points = [[xc, yc]]

N = 4
for k in range(4*N):
    angle = math.pi/2/N * k
    x = round(xc + rad * math.cos(angle), 5)
    y = round(yc + rad * math.sin(angle), 5)
    points.append([x, y])

corners = [[xhi, yhi], [xlo, yhi], [xlo, ylo], [xhi, ylo]]
points.extend(corners)

print('points= ', points)

triangles = []
densities = []

# circle pies
cy1 = list(range(1, 4*N + 1)) + [1]
for i in range(4*N):
    triangles.append([0, cy1[i], cy1[i+1]])
    densities.append([0.0, 0.0, 0.0092])

# corner triangles
box_inds = [4*N + j for j in range(1, 5)]
print('boundary= ', box_inds)
for j in range(4):
    for k in range(N):
        triangles.append([cy1[j*N + k], cy1[j*N + (k+1)], box_inds[j]])
        densities.append([0.03588, 0.01012, 0.0])

# edge triangles
cy2 = [box_inds[-1]] + box_inds
edges = [[1+j*N, cy2[j], cy2[j+1]] for j in range(4)]

triangles.extend(edges)
densities.extend([[0.03588, 0.01012, 0.0]] * 4)

assert len(triangles) == len(densities)
print('triangles= ', triangles)
print('densities= ', densities)

poi = np.array(points)
den = np.sum(densities, axis=1)

fig, ax = plt.subplots()
ax.tripcolor(poi[:, 0], poi[:, 1], triangles, den,
             edgecolor='k', cmap='Set1')

for i in range(len(cy2)-1):
    x, y = zip(points[cy2[i]], points[cy2[i+1]])
    ax.plot(x, y, c='k', lw=2)

ax.set_aspect('equal')
# ax.set_xlim([0, 10])
# ax.set_ylim([0, 10])
plt.show()
