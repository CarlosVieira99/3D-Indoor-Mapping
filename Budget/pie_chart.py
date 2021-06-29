import matplotlib.pyplot as plt
import numpy as np

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Lidar', 'Steppers', 'IMU', 'uController', "PCB", "Filament"
componentsPCB = 2.3084309 + 0.01229
PCB = componentsPCB + 0.354
filament = 1.29
sizes = np.array([35.99, 26, 19.90, 9.99, PCB, filament])
total = np.sum(sizes)
sizes = sizes/total
#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt.subplots()
#ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#        shadow=True, startangle=90)

ax1.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=0)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Budget: Influence of sectors")
plt.show()