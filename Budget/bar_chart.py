from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)

labels = ['LIDAR', 'Steppers', 'IMU', 'uController', "PCB", "Filament"]
x = np.arange(6)
componentsPCB = 2.3084309 + 0.01229
PCB = componentsPCB + 0.354
filament = 1.29

costs = np.array([35.99, 26, 19.90, 9.99, PCB, filament])

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1f€' % (x)


formatter = FuncFormatter(millions)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
plt.bar(x, costs, color=['blue', 'orange', 'green', 'red', 'purple', 'brown'])
plt.xticks(x, labels)
plt.title("Budget: price by sectors")
plt.show()
