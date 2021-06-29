import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from vtk.util.numpy_support import numpy_to_vtk
import matplotlib.pyplot as plt

reader = vtk.vtkPolyDataReader()
reader.SetFileName("cloud_quarter.vtk")
reader.Update()
data = reader.GetOutput()

points = data.GetPoints()
npts = points.GetNumberOfPoints()
x = vtk_to_numpy(points.GetData())
#print(x)
#print(x[:,0])
print(x[0])
print(len(x))
j=0
k=0
for i in x:
    if (abs(np.linalg.norm(i)) >= 3500 or abs(np.linalg.norm(i)) <= 10):
        print("Detected")
        k = k+1
        x[j] = [0, 0, 0] 
        #x = np.delete(x, j, axis=0)

    j = j+1

print(k)
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

data = numpy_to_vtk(x)
vtkPts = vtk.vtkPoints()
vtkPts.SetData(data)

polyPtsVTP = vtk.vtkPolyData()
polyPtsVTP.SetPoints(vtkPts)

outputFilename = 'cloud_quarter_clean.vtk'
print ( "Writing:", outputFilename )
writer = vtk.vtkPolyDataWriter()
writer.SetInputData( polyPtsVTP )
writer.SetFileName( outputFilename )
writer.Write()