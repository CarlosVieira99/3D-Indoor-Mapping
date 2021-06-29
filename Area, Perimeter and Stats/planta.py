import numpy as np
import matplotlib.pyplot as plt

#print(np.arctan2(3,2))
#print(np.arctan2(3,-2))
#print(np.arctan2(-3,2))
#print(np.arctan2(-3,-2))

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

with open("/media/kajo/1D05-96F1/Projeto_Completo/Code_for_Graphs_and_Stats/Area_and_Perimeter/quarter_clean.txt", "r") as fileObject:  # Use file to refer to the file object
    line = fileObject.readline()
    linesplitted = line.split(',')
    x_up.append(float(linesplitted[0]))
    y_up.append(float(linesplitted[1]))
    x_down.append(float(linesplitted[0]))
    y_down.append(float(linesplitted[1]))
    radian = np.arctan2(float(linesplitted[1]), float(linesplitted[0]))
    if radian < 0:
        radian = 2*np.pi + radian
    #print(radian)
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

    #print(cnt)

        #if cnt==399:
        #    print(line)
        #    cnt=0
        
        #cnt += 1

#fig, ax = plt.subplots()
#plt.subplot(2,1,1)
#plt.plot(x_up, y_up,'o')

widthPlot = []

for i in range(len(x_up)-1):
    widthPlot.append(x_up[i+1]-x_up[i])

x_left = x_up[:-1] # Left endpoints
y_left = y_up[:-1]
#x_mid = (x_up[:-1] + x_up[1:])/2
#y_mid = (y_up[:-1] + y_up[1:])/2
#plt.plot(x_left,y_left,'b.',markersize=10)
#plt.bar(x_left,y_left,width=widthPlot,align='edge',edgecolor='g', color='g')

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

#plt.plot(x2_up, y2_up, 'ro-')
#plt.plot(x2_down, y2_down, 'ro-')

#plt.xlim(-3000, 3000)
#plt.ylim(-3000, 3000)

#plt.plot(x[i:i+2], y[i:i+2], 'ro-')

#plt.figure()

widthPlot2 = []

#sorted(rad_r)

#rad_r.sort(0)
rad_r = sorted(rad_r,key=lambda x: x[0]) # Afinal não é preciso fazer sort
#print(rad_r)
#sorted(li,key=lambda x: x[1])

#print(rad_r[][:])
rad2 = [i[0] for i in rad_r]
r2 = [i[1] for i in rad_r]
#print([i[0] for i in rad_r])

#rad2 = [0, np.pi/4, np.pi/2, 0.75*np.pi, np.pi]
#r2 = [2, 6, 4, 6, 2]

for i in range(len(rad2)-1):
    widthPlot2.append(rad2[i+1]-rad2[i]) # Constante = 0.00785422

#print(widthPlot2)

rad_left = rad2[:-1] # Left endpoints
r_left = r2[:-1]

#print(rad_left)

rad2 = np.array(rad2)
r2 = np.array(r2)

rad_mid = (rad2[:-1] + rad2[1:])/2 # Midpoints
r_mid = (r2[:-1] + r2[1:])/2

#print(rad_mid)
#print(r_mid)

plt.polar(rad2, r2,'o-', markersize=2)
ax = plt.subplot(111, projection='polar')
#ax.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
ax.bar(rad_left, r_left, width=widthPlot2, bottom=0.0, align='edge', alpha=0.5, edgecolor='g', color='g')
#ax.bar(rad_mid, r_mid, width=widthPlot2, bottom=0.0, align='edge', alpha=0.5, edgecolor='g', color='g')

dx = widthPlot2[0]
x_left = np.linspace(0,2*np.pi-dx,len(widthPlot2))

array = [[1,1,1], [2, 2, 2], [3, 4, 5]]
array_test = np.array(array)
array_test_dist = np.linalg.norm(array_test, axis=1)
#array_test_dist = [i[:][0] for i in array_test]
#np.
#array_test_dist2 = np.zeros(len(array_test))
#dist = np.linalg.norm(array_test-array_test_dist2)
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
#print(arr)
#print(arr**2)
print("Partition with",len(widthPlot2),"subintervals.")
left_riemann_sum = np.sum(0.5 * arr * arr*np.tan(dx)) #0.5 * b * h
print("Left Riemann Sum Triangle:",left_riemann_sum/1000000)
left_riemann_sum = np.sum(np.pi * arr**2 * dx/(2*np.pi)) #pi*r^2
print("Left Riemann Sum Part of Circle:",left_riemann_sum/1000000)
perimetro = np.sum(arr*np.tan(dx))
print("Perimetro Triangle: ", perimetro/1000)
perimetro = np.sum(2*np.pi*arr*(dx/(2*np.pi)))
print("Perimetro Circle: ", perimetro/1000)
#left_riemann_sum = np.sum(np.pi * arr**2 * dx/(2*np.pi)) #0.5 * b * h
#print("Left Riemann Sum Triangle2:",left_riemann_sum/1000000)
#print("Left Riemann Sum Triangle:",left_riemann_sum/1000000)
#left_riemann_sum = np.sum(np.pi * arr**2 * dx/(2*np.pi)) #0.5 * b * h


#width=[(x[j+1]-x[j]).days for j in range(len(x)-1)] + [30])

#plt.subplot(2,1,2)
#plt.plot(x_down, y_down,'o')

#x_left = x[:-1] # Left endpoints
#y_left = y[:-1]
#plt.plot(x_left,y_left,'b.',markersize=10)
#plt.bar(x_left,y_left,width=(b-a)/N,alpha=0.2,align='edge',edgecolor='b')
plt.show()