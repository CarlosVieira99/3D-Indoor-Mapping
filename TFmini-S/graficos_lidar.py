import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

linearX12 = np.linspace(0, 4, 200)
linearY12 = linearX12
linearX3 = np.linspace(0, 1, 200)
linearY3 = linearX3

l_reg_x12 = np.linspace(0, 4, 200)
l_reg_x3 = np.linspace(0, 1, 200)
l_reg_y1 = (l_reg_x12 - 0.051)/0.958
l_reg_y2 = (l_reg_x12 - 0.118)/0.926
l_reg_y3 = (l_reg_x3 + 0.077)/0.911

x1 = [0.095, 0.201, 0.302, 0.393, 0.486, 0.587, 0.693, 0.792, 0.899, 0.990, 1.081, 1.186, 1.284, 1.390, 1.490, 1.592, 1.676, 1.790, 1.892, 1.993, 2.092, 2.192, 2.288, 2.387, 2.494, 2.589, 2.683, 2.789, 2.890, 2.988, 3.089, 3.192, 3.339, 3.447, 3.556, 3.801, 3.884, 3.978, 4.064, 4.100]
x2 = [0.102, 0.194, 0.287, 0.377, 0.462, 0.561, 0.668, 0.781, 0.859, 0.970, 1.070, 1.166, 1.269, 1.366, 1.458, 1.574, 1.664, 1.772, 1.876, 1.975, 2.072, 2.185, 2.282, 2.378, 2.484, 2.580, 2.688, 2.786, 2.881, 2.984, 3.082, 3.236, 3.399, 3.553, 3.770, 3.961, 4.102, 4.153, 4.199, 4.219]
y12 = np.arange(0.1, 4.1, 0.1)

x3 = [0.191, 0.333, 0.451, 0.526, 0.569, 0.988, 0.958, 0.824, 0.993, 1.048]
y3 = np.arange(0.1, 1.1, 0.1)

fig, ax = plt.subplots()
ax.plot(y3, x3, 'o',label = "Measured points")
ax.plot(l_reg_x3, l_reg_y3, '-' ,label = "Linear regression")
ax.plot(linearX3, linearY3, '--',label = "Perfect measurement")

ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax.legend()
ax.set(xlabel='Real distance (m)', ylabel='Sensor distance (m)')
ax.grid()

#ax.ticklabel_format(useOffset=False, style='plain') # Desativar notacao cientifica
plt.show()