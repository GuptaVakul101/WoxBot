import random
import statistics
from time import sleep

from arena import arena

ROBOTS_LIST = []
NUM_ROBOTS = 64
CHROMOSOME_LENGTH = 512
CHROMOSOME_BITS_TO_MUTATE = 32
PERCENTAGE_ROBOTS_TO_MUTATE = 10

def constructFSM(chromosome):

    def next_move(i):
        ''' Input is a 4 bit input, It can be from 0....15, extract the 2*i and 2*i + 1 '''
        output = chromosome[2*i:2*i+2]
        return int(output, 2)

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
        timeLivedList = []
        for robot in CURR_ROBOTS:
            fsm = constructFSM(robot)
            timeLived = arena.startLife(fsm, "life")
            timeLivedList.append(timeLived)
            lives.append((timeLived, robot))
            print("Robot #", robot, " Time Lived: ", timeLived)
            sleep(2)
        lives.sort()
        N = len(lives)
        mean = statistics.mean(timeLivedList)
        median = statistics.median(timeLivedList)
        print("Generation: ", generation)
        print("Mean: ", mean)
        print("Median: ", median)
        robotsData[generation] = lives
        CURR_ROBOTS = [robot for _, robot in lives[N // 2:N]]
        mutateRobots(CURR_ROBOTS)
        generation += 1
    print("Final Living Robot:")
    print(CURR_ROBOTS)

if __name__ == '__main__':
    main()
