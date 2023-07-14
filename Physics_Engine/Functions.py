"""


Author: Cano Jones, Alejandro
linkedin: www.linkedin.com/in/alejandro-cano-jones-5b20a7136
github: https://github.com/Cano-Jones
"""

########################################################################

#Libraries

from numpy import array, remainder, dot, sign
from numpy.linalg import norm
from math import atan2, cos, sin, pi
from pygame import draw, display, time, event, QUIT
from sys import exit
from itertools import combinations
from numpy import random

########################################################################

#Functions



def Closed_Box_Boundary(particle):
    
    if particle.Position[0] > (BoxSize[0]-particle.Radius):
        particle.Position[0] = (BoxSize[0]-particle.Radius)
        particle.Velocity[0] = -particle.Velocity[0]
    elif particle.Position[0] < particle.Radius:
        particle.Position[0] = particle.Radius
        particle.Velocity[0] = -particle.Velocity[0]
    elif particle.Position[1] > (BoxSize[1]-particle.Radius):
        particle.Position[1] = (BoxSize[1]-particle.Radius)
        particle.Velocity[1] = -particle.Velocity[1]
    elif particle.Position[1] < particle.Radius:
        particle.Position[1] = particle.Radius
        particle.Velocity[1] = -particle.Velocity[1]



def Periodic_Boundary(particle):
    
    particle.Position=remainder(particle.Position, array(BoxSize))
    
    
    
def Closed_Circle_Boundary(particle):
    
    Width, Height =BoxSize
    [X,Y]=particle.Position
    [Vx,Vy]=particle.Velocity
    if (X-Width/2)**2+(Y-Height/2)**2>=(min(Height,Width)/2-particle.Radius)**2:
        Angle=atan2(Y-Height/2,X-Width/2)+pi/2
        particle.Position[0]=Width/2+(min(Height,Width)/2-particle.Radius)*cos(Angle-pi/2)
        particle.Position[1]=Height/2+(min(Height,Width)/2-particle.Radius)*sin(Angle-pi/2)
        particle.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
        particle.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)



def Circle_Boundary_Background():
    
    screen.fill('gray')
    Center=[BoxSize[d]/2 for d in range(2)]
    draw.circle(screen, 'white', Center, min(Center))
        
        
        
def Particle_Particle_Distance(p1,p2):
    
    return norm(p1.Position-p2.Position)


def Particle_Line_Distance(particle, line):
    
    if line.Point_A[0] == line.Point_B[0]:
        if particle.Position[1]<max(line.Point_A[1], line.Point_B[1]) and particle.Position[1]>min(line.Point_A[1], line.Point_B[1]):
            return abs(particle.Position[0]-line.Point_A[0])
        
    elif line.Point_A[1] == line.Point_B[1]:
        if particle.Position[0]<max(line.Point_A[0], line.Point_B[0]) and particle.Position[0]>min(line.Point_A[0], line.Point_B[0]):
            return abs(particle.Position[1]-line.Point_A[1])
    
    
    if particle.Position[0]<max(line.Point_A[0], line.Point_B[0]) and particle.Position[0]>min(line.Point_A[0], line.Point_B[0]):
        if particle.Position[1]<max(line.Point_A[1], line.Point_B[1]) and particle.Position[1]>min(line.Point_A[1], line.Point_B[1]):
            
            aux1 = (line.Point_B[0]-line.Point_A[0])*(line.Point_A[1]-particle.Position[1])
            aux2 = (line.Point_B[1]-line.Point_A[1])*(line.Point_A[0]-particle.Position[0])
            return abs(aux1-aux2)/line.Length
        
    return max(BoxSize)



