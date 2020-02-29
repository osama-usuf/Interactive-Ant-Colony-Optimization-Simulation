'''
Computational Intelligence - Assignment 02 - Spring '19

Osama Yousuf - oy02945

Inspiration: 
Ants Colony Simulation AI game experiment 
https://www.youtube.com/watch?v=G5wb4f5n6qQ

Artwork: 
https://github.com/piXelicidio/locas-ants

For a quick demo of this project, refer to the provided
Demo.mp4 file or go to:
https://youtu.be/Dd_HzN8_IzE
'''

from map import Map
from gui import GUI
from cell import Cell

def setup():
    global map,hud,currBtn 
    
    #size(1120,640,P3D) #use this for low quality - good framerate
    size(1120,640,P2D) #use this for higher quality - low framerate
    
    map = Map()
    hud = GUI()
    currBtn = 1 
    numAnts = 100
    map.addAnts(numAnts)

def draw():
    background(0)
    global map,hud,currBtn
    map.draw()
    hud.draw()
    map.update() #update map actors

def mouseClicked():
    global currBtn,map
    #checking button pressed through GUI
    button = hud.mouseHover()
    
    #hud button clicked
    if (button):
        if (button == 6): #toggle pheromones
            map.toggleDebug()
            hud.toggleButton(button-1)
            return

        hud.toggleButton(currBtn-1)
        hud.toggleButton(button-1)
        currBtn = button
        return
    
    #map cell has been clicked, detect and take action based on button
    if (map.inMap(mouseX,mouseY) == False):
        return
    mapX = mouseX // 64
    mapY = mouseY // 64
    
    if (currBtn == 1): #Remove Objects
        map.cells[mapX][mapY].toGround()
    elif (currBtn == 2): #Add Block
        map.cells[mapX][mapY].toBlock()
    elif (currBtn == 3): #Add Colony
        map.cells[mapX][mapY].toCol()
    elif (currBtn == 4): #Add Food
        map.cells[mapX][mapY].toFood()
    elif (currBtn == 5): #Add Grass
        map.cells[mapX][mapY].toGrass()
