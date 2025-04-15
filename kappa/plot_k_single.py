import matplotlib.pyplot as plt

with open('run11_plain_ttm/log.lammps', 'r') as f:
    jar = f.readlines()

# jar = jar[299:2299]
jar = jar[222:2222]

t = []
k_cold = []
k_hot = []

for line in jar:
    tmp = line.split()

    time = float(tmp[1])
    cold = float(tmp[8])
    hot = -1 * float(tmp[9])

    q_cold = (cold * 1.6e-19) / (time * 1e-12) / 2 / (34.3e-10)**2
    q_hot = (hot * 1.6e-19) / (time * 1e-12) / 2 / (34.3e-10)**2

    t.append(time)
    k_cold.append(q_cold * (1716.3/2 * 1e-10) / 200)
    k_hot.append(q_hot * (1716.3/2 * 1e-10) / 200)

plt.plot(t, k_cold, label='sink')
plt.plot(t, k_hot, label='source')

plt.legend()
plt.show()
