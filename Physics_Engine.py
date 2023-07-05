from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
import time
from random import uniform
from math import sqrt
from itertools import combinations




dt=0.01
Width=500
Height=500
window_size=(Width,Height)
World='Closed'
screen=pygame.display.set_mode(window_size)
pygame.display.set_caption('2D Physics Engine')

def Distance(p1, p2):
    return sqrt((p1.Position[0]-p2.Position[0])**2+(p1.Position[1]-p2.Position[1])**2)

def Force(p):
    return [0,2000]

class Particle():
    def __init__(self, position, velocity, mass, radius):
        self.Position=position
        self.Velocity= velocity
        self.M=mass
        self.R=radius
    def Move(self):
        F=Force(self)
        for d in range(2):
            self.Velocity[d]+=0.5*F[d]*dt/self.M
        for d in range(2):
            self.Position[d]+=self.Velocity[d]*dt
        F=Force(self)
        for d in range(2):
            self.Velocity[d]+=0.5*F[d]*dt/self.M
        
        X, Y= self.Position
        Vx, Vy= self.Velocity
        
        
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
        
        
        self.Position=[X,Y]
        self.Velocity=[Vx, Vy]
        
        
        

def Draw_Window():
    
    screen.fill('white')
    for p in System:
        pygame.draw.circle(screen, 'blue', p.Position, p.R)
    
    pygame.display.update()

def Colision(p1,p2):
    n=[p1.Position[d]-p2.Position[d] for d in range(2)]
    aux=0
    for d in range(2): aux+=n[d]*(p2.Velocity[d]-p1.Velocity[d])
    c=2.0*aux/((n[0]**2+n[1]**2)*(1.0/p1.M+1.0/p2.M))
    
    p1.Velocity=[p1.Velocity[d]+c/p1.M*n[d] for d in range(2)]
    p2.Velocity=[p2.Velocity[d]-c/p2.M*n[d] for d in range(2)]

def Next_Step():
    for p in System:
        p.Move()
    
    for comb in combinations(System, 2):
        if Distance(comb[0], comb[1])<(comb[0].R+comb[1].R):
            Colision(comb[0],comb[1])
    Draw_Window()



if __name__ == "__main__":
    System=[Particle([uniform(0,250),uniform(0,250)],[uniform(-50,50),uniform(-10,10)],10,10) for i in range(20)]
    while True:
        start=time.process_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        Next_Step()
        finish=time.process_time()
        if (finish-start<dt): time.sleep(dt-(finish-start))
    