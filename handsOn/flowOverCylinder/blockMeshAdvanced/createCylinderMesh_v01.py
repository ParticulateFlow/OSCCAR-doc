#!/usr/bin/env python

import os
import shutil
import sys
import math

from operator import add

#execfile('libMagicMesh.py') # incompatible with python 3
exec(open('libMagicMesh.py').read())

# it's alive

# ----------------------------------------------------------------------------
# Captains log
#	nothing so far



# ----------------------------------------------------------------------------



# ----------------------------------------------
# input section
# ----------------------------------------------





# main dimensions
D = 0.05
L = 2.5
W = 1.0
C = 0.4

dx = 0.015
dy = 0.015
dr = 0.015


H = 0.01

doSingleCell = True
doSingleCell = False

doCurvedEdges = False
doCurvedEdges = True

doPatches = False
doPatches = True

doCylinderWallLayer = True


heights = list()
heights.append(0.0)
heights.append(H)


xCoords = list()
xCoords.append(0.0)
xCoords.append(C-0.25*W)
xCoords.append(C)
xCoords.append(C+0.25*W)
xCoords.append(L)


yCoords = list()
yCoords.append(-0.5*W)
yCoords.append(-0.25*W)
yCoords.append(0.0)
yCoords.append(0.25*W)
yCoords.append(0.5*W)


radiusCylinder = list()
radiusCylinder.append(0.5*D)
if (doCylinderWallLayer):
    radiusCylinder.append(0.5*D+0.5*(0.25*W+0.5*D))
radiusCylinder.append(0.25*W*math.sqrt(2.0))


xIndices = list(range(0, xCoords.__len__(), 1))
yIndices = list(range(0, yCoords.__len__(), 1))
zIndices = list(range(0, heights.__len__(), 1))

radIndices = list(range(0, radiusCylinder.__len__(), 1))

X_IN = 0
X_OUT = xCoords.__len__()-1

Y_LO = 0
Y_UP = yCoords.__len__()-1


print("foo")
print(X_IN)
print(X_OUT)
print(Y_LO)
print(Y_UP)

CYL_LEVEL_X1 = xCoords.index(C-0.25*W)
CYL_LEVEL_X2 = xCoords.index(C+0.25*W)
CYL_LEVEL_Y1 = yCoords.index(-0.25*W)
CYL_LEVEL_Y2 = yCoords.index(0.25*W)

CYL_LAYER_RAD = -1
if (doCylinderWallLayer):
    CYL_LAYER_RAD = radiusCylinder.index(0.5*D)


# do not touch
# -------------------
NN = 8;

dAngleDeg = int(360/NN)
dAngle = dAngleDeg*math.pi/180.0
anglesDeg = list(range(0, 360, dAngleDeg))
offsetAngleDeg = 0

angles = list(range(0, NN))
iAngles = list(range(0, NN))
indices = list(range(0, NN, 1))

for i in range(0,anglesDeg.__len__()):
    angles[i] = float(anglesDeg[i] + offsetAngleDeg)*math.pi/180.0
    iAngles[i] = (float(anglesDeg[i] + offsetAngleDeg)+float(dAngleDeg)/2.0)*math.pi/180.0
# end for

for i in range(0,anglesDeg.__len__()):
    anglesDeg[i] = angles[i]*180.0/math.pi
# end for


print (anglesDeg)



# ----------------------------------------------
# compute cell numbers
# ----------------------------------------------



nX = list()
for j in range(0, xCoords.__len__()-1):
	nX.append( max(1, int( (xCoords[j+1] - xCoords[j])/dx) ) )
# end for

nY = list()
for j in range(0, yCoords.__len__()-1):
	nY.append( max(1, int( (yCoords[j+1] - yCoords[j])/dy) ) )
# end for

nZ = list()
for j in range(0, heights.__len__()-1):
	#nZ.append( max(1, int( (heights[j+1] - heights[j])/dz) ) )
	nZ.append(1)
# end for


nRad = list()
for j in range(0, radiusCylinder.__len__()-1):
	nRad.append( max(1, int( (radiusCylinder[j+1] - radiusCylinder[j])/dr) ) )
# end for

