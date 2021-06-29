import numpy as np
import matplotlib.pyplot as plt

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

line = "ACK"

time = []
x = []
y = []
z = []

roll = []
pitch = []
yaw = []

with open("C:/Users/litos/Desktop/IMU/Mag_static.txt", "r") as fileObject:  # Use file to refer to the file object
    while True:
        line = fileObject.readline()
        if not line:
            break
        line = line[:-1]
        linesplitted = line.split(',')
        time.append(int(linesplitted[0]))
        x.append(float(linesplitted[1]))
        y.append(float(linesplitted[2]))
        z.append(float(linesplitted[3]))

#time = time - time[0]
time = np.array(time)
time = time - time[0]
time = time/1000

x = np.array(x)
#x = x*np.pi/180
#x_offset = np.linspace(0, 3.14/4, len(x))
#x = x+x_offset
x_mean = x.mean() * np.ones(len(x))


y = np.array(y)
#y = y*np.pi/180
#y_offset = np.linspace(0, 3.14/6, len(y))
#y = y+y_offset
y_mean = y.mean() * np.ones(len(y))

z = np.array(z)
#z = z*np.pi/180
#z_offset = np.linspace(0, 3.14/4, len(z))
#z = z+z_offset
z_mean = z.mean() * np.ones(len(z))


fig, ax = plt.subplots()

ax.plot(time, z, '-', label = "Z axis points")
ax.plot(time, z_mean, '--', label = "Average")
#axs[0].plot(time, x, 'o-', label = "X axis")
#axs[1].plot(time, y, 'o-', label = "Y axis")
#axs[2].plot(time, z, 'o-', label = "Z axis")

ax.set_xlim(0, 20)
#ax.set_ylim(-5, 5)
#axs[0].set_xlim(0, 1)
#axs[1].set_xlim(0, 1)
#axs[2].set_xlim(0, 1)
#axs[2].ylim(9.93, 10.03)

#plt.yscale("log")
ax.legend()
#axs[0].legend()
#axs[1].legend()
#axs[2].legend()
#plt.xticks(n)
#plt.yticks(points)

ax.set(xlabel=r'Time ($s$)', ylabel=r'Magnetic Field Strength ($\mu T$)') #, title='Total Points vs Stepper Motor Resolution')
#axs[0].set(xlabel='Stepper Resolution', ylabel='Total Points', title='Total Points vs Stepper Motor Resolution')
#axs[1].set(xlabel='Stepper Resolution', ylabel='Total Points', title='Total Points vs Stepper Motor Resolution')
#axs[2].set(xlabel='Stepper Resolution', ylabel='Total Points', title='Total Points vs Stepper Motor Resolution')
#plt.title("Accelerometer")
ax.grid()

#ax.ticklabel_format(useOffset=False, style='plain') # Desativar notacao cientifica

#fig.savefig("test.png")
plt.show()