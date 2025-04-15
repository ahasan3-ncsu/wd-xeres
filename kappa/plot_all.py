import matplotlib.pyplot as plt

fileName = 'log.ttm'
indFirst = 233
indLast = 2233

with open(fileName, 'r') as f:
    jar = f.readlines()

jar = jar[indFirst:indLast]

time = []
energ = []
cold = []
hot = []
ttm = []

for line in jar:
    tmp = line.split()

    time.append(float(tmp[1]))
    energ.append(float(tmp[3]))

    cold.append(float(tmp[6]))
    hot.append(-1 * float(tmp[7]))
    ttm.append(float(tmp[8]))

diff = [c-h for c, h in zip(cold, hot)]

potEng = [i-energ[0] for i in energ]
plt.plot(time, potEng, label='pot energy')

plt.plot(time, hot, label='source')
plt.plot(time, cold, label='sink')

plt.plot(time, diff, label='discrepancy')
plt.plot(time, ttm, label='elec energy')

plt.legend()
plt.show()
