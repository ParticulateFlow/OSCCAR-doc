# predefine strings
headerOF  = '/*--------------------------------*- C++ -*----------------------------------*\\\n'
headerOF += '| =========                 |                                                 |\n'
headerOF += '| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n'
headerOF += '|  \\    /   O peration     | Version:  2.1.x                                 |\n'
headerOF += '|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n'
headerOF += '|    \\/     M anipulation  |                                                 |\n'
headerOF += '\*---------------------------------------------------------------------------*/\n'
headerOF += 'FoamFile\n'
headerOF += '{\n'
headerOF += '\tversion\t\t2.0;\n'
headerOF += '\tformat\t\tascii;\n'
headerOF += '\tclass\t\tdictionary;\n'
headerOF += '\tobject\t\tblockMeshDict;\n'
headerOF += '}\n'
headerOF += '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'
headerOF += '\n\n'

seperator = '\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'

dictStart = '{\n'
dictEnd = '}\n'

listStart = '(\n'
listEnd = ');\n'

newLine = '\n'

new3Line = '\n\n\n'

def beginBlockMeshDict(mywfile):
	mywfile.write(headerOF)
	mywfile.write(newLine)
	mywfile.write(newLine)
	
	mywfile.write("convertToMeters 1.0;\n")

	mywfile.write(newLine)
	mywfile.write(newLine)
# end def

def beginPatch(mywfile, patchName, patchType):
	mywfile.write("\n"+patchName+"\n")
	mywfile.write(dictStart)
	mywfile.write("  " + "type " + patchType + ";\n")
	mywfile.write("  " + "faces\n")
	mywfile.write("  " + listStart)
# end def

def endPatch(mywfile):
	mywfile.write("  " + listEnd)
	mywfile.write(dictEnd+"\n")
# end def




## function definition

def writeCoord(coordRawString):
	tmp = coordRawString.partition('[')
	coordString = tmp[2]
	tmp = coordString.partition(']')
	coordString = tmp[0]
	
	tmp = coordString.partition(',')
	coordString = tmp[0] + tmp[2]
	tmp = coordString.partition(',')
	coordString = tmp[0] + tmp[2]
	
	return "( "+coordString+" )"


def inc(x):
	return x+1


def rotX(alpha, vx):
	rx = [0.0, 0.0, 0.0]
	
	rx[0] = vx[0]
	rx[1] = vx[1]*math.cos(alpha) - vx[2]*math.sin(alpha)
	rx[2] = vx[1]*math.sin(alpha) + vx[2]*math.cos(alpha)
	
	return rx

def rotY(beta, vy):
	ry = [0.0, 0.0, 0.0]
	
	ry[0] = vy[0]*math.cos(beta) + vy[2]*math.sin(beta)
	ry[1] = vy[1]
	ry[2] = -vy[0]*math.sin(beta) + vy[2]*math.cos(beta)
	
	return ry

def rotZ(gamma, vz):
	rz = [0.0, 0.0, 0.0]
	
	rz[0] = vz[0]*math.cos(gamma) - vz[1]*math.sin(gamma)
	rz[1] = vz[0]*math.sin(gamma) + vz[1]*math.cos(gamma)
	rz[2] = vz[2]
	
	return rz

def ex(h):
	return [h, 0.0, 0.0]

def ey(h):
	return [0.0, h, 0.0]

def ez(h):
	return [0.0, 0.0, h]

def xComp(vv):
	return vv[0]

def yComp(vv):
	return vv[1]

def zComp(vv):
	return vv[2]

def addVectors(vv1, vv2):
    return [vv1[0]+vv2[0], vv1[1]+vv2[1], vv1[2]+vv2[2]]

def subtractVectors(vv1, vv2):
    return [vv1[0]-vv2[0], vv1[1]-vv2[1], vv1[2]-vv2[2]]

def mul(sc, vv):
	return [sc*vv[0], sc*vv[1], sc*vv[2]]

def mag(vv):
	return math.sqrt(vv[0]**2 + vv[1]**2 + vv[2]**2)

# -----------------------------
# normal and tangential vectors
def en(omegaIn):
	return rotZ(omegaIn, [1.0,0.0,0.0])

def et(omegaIn):
	return rotZ(omegaIn + math.pi/2, [1.0,0.0,0.0])
# -----------------------------





def isContained(searchDictionary, searchCoord):
    for key, coord in searchDictionary.items():
        xEq = False
        yEq = False
        zEq = False
        
        if (math.fabs(searchCoord[0] - coord[0]) < 1e-6 ):
            xEq = True
        # end if
        if (math.fabs(searchCoord[1] - coord[1]) < 1e-6 ):
            yEq = True
        # end if
        if (math.fabs(searchCoord[2] - coord[2]) < 1e-6 ):
            zEq = True
        # end if
        
        if (xEq and yEq and zEq):
            return True
        # end if
    # end for
    
    return False


