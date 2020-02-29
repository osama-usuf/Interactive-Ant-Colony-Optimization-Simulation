#A Cell can have one type at a time, and is rendered accordingly
from map import *

class Cell:
    evapRate = 0.1
    def __init__(self,x,y):
        #Pheromones - each cell stores only the best quality pheromone trail in a specific direction based on visibility against intensity
        self.pheromInfo = { 'food': {'time':-1,'where':PVector(0,0)},
                            'cave': {'time':-1,'where':PVector(0,0)} }
        self.timer = 0
        self.blkImg = 'images/block01.png'
        self.gndImg = 'images/ground01.png'
        self.caveImg = 'images/cave.png'
        self.foodImg = 'images/food.png'
        self.grassImg = 'images/grass01.png'
        self.type = None
        self.img = None
        self.toGround()
        self.pos = x,y
        #Pheromone Color info
        self.color_food = color(255,0,0,128)
        self.color_cave = color(0,0,255,75)
        self.debug = False #will be set true by the map when the show pheromone button is toggled through the GUI
        
    def draw(self):
        image(self.img,self.pos[0],self.pos[1])
        self.evaporate()#evaporates pheromones based on time and evaporation rate
        if (self.debug):
            with (pushMatrix()):
                translate(self.pos[0]+32,self.pos[1]+32)
                #draw food phrmn
                if (self.pheromInfo['food']['where'] != PVector(0,0)):
                    noStroke()
                    fill(self.color_food)
                    circle(0,0,5)
                    stroke(self.color_food)
                    line(0,0,32*self.pheromInfo['food']['where'].x,32*self.pheromInfo['food']['where'].y)
                #draw cave phrm
                if (self.pheromInfo['cave']['where'] != PVector(0,0)):
                    noStroke()
                    fill(self.color_cave)
                    circle(0,0,5)
                    stroke(self.color_cave)
                    line(0,0,32*self.pheromInfo['cave']['where'].x,32*self.pheromInfo['cave']['where'].y)

    def evaporate(self): #evaporate pheromone rendering length i.e. location
        if (millis() - self.timer*1000 > 1000): #shorten pheromone position vectors each second
            self.timer += 1
            #evaporate food phrmns
            self.pheromInfo['food']['where'].limit(self.pheromInfo['food']['where'].mag() - (Cell.evapRate)/100)
            if (self.pheromInfo['food']['where'].mag() < 0.2):
                self.pheromInfo['food']['where'] = PVector(0,0)
                self.pheromInfo['food']['time'] = -1
            #evaporate cave phrmns
            self.pheromInfo['cave']['where'].limit(self.pheromInfo['cave']['where'].mag() - (Cell.evapRate)/100)
            if (self.pheromInfo['cave']['where'].mag() < 0.2):
                self.pheromInfo['cave']['where'] = PVector(0,0)
                self.pheromInfo['cave']['time'] = -1
            pass
    
    def toGround(self):
        self.pheromInfo['cave']['where'] = PVector(0,0)
        self.pheromInfo['cave']['time'] = -1
        self.pheromInfo['food']['where'] = PVector(0,0)
        self.pheromInfo['food']['time'] = -1
        self.type = 'ground'
        self.img = loadImage(self.gndImg)
        
    def toBlock(self):
        self.pheromInfo['cave']['where'] = PVector(0,0)
        self.pheromInfo['cave']['time'] = -1
        self.pheromInfo['food']['where'] = PVector(0,0)
        self.pheromInfo['food']['time'] = -1
        self.type = 'obstacle'
        self.img = loadImage(self.blkImg)
        
    def toCol(self):
        self.type = 'colony'
        self.img = loadImage(self.caveImg)
        self.pheromInfo['cave']['where'] = PVector(0,0)
        self.pheromInfo['cave']['time'] = -1
        self.pheromInfo['food']['where'] = PVector(0,0)
        self.pheromInfo['food']['time'] = -1
        
    def toFood(self):
        self.type = 'food'
        self.img = loadImage(self.foodImg)
        self.pheromInfo['cave']['where'] = PVector(0,0)
        self.pheromInfo['cave']['time'] = -1
        self.pheromInfo['food']['where'] = PVector(0,0)
        self.pheromInfo['food']['time'] = -1

    def toGrass(self):
        self.type = 'grass'
        self.img = loadImage(self.grassImg)
