"""
Functions.py

Python module contaning the funtions that describe the behaviour and responses of the objects on Objects.py.

These functions make up the Physics_Engine library; including the engine itself, and functions used to describe the 
environment to simulate. 

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
    """
    Particle boundary consisting of a closed box.
    
    This functiondescriibes the response of a particle as it moves inside a closed box the size of the screen. If the particle moves over 
    one side of the box, the particle will bounce.
    """
    
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
    """
    Particle boundary consisting of a 'periodic' world (torus).
    
    This function describes the response of a particle as it moves over one side of the screen, appearing on the other side 
    of the screen with the same velocity.
    
    Parameters:
        particle (Particle class): particle to bounce of the boundary (circle)
    """
    
    #Trivial particle traslation
    particle.Position=remainder(particle.Position, array(BoxSize))
    
    
    
def Closed_Circle_Boundary(particle):
    """
    Particle boundary consisting of a circle centered on the screen.
    
    This function describes the response of a particle as it bounces off the interior side of a circle.
    This function is intended to be used alongside the Circle_Boundary_Background function for better visualization.
    
    Parameters:
        particle (Particle class): particle to bounce of the boundary (circle)
    """
    #Auxiliar variables are defined
    Width, Height =BoxSize
    [X,Y]=particle.Position
    [Vx,Vy]=particle.Velocity
    
    #If the distance of the particle to the circunference is less than the particle radius, then it must bounce
    if (X-Width/2)**2+(Y-Height/2)**2>=(min(Height,Width)/2-particle.Radius)**2:
        #The particle will bounce according to the normal angle of the surface of the circunference
        Angle=atan2(Y-Height/2,X-Width/2)+pi/2
        particle.Position[0]=Width/2+(min(Height,Width)/2-particle.Radius)*cos(Angle-pi/2)
        particle.Position[1]=Height/2+(min(Height,Width)/2-particle.Radius)*sin(Angle-pi/2)
        particle.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
        particle.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)



def Circle_Boundary_Background():
    """
    Background for the Closed Circle Boundary
    
    This function (intended to be used alongside the Closed_Circle_Boundary boundary) draws a circle on which particles can bounce off.
    """
    
    #Screen background is painted gray color
    screen.fill('gray')
    #A circle centered on the center of the screen is drawn
    Center=[BoxSize[d]/2 for d in range(2)]
    #The circle is painted white
    draw.circle(screen, 'white', Center, min(Center))
        
        
        
def Particle_Particle_Distance(p1,p2):
    """
    Eucledian distance between two point-like particles
    
    Parameters:
        p1 (Particle class): One of the two particles
    """
    return norm(p1.Position-p2.Position)


def Particle_Line_Distance(particle, line):
    """
    Funcion that computes the eucledian distance between a particle and a line.
    
    Give a particle and a line (segment), this function returns the eucledian distance between them, if the particle lies in the 
    parallelogram described by the two points of the segment, otherwise, it returns the maximal distance posible on de system (either 
    the width or the height of the screen).
    
    Parameters:
        particle (Particle class): Particle whose distance to the line wants to be computed
        line (Line class): Line segment whose distance to the particle wants to be computed
    
    Returns:
        Distance (float): Eucledian distance between the line (segment) and the particle 
    
    """
    #There are three posible line configurations: Horizontal, Vertical and Other
    
    #Vertical configutarion
    if line.Point_A[0] == line.Point_B[0]:
        #If the vertical position of the particle lies between the two points of the segment
        if particle.Position[1]<max(line.Point_A[1], line.Point_B[1]) and particle.Position[1]>min(line.Point_A[1], line.Point_B[1]):
            #Then the distance equals the absolute value of the distance between the horizontal position of the line and the particle
            return abs(particle.Position[0]-line.Point_A[0])
    
    #Horizontal configuration
    elif line.Point_A[1] == line.Point_B[1]:
        #If the horizontal position of the particle lies between the two points of the segment
        if particle.Position[0]<max(line.Point_A[0], line.Point_B[0]) and particle.Position[0]>min(line.Point_A[0], line.Point_B[0]):
            #Then the distance equals the absolute value of the distance between the vertical position of the line and the particle
            return abs(particle.Position[1]-line.Point_A[1])
    
    #Other configuration
    elif particle.Position[0]<max(line.Point_A[0], line.Point_B[0]) and particle.Position[0]>min(line.Point_A[0], line.Point_B[0]):
        if particle.Position[1]<max(line.Point_A[1], line.Point_B[1]) and particle.Position[1]>min(line.Point_A[1], line.Point_B[1]):
            #If the particle lies inside the parallelogram described by the segment, then the distance is computed as it follows
            aux1 = (line.Point_B[0]-line.Point_A[0])*(line.Point_A[1]-particle.Position[1])
            aux2 = (line.Point_B[1]-line.Point_A[1])*(line.Point_A[0]-particle.Position[0])
            return abs(aux1-aux2)/line.Length
    #Otherwise, the distance is the maximal posible
    return max(BoxSize)



def Particle_Particle_Collision(p1,p2):
    """
    Particles response after collision
    
    This function rewrites the position and velocities of the particles involved in the collision (if they are dynamic).
    
    Parameters:
        p1 (Particle class): One of the two particles involved in the collision
        p2 (Particle class): Second of the two particles involved in the collision
    """
    
    #If both particles are dynamic
    if p1.Dynamic and p2.Dynamic:
        
        #Since the partcle might have tunnelled through the line due to numerical deviation, the particle is moved to the correct place
        vec=p1.Position-p2.Position
        vec_norm=norm(vec)
        
        #If both particles are on the same position, something wrong must happened...
        if vec_norm!=0:
            #Particles are relocated in accordance with their masses, mantainning the centre of mass
            n=vec/vec_norm
            Delta=(p1.Radius+p2.Radius-vec_norm)
            p1.Position=p1.Position + n*Delta*(p2.Mass/(p1.Mass+p2.Mass))
            p2.Position=p2.Position - n*Delta*(p1.Mass/(p1.Mass+p2.Mass))
            
            #Once particles are relocated, they bounce
            vec=p1.Position-p2.Position
            vec=vec/norm(vec)
            aux=0
            for d in range(2): aux+=vec[d]*(p2.Velocity[d]-p1.Velocity[d])
            c=2.0*aux/((vec[0]**2+vec[1]**2)*(1.0/p1.Mass+1.0/p2.Mass))
            
            p1.Velocity=p1.Velocity + vec*c/p1.Mass
            p2.Velocity=p2.Velocity - vec*c/p2.Mass
        
    #Only the first particle is dynamic
    elif p1.Dynamic:
        #Since the partcle might have tunnelled through the line due to numerical deviation, the particle is moved to the correct place
        vec=p1.Position-p2.Position
        vec_norm=norm(vec)
        
        #If both particles are on the same position, something wrong must happened...
        if vec_norm!=0:
            #Dynamic particle is relocated on correct place
            p1.Position = p2.Position + (vec/vec_norm)*(p1.Radius+p2.Radius)
            #And then it bounces
            Angle = atan2(vec[1], vec[0]) + pi/2
            [Vx, Vy]= p1.Velocity
            p1.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
            p1.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)

    #Only the second particle is dynamic
    elif p2.Dynamic: 
        #Since the partcle might have tunnelled through the line due to numerical deviation, the particle is moved to the correct place
        vec=p1.Position-p2.Position
        vec_norm=norm(vec)
        
        #If both particles are on the same position, something wrong must happened...
        if vec_norm!=0:
            #Dynamic particle is relocated on correct place
            p2.Position = p1.Position - (vec/vec_norm)*(p1.Radius+p2.Radius)
            #And then it bounces
            Angle = atan2(vec[1], vec[0]) - pi/2
            [Vx, Vy]= p2.Velocity
            p2.Velocity[0]=cos(2*Angle)*Vx+Vy*sin(2*Angle)
            p2.Velocity[1]=sin(2*Angle)*Vx-Vy*cos(2*Angle)


def Particle_Line_Collision(particle, line):
    """
    Particle response after collision with a line.
    
    This function rewrites the position and velocity of a particle that has collided with a line.
    
    Parameters:
        particle (Particle class): Particle that collides
        line (Line class): Line the particle has collided
    """
    #There are three posible line configurations: Horizontal, Vertical and Other
    
    #Horizontal line configuration
    if line.Point_A[0] == line.Point_B[0]: #The line is horizontal if the X position of the two points describing the segment are equal
        #Since the partcle might have tunnelled through the line due to numerical deviation, the particle is moved to the correct place
        particle.Position[0]=line.Point_A[0] + sign(particle.Position[0]-line.Point_A[0])*particle.Radius
        particle.Velocity[0]=-particle.Velocity[0] #After collision, the X velocity of the particle changes direction (bounces)
        
    #Vertical line configuration
    elif line.Point_A[1] == line.Point_B[1]: #The line is horizontal if the Y position of the two points describing the segment are equal
        #Since the partcle might have tunnelled through the line due to numerical deviation, the particle is moved to the correct place
        particle.Position[1]=line.Point_A[1] + sign(particle.Position[1]-line.Point_A[1])*particle.Radius
        particle.Velocity[1]=-particle.Velocity[1] #After collision, the Y velocity of the particle changes direction (bounces)
    
    #Other Configuration
    else:
        #First, the closest point of the line to the particle is computed
        v=line.Point_B-line.Point_A
        u=line.Point_A-particle.Position
        T=-dot(v,u)/dot(v,v)
        
        P=(1-T)*line.Point_A+T*line.Point_B #Closest point
        #Since the partcle might have tunnelled through the line due to numerical deviation, the particle is moved to the correct place
        n=(particle.Position-P)/norm(particle.Position-P)
        particle.Position=P+n*particle.Radius
        
        
        #After the particle is at the correct position, the velocity changes (bounce)
        Angle=line.Angle
        Vx,Vy=particle.Velocity
        aux_x=Vx
        aux_y=Vy
        Vx=cos(2*Angle)*aux_x+aux_y*sin(2*Angle)
        Vy=sin(2*Angle)*aux_x-aux_y*cos(2*Angle)
        particle.Velocity=array([Vx,Vy])
        

def Const_Gravity(g: float = 250):
    """
    Given a constant gravitational aceleration, this function returns the gravitational force (as a 2D
    array) that a point-like particle would experience.
    """
    return lambda x: [0, g*x.Mass]



def Dummy_Function():
    """
    Dummy function, this function does nothing, returns nothing
    """
    pass



def Pygame_Start(WindowSize=[600,600]):
    """
    Pygame inicialization
    
    Ths functions starts the needed pygame code.
    
    Patameters (Optionals):
        WindowSize (2D int list): Size of the window screen in pixels
    """
    
    global BoxSize, screen, clock #These variables are used throughout the program
    BoxSize=WindowSize 
    screen=display.set_mode(WindowSize) #Sets the screen size
    display.set_caption('2D Physics Engine') #Sets the screen caption
    clock = time.Clock() #Sets the Clock functionality that will be used to determine the TimeStep



def Engine(Window_Size: list = [600,600], Particle_System: list = [], Line_System: list = [],
           Background: 'function' = Dummy_Function, Boundary: 'function' = Closed_Box_Boundary, Force: 'function' = lambda self: [0,0]):
    """
    Main Engine function.
    
    Given a System comprised of particles and lines, this function draws in real time the movement of said particles according to newtonian mechanics.
    The environment in which the particles move is described by the screen window, once a particle crosses one side of the screen, the Boundary condition
    can rewrite the particle position (the particle might bounce off the side, or appear on the other side).
    
    Parameters (Optionals):
        Window_Size (2D int list): Size of the window screen in pixels
        Particle_System (list): List of Particle class objects
        Line_System (list): List of Line class objects
        Background (function()->None): Function comprised of pygame code to draw anything on the screen background
        Boundary (function(particle)->None): Function that changes the position and velocity of particles defining some boundary
        Force (function(particle)->2D array): Function that describes the force felt by a particle
    """
    
    #Pygame inicialization
    Pygame_Start(Window_Size)
    
    #Particle Boundary and force is specified
    for particle in Particle_System: #For each particle in Particle_System
        particle.Boundary=Boundary #Boundary
        particle.Force=Force #Force
        
    dt=0.1 #TimeStep placeholder
    while True: #This loop will determine each frame of the simulation until user external QUIT event
        
        #Program checks for external events
        for py_event in event.get(): 
            if py_event.type == QUIT: #If the event is QUIT the simulation stops
                exit()
        
        #The screen graphics are updated
        Draw_Window(Particle_System=Particle_System, Background=Background, Line_System=Line_System)
        
        #Each particle in Particle_System moves
        for particle in Particle_System:
            particle.Move(dt)
            
        #Once each particle has moved, collisions are checked
        #First, Particle-Particle collisions
        for comb in combinations(Particle_System,2): #For each pair of particles
            #If the distance of the two particles is less than the sum of their radius, then there is a collision
            if Particle_Particle_Distance(comb[0], comb[1]) < comb[0].Radius+comb[1].Radius:
                Particle_Particle_Collision(comb[0], comb[1])
        
        #Secondly, Particle-Line collision                
        for particle in Particle_System:
            for line in Line_System:
                #If the distance between the particle and the line is less than the radius of the particle, there is a collision
                if Particle_Line_Distance(particle=particle, line=line) < particle.Radius:
                    Particle_Line_Collision(particle=particle, line=line)
        
        #TimeStep is updated, equals the time spend calculating last frame
        dt = clock.tick(100)/1000



def Draw_Window(Particle_System: list =[], Line_System: list = [], Background: 'function' = Dummy_Function):
    """
    Function that updates the screen graphics.
    
    Given the arguments of the function, it draws on the screen the specified background, the lines and the
    position of the particles on the Particle_System (alongside its colors and radius).
    
    Parameters (Optionals):
        Particle_System (list): List of Particle class objects
        Line_System (list): List of Line class objects
        Background (function()->None): Function comprised of pygame code to draw anything on the screen background
    """
    
    #Firstly the screen is white painted
    screen.fill('white')
    #If there is some defined background, it is printed here
    Background()
    
    #Each line (segment) is drawn from its two defining points
    for line in Line_System:
        draw.line(screen, 'black', line.Point_A, line.Point_B, width=5)
        
    #Each particle (represented as a circle) is drawn
    for p in Particle_System:
        draw.circle(screen, p.Color, p.Position, p.Radius)
    
    #Graphics update
    display.update()
    
    
    
def Random_Color():
    """
    Function that returns a random RGB color, intended for Particle class inicialization
    """
    #A RGB color is described by a 3-dimensional intiger tuple, each element a value from 0 to 255      
    return tuple(random.random(size=3) * 255)

__all__ = ['Engine', 'Closed_Box_Boundary', 'Periodic_Boundary', 'Closed_Circle_Boundary',
           'Circle_Boundary_Background', 'Particle_Particle_Distance', 'Random_Color', 
           'Particle_Line_Distance', 'Const_Gravity']