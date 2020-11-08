import random
import statistics
from time import sleep

from arena import arena
from matplotlib import pyplot as plt
import numpy as np

ROBOTS_LIST = []
NUM_ROBOTS = 64
CHROMOSOME_LENGTH = 192
CHROMOSOME_BITS_TO_MUTATE = 5
PERCENTAGE_ROBOTS_TO_MUTATE = 1
PERFORMANCE_MEANS = []
PERFORMANCE_MEDIANS = []

def plotList(y, label=None):
    x = np.arange(1, len(y)+1)
    plt.clf()
    plt.xlabel("Generations")
    plt.xticks(x)
    if label is not None:
        plt.ylabel(label)
    plt.plot(x, y)
    plt.savefig("Plot_" + label + ".png")


def constructFSM(chromosome):
    random_choices = [random.randint(1, 5), random.randint(1, 5)]

    def next_move(i):
        ''' Input is a 6 bit input, It can be from 0....63, extract the 3*i, 3*i + 1 and 3*i + 2 '''
        output = chromosome[3*i:3*i+3]
        int_output = int(output, 2)
        if int_output > 5:
            int_output -= 5
            int_output = random_choices[int_output]
        return int_output

    return next_move  # FUNCTION OBJECT

def generateRandomBinaryString(N: int):
    s = ""
    for i in range(N):
        toAdd = str(random.randint(0, 1))
        s = s + toAdd
    return s

def flipBit(c):
    if c == '0':
        return '1'
    else:
        return '0'

def mutateChromosome(chromosome):
    BITS_MUTATION_LIST = random.sample(range(len(chromosome)), CHROMOSOME_BITS_TO_MUTATE)
    for i in BITS_MUTATION_LIST:
        newChromosome = chromosome[0:i] + flipBit(chromosome[i])
        if i != (len(chromosome) - 1):
            newChromosome = newChromosome + chromosome[i + 1:]
        chromosome = newChromosome

    return chromosome

def mutateRobots(robots):
    N = len(robots)
    numberToMutate = round(PERCENTAGE_ROBOTS_TO_MUTATE * N)
    ROBOTS_MUTATION_LIST = random.sample(range(N), numberToMutate)
    for i in ROBOTS_MUTATION_LIST:
        robots[i] = mutateChromosome(robots[i])

def main():
    for i in range(NUM_ROBOTS):
        chromosome = generateRandomBinaryString(CHROMOSOME_LENGTH)
        ROBOTS_LIST.append(chromosome)

    CURR_ROBOTS = ROBOTS_LIST
    robotsData = {}
    generation = 1
    while len(CURR_ROBOTS) != 1:
        lives = []
        performanceList = []
        for robot in CURR_ROBOTS:
            fsm = constructFSM(robot)
            performance = arena.startLife(fsm)
            performanceList.append(performance)
            lives.append((performance, robot))
            print("Robot #", robot, " Time Lived: ", performance)
            sleep(2)
        lives.sort()
        N = len(lives)
        mean = statistics.mean(performanceList)
        median = statistics.median(performanceList)
        print("Generation #", generation)
        print("Mean of Performance: ", mean)
        print("Median: ", median)
        robotsData[generation] = lives
        CURR_ROBOTS = [robot for _, robot in lives[N // 2:N]]
        mutateRobots(CURR_ROBOTS)
        PERFORMANCE_MEANS.append(mean)
        PERFORMANCE_MEDIANS.append(median)
        generation += 1
    print("Final Living Robot:")
    print(CURR_ROBOTS)
    plotList(PERFORMANCE_MEDIANS, 'Medians')
    plotList(PERFORMANCE_MEANS, "Mean")


if __name__ == '__main__':
    main()
