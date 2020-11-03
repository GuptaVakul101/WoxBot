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
    cube_dict = {}
    pyramid_dict = {}
    for x in range(NUM_CUBES):
        cube_dict[x] = setCubeVertices()
    for x in range(NUM_PYRAMIDS):
        pyramid_dict[x] = setPyramidVertices()
    object_passed = False
    _cameraAngle = 0
    for i in range(0, MAX_LIFE):
        # image = cv2.transpose(image)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # code = NeuralNetwork(image, [0, 255, 255])
        # print(code)
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
        glClear((GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT))
        glTranslatef(x_move, y_move, 0.1)
        glRotatef(_cameraAngle, 0.0, 1.0, 0.0)
        _cameraAngle = 0
        Ground()
        Walls()
        for cube in cube_dict:
            Cubes(cube_dict[cube])
        for pyramid in pyramid_dict:
            Pyramids(pyramid_dict[pyramid])
        pygame.display.flip()
        if i == 100:
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
            cv2.imshow('window1', open_cv_image)
            cv2.waitKey(0)
            code = NeuralNetwork(open_cv_image, [0, 255, 255])
            print(code)
