"""

"""

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' #Used so no wellcome message from pygame appears
import numpy as np
import pygame
import sys
from itertools import combinations
from math import cos, sin, atan2, pi


class Particle():
    def __init__(self, Position, Velocity, Mass, Radius, Color='blue'):
        self.Position=np.array(Position)
        self.Velocity=np.array(Velocity)
        self.M=Mass
        self.R=Radius
        self.Color=Color
        
    def Move(self):
        self.Velocity=self.Velocity+0.5*Force(self)/self.M*dt
        self.Position=self.Position+self.Velocity*dt
        self.Velocity=self.Velocity+0.5*Force(self)/self.M*dt
        
            
        if World == 'Closed':
            Win=[Width,Height]
            for d in range(2):
                if self.Position[d] > (Win[d]-self.R):
                    self.Position[d] = (Win[d]-self.R)
                    self.Velocity[d]*=-1
                if self.Position[d] < self.R:
                    self.Position[d] = self.R
                    self.Velocity[d]*=-1
                    
        elif World == 'Periodic':
            self.Position=np.remainder(self.Position, np.array([Width, Height]))
        
        elif World == 'Circle':
            [X,Y]=self.Position
            [Vx,Vy]=self.Velocity
            if (X-Width/2)**2+(Y-Height/2)**2>=(min(Height,Width)/2-self.R)**2:
                Angle=atan2(Y-Height/2,X-Width/2)+pi/2
                self.Position[0]=Width/2+(min(Height,Width)/2-self.R)*cos(Angle-pi/2)
                self.Position[1]=Height/2+(min(Height,Width)/2-self.R)*sin(Angle-pi/2)
                self.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
                self.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)
        
def Force(Particle):
    
    if Force_Type == 'None': return np.array([0,0])
    elif Force_Type == 'FreeFall':    return np.array([0,100*Particle.M])
    

def Particle_Particle_Distance(p1,p2):
    return np.linalg.norm(p1.Position-p2.Position)

def Particle_Particle_Collision(p1,p2):
    #https://physics.stackexchange.com/questions/599278/how-can-i-calculate-the-final-velocities-of-two-spheres-after-an-elastic-collisi
    
    aux=p1.Position-p2.Position
    norm=np.linalg.norm(aux)
    
    if norm!=0:
        n_norm=aux/norm
        Delta=(p1.R+p2.R-norm)
        p1.Position=p1.Position + n_norm*Delta*(p2.M/(p1.M+p2.M))
        p2.Position=p2.Position - n_norm*Delta*(p1.M/(p1.M+p2.M))
        
        n=p1.Position-p2.Position
        n_norm=n/np.linalg.norm(n)
        aux=0
        for d in range(2): aux+=n[d]*(p2.Velocity[d]-p1.Velocity[d])
        c=2.0*aux/((n[0]**2+n[1]**2)*(1.0/p1.M+1.0/p2.M))
        
        p1.Velocity=p1.Velocity + n*c/p1.M
        p2.Velocity=p2.Velocity - n*c/p2.M

def Draw_Window():
    screen.fill('white')
    
    if World=='Closed':
        pygame.draw.line(screen,'gray',[0,0],[Width,0], width=7)
        pygame.draw.line(screen,'gray',[Width,0], [Width, Height], width=7)
        pygame.draw.line(screen,'gray',[0,0],[0,Height], width=7)
        pygame.draw.line(screen,'gray',[0,Height], [Width,Height], width=7)
    
    elif World=='Circle':
        screen.fill('gray')
        pygame.draw.circle(screen, 'white', [Width/2,Height/2], min(Height,Width)/2)
        pygame.draw.circle(screen, 'black', [Width/2,Height/2], min(Height,Width)/2, width=2)
    
    for particle in Particle_System:
        pygame.draw.circle(screen, particle.Color, particle.Position, particle.R)

    pygame.display.update()

def Pygame_Start(W=600, H=600):
    global Width
    global Height
    global screen
    global clock
    Width=W
    Height=H
    screen=pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('2D Physics Engine')
    clock = pygame.time.Clock()
    
    

def Physics_Engine():
    global World
    global Force_Type
    global dt
    World='Closed'
    Force_Type='None'
    dt=0.1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for particle in Particle_System:
            particle.Move()
        for part in combinations(Particle_System, 2):
            if Particle_Particle_Distance(part[0],part[1]) < (part[0].R+part[1].R):
                Particle_Particle_Collision(part[0], part[1])
            
        Draw_Window()
        dt = clock.tick(80)/1000
        
    

if __name__ == "__main__":
    Particle_System=[]
    Particle_System=[Particle([np.random.uniform(100,500),np.random.uniform(100,500)], [np.random.uniform(-100,100),np.random.uniform(-100,100)], 5, 5, 'skyblue') for n in range(25)]
    Particle_System.append(Particle([300,300], [0,0], 20,20, 'red'))
    Particle_System.append(Particle([200,300], [0,0], 10,10, 'green'))
    Particle_System.append(Particle([400,100], [-60,20], 30,30, 'blue'))
    Pygame_Start()
    Physics_Engine()