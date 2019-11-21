# Essential in all strategies for optimal movement
import numpy as np


def BFS(agent, enemies, field, considerAgents=True):
    bfsQueue = []

    visitedField = np.full((len(field.uid_map), len(field.uid_map[0])), np.inf)
    visitedField[agent] = 0
    bfsQueue.append(agent)

    while (not len(bfsQueue) == 0):

        currentPoint = bfsQueue.pop(0)

        for point in field.neigh_dict.get(currentPoint):

            if considerAgents:
                isCellEmpty = field.uid_map[point] == 0
            else:
                isCellEmpty = field.uid_map[point] >= 0

            if (isCellEmpty and visitedField[point] > visitedField[currentPoint] + 1):
                bfsQueue.append(point)
                visitedField[point] = visitedField[currentPoint] + 1

    return visitedField

    # More computation but more efficient movement


def makePath(agent, enemies, field, visitedField):
    paths = []
    for enemy in enemies:
        path = []
        stepValue = visitedField[enemy]
        path.append(enemy)
        currentPoint = nextStep = enemy
        nextStepValue = np.inf

        while (not stepValue == 1):
            for point in field.neigh_dict.get(currentPoint):
                if (visitedField[point] < visitedField[currentPoint] and visitedField[point] < nextStepValue):
                    nextStepValue = visitedField[point]
                    nextStep = point

            if (currentPoint == nextStep):  # if path leads nowhere stop condition
                break

            # if ()
            path.append(nextStep)
            currentPoint = nextStep
            stepValue = nextStepValue

        paths.append(path)

    return getShortestPath(paths, visitedField)


def getShortestPath(paths, visitedField):
    minLen = np.inf
    minPath = []

    for path in paths:
        if (len(path) == 0):
            continue
        if (not visitedField[path[-1]] == 1):
            continue
        if (len(path) < minLen):
            minLen = len(path)
            minPath = path

    return minPath
