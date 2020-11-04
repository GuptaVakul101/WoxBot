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
import cv2

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


def arena():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, 2, 0.1, 150.0)
    glTranslatef(0, 0, 0)
    x_move = 0
    y_move = 0
    z_move = 0
    direction = 0
    _cameraAngle = 0

    cube_dict = {}
    pyramid_dict = {}
    for x in range(NUM_CUBES):
        cube_dict[x] = setCubeVertices()
    for x in range(NUM_PYRAMIDS):
        pyramid_dict[x] = setPyramidVertices()

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
            z_move = 1
        elif direction == 1:
            x_move = 1
        elif direction == 2:
            z_move = -1
        elif direction == 3:
            x_move = -1

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

        pygame.display.flip()

    pygame.quit()
    return MAX_TIME
