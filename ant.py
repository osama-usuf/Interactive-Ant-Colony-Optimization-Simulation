from random import *
from math import sqrt

class Ant:
    speed = 2 #global variables - bound globally to corresponding sliders
    erratic = 0.15
    comRate = 5 #ants communicate thru pheromones after every 50 frames by default [times 10 for slider]
    def __init__(self,map,x,y):
        self.map = map
        self.img = [loadImage('images/antWalk_00.png'),
                    loadImage('images/antWalk_01.png'),
                    loadImage('images/antWalk_02.png'),
                    loadImage('images/antWalk_03.png')]
        self.noFrame = len(self.img)
        self.dir = PVector(-1,-1) #direction vector/velocity
        self.pos = PVector(x,y)
        self.friction = 0
        self.frame = 0
        self.counter=0 #counter for animation
        self.pastPositions = [self.pos.copy()] #All positions ants remember, fixed at 10, list of vectors
        self.pastDir = [self.dir.copy()] #corresponding past directions
        self.memory = 25
        self.debug = False
        self.radius = 32 #ant body radius
        self.blocked = False
        #ant is by default looking for food
        self.prePostTask = 'cave'
        self.currTask = 'food'
        self.cargo = False #false means ant isn't carrying food, true means food is being carried
        self.comRadius = 64*2 #ant sight radius - radius in which ants will try to avoid/locate surfaces
        self.FOV =  radians(45) #ant FOV - in radians - fixed at 45 degrees - increase if direction keeps inverting after block
        self.maxTimeSeen = -1
        self.lastTimeSeen = {'food':-1,'cave':-1}
        self.phrmnWrite = True
        self.phrmnTime = -1

    def move(self):
        #unblocking ant
        if (self.blocked):
            new_pos = self.map.getPassable(self.pos)
            self.pos = PVector(new_pos[0]*64,new_pos[1]*64)
            self.blocked = False
        
        self.cellAction()
    
        #updating position based on velocity/dir OR pheromone [if deposited]
        cell = self.getCell()

        #pheromone handling - reading + deposit?
        mapX = int(self.pos[0] // 64)
        mapY = int(self.pos[1] // 64)
        
        #scan neighbor grid for relevant pheromones
        #ants communicate after every 20 frames
        if (mapX > 0 and mapX < 14 and mapY > 0 and mapY < 9): #excluding boundary line - try removing this and adding mod to mapX,mapY
            task = self.currTask
            if (frameCount % int(self.comRate*10) == 0):
                for i in self.map.gridScan:
                    cell = self.map.cells[mapX+i[0]][mapY+i[1]]
                    pheromInfoSeen = cell.pheromInfo
                    myInterest = pheromInfoSeen[task]
                    if (myInterest['time'] > self.maxTimeSeen and myInterest['where'] != PVector(0,0)):
                        self.maxTimeSeen = myInterest['time']
                        self.dir = PVector(i[0],i[1]).sub(myInterest['where']).normalize() #either use this or the one below
                        #self.dir = PVector.mult(myInterest['where'].normalize(),-1)

        #deposit pheromones if in drop mode
        if (mapX > 0 and mapX < 14 and mapY > 0 and mapY < 9): #excluding boundary line - try removing this and adding mod to mapX,mapY
            if (self.phrmnWrite):
                cell = self.map.cells[mapX][mapY]
                pheromInfoSeen = cell.pheromInfo
                for name,time in self.lastTimeSeen.items():
                    interest = pheromInfoSeen[name]
                    if (time > interest['time'] and cell.type != 'colony' and cell.type != 'food'):
                        cell.pheromInfo[name]['time'] = time
                        cell.pheromInfo[name]['where'] = self.pastDir[0].copy().normalize()
            if (frameCount >= self.phrmnTime):
                self.disablePhrmnWrite()
        
        #applying actions on ant based on comRadius/ant sight
        self.collisionAvoid()
        
        #randomness + move
        self.pos.add(self.speed*self.dir*(1-self.friction))
        self.dir.rotate(self.erratic/10 * random() -(self.erratic*0.05))
        
        #memorizing past Positions, fixed queue
        if(len(self.pastPositions) < self.memory):
            self.pastPositions.append(self.pos.copy())
            self.pastDir.append(self.dir.copy())
        else:
            self.pastPositions.pop(0)
            self.pastPositions.append(self.pos.copy())
            self.pastDir.pop(0)
            self.pastDir.append(self.dir.copy())
            
        #checking blockage
        if (self.getCell().type == 'obstacle'):
            self.blocked = True
            self.pastPositions = [self.pastPositions[0]]
            self.pastDir = [self.pastDir[0]]        
            
    def getCell(self,pos=PVector(0,0)): #detect cell on which ant is on #try to remove all mods
        if(pos==PVector(0,0)):
            mapX = int(self.pos[0] // 64) % 15
            mapY = int(self.pos[1] // 64) % 10
        else:
            mapX = int(pos[0] // 64) % 15
            mapY = int(pos[1] // 64) % 10
        return self.map.cells[mapX][mapY]
    
    def collisionAvoid(self):
        ahead = self.dir.copy().mult(self.comRadius/2) #remove / 2 in original implementation, see performance
        new_pos = PVector(self.pos[0]+ahead.x,ahead.y+self.pos[1])
        nTry = 0
        if (self.getCell(new_pos).type == 'obstacle'):
            #possible collision, check left or right and move a/c
            right = self.dir.copy().rotate(self.FOV).mult(self.comRadius/2)
            right =  PVector(self.pos[0]+right.x,right.y+self.pos[1])
            left = self.dir.copy().rotate(-self.FOV).mult(self.comRadius/2)
            left =  PVector(self.pos[0]+left.x,left.y+self.pos[1])
            lType = self.getCell(left).type
            rType = self.getCell(right).type
            if (rType != 'obstacle'):#right is free
                self.dir.rotate(self.FOV)
            elif (lType  != 'obstacle'):#left is free
                self.dir.rotate(-self.FOV)
            elif (nTry <= 5): #both blocked - attempt left turn
                self.dir.rotate(-self.FOV)
                nTry += 1
            else:
                self.blocked = True
        pass
    
    def cellAction(self):
        #Boundary collision - simply invert direction
        if(self.map.inMap(self.pos[0]+16,self.pos[1]+16) == False):
            self.dir = PVector.mult(self.dir,-1).normalize()

        cell = self.getCell()
        cellType = cell.type
        if(cellType == 'grass'):
            self.friction = 0.6
        elif(cellType == 'obstacle'):
            ##implement map.fixTraped
            self.dir = PVector.mult(self.dir,-1).normalize()
        elif(cellType == 'ground'):
            #for smoothness, decreasing friction gradually
            if(self.friction>0):
                self.friction-=0.01
            else:
                self.friction = 0
        elif(cellType == 'food'):
            if(self.currTask == 'food' and not self.cargo): #ant has taken food, deduct food from cell + add to ant:
                self.cargo = True
            self.maxTimeSeen = 0
            self.taskFound('food')
                    
        elif(cellType == 'colony'):
        #phrmns
            if(self.currTask == 'cave' and self.cargo): #ant has food, brought back to colony
                self.cargo = False
            self.maxTimeSeen = 0
            self.taskFound('cave')

    def taskFound(self,taskDone):
        self.dir = PVector.mult(self.dir,-1).normalize()
        self.lastTimeSeen[taskDone] = frameCount
        self.pastPositions = [self.pos]
        self.pastDir = [self.dir]
        if (taskDone == 'cave'):
            self.currTask, self.prePostTask = 'food', taskDone
        else:
            self.currTask, self.prePostTask = 'cave', taskDone
        self.enablePhrmnWrite(self.memory*7)   

            
    def disablePhrmnWrite(self): #disable phrmn writing for passed no. of frames
        self.maxTimeSeen = -1
        self.phrmnWrite = False
        self.lastTimeSeen = {'food':-1,'cave':-1}
        
    def enablePhrmnWrite(self,memSize):
        self.phrmnWrite = True
        self.phrmnTime = frameCount + memSize
        
    def draw(self):
        with pushMatrix():
            translate(self.pos[0],self.pos[1])#translate origin to ant center
            rotate(self.dir.heading())#rotate a/c to ant direction           
            noStroke()
            fill(250,250,20)
            if (self.cargo): #render food particle if ant is loaded i.e. if cargo is full
                circle(self.dir.x+8,self.dir.y,8)
            image(self.img[self.frame],-16,-16)
            
            if (self.debug): #draw ant communication radius
                stroke(0,0,255)
                noFill()
                circle(0,0,self.comRadius)
                fill(0,0,255)
                line(0,0,self.dir.x,self.dir.y)

            self.counter += 1
            if (self.counter % 5 == 0):
                self.frame = (self.frame + 1) % self.noFrame
                
        with pushMatrix():
            if(self.debug):#draw ant oldest past position [10]
                translate(self.pastPositions[0][0],self.pastPositions[0][1])
                stroke(0,0,255)
                fill(0,0,255)
                circle(0,0,5)
                
