import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

from constants import *

wall1Vertices = ((-GROUND_X_LENGTH/2,0,GROUND_Z_LENGTH/2),
                (-GROUND_X_LENGTH/2,WALL_HEIGHT,GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,WALL_HEIGHT,GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,0,GROUND_Z_LENGTH/2))

wall2Vertices = ((-GROUND_X_LENGTH/2,0,-GROUND_Z_LENGTH/2),
                (-GROUND_X_LENGTH/2,WALL_HEIGHT,-GROUND_Z_LENGTH/2),
                (-GROUND_X_LENGTH/2,WALL_HEIGHT,GROUND_Z_LENGTH/2),
                (-GROUND_X_LENGTH/2,0,GROUND_Z_LENGTH/2))

wall3Vertices = ((-GROUND_X_LENGTH/2,0,-GROUND_Z_LENGTH/2),
                (-GROUND_X_LENGTH/2,WALL_HEIGHT,-GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,WALL_HEIGHT,-GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,0,-GROUND_Z_LENGTH/2))

wall4Vertices = ((GROUND_X_LENGTH/2,0,-GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,WALL_HEIGHT,-GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,WALL_HEIGHT,GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,0,GROUND_Z_LENGTH/2),)

def Walls():
    glBegin(GL_QUADS)
    for i in range(0, 4):
        glColor3fv((0,0,1))
        glVertex3fv(wall1Vertices[i])
    glEnd()

    glBegin(GL_QUADS)
    for i in range(0, 4):
        glColor3fv((0,0,1))
        glVertex3fv(wall2Vertices[i])
    glEnd()

    glBegin(GL_QUADS)
    for i in range(0, 4):
        glColor3fv((0,0,1))
        glVertex3fv(wall3Vertices[i])
    glEnd()

    glBegin(GL_QUADS)
    for i in range(0, 4):
        glColor3fv((0,0,1))
        glVertex3fv(wall4Vertices[i])
    glEnd()
