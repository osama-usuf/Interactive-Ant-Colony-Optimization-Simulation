from button import Button
from slider import Slider 
class GUI:#resolution is hard-coded for now, can be generalized by adding association to Map
    def __init__(self):
        self.buttons = []
        self.sliders = []
        self.bg = [960,0,160,640] #x,y,w,h
        #Pressable Buttons
        self.buttons.append(Button('Remove Object',self.bg))
        self.buttons.append(Button('Add Obstacle',self.bg))
        self.buttons.append(Button('Add Colony',self.bg))
        self.buttons.append(Button('Add Food',self.bg))
        self.buttons.append(Button('Add Grass',self.bg))
        #Toggle Buttons
        self.buttons.append(Button('Toggle Pheromones',self.bg))
        self.buttons[0].pressed = True #press remove by default
        #Sliders
        self.sliders.append(Slider('Ant Speed',2,6,2,self.bg))
        self.sliders.append(Slider('Evap. Rate',1,10,5,self.bg))
        self.sliders.append(Slider('Ant Randomness',0,4,1,self.bg))
        self.sliders.append(Slider('Communication Rate',1,10,7,self.bg))
        self.tit = 'Ant Colony Optimization\nShortest Path Simulation\n'
        self.crs = 'Computational Intelligence\n'
        self.auth = 'Osama Yousuf - oy02945'
        self.crdt = self.crs+self.tit+self.auth
        
    def draw(self):
        text
        noStroke()
        rectMode(CORNER)
        fill(77,155,247,100)
        rect(*self.bg)
        self.drawElements()
        textSize(11)
        fill(255)
        text(self.crdt,self.bg[0],self.bg[1] + (Slider.sliderCount+1)*Button.buttonSpacing,160,120)
        
    
    def drawElements(self):
        for i in self.buttons:
            i.draw()
        for i in self.sliders:
            i.draw()
            
    def mouseHover(self):
        for i in self.buttons:
            if (i.mouseHover()):
                return i.id
        return None

    def toggleButton(self,id):
        self.buttons[id].pressed = not self.buttons[id].pressed 
        
        
        