if (doCylinderWallLayer):
    nRad[CYL_LAYER_RAD] = int(nRad[CYL_LAYER_RAD]*2.8)

print( 'printing radiusCylinder + nRad')
print( radiusCylinder)
print( nRad)

# ----------------------------------------------
# compute vertex coordinates
# ----------------------------------------------



# point coordinates
pC = {}
piC = {}
p3C = {}
pCduplicate = {}

key2 = 'none'

# -------------------
# channel body
for i in xIndices:
    for j in yIndices:
        for k in zIndices:
            key = 'x'+str(i)+'y'+str(j)+'z'+str(k)
            
            pC[key] = [xCoords[i], yCoords[j], heights[k]]
            
            
            # cylinder block
            for l in indices:
                keyA = chr(ord('a')+radIndices.__len__()-1)+str(l)+'h'+str(k)
                xKey = int((CYL_LEVEL_X1 + CYL_LEVEL_X2)/2) + int(math.sqrt(2)*math.sin(math.pi*((l+2)%NN)/4))
                yKey = int((CYL_LEVEL_Y1 + CYL_LEVEL_Y2)/2) + int(math.sqrt(2)*math.sin(math.pi*l/4))
                
                if (i == xKey and j == yKey):
                    pC[keyA] = pC[key]
            # end for
            
        # end for
    # end for
# end for


# -------------------
# cylinder block
for k in zIndices:
    for l in indices:
        for m in radIndices[0:radIndices.__len__()]:
            key = chr(ord('a') + m)+str(l)+'h'+str(k)
            
            if (m < radIndices.__len__()-1):
                piC[key] = addVectors([C, 0.0, heights[k]], rotZ(iAngles[l], [radiusCylinder[m], 0.0, 0.0]))
            
            
            if (m == radIndices.__len__()-1 and l%2 == 0):
                newCoords = addVectors([C, 0.0, heights[k]], rotZ(angles[l], [0.25*W*(0.5*(1+math.sqrt(2.0))), 0.0, 0.0]))
                modifyPointCoordinates(pC, key, newCoords)
            else:
                pC[key] = addVectors([C, 0.0, heights[k]], rotZ(angles[l], [radiusCylinder[m], 0.0, 0.0]))
            # end if
        # end for
    # end for
# end for

# ----------------------------------------------
# some evil global variables
blockCount = 0

# ----------------------------------------------
# set up IO
# ----------------------------------------------

#filename = './constant/polyMesh/blockMeshDict'
filename = './system/blockMeshDict'
mywfile = open(filename,'w')



# ----------------------------------------------
# write blockMeshDict

beginBlockMeshDict(mywfile) # kindly provided by libMagicMesh


# ----------------------------------------------

counter = [0]
pTotal = {}
pWritten = {}

# write points
mywfile.write("vertices\n")
mywfile.write(listStart)


for i in xIndices:
    for j in yIndices:
        for k in zIndices:
            key = 'x'+str(i)+'y'+str(j)+'z'+str(k)
            
            if (not isContained(pWritten, pC[key])):
                print('  writing ' +key)
                registerPoint(pC, pTotal, pWritten, key, counter)
                mywfile.write("\t"+writeCoord(str(pC[key]))+"\t // "+key+" = "+str(pTotal[key])+"\n")
            else:
                print('  duplicate ' +key)
                registerDuplicatePoint(pC, pTotal, key)
            # end if
        # end for
    # end for
# end for

mywfile.write(newLine)

# -------------------
# cylinder block
for k in zIndices:
    for l in indices:
        for m in radIndices:
            key = chr(ord('a') + m)+str(l)+'h'+str(k)
            
            if (not isContained(pWritten, pC[key])):
                print('  writing ' +key)
                registerPoint(pC, pTotal, pWritten, key, counter)
                mywfile.write("\t"+writeCoord(str(pC[key]))+"\t // "+key+" = "+str(pTotal[key])+"\n")
            else:
                print('  duplicate ' +key)
                registerDuplicatePoint(pC, pTotal, key)
        # end if
    # end for
# end for

mywfile.write(listEnd)
mywfile.write(newLine)
# ----------------------------------------------




#print pTotal


