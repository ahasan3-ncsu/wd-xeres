import matplotlib.pyplot as plt

with open('log.knock5', 'r') as f:
    jar = f.readlines()

jar = jar[230:]
print(jar[0].split())

time = []; temp = []
for line in jar:
    tmp = line.split()
    time.append(float(tmp[2]))
    temp.append(float(tmp[3]))

plt.plot(time, temp, label='with 9 eV ES')
plt.xlabel('Time (ps)')
plt.ylabel('Temp (K)')
plt.legend()
plt.show()
