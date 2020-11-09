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
green_sphere_dict = {}
global_green_sphere = []
dictIDGreenSphere = {}
blue_sphere_dict = {}
global_blue_sphere = []
dictIDBlueSphere = {}
maxMoney = INITIAL_MONEY
maxLife = INITIAL_LIFE

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


def startLife(fsm, perf):
    time = arena(fsm, perf)
    return time


def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def change_money(money, x, z):
    global green_sphere_dict
    global global_green_sphere
    global dictIDGreenSphere
    global blue_sphere_dict
    global global_blue_sphere
    global dictIDBlueSphere

    newGlobalGreenSphere = []
    newGlobalBlueSphere = []
    sum = 0
    for (sphere_x, sphere_z) in global_blue_sphere:
        if dist(x, z, sphere_x, sphere_z) <= RADIUS:
            sum += 1
            money -= random.randint(MONEY_FACTOR - 3, MONEY_FACTOR)

            new_vertices, x_value, z_value = setCubeVertices()
            id = dictIDBlueSphere[(sphere_x, sphere_z)]
            dictIDBlueSphere.pop((sphere_x, sphere_z))
            blue_sphere_dict[id] = new_vertices
            dictIDBlueSphere[(x_value, z_value)] = id

            newGlobalBlueSphere.append((x_value, z_value))
        else:
            newGlobalBlueSphere.append((sphere_x, sphere_z))
    # print("NUMBLUESPHERES ", sum)
    sum = 0
    for (sphere_x, sphere_z) in global_green_sphere:
        if dist(x, z, sphere_x, sphere_z) <= RADIUS:
            sum += 1
            money += random.randint(MONEY_FACTOR - 3, MONEY_FACTOR)

            new_vertices, x_value, z_value = setPyramidVertices()
            id = dictIDGreenSphere[(sphere_x, sphere_z)]
            dictIDGreenSphere.pop((sphere_x, sphere_z))
            green_sphere_dict[id] = new_vertices
            dictIDGreenSphere[(x_value, z_value)] = id

            newGlobalGreenSphere.append((x_value, z_value))
        else:
            newGlobalGreenSphere.append((sphere_x, sphere_z))
    # print("NUMGREENSPHERES ", sum)
    global_green_sphere = newGlobalGreenSphere
    global_blue_sphere = newGlobalBlueSphere

    return money

def change_life(life, x, z):
    global cube_dict
    global pyramid_dict
    global global_cube
    global global_pyramid
    global dictIDCube
    global dictIDPyramid

    newGlobalCube = []
    newGlobalPyramid = []
    sum = 0
    for (cube_x, cube_z) in global_cube:
        if dist(x, z, cube_x, cube_z) <= RADIUS:
            sum += 1
            life -= random.randint(LIFE_FACTOR - 3, LIFE_FACTOR)

            new_vertices, x_value, z_value = setCubeVertices()
            id = dictIDCube[(cube_x, cube_z)]
            dictIDCube.pop((cube_x, cube_z))
            cube_dict[id] = new_vertices
            dictIDCube[(x_value, z_value)] = id

            newGlobalCube.append((x_value, z_value))
        else:
            newGlobalCube.append((cube_x, cube_z))
    # print("NUMCUBES ", sum)
    sum = 0
    for (pyr_x, pyr_z) in global_pyramid:
        if dist(x, z, pyr_x, pyr_z) <= RADIUS:
            sum += 1
            life += random.randint(LIFE_FACTOR - 3, LIFE_FACTOR)

            new_vertices, x_value, z_value = setPyramidVertices()
            id = dictIDPyramid[(pyr_x, pyr_z)]
            dictIDPyramid.pop((pyr_x, pyr_z))
            pyramid_dict[id] = new_vertices
            dictIDPyramid[(x_value, z_value)] = id

            newGlobalPyramid.append((x_value, z_value))
        else:
            newGlobalPyramid.append((pyr_x, pyr_z))
    # print("NUMPYRAMIDS ", sum)
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
    global green_sphere_dict
    global global_green_sphere
    global dictIDGreenSphere
    global blue_sphere_dict
    global global_blue_sphere
    global dictIDBlueSphere
    global maxMoney
    global maxLife

    cube_dict = {}
    pyramid_dict = {}
    global_cube = []
    global_pyramid = []
    dictIDCube = {}
    dictIDPyramid = {}
    green_sphere_dict = {}
    global_green_sphere = []
    dictIDGreenSphere = {}
    blue_sphere_dict = {}
    global_blue_sphere = []
    dictIDBlueSphere = {}
    maxMoney = INITIAL_MONEY
    maxLife = INITIAL_LIFE

