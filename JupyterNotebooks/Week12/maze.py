import random
from pyamaze import maze, agent


# create a maze, with 7 rows and 7 columns, using the pyamaze library
#
# the CreateMaze() function takes in a parameter called loopPercent
# which is the percentage of cells that will be looped through
# to create a maze. The default value is 70%. You can change it
# to 0% or 100% to see the difference.
#
# the CreateMaze() function also takes in a parameter called
# loopType which can be either "DFS" or "Prim". The default
# value is "DFS". You can change it to "Prim" to see the
# difference.
#
# the CreateMaze() function also takes in a parameter called
# seed which is the random seed used to generate the maze.
# You can change it to any integer value to see the
# difference.
#
# the CreateMaze() function also takes in a parameter called
# start which is the starting cell of the maze. You can
# change it to any tuple value to see the difference.
#
column = 7
rows = 7
m = maze(rows, column)
m.CreateMaze(loopPercent=70)

# create an agent (the guy who is trying to navigate the
# maze), with the maze and the starting cell
# the agent is created with a default shape of a circle
# and a default color of red
#
a = agent(m, filled=True, footprints=True, shape="arrow")
# m.tracePath({a:m.path})
# print(m.maze_map)

# Call the maze_map attribute of the maze object to get
# the maze map. The maze map is a dictionary of dictionaries.
# The keys of the outer dictionary are the cells of the maze.
# The values of the outer dictionary are the inner dictionaries.
# The keys of the inner dictionary are the directions (N, S, E, W)
# from the cell. The values of the inner dictionary are the
# walls (0) or openings (1) in the direction from the cell.
#
# Personally, I think that is a pretty awesome data structure!!!!
#
direction = m.maze_map


# Okay, now we can start the genetic algorithm!
#
# The genetic algorithm will try to find a path from the
# starting cell to the ending cell of the maze.

# The genetic algorithm will use a population of 400
pop_size = 400

# Create some lists to store the population, the paths,
# the number of obstacles, the number of steps, and the
# number of turns for each individual in the population
#
# The population is a list of lists. Each individual in
# the population is a list of cells that the agent will
# visit to get from the starting cell to the ending cell.

population = []
path = []
no_of_obstacles = []
no_of_steps = []
no_of_turn = []

# Create a list to store the final path, the final number
# of obstacles, the final number of steps, and the final
# number of turns for the best individual in the population

final_obstacle = []
final_turn = []
final_steps = []
final_fitness = []

def generatepop():
    for i in range(pop_size):
        popu = []
        popu.append(1)
        for j in range(1, column-1):
            individual = random.randint(1, rows)
            popu.append(individual)
        popu.append(rows)
        population.append(popu)
    # for i in population:
    #     print(i)

def mutation():
    for i in population:
        i[random.randint(1, column-2)] = random.randint(1, rows)

def cross_over():
    
    for i in range(0, pop_size//2, 2):

        cutpoint = random.randint(1, len(population)-1)

        parent1 = population[i]
        parent2 = population[i+1]
        child1 = parent1[:cutpoint] + parent2[cutpoint:]
        child2 = parent2[:cutpoint] + parent1[cutpoint:]
        population[(pop_size//2)+i] = child1
        population[(pop_size//2)+(i+1)] = child2


def fitness():
    # paths
    turns()
    for i in population:
        p = []
        for j in range(column-1):
            if i[j+1] - i[j] >= 0:
                for k in range(i[j], i[j+1]+1):
                    p.append((k, j+1))
            if i[j+1] - i[j] < 0:
                for k in range(i[j], i[j+1]-1, -1):
                    p.append((k, j+1))
        p.append((rows, column))
        path.append(p)
        p = 0

    # obstacles
    obs = 0
    for i in path:
        for j in range(len(i)-1):
            if i[j+1][0]-i[j][0] >= 0 and i[j+1][1] == i[j][1]:
                if direction[i[j]]["S"] == 0:
                    obs += 1
            if i[j+1][0]-i[j][0] < 0 and i[j+1][1] == i[j][1]:
                if direction[i[j]]["N"] == 0:
                    obs += 1
            if i[j+1][1]-i[j][1] >= 0 and i[j+1][0] == i[j][0]:
                if direction[i[j]]["E"] == 0:
                    obs += 1
            if i[j+1][1]-i[j][1] < 0 and i[j+1][0] == i[j][0]:
                if direction[i[j]]["W"] == 0:
                    obs += 1
        no_of_obstacles.append(obs)
        obs = 0
    #no of steps 
    for i in path:
        no_of_steps.append(len(i))

    #formulas 
    max_obstacles = max(no_of_obstacles)
    min_obstacles = min(no_of_obstacles)
    max_turn = max(no_of_turn)
    min_turn = min(no_of_turn)
    max_step = max(no_of_steps)
    min_step = min(no_of_steps)

    w_obs = 3
    w_turn = 2
    w_path = 2

    for i in range(pop_size):
        f_obs = 1 - \
            ((no_of_obstacles[i]-min_obstacles)/(max_obstacles-min_obstacles))
        final_obstacle.append(f_obs)
        f_turn = 1 - ((no_of_turn[i]-min_turn)/(max_turn-min_turn))
        final_turn.append(f_turn)
        f_steps = 1 - ((no_of_steps[i]-min_step)/(max_step-min_step))
        final_steps.append(f_steps)
        final_fitness.append(
            (100*w_obs*f_obs) * (((w_path * f_steps) + (w_turn * f_turn)) / (w_path + w_turn)))

def turns():
    for i in population:
        turn = 0
        for j in range(0, column-2):
            if i[j] != i[j+1]:
                turn += 1
        no_of_turn.append(turn)
        turn = 0

def sorting():
    for i in range(pop_size - 1):
        for j in range(i+1 , pop_size):
            if final_fitness[j] > final_fitness[i]:
                population[i] , population[j] = population[j], population[i]
                final_fitness[i] , final_fitness[j] = final_fitness[j],final_fitness[i]
    
    print("After Parenting")
    for i in range(pop_size):
        print(f"{population[i]}        {final_fitness[i]:.2f}")

dictionary = {}
def solution():
    sol = []
    for i in range(pop_size):
        if final_fitness[i] > 0 and no_of_obstacles[i] == 0:
            sol=(path[i])
            for j in range(len(sol)-1):
                dictionary.update({sol[j+1]:sol[j]})
            return 1
    return 0

# Main Function

generatepop()
i = 0
while True:
    i+=1
    fitness()
    if solution():
        print(f"Solution found in iteration = {i}")
        m.tracePath({a:dictionary})
        m.run()
        break

    sorting()
    cross_over()
    mutation()

    # turn = []
    # print(no_of_obstacles)
    # print(no_of_steps)
    # print(no_of_turn)
    # print(path)
    
    path = []
    no_of_obstacles = []
    no_of_steps = []
    no_of_turn = []

    final_obstacle = []
    final_turn = []
    final_steps = []
    final_fitness = []
