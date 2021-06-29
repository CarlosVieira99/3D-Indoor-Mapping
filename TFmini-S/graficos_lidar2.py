import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

dataErrorX12 = np.linspace(0, 4, 200)
dataErrorX3  = np.linspace(0, 1, 200)
dataErrorY12 = 0.06*np.ones(200)
dataErrorY3  = 0.06*np.ones(200)

#x1 = [0.095, 0.201, 0.302, 0.393, 0.486, 0.587, 0.693, 0.792, 0.899, 0.990, 1.081, 1.186, 1.284, 1.390, 1.490, 1.592, 1.676, 1.790, 1.892, 1.993, 2.092, 2.192, 2.288, 2.387, 2.494, 2.589, 2.683, 2.789, 2.890, 2.988, 3.089, 3.192, 3.339, 3.447, 3.556, 3.801, 3.884, 3.978, 4.064, 4.100]
#x2 = [0.102, 0.194, 0.287, 0.377, 0.462, 0.561, 0.668, 0.781, 0.859, 0.970, 1.070, 1.166, 1.269, 1.366, 1.458, 1.574, 1.664, 1.772, 1.876, 1.975, 2.072, 2.185, 2.282, 2.378, 2.484, 2.580, 2.688, 2.786, 2.881, 2.984, 3.082, 3.236, 3.399, 3.553, 3.770, 3.961, 4.102, 4.153, 4.199, 4.219]
#x3 = [0.191, 0.333, 0.451, 0.526, 0.569, 0.988, 0.958, 0.824, 0.993, 1.048]
x1 = np.arange(0.1, 4.1, 0.1)
x2 = np.arange(0.1, 4.1, 0.1)
x3 = np.arange(0.1, 1.1, 0.1)

y1 = [0.005, 0.001, 0.002, 0.007, 0.014, 0.013, 0.007, 0.008, 0.001, 0.010, 0.019, 0.014, 0.016, 0.010, 0.010, 0.008, 0.024, 0.010, 0.008, 0.007, 0.008, 0.008, 0.012, 0.013, 0.006, 0.011, 0.017, 0.011, 0.010, 0.012, 0.011, 0.008, 0.039, 0.048, 0.056, 0.201, 0.184, 0.178, 0.164, 0.100]
y2 = [0.002, 0.006, 0.013, 0.023, 0.038, 0.039, 0.032, 0.019, 0.041, 0.030, 0.030, 0.034, 0.031, 0.034, 0.042, 0.026, 0.036, 0.028, 0.024, 0.025, 0.028, 0.015, 0.018, 0.022, 0.016, 0.020, 0.012, 0.014, 0.019, 0.016, 0.018, 0.036, 0.099, 0.153, 0.250, 0.361, 0.402, 0.353, 0.299, 0.219]
y3 = [0.091, 0.133, 0.151, 0.126, 0.069, 0.388, 0.258, 0.024, 0.093, 0.048]

fig, ax = plt.subplots()
ax.plot(x3, y3, 'o',label = "Measurement error")
ax.plot(dataErrorX3, dataErrorY3, '--' ,label = "Datasheet reference error")

ax.legend()
ax.set(xlabel="Real distance (m)", ylabel='Accuracy error (m)')
ax.grid()
ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))

#ax.ticklabel_format(useOffset=False, style='plain') # Desativar notacao cientifica
plt.show()