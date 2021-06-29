import matplotlib.pyplot as plt
import numpy as np

circle1 = plt.Circle((0, 0), 14/2, color='g')
circle2 = plt.Circle((0, 0), 28/2, color='y')
circle3 = plt.Circle((0, 0), 42/2, color='r')

fig, ax = plt.subplots()

plt.xlim(-25,25)
plt.ylim(-25,25)

plt.grid(linestyle='--')

ax.set_aspect(1)

ax.add_artist(circle3)
ax.add_artist(circle2)
ax.add_artist(circle1)

ax.set(xlabel='Radius (cm)', ylabel='Radius (cm)')

#print(ax.get_yticks())
#print(abs(ax.get_yticks()))

sal = np.array([42/2, -28/2, -14/2, 0, 14/2, 28/2, 42/2])

print(sal)

plt.xticks(abs(sal))
plt.yticks(abs(sal))

plt.title('Different Light Spots')

plt.legend((circle1,circle2,circle3),('Distance = 4m','Distance = 8m', 'Distance = 12m'),numpoints=1, loc=3)
#plt.legend()

plt.show()