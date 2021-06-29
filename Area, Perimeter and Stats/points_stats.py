import numpy as np
import matplotlib.pyplot as plt

x_up = []
y_up = []

x_down = []
y_down = []

x = []
y = []
xy = []

rad = []
r = []
rad_r = []

with open("quarter_clean.txt", "r") as fileObject:  # Use file to refer to the file object
    line = fileObject.readline()
    linesplitted = line.split(',')
    x_up.append(float(linesplitted[0]))
    y_up.append(float(linesplitted[1]))
    x_down.append(float(linesplitted[0]))
    y_down.append(float(linesplitted[1]))
    radian = np.arctan2(float(linesplitted[1]), float(linesplitted[0]))
    if radian < 0:
        radian = 2*np.pi + radian
    rad.append(radian)
    r.append(np.sqrt(float(linesplitted[0])**2 + float(linesplitted[1])**2))

    cnt = 0
    while line:
        line = fileObject.readline()
        linesplitted = line.split(',')
        if(len(linesplitted)) == 3:
            if float(linesplitted[2])==0:
                if float(linesplitted[1])>=0:
                    x_up.append(float(linesplitted[0]))
                    y_up.append(float(linesplitted[1]))
                elif float(linesplitted[1])<=0:
                    x_down.append(float(linesplitted[0]))
                    y_down.append(float(linesplitted[1]))
                
                x.append(float(linesplitted[0]))
                y.append(float(linesplitted[1]))
                xy.append([float(linesplitted[0]), float(linesplitted[1])])
                radian = np.arctan2(float(linesplitted[1]), float(linesplitted[0]))
                if radian < 0:
                    radian = 2*np.pi + radian
                
                ## Para ordernar
                rad.append(radian)
                r.append(np.sqrt(float(linesplitted[0])**2 + float(linesplitted[1])**2))
                rad_r.append([radian, np.sqrt(float(linesplitted[0])**2 + float(linesplitted[1])**2)])

            cnt = cnt+1

widthPlot = []

for i in range(len(x_up)-1):
    widthPlot.append(x_up[i+1]-x_up[i])

x_left = x_up[:-1] # Left endpoints
y_left = y_up[:-1]

plt.plot(x, y, 'bo')
plt.figure()

xy = sorted(xy,key=lambda x: x[0]) # Afinal não é preciso fazer sort

x2_up = []
y2_up = []
x2_down = []
y2_down = []

for i in range(len(xy)-1):
    if xy[i][1]>=0:
        x2_up.append(xy[i][0])
        y2_up.append(xy[i][1])
    else:
        x2_down.append(xy[i][0])
        y2_down.append(xy[i][1])

widthPlot2 = []

rad_r = sorted(rad_r,key=lambda x: x[0]) # Afinal não é preciso fazer sort

rad2 = [i[0] for i in rad_r]
r2 = [i[1] for i in rad_r]

for i in range(len(rad2)-1):
    widthPlot2.append(rad2[i+1]-rad2[i]) # Constante = 0.00785422

rad_left = rad2[:-1] # Left endpoints
r_left = r2[:-1]

rad2 = np.array(rad2)
r2 = np.array(r2)

rad_mid = (rad2[:-1] + rad2[1:])/2 # Midpoints
r_mid = (r2[:-1] + r2[1:])/2

plt.polar(rad2, r2,'o-', markersize=2)
ax = plt.subplot(111, projection='polar')
ax.bar(rad_left, r_left, width=widthPlot2, bottom=0.0, align='edge', alpha=0.5, edgecolor='g', color='g')

dx = widthPlot2[0]
x_left = np.linspace(0,2*np.pi-dx,len(widthPlot2))

array = [[1,1,1], [2, 2, 2], [3, 4, 5]]
array_test = np.array(array)
array_test_dist = np.linalg.norm(array_test, axis=1)

print("Distancia ao ponto mais distante", np.max(array_test_dist))
print(array_test.mean(axis=0)) # Ponto médio
print(np.median(array_test, axis=0)) # Ponto do meio
hpoint = np.max(array_test, axis=0)
print("Ponto mais alto: ", hpoint) # Ponto mais alto
print("Altura do ponto mais alto: ", hpoint[2]) # Altura
print("STD: ", np.std(array_test, dtype=np.float64))
print("Variancia", np.var(array_test, dtype=np.float64))
print(array_test_dist)
print(array_test_dist.mean())
print("STD: ", np.std(array_test_dist, dtype=np.float64))
print("Variancia", np.var(array_test_dist, dtype=np.float64))

print(dx) # 0.45 graus
arr = np.array(r2)
print("Partition with",len(widthPlot2),"subintervals.")
left_riemann_sum = np.sum(0.5 * arr * arr*np.tan(dx)) #0.5 * b * h
print("Left Riemann Sum Triangle:",left_riemann_sum/1000000)
left_riemann_sum = np.sum(np.pi * arr**2 * dx/(2*np.pi)) #pi*r^2
print("Left Riemann Sum Part of Circle:",left_riemann_sum/1000000)
perimetro = np.sum(arr*np.tan(dx))
print("Perimetro Triangle: ", perimetro/1000)
perimetro = np.sum(2*np.pi*arr*(dx/(2*np.pi)))
print("Perimetro Circle: ", perimetro/1000)

plt.show()