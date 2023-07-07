from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
from random import uniform
from math import sqrt, atan2, cos, sin, pi
from itertools import combinations, permutations
from numpy.random import choice




dt=0.01
Width=600
Height=600
window_size=(Width,Height)
World='Circle'
Force_Type='FreeFall'
screen=pygame.display.set_mode(window_size)
pygame.display.set_caption('2D Physics Engine')
clock = pygame.time.Clock()

def Distance(p1, p2):
    if World=='Periodic':
        #Distances are different here
        pass
    return sqrt((p1.Position[0]-p2.Position[0])**2+(p1.Position[1]-p2.Position[1])**2)


def Force(p):
    if Force_Type=='None':    return [0,0]
    if Force_Type=='FreeFall': return [0,500*p.M]
    if Force_Type=='Coulomb':
        # If World== Periodic, this has to change
        G=50
        F=[0,0]
        for q in System:
            if q is not p:
                cte=G*p.M*q.M
                R=Distance(p,q)
                F[0]-=cte/R/R*(p.Position[0]-q.Position[0])
                F[1]-=cte/R/R*(p.Position[1]-q.Position[1])
        return F

class Particle():
    def __init__(self, position, velocity, mass=10, radius=10, color='White'):
        self.Position=position
        self.Velocity= velocity
        self.M=mass
        self.R=radius
        self.Color=color
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
        if World=='Circle':
            if (X-Width/2)**2+(Y-Height/2)**2>=(min(Height,Width)/2-self.R)**2:
                Angle=atan2(Y-Height/2,X-Width/2)+pi/2
                X=Width/2+(min(Height,Width)/2-self.R)*cos(Angle-pi/2)
                Y=Height/2+(min(Height,Width)/2-self.R)*sin(Angle-pi/2)
                aux_x=Vx
                aux_y=Vy
                Vx=cos(2*Angle)*aux_x+aux_y*sin(2*Angle)
                Vy=sin(2*Angle)*aux_x-aux_y*cos(2*Angle)
                
                
                
        self.Position=[X,Y]
        self.Velocity=[Vx, Vy]
        
        

def Draw_Window():
    
    screen.fill('white')
    if World=='Closed':
        pygame.draw.line(screen,'gray',[0,0],[Width,0], width=7)
        pygame.draw.line(screen,'gray',[Width,0], [Width, Height], width=7)
        pygame.draw.line(screen,'gray',[0,0],[0,Height], width=7)
        pygame.draw.line(screen,'gray',[0,Height], [Width,Height], width=7)
    if World=='Circle':
        screen.fill('gray')
        pygame.draw.circle(screen, 'white', [Width/2,Height/2], min(Height,Width)/2)
        pygame.draw.circle(screen, 'black', [Width/2,Height/2], min(Height,Width)/2, width=2)
        
    for p in System:
        pygame.draw.circle(screen, p.Color, p.Position, p.R)
    
    pygame.display.update()
    
    

def Particle_Particle_Colision(p1,p2):
    #https://physics.stackexchange.com/questions/599278/how-can-i-calculate-the-final-velocities-of-two-spheres-after-an-elastic-collisi
    
    
    aux=[p1.Position[d]-p2.Position[d] for d in range(2)]
    norm=Distance(Particle(aux,aux),Particle([0,0],aux))
    if norm!=0:
        n_norm=[aux[d]/norm for d in range(2)]
        Delta=(p1.R+p2.R-norm)
    
        p1.Position=[p1.Position[d] + n_norm[d]*Delta*p2.M/(p1.M+p2.M) for d in range(2)]
        p2.Position=[p2.Position[d] - n_norm[d]*Delta*p1.M/(p1.M+p2.M) for d in range(2)]
    
    
    n=[p1.Position[d]-p2.Position[d] for d in range(2)]
    norm=Distance(Particle(n,n),Particle([0,0],n))
    if norm!=0:
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
            Particle_Particle_Colision(comb[0],comb[1])
    
    
    Draw_Window()



if __name__ == "__main__":
    System=[]
    #System=[Particle([uniform(Width*1/3,Width*2/3),uniform(Height/3,Height*2/3)],[uniform(-10,10),uniform(-10,10)],2,3,'skyblue3') for i in range(200)]
    System.append(Particle([Width*2/3, Height/2], [0,0], 30, 30, 'red'))
    System.append(Particle([Width/2,Height/2], [0,0], 20, 20, 'green'))
    System.append(Particle([Width/3,Height/2], [0,0], 15, 15, 'blue'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        Next_Step()
        dt = clock.tick(80)/1000
    