mywfile.write(new3Line)


# ----------------------------------------------

grading = [1, 1, 1]
nCells = [2, 2, 1]

# create blocks
mywfile.write("blocks\n")
mywfile.write(listStart)


for i in xIndices[0:xIndices.__len__()-1]:
    for j in yIndices[0:yIndices.__len__()-1]:
        for k in zIndices[0:zIndices.__len__()-1]:
            
            # stopper
            if (i >= CYL_LEVEL_X1 and i < CYL_LEVEL_X2 and j >= CYL_LEVEL_Y1 and j < CYL_LEVEL_Y2):
                continue
            
            key1 = 'x'+str(i)+'y'+str(j)+'z'+str(k)
            key2 = 'x'+str(i+1)+'y'+str(j)+'z'+str(k)
            key3 = 'x'+str(i+1)+'y'+str(j+1)+'z'+str(k)
            key4 = 'x'+str(i)+'y'+str(j+1)+'z'+str(k)
            
            lowerNodes = [key1, key2, key3, key4]
            
            nCells = [nX[i], nY[j], nZ[k]]
            grading = [1, 1, 1]
            
            if (doSingleCell):
                nCells = [1, 1, 1]
            
            mywfile.write("    " + writeBlock(lowerNodes, nCells, grading) + "  " + str(lowerNodes) + "\n")
        # end for
    # end for
# end for

mywfile.write("// cylinder block\n")

for k in zIndices[0:zIndices.__len__()-1]:
    for l in indices:
        
        for m in radIndices[0:radIndices.__len__()-1]:
            key1 = chr(ord('a') + m)+str(l)+'h'+str(k)
            key2 = chr(ord('a') + m+1)+str(l)+'h'+str(k)
            key3 = chr(ord('a') + m+1)+str((l+1)%NN)+'h'+str(k)
            key4 = chr(ord('a') + m)+str((l+1)%NN)+'h'+str(k)
            
            lowerNodes = [key1, key2, key3, key4]
            
            if (l%2 == 0):
                nCells = [nRad[m], nY[CYL_LEVEL_Y1], nZ[k]]
            else:
                nCells = [nRad[m], nX[CYL_LEVEL_X1], nZ[k]]
            # end if
            
            if (doSingleCell):
                nCells = [1, 1, 1]
            
            grading = [1, 1, 1]
            if (doCylinderWallLayer and m == CYL_LAYER_RAD):
                grading = [5, 1, 1]
            
            mywfile.write("    " + writeBlock(lowerNodes, nCells, grading) + "  " + str(lowerNodes) + "\n")
        # end for
    # end for
# end for

mywfile.write(listEnd)
mywfile.write(newLine)
# ----------------------------------------------


mywfile.write(new3Line)



# ----------------------------------------------
# create edges
mywfile.write("edges\n")
mywfile.write(listStart)


if (doCurvedEdges):
    # -------------------
    # cylinder block
    for k in zIndices:
        for l in indices:
            for m in radIndices[0:radIndices.__len__()]:
                key1 = chr(ord('a') + m)+str(l)+'h'+str(k)
                key2 = chr(ord('a') + m)+str((l+1)%NN)+'h'+str(k)
                
                if (piC.__contains__(key1)):
                    mywfile.write(writeEdge(key1, key2, key1) + "// cyl block\n")
                


mywfile.write(listEnd)
mywfile.write(newLine)
# ----------------------------------------------


mywfile.write(new3Line)


# ----------------------------------------------
# create boundaries
mywfile.write("boundary\n")
if (not doPatches):
    mywfile.write(listStart)
    mywfile.write(listEnd)
    mywfile.write(new3Line)
    mywfile.write("banana\n")
# end if
mywfile.write(listStart)

beginPatch(mywfile, "inlet", "patch")

