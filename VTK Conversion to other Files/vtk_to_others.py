import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import matplotlib.pyplot as plt

def main():
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName("cloud.vtk")
    reader.Update()
    data = reader.GetOutput()

    points = data.GetPoints()
    pointsData = points.GetData()
    npts = points.GetNumberOfPoints()
    array3d = vtk_to_numpy(points.GetData())

    xPoints = array3d[:, 0]
    yPoints = array3d[:, 1]
    zPoints = array3d[:, 2]

    #autocad_points(xPoints, yPoints, zPoints)
    #autocad_lines(xPoints, yPoints, zPoints)
    #file_xyz(xPoints, yPoints, zPoints)
    statistics(npts, xPoints, yPoints, zPoints)

def autocad_points(x, y, z):
    with open('autocad_points1.scr', 'w') as f:
        f.write("_MULTIPLE _POINT\n")
        for i in range(len(x)):
            f.write(f"{x[i]},{y[i]},{z[i]}\n")

def autocad_lines(x, y, z):
    with open('autocad_lines0.scr', 'w') as f:
        f.write("._3DPOLY\n")
        for i in range(len(x)):
            f.write(f"{x[i]},{y[i]},{z[i]}\n")

def file_xyz(x, y, z):
    depth = np.sqrt(x**2 + y**2 + z**2)
    red = []
    green = []
    blue = []
    #print(depth)

    for i in range(len(depth)):
        if depth[i] <= 6000:
            red.append(255-0.0425*depth[i])
            green.append(0.0425*depth[i])
            blue.append(0)
        else:
            red.append(0)
            green.append(255-0.0425*(depth[i]-6000))
            blue.append(0.0425*(depth[i]-6000))
    
    with open('xyz_file3.txt', 'w') as f:
        for i in range(len(depth)):
            f.write(f"{x[i]} {y[i]} {z[i]} {red[i]} {green[i]} {blue[i]}\n")

def statistics(nPoints, x, y, z):
    x0 = []
    y0 = []

   
    rad_r = []

    widthPlot2 = []
    
    # Descobrir pontos da planta
    for i in range(len(z)):
        if z[i] == 0:
            x0.append(x[i])
            y0.append(y[i])

            radian = np.arctan2(x[i], y[i])
            if radian < 0:
                radian = 2*np.pi + radian
                
            ## Para ordernar
            rad_r.append([radian, np.sqrt(x[i]**2 + y[i]**2)])

    x0 = np.array(x0)
    y0 = np.array(y0)
    plt.plot(x0, y0, 'bo')
    plt.figure()

    
    rad_r = sorted(rad_r,key=lambda x: x[0]) # Afinal não é preciso fazer sort

    rad2 = [i[0] for i in rad_r]
    r2 = [i[1] for i in rad_r]

    for i in range(len(rad2)-1):
        widthPlot2.append(rad2[i+1]-rad2[i]) # Constante = 0.00785422

    rad2 = np.array(rad2)
    r2 = np.array(r2)
    rad_mid = (rad2[:-1] + rad2[1:])/2 # Midpoints
    r_mid = (r2[:-1] + r2[1:])/2

    plt.polar(rad2, r2,'o-', markersize=2)
    ax = plt.subplot(111, projection='polar')
    ax.bar(rad_mid, r_mid, width=widthPlot2, bottom=0.0, align='edge', alpha=0.5, edgecolor='g', color='g')

    dx = widthPlot2[0]
    #x_left = np.linspace(0,2*np.pi-dx,len(widthPlot2))

    print("Distancia ao ponto mais distante", np.max(r2))
    hpoint = np.max(z, axis=0)
    print("Maximum height: ", hpoint) # Ponto mais alto

    #print("Partition with",len(widthPlot2),"subintervals.")
    riemann_sum = np.sum(0.5 * r2 * r2*np.tan(dx)) #0.5 * b * h
    print("Riemann Sum Triangle:", riemann_sum/1000000)
    riemann_sum = np.sum(np.pi * r2**2 * dx/(2*np.pi)) #pi*r^2
    print("Riemann Sum Semi Circle:", riemann_sum/1000000)
    perimetro = np.sum(r2*np.tan(dx))
    print("Perimeter Triangle: ", perimetro/1000)
    perimetro = np.sum(2*np.pi*r2*(dx/(2*np.pi)))
    print("Perimeter Circle: ", perimetro/1000)

    plt.show()

if __name__ == '__main__':
    main()