def getPerformance(maxLife, maxMoney):
    return ((maxLife * maxMoney) - (INITIAL_LIFE * INITIAL_MONEY))

def arena(fsm, perf):
    global maxLife
    global maxMoney
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
        new_vertices, x_value, z_value = setCubeVertices()
        blue_sphere_dict[i] = new_vertices
        dictIDBlueSphere[(x_value, z_value)] = i
        global_blue_sphere.append((x_value, z_value))

    for i in range(NUM_SPHERES):
        new_vertices, x_value, z_value = setPyramidVertices()
        green_sphere_dict[i] = new_vertices
        dictIDGreenSphere[(x_value, z_value)] = i
        global_green_sphere.append((x_value, z_value))

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
    money = INITIAL_MONEY
    for i in range(0, MAX_TIME):
        if life < MIN_LIFE or money < MIN_MONEY:
            pygame.quit()
            if perf == "life":
                return i
            if perf == "max-money":
                return maxMoney
            if perf == "max-health":
                return maxLife
            if perf == "money-health":
                return getPerformance(maxLife, maxMoney)

        pixels = glReadPixels(0, 0, 800, 600, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes('RGB', (800, 600), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        pil_image = image.convert('RGB')
        open_cv_image = np.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        yellow_code = NeuralNetwork(open_cv_image, [0, 255, 255])
        red_code = NeuralNetwork(open_cv_image, [0, 0, 255])
        green_code = NeuralNetwork(open_cv_image, [0, 255, 0])
        blue_code = NeuralNetwork(open_cv_image, [255, 0, 0])
        code = (green_code<<6) + (blue_code<<4) + (yellow_code<<2) + red_code

        next_state = fsm(code)
        print("ITERATION:", i, end='\t')
        if next_state == 0:
            print('ACTION -> Turn left', end='\t')
            _cameraAngle += 270
            _cameraAngle %= 360
            direction += 1
            direction %= 4
        elif next_state == 1:
            print('ACTION -> Go straight', end='\t')
            pass
        elif next_state == 2:
            print('ACTION -> Turn right', end='\t')
            _cameraAngle += 90
            _cameraAngle %= 360
            direction += 3
            direction %= 4
        elif next_state == 3:
            print('ACTION -> Go backwards', end='\t')
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
        glClear((GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT))
        glTranslatef(x_move, y_move, z_move)
        glRotatef(_cameraAngle, 0.0, 1.0, 0.0)
        _cameraAngle = 0
        x_move = 0
        z_move = 0

        Ground()
        # Walls()
        for cube in cube_dict:
            Cubes(cube_dict[cube], (1,0,0))
        for pyramid in pyramid_dict:
            Pyramids(pyramid_dict[pyramid], (1,1,0))
        for sphere in green_sphere_dict:
            Pyramids(green_sphere_dict[sphere], (0,1,0))
        for sphere in blue_sphere_dict:
            Cubes(blue_sphere_dict[sphere], (0,0,1))

        life = change_life(life, x, z)
        money = change_money(money, x, z)
        life -= 1
        money -= 1
        maxLife = max(maxLife, life)
        maxMoney = max(maxMoney, money)
        # print("x", x)
        # print("z", z)
        print('CURRENT LIFE:', life, end='\t')
        print('CURRENT MONEY:', money)
        # print("Iteration", i)
        sleep(0.1)
        pygame.display.flip()

    pygame.quit()
    if perf == "life":
        return MAX_TIME
    if perf == "max-money":
        return maxMoney
    if perf == "max-health":
        return maxLife
    if perf == "money-health":
        return getPerformance(maxLife, maxMoney)
