#borrowed from: https://github.com/hackingmath/python-sliders/blob/master/slider.py
from button import Button
from ant import Ant
from cell import Cell

class Slider:
    sliderCount = 0
    def __init__(self,label,low,high,default,bg):
        '''slider has range from low to high
        and is set to default'''
        self.low = low
        self.high = high
        self.val = default
        self.clicked = False
        self.label = label #blank label
        self.bg = bg
        self.x = bg[0] + (bg[2]-120)/2
        if(Slider.sliderCount==0):
            self.y = bg[1] + (Button.buttonCount+1)*Button.buttonSpacing
            Slider.sliderCount  = Button.buttonCount 
        else:
            self.y = bg[1] + (Slider.sliderCount+1)*Button.buttonSpacing
        self.rectx = self.x + map(self.val,self.low,self.high,0,120)
        self.recty = self.y - 10
        Slider.sliderCount += 1
    def draw(self):
        '''updates the slider and returns value'''
        #gray line behind slider
        strokeWeight(4)
        stroke(200)
        line(self.x,self.y,self.x + 120,self.y)
        #press mouse to move slider
        if mousePressed and dist(mouseX,mouseY,self.rectx,self.recty) < 20:
            self.rectx = mouseX
        #constrain rectangle
        self.rectx = constrain(self.rectx, self.x, self.x + 120)
        #draw rectangle
        strokeWeight(1)
        stroke(0)
        fill(255)
        rect(self.rectx,self.recty,15,20)
        self.val = map(self.rectx,self.x,self.x + 120,self.low,self.high)
        #draw label
        fill(0)
        textSize(12)
        text(int(self.val),self.rectx+8,self.recty+8)
        #text label
        fill(255,255,255)
        text(self.label,self.x+60,self.y+20)
        if(self.label=='Ant Speed'):
            Ant.speed = self.val
        elif(self.label=='Evap. Rate'):
            Cell.evapRate = self.val
        elif(self.label=='Ant Randomness'):
            Ant.erratic = self.val
        elif(self.label=='Communication Rate'):
            Ant.comRate = self.val
