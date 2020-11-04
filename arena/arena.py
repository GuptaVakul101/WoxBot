import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

from arena.constants import *
from arena.cube import *
from arena.pyramid import *
from arena.wall import *
from NeuralNetwork import NeuralNetwork
from time import sleep
from PIL import Image
import numpy as np
import math
import cv2

cube_dict = {}
pyramid_dict = {}
global_cube = []
global_pyramid = []

ground_vertices = ((-GROUND_X_LENGTH / 2, -ROBOT_HEIGHT, GROUND_Z_LENGTH / 2),
                   (GROUND_X_LENGTH / 2, -ROBOT_HEIGHT, GROUND_Z_LENGTH / 2),
                   (GROUND_X_LENGTH / 2, -ROBOT_HEIGHT, -GROUND_Z_LENGTH / 2),
                   (-GROUND_X_LENGTH / 2, -ROBOT_HEIGHT, -GROUND_Z_LENGTH / 2))


def Ground():
    glBegin(GL_QUADS)
    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0, 1, 1))
        glVertex3fv(vertex)
    glEnd()


def startLife(fsm):
    arena()
    return random.randint(0,500)


def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def change_life(life, x, z):
    for (cube_x, cube_z) in global_cube:
        if dist(x, z, cube_x, cube_z) <= RADIUS:
            life -= LIFE_FACTOR
    for (pyr_x, pyr_z) in global_pyramid:
        if dist(x, z, pyr_x, pyr_z) <= RADIUS:
            life += LIFE_FACTOR
    return life

def arena():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, 2, 0.1, 150.0)
    glTranslatef(0, 0, 0)
    x_move = 0
    y_move = 0
    z_move = 0
    x = 0
    z = 0
    direction = 0
    _cameraAngle = 0

    for x in range(NUM_CUBES):
        new_vertices, x_value, z_value = setCubeVertices()
        cube_dict[x] = new_vertices
        global_cube.append((x_value, z_value))

    for x in range(NUM_PYRAMIDS):
        new_vertices, x_value, z_value = setPyramidVertices()
        pyramid_dict[x] = new_vertices
        global_pyramid.append((x_value, z_value))

    life = INITIAL_LIFE
    for i in range(0, MAX_TIME):
        if life < MIN_LIFE:
            pygame.quit()
            return i

        # read the colour buffer
        pixels = glReadPixels(0, 0, 800, 600,
                                 GL_RGB, GL_UNSIGNED_BYTE)
        # convert to PIL image
        image = Image.frombytes('RGB', (800, 600), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        pil_image = image.convert('RGB')
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        # cv2.imshow('window1', open_cv_image)
        # cv2.waitKey(0)
        yellow_code = NeuralNetwork(open_cv_image, [0, 255, 255])
        red_code = NeuralNetwork(open_cv_image, [0, 0, 255])
        code = (yellow_code<<2) + red_code

        # next_state = next_move(code)
        next_state = 1

        if next_state == 0:
            print('Turn left')
            _cameraAngle += 270
            _cameraAngle %= 360
            direction += 1
            direction %= 4
        elif next_state == 1:
            print('Go straight ahead')
            pass
        elif next_state == 2:
            print('Turn right')
            _cameraAngle += 90
            _cameraAngle %= 360
            direction += 3
            direction %= 4
        elif next_state == 3:
            print('Go backwards')
            _cameraAngle += 180
            _cameraAngle %= 360
            direction += 2
            direction %= 4

        if direction == 0:
            z_move = MOVE_SIZE
            z += MOVE_SIZE
        elif direction == 1:
            x_move = MOVE_SIZE
            x += MOVE_SIZE
        elif direction == 2:
            z_move = -MOVE_SIZE
            z -= MOVE_SIZE
        elif direction == 3:
            x_move = -MOVE_SIZE
            x -= MOVE_SIZE

        glClear((GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT))
        glTranslatef(x_move, y_move, z_move)
        glRotatef(_cameraAngle, 0.0, 1.0, 0.0)
        _cameraAngle = 0
        x_move = 0
        z_move = 0

        Ground()
        Walls()
        for cube in cube_dict:
            Cubes(cube_dict[cube])
        for pyramid in pyramid_dict:
            Pyramids(pyramid_dict[pyramid])

        life = change_life(life, x, z)
        print('Current life', life)

        pygame.display.flip()

    pygame.quit()
    return MAX_TIME
