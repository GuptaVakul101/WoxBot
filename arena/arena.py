import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

from arena.constants import *
from arena.cube import *
from arena.pyramid import *
from arena.wall import *
from arena.sphere import *
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
dictIDCube = {}
dictIDPyramid = {}
sphere_dict = {}
global_sphere = []
dictIDSphere = {}

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
    time = arena(fsm)
    return time


def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def change_life(life, x, z):
    global cube_dict
    global pyramid_dict
    global global_cube
    global global_pyramid
    global dictIDCube
    global dictIDPyramid

    newGlobalCube = []
    newGlobalPyramid = []

    for (cube_x, cube_z) in global_cube:
        if dist(x, z, cube_x, cube_z) <= RADIUS:
            life -= LIFE_FACTOR

            new_vertices, x_value, z_value = setCubeVertices()
            id = dictIDCube[(cube_x, cube_z)]
            dictIDCube.pop((cube_x, cube_z))
            cube_dict[id] = new_vertices
            dictIDCube[(x_value, z_value)] = id

            newGlobalCube.append((x_value, z_value))
        else:
            newGlobalCube.append((cube_x, cube_z))

    for (pyr_x, pyr_z) in global_pyramid:
        if dist(x, z, pyr_x, pyr_z) <= RADIUS:
            life += LIFE_FACTOR

            new_vertices, x_value, z_value = setPyramidVertices()
            id = dictIDPyramid[(pyr_x, pyr_z)]
            dictIDPyramid.pop((pyr_x, pyr_z))
            pyramid_dict[id] = new_vertices
            dictIDPyramid[(x_value, z_value)] = id

            newGlobalPyramid.append((x_value, z_value))
        else:
            newGlobalPyramid.append((pyr_x, pyr_z))

    global_cube = newGlobalCube
    global_pyramid = newGlobalPyramid

    return life


def check_location_bounds(x, z):
    if abs(x) >= GROUND_X_LENGTH / 2:
        return False
    if abs(z) >= GROUND_Z_LENGTH / 2:
        return False
    return True

def clearGlobal():
    global cube_dict
    global pyramid_dict
    global global_cube
    global global_pyramid
    global dictIDCube
    global dictIDPyramid

    cube_dict = {}
    pyramid_dict = {}
    global_cube = []
    global_pyramid = []
    dictIDCube = {}
    dictIDPyramid = {}

def arena(fsm):
    clearGlobal()
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

    for i in range(NUM_SPHERES):
        (x_value, z_value) = setSphereVertices()
        sphere_dict[i] = (x_value, z_value)
        dictIDSphere[(x_value, z_value)] = i
        global_sphere.append((x_value, z_value))

    for i in range(NUM_PYRAMIDS):
        new_vertices, x_value, z_value = setPyramidVertices()
        pyramid_dict[i] = new_vertices
        dictIDPyramid[(x_value, z_value)] = i
        global_pyramid.append((x_value, z_value))

    for i in range(NUM_CUBES):
        new_vertices, x_value, z_value = setCubeVertices()
        cube_dict[i] = new_vertices
        dictIDCube[(x_value, z_value)] = i
        global_cube.append((x_value, z_value))

    life = INITIAL_LIFE
    for i in range(0, MAX_TIME):
        if life < MIN_LIFE:
            pygame.quit()
            return i

        pixels = glReadPixels(0, 0, 800, 600, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes('RGB', (800, 600), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        pil_image = image.convert('RGB')
        open_cv_image = np.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        yellow_code = NeuralNetwork(open_cv_image, [0, 255, 255])
        red_code = NeuralNetwork(open_cv_image, [0, 0, 255])
        code = (yellow_code<<2) + red_code

        next_state = fsm(code)

        if next_state == 0:
            # print('Turn left')
            _cameraAngle += 270
            _cameraAngle %= 360
            direction += 1
            direction %= 4
        elif next_state == 1:
            # print('Go straight ahead')
            pass
        elif next_state == 2:
            # print('Turn right')
            _cameraAngle += 90
            _cameraAngle %= 360
            direction += 3
            direction %= 4
        elif next_state == 3:
            # print('Go backwards')
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


        if not check_location_bounds(x, z):
            if abs(x) >= GROUND_X_LENGTH / 2 or abs(z) >= GROUND_Z_LENGTH / 2:
                x_move = -x
                x = 0
                z_move = -z
                z = 0
        # print("x: ", x)
        # print("z: ", z)
        # print("x_move: ", x_move)
        # print("z_move: ", z_move)
        glClear((GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT))
        glTranslatef(x_move, y_move, z_move)
        glRotatef(_cameraAngle, 0.0, 1.0, 0.0)
        _cameraAngle = 0
        x_move = 0
        z_move = 0

        Ground()
        # Walls()
        for cube in cube_dict:
            Cubes(cube_dict[cube])
        for pyramid in pyramid_dict:
            Pyramids(pyramid_dict[pyramid])
        for sphere in sphere_dict:
            Spheres(sphere_dict[sphere])
        
        life = change_life(life, x, z)
        life -= 1
        # print('Current life', life)
        # print("Iteration", i)
        # sleep(0.2)
        pygame.display.flip()

    pygame.quit()
    return MAX_TIME
