import vtk
import os
import sys
import argparse



# Change working directory to allow script to be run from the ParaView shell
datapath = os.path.dirname(os.path.abspath(__file__))
os.chdir(datapath)


# This should allow modules to be imported correctly in the ParaView shell
sys.path.append(datapath)

#from ReadPointsCSV import readPoints
#if using python from pandas, uncomment line below and comment line above
from ReadPoints3 import readPoints
from ReadPoints3 import readPoints_magnitude_scale
from ReadPoints3 import readPoints_earthquake_occurences


parser = argparse.ArgumentParser(description='ExportPoints')
parser.add_argument('--input_file', type=str, default='data_90days.txt')
parser.add_argument('--magnitude', type=int, default=0)
parser.add_argument('--output_file', type=str, default='earthquake.vtk')
parser.add_argument('--occurences', type=int, default=0)


# Change working directory to allow script to be run from the ParaView shell
datapath = os.path.dirname(os.path.abspath(__file__))
os.chdir(datapath)

args = parser.parse_args()

# Read the data in CSV format
filename = args.input_file
magnitude_scaling = args.magnitude
out_vtk = args.output_file
occurences = args.occurences
#points, scalars, tid, depth = readPoints(filename)
#depth_scale = 0.01
depth_scale = 'log'  # modified here

if occurences == 0:
	points, scalars, tid, depth = readPoints_magnitude_scale(file=filename, sep="|", depth_scaling=depth_scale, time_shift=-1467247524, magnitude_scaling=magnitude_scaling)
	scalars.SetName("magnitude")
	tid.SetName("time")
	depth.SetName("depth")
	data = vtk.vtkPolyData()
	data.SetPoints(points)
	data.GetPointData().AddArray(scalars)
	data.GetPointData().AddArray(tid)
	data.GetPointData().AddArray(depth)
	data.GetPointData().SetActiveScalars("magnitude")

else:
	points, scalars = readPoints_earthquake_occurences(file=filename, sep="|", depth_scaling=0.01, quake_number = occurences)
	scalars.SetName("occurences")
	data = vtk.vtkPolyData()
	data.SetPoints(points)
	data.GetPointData().AddArray(scalars)
	data.GetPointData().SetActiveScalars("occurences")


# Write data to VTK legacy format that Paraview can import
writer = vtk.vtkPolyDataWriter()
writer.SetFileName(out_vtk)
writer.SetFileTypeToBinary()
writer.SetInputData(data)
writer.Write()