def Particle_Particle_Collision(p1,p2):
    #https://physics.stackexchange.com/questions/599278/how-can-i-calculate-the-final-velocities-of-two-spheres-after-an-elastic-collisi
    
    if p1.Dynamic and p2.Dynamic:
    
        vec=p1.Position-p2.Position
        vec_norm=norm(vec)
        
        if vec_norm!=0:
            n=vec/vec_norm
            Delta=(p1.Radius+p2.Radius-vec_norm)
            p1.Position=p1.Position + n*Delta*(p2.Mass/(p1.Mass+p2.Mass))
            p2.Position=p2.Position - n*Delta*(p1.Mass/(p1.Mass+p2.Mass))
            
            vec=p1.Position-p2.Position
            vec=vec/norm(vec)
            aux=0
            for d in range(2): aux+=vec[d]*(p2.Velocity[d]-p1.Velocity[d])
            c=2.0*aux/((vec[0]**2+vec[1]**2)*(1.0/p1.Mass+1.0/p2.Mass))
            
            p1.Velocity=p1.Velocity + vec*c/p1.Mass
            p2.Velocity=p2.Velocity - vec*c/p2.Mass
            
    elif p1.Dynamic:
        vec=p1.Position-p2.Position
        vec_norm=norm(vec)
        
        if vec_norm!=0:
            p1.Position = p2.Position + (vec/vec_norm)*(p1.Radius+p2.Radius)
            Angle = atan2(vec[1], vec[0]) + pi/2
            [Vx, Vy]= p1.Velocity
            p1.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
            p1.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)

    elif p2.Dynamic: 
        vec=p1.Position-p2.Position
        vec_norm=norm(vec)
        
        if vec_norm!=0:
            p2.Position = p1.Position - (vec/vec_norm)*(p1.Radius+p2.Radius)
            Angle = atan2(vec[1], vec[0]) - pi/2
            [Vx, Vy]= p2.Velocity
            p2.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
            p2.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)


def Particle_Line_Collision(particle, line):
    
    if line.Point_A[0] == line.Point_B[0]:
        particle.Position[0]=line.Point_A[0] + sign(particle.Position[0]-line.Point_A[0])*particle.Radius
        particle.Velocity[0]=-particle.Velocity[0]
        
    elif line.Point_A[1] == line.Point_B[1]:
        particle.Position[1]=line.Point_A[1] + sign(particle.Position[1]-line.Point_A[1])*particle.Radius
        particle.Velocity[1]=-particle.Velocity[1]
    
    else:
        v=line.Point_B-line.Point_A
        u=line.Point_A-particle.Position
                
        T=-dot(v,u)/dot(v,v)
        P=(1-T)*line.Point_A+T*line.Point_B
        n=(particle.Position-P)/norm(particle.Position-P)
        particle.Position=P+n*particle.Radius
        
        Angle=line.Angle
        Vx,Vy=particle.Velocity
        aux_x=Vx
        aux_y=Vy
        Vx=cos(2*Angle)*aux_x+aux_y*sin(2*Angle)
        Vy=sin(2*Angle)*aux_x-aux_y*cos(2*Angle)
        particle.Velocity=array([Vx,Vy])
        

def Const_Gravity(g: float = 250):
    
    return lambda x: [0, g*x.Mass]



def Dummy_Function(): pass



def Pygame_Start(WindowSize):
    global BoxSize, screen, clock
    BoxSize=WindowSize
    screen=display.set_mode(WindowSize)
    display.set_caption('2D Physics Engine')
    clock = time.Clock()



def Engine(Window_Size: list = [600,600], Particle_System: list = [], Line_System: list = [],
           Background: 'function' = Dummy_Function, Boundary: 'function' = Closed_Box_Boundary, Force: 'function' = lambda self: [0,0]):
    
    
    Pygame_Start(Window_Size)
    
    for particle in Particle_System:
        particle.Boundary=Boundary
        particle.Force=Force
        
    dt=0.1
    while True:
        
        for py_event in event.get():
            if py_event.type == QUIT:
                exit()
                
        Draw_Window(Particle_System=Particle_System, Background=Background, Line_System=Line_System)
        
        for particle in Particle_System:
            particle.Move(dt)
            
        for comb in combinations(Particle_System,2):
            if Particle_Particle_Distance(comb[0], comb[1]) < comb[0].Radius+comb[1].Radius:
                Particle_Particle_Collision(comb[0], comb[1])
                
        for particle in Particle_System:
            for line in Line_System:
                if Particle_Line_Distance(particle=particle, line=line) < particle.Radius:
                    Particle_Line_Collision(particle=particle, line=line)
                    
        dt = clock.tick(100)/1000



def Draw_Window(Particle_System: list =[], Line_System: list = [], Background: 'function' = Dummy_Function):
    
    screen.fill('white')
    Background()
    for line in Line_System:
        draw.line(screen, 'black', line.Point_A, line.Point_B, width=5)
    for p in Particle_System:
        draw.circle(screen, p.Color, p.Position, p.Radius)
    display.update()
    
    
    
def Random_Color():     
    return tuple(random.random(size=3) * 256)

__all__ = ['Engine', 'Closed_Box_Boundary', 'Periodic_Boundary', 'Closed_Circle_Boundary',
           'Circle_Boundary_Background', 'Particle_Particle_Distance', 'Random_Color', 'Const_Gravity']