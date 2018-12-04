import random, copy
from ga import *
from neuralNetwork_API import *

height = 600
width =  600
rezolution = 10
fps = 60
populationSize = 10000
savedSnakes = []
snakes = []
bestSnakesOfEachGen = []
saveOrNot = 0
def nextGeneration():
    global savedSnakes,snakes,saveOrNot
    for i in range (80):
        snakes.append(Snake(5))
    saveOrNot = 0
    print("New Generation")
    calcFitness()
    for i in range(populationSize-1):
        snakes.append(pickOne())
    savedSnakes = []

def pickOne():
    global savedSnakes, saveOrNot
    parent = savedSnakes[0]
    for snake in savedSnakes:
        if snake.fitness > parent.fitness:
            parent  = snake
    bestSnakesOfEachGen.append(parent)
    if highscore > 300 and save0rNot == 0:
        filename =  "genData/best_of_all.npy"
        parent.brain.saveNetwork(filename)
        filename2 = "genData/best_of_gen"
        x = 0
        for snake in bestSnakesOfEachGen :
            x += 1
            snake.brain.saveNetwork(filename2+str(x)+".npy")

        print("saved best of all")
        run = False

    saveOrNot += 1
    child = Snake(parent.brain)
    child.brain.mutate(0.1)
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
            self.brain = neuralNetwork(8,25,5,0.15)
        self.lastDecisions = []
        self.fitness = 0

    def grow(self):
        self.score += 1
        head = copy.copy(self.body[len(self.body) -1 ])
        self.body.append(head)

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



currentGen = 1

cols = int(width/rezolution)
rows = int(height/rezolution)
highscore = 0

i = 0
run = True

for i in range(populationSize):
    snakes.append(Snake(5))

while run:

    for f in range(fps):
        for snake in snakes:
            snake.think()
            if (snake.eat()):
                snake.newFood()
            if i %2 == 0 :
                snake.update()
            snake.update()
            if snake.score> highscore:
                i = 0
                highscore = snake.score
            if snake.endGame() :
                savedSnakes.append(snake)
                snakes.remove(snake)


        if (len(snakes) < 2):
            snakes = []
            nextGeneration()
            currentGen += 1
            i= 0
            highscore = 0
        if (i>1000): # If snakes are doing nothing special for a long time
            highscore = 0
            i = 0
            snakes = []
            nextGeneration()
            currentGen += 1

        if f == 1:
            print("Highscore:",highscore,"Current Gen:",currentGen)

        i += 1
