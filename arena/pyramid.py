import random
from OpenGL.GL import *
from arena.constants import *

pyramidVertices = ((-PYRAMID_SIDE / 2, -PYRAMID_SIDE / 2, (PYRAMID_SIDE * 1.732) / 6),
                   (PYRAMID_SIDE / 2, -PYRAMID_SIDE / 2, (PYRAMID_SIDE * 1.732) / 6),
                   (0, -PYRAMID_SIDE / 2, -(PYRAMID_SIDE * 1.732) / 3),
                   (0, PYRAMID_SIDE - PYRAMID_SIDE / 2, 0))

pyramidEdges = ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3))

pyramidSurfaces = ((0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3))

pyramidColors = ((1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0))


def Pyramid():
    x = 0
    glBegin(GL_TRIANGLES)
    for surface in pyramidSurfaces:
        for vertex in surface:
            x += 1
            glColor3fv(pyramidColors[x])
            glVertex3fv(pyramidVertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in pyramidEdges:
        for vertex in edge:
            glVertex3fv(pyramidVertices[vertex])
    glEnd()


def setPyramidVertices():
    x_value_change = random.randrange(-GROUND_X_LENGTH + PYRAMID_SIDE, GROUND_X_LENGTH - PYRAMID_SIDE)
    y_value_change = 0
    z_value_change = random.randrange(-GROUND_Z_LENGTH + PYRAMID_SIDE, GROUND_Z_LENGTH - PYRAMID_SIDE)
    new_vertices = []
    for vert in pyramidVertices:
        new_vert = []
        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        new_vertices.append(new_vert)
    return new_vertices, x_value_change, z_value_change


def Pyramids(new_vertices):
    glBegin(GL_TRIANGLES)
    for surface in pyramidSurfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(pyramidColors[x])
            glVertex3fv(new_vertices[vertex])
    glEnd()
