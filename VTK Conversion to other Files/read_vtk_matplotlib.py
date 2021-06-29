import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import matplotlib.pyplot as plt

reader = vtk.vtkPolyDataReader()
reader.SetFileName("cloud.vtk")
reader.Update()
data = reader.GetOutput()

#sal1 = reader.GetNumberOfPoints()
#sal2 = reader.GetNumberOfCells()

#print(sal1)
#print(sal2)
points = data.GetPoints()
#pointsData = points.GetData()
#print(pointsData)
npts = points.GetNumberOfPoints()
#print(npts)
x = vtk_to_numpy(points.GetData())
#print(x)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#print(x)
#print(x[:,0])

ax.scatter(x[:,0],x[:,1],x[:,2], s=0.1)
ax.set_xlim((-3000, 3000))
ax.set_ylim((-3000, 3000))
ax.set_zlim((-3000, 3000))
#plt.xlim(-1, 1)
#plt.ylim(-1, 1)
#plt.zlim(-1,1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

