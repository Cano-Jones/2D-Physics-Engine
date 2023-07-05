from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
import time
from random import uniform



dt=0.01
Width=500
Height=500
window_size=(Width,Height)
World='Closed'

screen=pygame.display.set_mode(window_size)
pygame.display.set_caption('2D Physics Engine')

class Particle():
    def __init__(self, position, velocity, mass, radius):
        self.Position=position
        self.Velocity= velocity
        self.M=mass
        self.R=radius
    def Move(self):
        X, Y = self.Position
        Vx, Vy = self.Velocity
        
        X+=Vx*dt
        Y+=Vy*dt
        
        
        if World=='Closed':
            if X>Width-self.R:
                X=Width-self.R
                Vx=-Vx
            if X<self.R:
                X=self.R
                Vx=-Vx
            
            if Y>Height-self.R:
                Y=Height-self.R
                Vy=-Vy
            if Y<self.R:
                Y=self.R
                Vy=-Vy
        if World=='Periodic':
            if X>Width:
                X=0
            if X<0:
                X=Width
            
            if Y>Height:
                Y=0
            if Y<0:
                Y=Height
        
        
        self.Position=(X,Y)
        self.Velocity=(Vx, Vy)
        
        
        

def Draw_Window(t):
    
    screen.fill('white')
    for p in System:
        pygame.draw.circle(screen, 'blue', p.Position, p.R)
    
    pygame.display.update()

t=0
System=[Particle((uniform(0,250),uniform(0,250)),(uniform(0,180),uniform(0,180)),10,10) for i in range(10)]
while True:
    start=time.process_time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for p in System:
        p.Move()
    Draw_Window(t)
    
    
    t+=dt
    finish=time.process_time()
    if (finish-start<dt): time.sleep(dt-(finish-start))
    