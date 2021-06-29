import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
d = np.arange(0.00, 12.00, 0.01)
error = d*np.tan(np.deg2rad(2))

fig, ax = plt.subplots()
ax.plot(d, error)

#plt.yscale("log")
#ax.legend()
#plt.xticks(n)
#plt.yticks(points)

ax.set(xlabel='Detecting range (m)', ylabel='Minimum side length (m)',
       title='Minimum side length of effective detection\ncorresponding to Detecting Range')
ax.grid()

ax.ticklabel_format(useOffset=False, style='plain') # Desativar notacao cientifica

#fig.savefig("test.png")
plt.show()