# pTotal contains a continuous, unique counter
# pWritten contains the points that were written to the vertex list
# registerPoint(pC, pTotal, pWritten, key, counter)
def registerPoint(pointsDictionary, counterDictionary, registerDictonary, key, counter):
    counterDictionary[key] = counter[0]
    counter[0] = inc(counter[0])
    registerDictonary[key] = pointsDictionary[key]
    #print 'registering point ' + key + ' as ' + str(counter[0]) + 'th point'


# a0h1 = 0.0; b3h1 = 0.0, pTotal[a0h1] = 23, get 23 for key b3h1
# registerDuplicatePoint(pC, pTotal, key)
def registerDuplicatePoint(pointsDictionary, counterDictionary, dupKey):
    #print " dupKey = " + dupKey
    for key, coord in pointsDictionary.items():
        if ( mag(subtractVectors(coord, pointsDictionary[dupKey])) < 1e-6 ):
        #
        #if (coord == pointsDictionary[dupKey]):
            # avoid double registering a duplicate, i.e. d0h1 as duplicate of d0h1
            if (key != dupKey and key in counterDictionary):
                counterDictionary[dupKey] = counterDictionary[key]
## end function definition

def modifyPointCoordinates(pointsDictionary, modKey, newCoords):
    oldCoords = pointsDictionary[modKey]
    for key, coord in pointsDictionary.items():
        if (coord == oldCoords):
            pointsDictionary[key] = newCoords
        # end if
    # end for
# end function


# ----------------------------------------------
# methods
# ----------------------------------------------



### /*              write block               */ ###
### node labelling wXaYjZ
def writeBlock(lowerNodes, nCells, grading, zone=""):
	
	n1 = lowerNodes[0]
	n2 = lowerNodes[1]
	n3 = lowerNodes[2]
	n4 = lowerNodes[3]
	
	t5 = lowerNodes[0]
	t6 = lowerNodes[1]
	t7 = lowerNodes[2]
	t8 = lowerNodes[3]

	n5 = t5[0:t5.__len__()-1]+str(int(t5[t5.__len__()-1])+1)
	n6 = t6[0:t6.__len__()-1]+str(int(t6[t6.__len__()-1])+1)
	n7 = t7[0:t7.__len__()-1]+str(int(t7[t7.__len__()-1])+1)
	n8 = t8[0:t8.__len__()-1]+str(int(t8[t8.__len__()-1])+1)
	
	nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
	
	#print ("nodes: " + str(nodes))
	
	return writeFullBlock(nodes, nCells, grading, zone)
### /*              write block               */ ###


### /*              write full block               */ ###
def writeFullBlock(nodes, nCells, grading, zone=""):
	global blockCount
	blockString = "hex "
	
	n1 = nodes[0]
	n2 = nodes[1]
	n3 = nodes[2]
	n4 = nodes[3]
	
	n5 = nodes[4]
	n6 = nodes[5]
	n7 = nodes[6]
	n8 = nodes[7]
	
	blockString += "( " + str(pTotal[n1]) + " " + str(pTotal[n2]) + " " + str(pTotal[n3]) + " " + str(pTotal[n4])
	blockString += " " + str(pTotal[n5]) + " " + str(pTotal[n6]) + " " + str(pTotal[n7]) + " " + str(pTotal[n8]) + " )"
	blockString += " " + zone + " "
	blockString +=  " ( " + str(nCells[0]) + " " + str(nCells[1]) + " " + str(nCells[2]) + " )"
	blockString += " simpleGrading"
	blockString +=  " ( " + str(grading[0]) + " " + str(grading[1]) + " " + str(grading[2]) + " )"
	
	blockString += "  // " + str(blockCount) + " "
	blockCount += 1
	
	return blockString
### /*              write full block               */ ###





### /*              write edge               */ ###
def writeEdge(pk1, pk2, pi=""):
	edgeString = "    arc "
	
	edgeString += str(pTotal[pk1]) + " "
	edgeString += str(pTotal[pk2]) + " "
	if (pi == ""):
		edgeString += writeCoord(str(piC[pk1]))
	else:
		# key of interpolation point passed
		edgeString += writeCoord(str(piC[pi]))
	# end if
	
	return edgeString
### /*              write edge               */ ###



### /*              write fullFace               */ ###
def writeFullFace(faceNodes):
	faceString = "( "
	
	# loop over passed node keys
	for nn in faceNodes:
	    faceString += str(pTotal[nn]) + " "
	# end for

	faceString += ")"
	
	return faceString
### /*              write fullFace               */ ###
