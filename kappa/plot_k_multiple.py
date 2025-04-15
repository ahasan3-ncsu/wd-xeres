import matplotlib.pyplot as plt

def prn(fileName, delta, indFirst, indLast):
    with open(fileName, 'r') as f:
        jar = f.readlines()

    jar = jar[indFirst:indLast]

    t = []
    k_hot = []; k_cold = []

    for line in jar:
        tmp = line.split()

        time = float(tmp[1])
        hot = -1 * float(tmp[7])
        cold = float(tmp[6])

        q_hot = (hot * 1.6e-19) / (time * 1e-12) / 2 / (34.3e-10)**2
        q_cold = (cold * 1.6e-19) / (time * 1e-12) / 2 / (34.3e-10)**2

        t.append(time)
        k_hot.append(q_hot * (1716.3/2 * 1e-10) / delta)
        k_cold.append(q_cold * (1716.3/2 * 1e-10) / delta)

    colo = plt.cm.jet(delta/500)
    plt.plot(t, k_hot, c=colo, label=f'{1200 + delta/2} K source')
    plt.plot(t, k_cold, ls='-.', c=colo, label=f'{1200 - delta/2} K sink')

prn('log.100K', 100, 233, 2233)
prn('log.200K', 200, 299, 2299)
prn('log.300K', 300, 233, 2233)

plt.xlabel('Time (ps)')
plt.ylabel('Thermal Conductivity (W/m/K)')

plt.legend(ncol=3)
plt.show()
