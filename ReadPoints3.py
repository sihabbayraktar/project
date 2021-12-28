#To use this you need to install pandas
#This sccript is more roust to new data and works best with python 3 +

import pandas as pd
import numpy as np
import vtk
from vtk.util import numpy_support
import pandasql as ps


def readPoints(file, sep="|", depth_scaling=0.01, time_shift=-1467247524):
    '''
    df=pd.read_csv(file,sep=sep)
    #df["Magnitude"].isna().values.any()

    df[['Latitude', 'Longitude']]=df[['Latitude', 'Longitude']].clip(lower=0,upper=360)
    df['NewDepth']=df['Depth/Km']*depth_scaling
    df["NewTime"]= pd.to_datetime(df['Time']).values.astype(np.int64) // 10 ** 6

    points=df[['Latitude', 'Longitude', 'NewDepth']].to_numpy()
    times=df["NewTime"].to_numpy()+time_shift
    scalars=df["Magnitude"].to_numpy()
    depth=df["NewDepth"].to_numpy()

    p = vtk.vtkPoints()
    for i in range(points.shape[0]):
        p.InsertNextPoint(points[i,:])
    s = numpy_support.numpy_to_vtk(scalars)
    t = numpy_support.numpy_to_vtk(times)
    d = numpy_support.numpy_to_vtk(depth)

    return p,s,t,d
    '''
    return readPoints_magnitude_scale(file, sep, depth_scaling, time_shift, 0)

def readPoints_magnitude_scale(file, sep="|", depth_scaling=0.01, time_shift=-1467247524, magnitude_scaling=0):
    df = pd.read_csv(file, sep=sep)
    
    if magnitude_scaling != 0:
        df = df[df.apply(lambda x: x["Magnitude"] >= magnitude_scaling, axis=1)]
    
    df[['Latitude', 'Longitude']]=df[['Latitude', 'Longitude']].clip(lower=0,upper=360)
    df['NewDepth']=df['Depth/Km']*depth_scaling
    df["NewTime"]= pd.to_datetime(df['Time']).values.astype(np.int64) // 10 ** 6

    points=df[['Latitude', 'Longitude', 'NewDepth']].to_numpy()
    times=df["NewTime"].to_numpy()+time_shift
    scalars=df["Magnitude"].to_numpy()
    depth=df["NewDepth"].to_numpy()

    p = vtk.vtkPoints()
    for i in range(points.shape[0]):
        p.InsertNextPoint(points[i,:])
    s = numpy_support.numpy_to_vtk(scalars)
    t = numpy_support.numpy_to_vtk(times)
    d = numpy_support.numpy_to_vtk(depth)

    return p,s,t,d


def readPoints_earthquake_occurences(file, sep="|", depth_scaling=0.01, quake_number=1):
    df = pd.read_csv(file, sep=sep)

    #NECESSARY OPERATIONS FOR FILTERING
    df_copy = df.copy()
    df_copy=df_copy.rename(columns={"#EventID": "ID", "Depth/Km": "Depth"})
    df_copy=ps.sqldf("select COUNT(ID) as Count, AVG(Depth) as AvgDepth, Latitude, Longitude, EventLocationName from df_copy group by EventLocationName")

    df_filter = df_copy[df_copy.Count > quake_number]

    df_filter[['Latitude', 'Longitude']]=df_filter[['Latitude', 'Longitude']].clip(lower=0,upper=360)
    df_filter['NewAvgDepth'] = df_filter['AvgDepth']*depth_scaling
    

    points=df_filter[['Latitude', 'Longitude', 'NewAvgDepth']].to_numpy()
    scalars = df_filter["Count"].to_numpy()

    p = vtk.vtkPoints()
    for i in range(points.shape[0]):
        p.InsertNextPoint(points[i,:]) 
 
    s = numpy_support.numpy_to_vtk(scalars)

    return p,s
