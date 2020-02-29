class Button:
    buttonCount = 0
    buttonSpacing = 48
    def __init__(self,label,bg):
        self.label = label
        self.id = Button.buttonCount+1
        self.w = 130
        self.h = 32
        self.bg = bg
        self.x = bg[0] + (bg[2]-self.w)/2
        self.y = bg[1] + (Button.buttonCount+0.5)*Button.buttonSpacing
        Button.buttonCount += 1
        self.pressed = False
        self.color = [50,95,149]

    def draw(self):
        stroke(0)
        if(self.mouseHover() or self.pressed):
            fill(27,52,82)
        else:
            fill(*self.color)
        #Create Button
        rect(self.x,self.y,self.w,self.h)
        #Label button
        fill(255)
        textSize(12)
        textAlign(CENTER, CENTER);
        text(self.label, self.x + self.w/2, self.y + self.h/2)
        
    def mouseHover(self):#executed only after a click has occured on-screen
        return (mouseX >= self.x and mouseX <= (self.x + self.w) and mouseY >= self.y and mouseY <= (self.y + self.h))
