import matplotlib.pyplot as plt

fileName = 'log.200K'
indFirst = 299
indLast = 2299

with open(fileName, 'r') as f:
    jar = f.readlines()

jar = jar[indFirst:indLast]

time = []
hot = []
cold = []

for line in jar:
    tmp = line.split()

    time.append(float(tmp[1]))
    hot.append(float(tmp[6]))
    cold.append(-1 * float(tmp[7]))

# hot/cold naming issue here
plt.plot(time, hot, label='sink')
plt.plot(time, cold, label='source')

plt.legend()
plt.show()
