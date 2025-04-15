import matplotlib.pyplot as plt

fileName = 'run10_half_empty/chunk_temp.out'

with open(fileName, 'r') as f:
    jar = f.readlines()

def prn(data, nChunk=0):
    nx = []
    temp = []

    for line in data[4 + 51*nChunk : 54 + 51*nChunk]:
        tmp = line.split()
        nx.append(float(tmp[0]))
        temp.append(float(tmp[1]))

    plt.plot(nx, temp, label=f'time: {nChunk+1}n')

for i in range(5, 9):
    prn(jar, i)

plt.xlabel('Grid number')
plt.ylabel('Temperature (K)')
#plt.ylim([1080, 1320])

plt.legend()
plt.show()
