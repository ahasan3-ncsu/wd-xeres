import numpy as np
import matplotlib.pyplot as plt

def get_grid_points(x, w, alpha, D, H, L, nel_mesh):
    T = np.linspace(0, 1, nel_mesh+1)
    T = (T[1:] + T[:-1]) / 2

    cos_a = np.cos(alpha)
    sin_a = np.sin(alpha)

    xp, wp = x  - D * cos_a, w  - D * sin_a
    p1, q1 = xp - H * sin_a, wp + H * cos_a
    p2, q2 = xp + H * sin_a, wp - H * cos_a
    f1, f2 = (H - L) / (2 * H), (H + L) / (2 * H)

    points = []
    for t1 in T:
        p = p1 + t1 * (p2 - p1)
        q = q1 + t1 * (q2 - q1)
        for t2 in T:
            # discard points outside the region
            if f1 < t1 and t1 < f2 and f1 < t2 and t2 < f2:
                continue

            z = -H + t2 * (2 * H)
            # point in question: (p, q, z)
            # central point: (xp, wp, 0)

            # _w = (q**2 + z**2) ** 0.5
            # _l = ((p - xp)**2 + (q - wp)**2 + z**2) ** 0.5
            # points.append((p, _w, _l))

            points.append((p, q, z))

    return points

def plotter(points):
    plt.figure(figsize=(5, 4))

    # plt.scatter(x, w, s=500, color='r')
    # plt.plot([p1, p2], [q1, q2], color='k', ls=':')

    u = []; v = []
    for p in points:
        x, y, z = p
        u.append(x)
        v.append(y)
    plt.scatter(u, v, color='teal')

    plt.xlabel('x')
    plt.ylabel('y')

    plt.xlim([2e3, 6e3])
    plt.ylim([3e3, 7e3])

    # plt.axis('equal')
    plt.tight_layout()
    plt.savefig('test1.pdf')

    plt.clf()

    # plt.scatter(0, w, s=500, color='r')

    u = []; v = []
    for p in points:
        x, y, z = p
        u.append(y)
        v.append(z)
    plt.scatter(v, u, color='teal')

    plt.xlabel('z')
    plt.ylabel('y')

    plt.xlim([-2e3, 2e3])
    plt.ylim([3e3, 7e3])

    # plt.axis('equal')
    plt.tight_layout()
    plt.savefig('test2.pdf')

    return True

def main():
    P = []

    points1 = get_grid_points(5e3, 5e3, 0.0, 1010, 1010, 202, 5)
    P.extend(points1)

    points2 = get_grid_points(5e3, 5e3, 0.0, 1010, 202, 0, 3)
    P.extend(points2)

    plotter(P)

if __name__ == '__main__':
    main()
