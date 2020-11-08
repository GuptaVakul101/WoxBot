import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from arena.constants import *

sphereColors = (
(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
(1, 0, 0))


def Sphere():
    x = 0
    glBegin(GL_QUADS)
    for surface in sphereSurfaces:
        for vertex in surface:
            x += 1
            glColor3fv(sphereColors[x])
            glVertex3fv(sphereVertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in sphereEdges:
        for vertex in edge:
            glVertex3fv(sphereVertices[vertex])
    glEnd()


def setSphereVertices():
    x_value_change = random.randrange(-OBST_X_LENGTH + SPHERE_RADIUS, OBST_X_LENGTH - SPHERE_RADIUS)
    z_value_change = random.randrange(-OBST_Z_LENGTH + SPHERE_RADIUS, OBST_Z_LENGTH - SPHERE_RADIUS)
    return (x_value_change, z_value_change)


def Spheres(new_vertices):
    (x_value, z_value) = new_vertices
    for surface in sphereSurfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(sphereColors[x])
            glVertex3fv(new_vertices[vertex])
