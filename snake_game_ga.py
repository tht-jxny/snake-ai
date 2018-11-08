import pygame as game
import random, copy
from ga import *
from neuralNetwork_API import *

height = 800
width =  800
rezolution = 10
fps = 10
populationSize = random.randint(1,10000)
savedSnakes = []
snakes = []
bestSnakesOfEachGen = []

def nextGeneration():
    global savedSnakes,snakes
    print("New Generation")
    calcFitness()
    for i in range(populationSize-3):
        snakes.append(pickOne())
    savedSnakes = []
    return snakes

def pickOne():
    global savedSnakes, currentGen,highscore
    index = 0
    r = random.uniform(0.0,1.0)

    while (r > 0 and index <99):
        r = r - savedSnakes[index].fitness
        index += 1
    parent = savedSnakes[index-1]
    bestSnakesOfEachGen.append(parent)
    if currentGen > 350 or highscore > 300:
        filename =  "genData/best_of_all.npy"
        parent.brain.saveNetwork(filename)
    filename =  "genData/best_of_gen_"+str(currentGen) +".npy"
    parent.brain.saveNetwork(filename)
    child = Snake(parent.brain)
    child.brain.mutate(0.01)
    return child

def calcFitness():
    global savedSnakes
    sum = 0
    for snake in savedSnakes:
        sum += snake.score
    for snake in savedSnakes:
        snake.fitness = snake.score / sum


class Snake:

    def __init__(self,brain):
        self.score = 1
        self.body = []
        x = random.randint(0,width/rezolution)
        y = random.randint(0,height/rezolution)
        x *= rezolution
        y *= rezolution
        if x == width:
            x-=rezolution
        if y == height:
            y -= rezolution
        if y == height:
            y -= rezolution
        if x == 0:
            x+= rezolution
        if y == 0:
            y += rezolution
        self.body.append([x,y])
        self.xdir = 1
        self.ydir = 0
        self.food = [width/2+rezolution/2,height/2+rezolution/2+60]
        self.newFood()
        if type(brain)!= int:
            self.brain = copy.copy(brain)
        else:
            self.brain = neuralNetwork(12,20,5,0.2)
        self.lastDecisions = []
        self.fitness = 0

    def grow(self):
        self.score += 1
        global fps
        head = copy.copy(self.body[len(self.body) -1 ])
        self.body.append(head)
        fps *= 1.1

    def eat(self):
        x = self.body[len(self.body) -1][0]
        y = self.body[len(self.body) -1][1]
        if (x == self.food[0] and y == self.food[1]):
            self.grow()
            return True
        return False

    def think(self):
        inputs = getInputArray(self,width,height)
        outputs = self.brain.query(inputs)
        decision = np.argmax(outputs)
        self.lastDecisions.append(decision)
        if (len(self.lastDecisions)>4 and decision == self.lastDecisions[-5]):
            if decision != 4:
                decision += 1
            else:
                decision = 0
        if decision == 0:
                self.setDir(-1,0) #go left
        elif decision == 1:
                self.setDir(1,0) #go right
        elif decision == 2:
                self.setDir(0,-1) #go up
        elif decision == 3:
                self.setDir(0,1) #go down
        elif decision == 4:
                nothing = 1 #stay in direction
        else:
                print("Error with outputs: ",outputs)

    def endGame(self):
        x = self.body[len(self.body) -1 ][0]
        y = self.body[len(self.body) -1 ][1]
        if (x > width-rezolution/2 or x < 0 or y > height-rezolution/2 or y < 0):
            return True
        for i in range(0,len(self.body)-15):
            part = self.body[i]
            if (part[0]==x and part[1] == y):
                return True
        return False


    def draw(self):
        for i in range(len(self.body)):
            game.draw.rect(window, game.Color(120,120,120),(self.body[i][0],self.body[i][1],rezolution,rezolution))


    def setDir(self,x,y):
        self.xdir = x
        self.ydir = y

    def update(self):
        head = copy.copy(self.body[len(self.body)-1])
        self.body.remove(self.body[0])
        head[0] += self.xdir * rezolution
        head[1] += self.ydir * rezolution
        self.body.append(head);

    def newFood(self):
        x = random.randint(0,width/rezolution)
        y = random.randint(0,height/rezolution)
        x *= rezolution
        y *= rezolution

        if x == width:
            x-=rezolution
        if y == height:
            y -= rezolution

        self.food = [x,y]
        if (self.food in self.body):
            self.newFood()

    def showFood(self):
        game.draw.rect(window, (100,0,0),(self.food[0],self.food[1],rezolution,rezolution))

game.init()
for i in range(populationSize):
    snakes.append(Snake(5))
window =   game.display.set_mode((height,width))
clock = game.time.Clock()
game.display.set_caption("Snake Game")
myfont = game.font.SysFont("Comic Sans MS", 30)
currentGen = 1

cols = int(width/rezolution)
rows = int(height/rezolution)
highscore = 0

i = 0
run = True

while run:
    if currentGen  > 355:
        run = False
    clock.tick(fps)

    if currentGen  == 15:
        fps = 10

    textsurface = myfont.render("highest Score: "+str(highscore), False, (255,255,255))

    window.fill((50,50,50))
    for snake in snakes:
        snake.think()
        if (snake.eat()):
            snake.newFood()
        snake.draw()
        if i %2 == 0 :
            snake.update()
        snake.update()
        snake.showFood()
        if snake.score> highscore:
            highscore = snake.score
        if snake.endGame() :
            savedSnakes.append(snake)
            snakes.remove(snake)

    for y in range(rows):
        y *= rezolution
        for x in range(cols):
            x *= rezolution
            game.draw.line(window,(0,0,0),(x,y),(x+rezolution,y),rezolution/10)
            game.draw.line(window,(0,0,0),(x+rezolution,y),(x+rezolution,y+rezolution),rezolution/10)
            game.draw.line(window,(0,0,0),(x+rezolution,y+rezolution),(x,y+rezolution),rezolution/10)
            game.draw.line(window,(0,0,0),(x,y+rezolution),(x,y),rezolution/10)

    for y in range(rows):
        y *= rezolution
        for x in range(cols):
            x *= rezolution
            game.draw.line(window,(0,0,255),(x,y),(x+rezolution,y),rezolution/10)
            game.draw.line(window,(0,0,255),(x+rezolution,y),(x+rezolution,y+rezolution),rezolution/10)
            game.draw.line(window,(0,0,255),(x+rezolution,y+rezolution),(x,y+rezolution),rezolution/10)
            game.draw.line(window,(0,0,255),(x,y+rezolution),(x,y),rezolution/10)

    if (currentGen < 100 and len(snakes) < 3):
        snakes = []
        snakes = nextGeneration()
        currentGen += 1


    textsurface2 = myfont.render("Gen: "+str(currentGen),False, (255,255,255))
    window.blit(textsurface,(width-rezolution*50,height/20))
    window.blit(textsurface2,(0+rezolution*3,height/20))

    game.display.update()
    i += 1
game.quit()
