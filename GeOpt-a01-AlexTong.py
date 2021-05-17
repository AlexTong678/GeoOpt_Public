"""Provides a scripting component.
    Inputs:
        m: a mesh
        s: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        """

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a

#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

#b = centers

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

#c = angleList

#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

#d = exploded

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!
import Rhino.Geometry as rg 
import rhinoscriptsyntax as rs
import math as math

mesh = m
sunvector = s
angle = a

vectorlist = []
centrelist = []
anglelist =[]
meshlist =[]
meshlist2 = []
meshlist3 = []
spherelist = []
joined_outlines = []

m.FaceNormals.ComputeFaceNormals()
normals = m.FaceNormals

faces = m.Faces

for i in range(m.Faces.Count):
    fc = m.Faces.GetFaceCenter(i)
    vector = rs.CreateVector(normals[i])
    angle = rg.Vector3d.VectorAngle(vector,sunvector)
    vectorlist.append(vector)
    centrelist.append(fc)
    anglelist.append(angle)

mesh2 = rg.Mesh.Duplicate(mesh)
m2 = mesh2

for j in range(len(m2.Faces)):
    m = m2.Faces.ExtractFaces([0])
    meshlist.append(m)

for i in range(len(anglelist)):    
    m = meshlist[i]
    v = vectorlist[i]
    n = rg.Vector3d(0,0,1)
    v1 = v.Rotate(3.14,n)
    m1 = m.Rotate(2*3.14*anglelist[i]/max(anglelist),v,centrelist[i])
    meshlist2.append(m1)

for k in range(len(centrelist)):
    i = 0.15*anglelist[k]/max(anglelist)
    c = rg.Sphere(centrelist[k],i)
    sphere = rg.Mesh.CreateFromSphere(c,10,10)
    spherelist.append(sphere)


#try another one with CreateBooleanDifference but cannot create the hole as intended.

mesh3 = rg.Mesh.Duplicate(mesh)
m3 = mesh3

for j in range(len(m3.Faces)):
    m = m3.Faces.ExtractFaces([0])
    meshlist3.append(m)

for k in range(len(centrelist)):
    c = rg.Sphere(centrelist[k],0.1)
    sphere = rg.Mesh.CreateFromSphere(c,10,10)
    spherelist.append(sphere)


newmesh = rg.Mesh.CreateBooleanDifference(meshlist3,spherelist)

a = vectorlist
b = centrelist
c = anglelist
d = meshlist
e = meshlist2
f = newmesh
