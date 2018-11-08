#from snake_game_ga import *

def getInputArray(snake,width,height):
    xPosDistToWall = (snake.body[len(snake.body)-1][0] - width) * -1
    yPosDistToWall = (snake.body[len(snake.body)-1][1] - height) * -1
    xNegDistToWall = snake.body[len(snake.body)-1][0]
    yNegDistToWall = snake.body[len(snake.body)-1][1]
    finalArray= [xPosDistToWall,yPosDistToWall,xNegDistToWall,yNegDistToWall]
    xPosDistToBody = 0
    yPosDistToBody = 0
    xNegDistToBody = 0
    yNegDistToBody = 0
    if (len(snake.body)>1):
        for x in range(len(snake.body)-1):
            if (snake.body[x][0] == snake.body[len(snake.body)-1][0]):
                xDist = snake.body[x][1] - snake.body[len(snake.body)-1][1]
                if xDist > 0:
                    xPosDistToBody = xDist
                else:
                    xNegDistToBody = xDist * -1
            if (snake.body[x][1] == snake.body[len(snake.body)-1][1]):
                yDist = snake.body[x][0] - snake.body[len(snake.body)-1][0]
                if yDist > 0:
                    yPosDistToBody = yDist
                else:
                    yNegDistToBody = yDist * -1

    finalArray2 = [xPosDistToBody,yPosDistToBody,xNegDistToBody,yNegDistToBody]
    finalArray += finalArray2
    xPosDistToFood = 0
    yPosDistToFood = 0
    xNegDistToFood = 0
    yNegDistToFood = 0
    xDist = snake.food[0] - snake.body[len(snake.body)-1][0]
    yDist = snake.food[1] - snake.body[len(snake.body)-1][1]
    if xDist > 0:
        xPosDistToFood = xDist
    else:
        xNegDistToFood = xDist * -1
    if yDist > 0:
        yPosDistToFood = yDist
    else:
        yNegDistToFood = yDist * -1
    finalArray2 = [xPosDistToFood,yPosDistToFood,xNegDistToFood,yNegDistToFood]
    finalArray += finalArray2
    for i in range(len(finalArray)):
        finalArray[i] /= 1000.0
        if finalArray[i] == 0.0:
            finalArray[i] = 0.001
    return finalArray

#
# def nextGeneration():
#     global savedSnakes,snakes,populationSize,snake
#     print("New Generation")
#     calcFitness(savedSnakes)
#     for i in range(populationSize):
#         snakes.append(snake())
#     return snakes
#
#
#
# def calcFitness(savedSnakes):
#     global snakes,populationSize,snake
#     sum = 0
#     for snake in savedSnakes:
#         sum += snake.score
#     for snake in snakes:
#         snake.fitness = snake.score / sum
