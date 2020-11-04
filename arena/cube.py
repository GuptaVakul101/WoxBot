import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

from arena.constants import *

cubeVertices = ((CUBE_SIDE / 2, -CUBE_SIDE / 2, -CUBE_SIDE / 2),
                (CUBE_SIDE / 2, CUBE_SIDE / 2, -CUBE_SIDE / 2),
                (-CUBE_SIDE / 2, CUBE_SIDE / 2, -CUBE_SIDE / 2),
                (-CUBE_SIDE / 2, -CUBE_SIDE / 2, -CUBE_SIDE / 2),
                (CUBE_SIDE / 2, -CUBE_SIDE / 2, CUBE_SIDE / 2),
                (CUBE_SIDE / 2, CUBE_SIDE / 2, CUBE_SIDE / 2),
                (-CUBE_SIDE / 2, -CUBE_SIDE / 2, CUBE_SIDE / 2),
                (-CUBE_SIDE / 2, CUBE_SIDE / 2, CUBE_SIDE / 2))

cubeEdges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))

cubeSurfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

cubeColors = (
(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
(1, 0, 0))


def Cube():
    x = 0
    glBegin(GL_QUADS)
    for surface in cubeSurfaces:
        for vertex in surface:
            x += 1
            glColor3fv(cubeColors[x])
            glVertex3fv(cubeVertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in cubeEdges:
        for vertex in edge:
            glVertex3fv(cubeVertices[vertex])
    glEnd()


def setCubeVertices():
    x_value_change = random.randrange(-GROUND_X_LENGTH + CUBE_SIDE, GROUND_X_LENGTH - CUBE_SIDE)
    y_value_change = 0
    z_value_change = random.randrange(-GROUND_Z_LENGTH + CUBE_SIDE, GROUND_Z_LENGTH - CUBE_SIDE)
    new_vertices = []
    for vert in cubeVertices:
        new_vert = []
        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        new_vertices.append(new_vert)
    return new_vertices, x_value, z_value


def Cubes(new_vertices):
    glBegin(GL_QUADS)
    for surface in cubeSurfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(cubeColors[x])
            glVertex3fv(new_vertices[vertex])
    glEnd()
