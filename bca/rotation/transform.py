import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# https://mathworld.wolfram.com/SpherePointPicking.html
def sample_sphere_area(num_samples):
    u = np.random.uniform(0, 1, num_samples)
    v = np.random.uniform(0, 1, num_samples)

    theta = 2 * np.pi * u
    phi = np.arccos(2 * v - 1)

    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    return np.stack((x, y, z), axis=-1)

# https://stackoverflow.com/questions/5408276/
# sampling-uniformly-distributed-random-points-inside-a-spherical-volume
def sample_sphere_vol(num_samples):
    u = np.random.uniform(0, 1, num_samples)
    v = np.random.uniform(0, 1, num_samples)
    w = np.random.uniform(0, 1, num_samples)

    theta = 2 * np.pi * u
    phi = np.arccos(2 * v - 1)
    r = np.cbrt(w)

    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    return np.stack((x, y, z), axis=-1)

# rejection oversampling
def sample_sphere_vol_2(num_samples):
    samples = []
    while len(samples) < N:
        xyz = np.random.uniform(-1, 1, (num_samples * 2, 3))
        norms_squared = np.sum(xyz**2, axis=1)
        inside_sphere = xyz[norms_squared <= 1]
        samples.extend(inside_sphere.tolist())
    return np.array(samples[:N])

# https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula
def xalign_matrix(v):
    theta = np.arccos(v[0])
    axis = np.cross(v, np.array([1, 0, 0]))
    k = axis / np.linalg.norm(axis)
    K = np.array([
        [0, -k[2], k[1]],
        [k[2], 0, -k[0]],
        [-k[1], k[0], 0]
    ])

    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    return R

# settings
N = 700
p_colo = 'red'
v_colo = 'silver'
np.random.seed(97)

positions = sample_sphere_vol(N)
velocities = sample_sphere_area(N)

t_positions = np.array([
    xalign_matrix(velocities[i]) @ positions[i]
    for i in range(N)
])
t_velocities = np.array([
    xalign_matrix(velocities[i]) @ velocities[i]
    for i in range(N)
])

# plotting
plt.style.use('../science.mplstyle')
fig = plt.figure(figsize=(7, 3.5))

ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(
    positions[:, 0], positions[:, 1], positions[:, 2],
    color=p_colo, s=7
)
ax1.quiver(
    positions[:, 0], positions[:, 1], positions[:, 2],
    velocities[:, 0], velocities[:, 1], velocities[:, 2],
    length=0.1, normalize=True, color=v_colo, alpha=0.7
)

ax1.set_title(r"Original $(\mathbf{r_i}, \mathbf{v_i})$")
ax1.set_xlim([-0.4, 0.4])
ax1.set_ylim([-0.4, 0.4])
ax1.set_zlim([-0.4, 0.4])
ax1.view_init(elev=10, azim=270)
ax1.axis('off')

ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(
    t_positions[:, 0], t_positions[:, 1], t_positions[:, 2],
    color=p_colo, s=7
)
ax2.quiver(
    t_positions[:, 0], t_positions[:, 1], t_positions[:, 2],
    t_velocities[:, 0], t_velocities[:, 1], t_velocities[:, 2],
    length=0.1, normalize=True, color=v_colo, alpha=0.7
)

ax2.set_title(r"Transformed $(\mathbf{r_i'}, \mathbf{v_i'})$")
ax2.set_xlim([-0.4, 0.4])
ax2.set_ylim([-0.4, 0.4])
ax2.set_zlim([-0.4, 0.4])
ax2.view_init(elev=10, azim=90)
ax2.axis('off')

plt.savefig('rotation.pdf')
