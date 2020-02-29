from cell import Cell
from random import *
from ant import Ant
class Map:
    def __init__(self):
        self.ants = []
        self.cols = 15
        self.rows = 10
        self.cells = []
        self.floorOut()
        self.center = 64*self.cols / 2, 64*self.rows / 2
        self.timer = 0 #stores time in seconds since program execution, used for pheromone evaporation - a statically global variable
        # gridScan stores neighbor grids which will be scanned when
        # ants are communicating
        # N N N
        # N C N
        # N N N
        self.gridScan = [[0,0],[-1,-1],[ 0,-1],[ 1,-1],[-1, 0],[ 1, 0],[-1, 1],[ 0, 1],[ 1, 1]]


    def toggleDebug(self): #toggle pheromone display of cells
        for i in self.cells:
            for j in i:
                j.debug = not j.debug
                

    def floorOut(self):#layouts the floorplan of the map
        x_pos = 0
        extreme = [0,self.cols-1,self.rows-1]
        for i in range(self.cols):
            y_pos = 0
            self.cells.append([])
            for j in range(self.rows):
                self.cells[i].append(Cell(x_pos,y_pos))
                y_pos += 64
                rnd = randint(0,99)
                if (rnd < 2):
                    self.cells[i][j].toGrass()
                if (i == 0 or i == self.cols-1 or j == 0 or j == self.rows-1):
                    self.cells[i][j].toBlock()
            x_pos += 64
        self.cells[7][1].toCol()
        self.cells[7][8].toFood()
            
    def draw(self):
        for i in self.cells:#rendering all cells
            for j in i:
                j.draw()
        for i in self.ants:#rendering all ants
            i.draw()
        if (millis() - self.timer*1000 > 1000):
            self.timer += 1
        #Rendering boundary
        noFill()
        stroke(0,0,0,100)        
        rect(64,64,64*(self.cols-2),64*(self.rows-2))
        
    def inMap(self,x,y):#hard-coded for now, should be associated with main for resolution generalization
        return (x >= 20+64 and x <= (64*(self.cols-1)) and y >= 20+64 and y <= (64*(self.rows-1)))
    
    def getPassable(self,pos):#returns [i,j] of first passable cell, first attempts to search in the same row and col
        i = (int(pos[0] // 64) % 13)+1
        j = (int(pos[1] // 64) % 8)+1
        #check immediate neighborhood
        if(self.cells[i][j].type != 'obstacle'):
            return i,j
        elif(self.cells[i-1][j].type != 'obstacle'):
            return i-1,j
        elif(self.cells[i+1][j].type != 'obstacle'):
            return i+1,j
        elif(self.cells[i][j+1].type != 'obstacle'):
            return i,j+1
        elif(self.cells[i][j-1].type != 'obstacle'):
            return i,j-1
        else:
            return self.getPassable((i*64 - 1,j*64 - 1))
        
    def addAnts(self,numAnts):
        for i in range(numAnts):
            ang = random()*6.28
            #spawn ant at random position w/ random angle - FIX bounds
            self.ants.append(Ant(self,60*cos(ang)*2+self.center[0],60*sin(ang)*2+self.center[1])) #ants are spawned in circles - radius hard coded at 60
            self.ants[i].dir = PVector(cos(ang),sin(ang)).normalize()
            #if (i<1): #uncomment to get debug ant[s]
            #    self.ants[i].debug = True
            
    def update(self):
        #move ants
        for i in self.ants:
            i.move()
