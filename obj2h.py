'''
Created on Sep 1, 2013

@author: Michal Karm Babacek
'''
import sys
import re

"""
Vertices
"""
regexVertices = re.compile("^v ([\-0-9\.]*) ([\-0-9\.]*) ([\-0-9\.]*)$")
"""
Texture coordinates
"""
regexTexCoords = re.compile("^vt ([\-0-9\.]*) ([\-0-9\.]*)$")
"""
Normals
"""
regexNormals = re.compile("^vn ([\-0-9\.]*) ([\-0-9\.]*) ([\-0-9\.]*)$")
"""
TRIANGULATED faces (triangles, not quads...)
                             v1       vt1      vn1
"""
regexFaces = re.compile("^f ([0-9]*)/([0-9]*)/([0-9]*) ([0-9]*)/([0-9]*)/([0-9]*) ([0-9]*)/([0-9]*)/([0-9]*)$")

"""
Used as temporary variables
"""
meshVertices = []
meshNormals = []
meshTexCoords = []
meshFaces = []

def vector3fListToFloatArray(vector3fList):
    floatArray=[]
    for vector3f in vector3fList:
        floatArray.append(vector3f[0])
        floatArray.append(vector3f[1])
        floatArray.append(vector3f[2])
    return floatArray

def vector2fListToFloatArray(vector2fList):
    floatArray=[]
    for vector2f in vector2fList:
        floatArray.append(vector2f[0])
        floatArray.append(vector2f[1])
    return floatArray

if __name__ == '__main__':
    thisScript, objFilePath = sys.argv

    """
    Begin loading obj file and its data...
    """
    objFile = open(objFilePath, "r")
    for line in iter(objFile):
        match = regexVertices.search(line)
        if match is not None:
            meshVertices.append([match.group(1),match.group(2),match.group(3)])
        else:
            match = regexTexCoords.search(line)
            if match is not None:
                meshTexCoords.append([match.group(1),match.group(2)])
            else:
                match = regexNormals.search(line)
                if match is not None:
                    meshNormals.append([match.group(1),match.group(2),match.group(3)])
                else:
                    match = regexFaces.search(line)
                    if match is not None:
                        """
                        A face is actually a list of three vertices.
                        Each of these vertices consists of three components:
                            - the actual x,y,z position represented as an array
                            - texture coordinates u,v as an array of length two
                            - normals represented as an array of length three
                        """
                        meshFaces.append([
                            {'v':meshVertices[int(match.group(1))-1], 't':meshTexCoords[int(match.group(2))-1], 'n':meshNormals[int(match.group(3))-1]},
                            {'v':meshVertices[int(match.group(4))-1], 't':meshTexCoords[int(match.group(5))-1], 'n':meshNormals[int(match.group(6))-1]},
                            {'v':meshVertices[int(match.group(7))-1], 't':meshTexCoords[int(match.group(8))-1], 'n':meshNormals[int(match.group(9))-1]}
                        ])

    """
    Begin conversion from faces to arrays of floats
    """
    vboVertices = []
    vboTextureCoords = []
    vboNormals = []
    vboIndices = []

    counter = 0
    for face in meshFaces:
        for vertex in face:
            vboVertices.append(vertex['v'])
            vboNormals.append(vertex['n'])
            vboTextureCoords.append(vertex['t'])
            vboIndices.append(counter)
            counter += 1

    vboVerticesArray = vector3fListToFloatArray(vboVertices)
    vboTextureCoordsArray = vector2fListToFloatArray(vboTextureCoords)
    vboNormalsArray = vector3fListToFloatArray(vboNormals)

    print "//   Vertices:  %d" % len(vboVerticesArray)
    print "//   Normals:   %d" % len(vboNormalsArray)
    print "//   TexCoords: %d" % len(vboTextureCoordsArray)
    print "//   Indices:   %d" % len(vboIndices)
    print ""
    print "#ifndef _QCAR_HEAD_OBJECT_H_"
    print "#define _QCAR_HEAD_OBJECT_H_"
    print "#define NUM_HEAD_OBJECT_VERTEX %d" % (len(vboVerticesArray)/3)
    print "#define NUM_HEAD_OBJECT_INDEX %d" % len(vboIndices)
    print ""
    print "static const float headVertices[NUM_HEAD_OBJECT_VERTEX * 3] = {%s};" % (', '.join('%-5.6f' % float(v) for v in vboVerticesArray))
    print ""
    print "static const float headNormals[NUM_HEAD_OBJECT_VERTEX * 3] = {%s};" % (', '.join('%-5.6f' % float(v) for v in vboNormalsArray))
    print ""
    print "static const float headTexCoords[%d] = {%s};" % (len(vboTextureCoordsArray), (', '.join('%5.6f' % float(v) for v in vboTextureCoordsArray)))
    print ""
    print "static const unsigned short headIndices[NUM_HEAD_OBJECT_INDEX] = {%s};" % (', '.join('%d' % int(v) for v in vboIndices))
    print ""
    print "#endif // _QCAR_HEAD_OBJECT_H_"
    print ""
