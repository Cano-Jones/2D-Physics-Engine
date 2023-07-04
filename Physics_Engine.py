from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
import time



dt=0.1
Width=500
Height=500
window_size=(Width,Height)

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
        
        self.Position=(X,Y)
        
        

def Draw_Window(t):
    
    screen.fill('white')
    pygame.draw.circle(screen, 'blue', p.Position, p.R)
    
    pygame.display.update()

t=0
p=Particle((250,250), (10,10), 10, 20)
while True:
    start=time.process_time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    p.Move()
    Draw_Window(t)
    
    
    t+=dt
    finish=time.process_time()
    if (finish-start<dt): time.sleep(dt-(finish-start))
    