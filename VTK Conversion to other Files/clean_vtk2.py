import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from vtk.util.numpy_support import numpy_to_vtk
import matplotlib.pyplot as plt

reader = vtk.vtkPolyDataReader()
reader.SetFileName("cloud.vtk")
reader.Update()
data = reader.GetOutput()

points = data.GetPoints()
npts = points.GetNumberOfPoints()
x = vtk_to_numpy(points.GetData())
#print(x)
#print(x[:,0])
print(x[0])
print(len(x))

points   = vtk.vtkPoints()
vertices = vtk.vtkCellArray()
vtkdepth = vtk.vtkDoubleArray()
vtkdepth.SetNumberOfComponents(1)
vtkdepth.SetName('vtkdepth')

cloud = vtk.vtkPolyData()
cloud.SetPoints( points )
cloud.SetVerts( vertices )
cloud.GetPointData().SetScalars(vtkdepth)
cloud.GetPointData().SetActiveScalars('vtkdepth')

j=0
k=0
for i in x:
    if np.linalg.norm(i) > 4000:
        print("Detected")
        k = k+1
        x = np.delete(x, j, axis=0)
    else:
        depth = np.sqrt(x[j-k, 0]**2 + x[j-k, 1]**2 + x[j-k, 2]**2) # Distancia absoluta desde o LIDAR
        pid = points.InsertNextPoint( x[j-k] )
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(pid)
        vtkdepth.InsertNextValue( depth )

        # update cloud polydata
        points.Modified()
        vertices.Modified()
        vtkdepth.Modified()
        cloud.Modified()

    j = j+1

print(k)
print(len(x))

data = numpy_to_vtk(x)
vtkPts = vtk.vtkPoints()
vtkPts.SetData(data)

polyPtsVTP = vtk.vtkPolyData()
polyPtsVTP.SetPoints(vtkPts)

outputFilename = 'cloud5.vtk'
print ( "Writing:", outputFilename )
writer = vtk.vtkPolyDataWriter()
writer.SetInputData( cloud )
writer.SetFileName( outputFilename )
writer.Write()