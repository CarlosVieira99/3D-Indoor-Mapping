import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
d1 = np.arange(0.00, 6.00, 0.01)
d2 = np.arange(6.00, 12.00, 0.01)
d = np.append(d1, d2)
error1 = np.ones(len(d1))*0.06
error2 = d2*0.01
error = np.append(error1, error2)
# = 1 + np.sin(2 * np.pi * t)
#n = np.array([1, 2, 4, 8, 16, 32])
#points = n*(n*10000 + 100)

fig, ax = plt.subplots()
ax.plot(d, error)
#ax.plot(d, error, label = "Legenda")

#plt.yscale("log")
#ax.legend()
#plt.xticks(n)
#plt.yticks(points)

ax.set(xlabel='Detecting range (m)', ylabel='Error (m)',
       title='Lidar accuracy')
ax.grid()

ax.ticklabel_format(useOffset=False, style='plain') # Desativar notacao cientifica

#fig.savefig("test.png")
plt.show()