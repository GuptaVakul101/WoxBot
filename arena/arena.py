import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

from constants import *
from cube import *
from pyramid import *
from wall import *

ground_vertices = ((-GROUND_X_LENGTH/2,-ROBOT_HEIGHT,GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,-ROBOT_HEIGHT,GROUND_Z_LENGTH/2),
                (GROUND_X_LENGTH/2,-ROBOT_HEIGHT,-GROUND_Z_LENGTH/2),
                (-GROUND_X_LENGTH/2,-ROBOT_HEIGHT,-GROUND_Z_LENGTH/2))

def Ground():
    glBegin(GL_QUADS)
    x = 0
    for vertex in ground_vertices:
        x+=1
        glColor3fv((0,1,1))
        glVertex3fv(vertex)
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, 2, 0.1, 150.0)
    glTranslatef(0,0,0)
    x_move = 0
    y_move = 0
    cube_dict = {}
    pyramid_dict = {}
    for x in range(NUM_CUBES):
        cube_dict[x] = setCubeVertices()
    for x in range(NUM_PYRAMIDS):
        pyramid_dict[x] = setPyramidVertices()
    object_passed = False
    _cameraAngle = 0
    while not object_passed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 1
                if event.key == pygame.K_RIGHT:
                    x_move = -1
                if event.key == pygame.K_UP:
                    y_move = -1
                if event.key == pygame.K_DOWN:
                    y_move = 1
                if event.key == pygame.K_d:
                    _cameraAngle += 90
                    _cameraAngle %= 360
                if event.key == pygame.K_a:
                    _cameraAngle += 270
                    _cameraAngle %= 360
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_move = 0
                if event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP:
                    y_move = 0
                if event.key == pygame.K_DOWN:
                    y_move = 0
        glClear((GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT))
        glTranslatef(x_move,y_move,0.1)
        glRotatef(_cameraAngle, 0.0, 1.0, 0.0)
        _cameraAngle = 0
        Ground()
        Walls()
        for cube in cube_dict:
            Cubes(cube_dict[cube])
        for pyramid in pyramid_dict:
            Pyramids(pyramid_dict[pyramid])
        pygame.display.flip()

main()
