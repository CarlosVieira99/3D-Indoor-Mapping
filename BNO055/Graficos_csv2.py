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

with open("C:/Users/litos/Desktop/IMU/Eul_pitch.txt", "r") as fileObject:  # Use file to refer to the file object
    while True:
        line = fileObject.readline()
        if not line:
            break
        line = line[:-1]
        linesplitted = line.split(',')
        time.append(int(linesplitted[0]))
        x.append(float(linesplitted[2]))
        y.append(float(linesplitted[5]))
        #z.append(float(linesplitted[3]))

#time = time - time[0]
time = np.array(time)
time = time - time[0]
time = time/1000

x = np.array(x)
y = np.array(y)

fig, ax = plt.subplots()

ax.plot(time, x, '-', label = "Euler")
ax.plot(time, y, '--', label = "Quaternions")

ax.set_xlim(0, 15)
#ax.set_ylim(-5, 5)

ax.legend()

ax.set(xlabel=r'Time ($s$)', ylabel=r'Degrees (º)') #, title='Total Points vs Stepper Motor Resolution')
ax.grid()

plt.show()