for j in yIndices[0:yIndices.__len__()-1]:
    for k in zIndices[0:zIndices.__len__()-1]:
        
        # stopper
        if (i >= CYL_LEVEL_X1 and i < CYL_LEVEL_X2 and j >= CYL_LEVEL_Y1 and j < CYL_LEVEL_Y2):
            continue
        
        key1 = 'x'+str(X_IN)+'y'+str(j)+'z'+str(k)
        key2 = 'x'+str(X_IN)+'y'+str(j+1)+'z'+str(k)
        key3 = 'x'+str(X_IN)+'y'+str(j+1)+'z'+str(k+1)
        key4 = 'x'+str(X_IN)+'y'+str(j)+'z'+str(k+1)
        
        lowerNodes = [key1, key2, key3, key4]
        
        mywfile.write("    " + writeFullFace(lowerNodes) + "  // " + str(lowerNodes) + "\n")
    # end for
# end for


endPatch(mywfile)
# end patch inlet

beginPatch(mywfile, "outlet", "patch")

for j in yIndices[0:yIndices.__len__()-1]:
    for k in zIndices[0:zIndices.__len__()-1]:
        
        # stopper
        if (i >= CYL_LEVEL_X1 and i < CYL_LEVEL_X2 and j >= CYL_LEVEL_Y1 and j < CYL_LEVEL_Y2):
            continue
        
        key1 = 'x'+str(X_OUT)+'y'+str(j)+'z'+str(k)
        key2 = 'x'+str(X_OUT)+'y'+str(j+1)+'z'+str(k)
        key3 = 'x'+str(X_OUT)+'y'+str(j+1)+'z'+str(k+1)
        key4 = 'x'+str(X_OUT)+'y'+str(j)+'z'+str(k+1)
        
        lowerNodes = [key1, key2, key3, key4]
        
        mywfile.write("    " + writeFullFace(lowerNodes) + "  // " + str(lowerNodes) + "\n")
    # end for
# end for


endPatch(mywfile)
# end patch outlet



beginPatch(mywfile, "cylinder", "wall")

for k in zIndices[0:zIndices.__len__()-1]:
    for l in indices:
        key1 = chr(ord('a'))+str(l)+'h'+str(k)
        key2 = chr(ord('a'))+str((l+1)%NN)+'h'+str(k)
        key3 = chr(ord('a'))+str((l+1)%NN)+'h'+str(k+1)
        key4 = chr(ord('a'))+str(l)+'h'+str(k+1)
        
        lowerNodes = [key1, key2, key3, key4]
        
        mywfile.write("    " + writeFullFace(lowerNodes) + "  // " + str(lowerNodes) + "\n")
    # end for
# end for

endPatch(mywfile)
# end patch cylinder


beginPatch(mywfile, "sides", "patch")

for i in xIndices[0:xIndices.__len__()-1]:
    for k in zIndices[0:zIndices.__len__()-1]:
        
        key1 = 'x'+str(i)+'y'+str(Y_LO)+'z'+str(k)
        key2 = 'x'+str(i+1)+'y'+str(Y_LO)+'z'+str(k)
        key3 = 'x'+str(i+1)+'y'+str(Y_LO)+'z'+str(k+1)
        key4 = 'x'+str(i)+'y'+str(Y_LO)+'z'+str(k+1)
        
        lowerNodes = [key1, key2, key3, key4]
        
        mywfile.write("    " + writeFullFace(lowerNodes) + "  // " + str(lowerNodes) + "\n")
        
        
        key1 = 'x'+str(i)+'y'+str(Y_UP)+'z'+str(k)
        key2 = 'x'+str(i+1)+'y'+str(Y_UP)+'z'+str(k)
        key3 = 'x'+str(i+1)+'y'+str(Y_UP)+'z'+str(k+1)
        key4 = 'x'+str(i)+'y'+str(Y_UP)+'z'+str(k+1)
        
        lowerNodes = [key1, key2, key3, key4]
        
        mywfile.write("    " + writeFullFace(lowerNodes) + "  // " + str(lowerNodes) + "\n")
    # end for
# end for

endPatch(mywfile)
# end patch sides


mywfile.write(listEnd)
mywfile.write(newLine)
# ----------------------------------------------

mywfile.write(new3Line)



# ----------------------------------------------
# write mergePatchPairs dict
mywfile.write("mergePatchPairs\n")
mywfile.write(listStart)
mywfile.write(listEnd)
mywfile.write(newLine)
mywfile.write(newLine)

mywfile.write(seperator)

# finished
mywfile.close()






