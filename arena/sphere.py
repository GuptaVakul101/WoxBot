import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from arena.constants import *

def setSphereVertices():
    x_value_change = random.randrange(-OBST_X_LENGTH + SPHERE_RADIUS, OBST_X_LENGTH - SPHERE_RADIUS)
    z_value_change = random.randrange(-OBST_Z_LENGTH + SPHERE_RADIUS, OBST_Z_LENGTH - SPHERE_RADIUS)
    return (x_value_change, z_value_change)

def Spheres(new_vertices, color):
    (x_value, z_value) = new_vertices
    glTranslatef(x_value, 0, z_value)
    sphere = gluNewQuadric()
    (R, G, B) = color
    glColor3f(R, G, B)
    gluSphere(sphere, SPHERE_RADIUS, SPHERE_SLICES, SPHERE_STACKS)
    glTranslatef(-x_value, 0, -z_value)
