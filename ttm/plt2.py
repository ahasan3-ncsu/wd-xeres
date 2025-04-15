import matplotlib.pyplot as plt

with open('tmpChunk.knock4') as f:
    jar = f.readlines()

c = []
nChunk = 10
for i in range(4, 113, nChunk+1):
    c.append(float(jar[i+0].split()[1]))

plt.plot(c)
plt.show()
