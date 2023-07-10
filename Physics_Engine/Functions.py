from numpy import array, remainder
from numpy.linalg import norm
from math import atan2, cos, sin, pi
from pygame import draw, display, time, event, QUIT
from sys import exit
from itertools import combinations
from numpy import random


def Closed_Box_Boundary(particle,):
    
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

def Particle_Particle_Collision(p1,p2):
    #https://physics.stackexchange.com/questions/599278/how-can-i-calculate-the-final-velocities-of-two-spheres-after-an-elastic-collisi
    
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

def Coulomb_Force(p):
    G=100000
    aux=[0,0]
    for q in Particle_System:
        if q is not p:
            cte=G*p.Charge*q.Charge
            R=Particle_Particle_Distance(p,q)
            aux[0]-=cte/R/R/R*(p.Position[0]-q.Position[0])
            aux[1]-=cte/R/R/R*(p.Position[1]-q.Position[1])
    return aux

def Dummy_Function(): 
    pass

def Pygame_Start(WindowSize):
    global BoxSize
    global screen
    global clock
    BoxSize=WindowSize
    screen=display.set_mode(WindowSize)
    display.set_caption('2D Physics Engine')
    clock = time.Clock()



def Engine(Window_Size: list = [600,600], System: list = [], Background: 'function' = Dummy_Function, 
           Boundary: 'function' = lambda self: None, Force: 'function' = lambda self: [0,0]):
    global Particle_System
    Particle_System=System
    
    Pygame_Start(Window_Size)
    for particle in System:
        particle.Boundary=Boundary
        particle.Force=Force
        
    dt=0.1
    while True:
        for py_event in event.get():
            if py_event.type == QUIT:
                exit()
        Draw_Window(system=System, Background=Background)
        for particle in System:
            particle.Move(dt)
        for comb in combinations(System,2):
            if Particle_Particle_Distance(comb[0], comb[1]) < comb[0].Radius+comb[1].Radius:
                Particle_Particle_Collision(comb[0], comb[1])
        dt = clock.tick(100)/1000

def Draw_Window(system: list =[], Background: 'function' = Dummy_Function):
    screen.fill('white')
    Background()
    for p in system:
        draw.circle(screen, p.Color, p.Position, p.Radius)
    display.update()
    
def Random_Color():
    return tuple(random.random(size=3) * 256)

__all__ = ['Engine', 'Closed_Box_Boundary', 'Periodic_Boundary', 'Closed_Circle_Boundary', 'Circle_Boundary_Background', 'Particle_Particle_Distance', 
           'Coulomb_Force', 'Random_Color']