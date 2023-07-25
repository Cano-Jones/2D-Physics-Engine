"""
Objects.py

Python module contaning the classes that describe the objects that determine the system.

There are two existing objects: Particles and Lines. Particles (dynamic or not) are repressented as circles, their movement is described by interactions with
other perticles, lines of boundaries; responnses of collision are determined by newtonian mechanics. Lines (not dynamic) are one dimensional segments on
which particles bounce off.


Author: Cano Jones, Alejandro
linkedin: www.linkedin.com/in/alejandro-cano-jones-5b20a7136
github: https://github.com/Cano-Jones
"""

########################################################################

#Libraries

from numpy import array
from numpy.linalg import norm
from math import atan2

from Physics_Engine.Functions import Closed_Box_Boundary

########################################################################

#Objects defined by classes

class Particle():
    """
        Class Particle.
        
        The Particle class defines a circle in the screen, it can interact with the screen boundaries (if any), other particles and lines from the Line class. 
        Interactions of a particle with its environment correspond to newtonian mechanics.
        
        Class attributes:
            Position (2D array): Position of the circle center
            Velocity (2D array): Velocity of the circle center
            Mass (float): Mass of the particle
            Radius (float): Radius of the circle
            Color (str): Color of the circle
            Dynamic (bool): Determines if the particle moves
            Force (function(self)->2D array): Force acting on the particle
            Boundary (function(self)->None): Boundary conditions of the particle environment
        """
    
    def __init__(self, Position: list = [0,0], Velocity: list = [0,0], Mass: float = 10,
                 Radius: float = 10, Color: str = 'navy', Dynamic: bool = True):
        """
        Constructor for Particle class.
        
        Parameters (Optionals):
            Position (2D array): Position of the circle center
            Velocity (2D array): Velocity of the circle center
            Mass (float): Mass of the particle
            Radius (float): Radius of the circle
            Color (str): Color of the circle
            Dynamic (bool): Determines if the particle moves
        """
        
        self.Position = array(Position) #Position of the circle center
        self.Velocity = array(Velocity) #Velocity of the circle center
        self.Mass = Mass #Mass of the particle
        self.Radius = Radius #Radius of the circle
        self.Color = Color #Color of the circle
        self.Dynamic = Dynamic #Determines if the particle can move
        
        self.Force = lambda self: [0,250*self.Mass] #Force acting on the particle
        self.Boundary = Closed_Box_Boundary #Boundary conditions of the particle environment
        
    
    def Move(self, TimeStep: float = 0.1):
        """
        Move method.
        
        This method changes the position and velocity of the particle, according to the Verlet integrator algorithm if self.Dynamic is set to True. 
        After a timestep has passed, position and velocity can change according to corresponding boundary conditions, by means of the self.Boundary function.
        
        Parameters (Optionals):
            TimeStep (float): time step of the Verlet integration algorithm        
        """
        
        if self.Dynamic: #The particle moves only if it's Dynamic
            
            #Verlet algorithm
            self.Velocity=self.Velocity+0.5*array(self.Force(self))/self.Mass*TimeStep
            self.Position=self.Position+self.Velocity*TimeStep
            self.Velocity=self.Velocity+0.5*array(self.Force(self))/self.Mass*TimeStep
            
            self.Boundary(self) #After the movement, the position and velocity can change according to Boundaries

class Line():
    """
    Class Line.
        
    The Line class defines a line in the screen, particles (from Particle class) can bounce off it according to newtonian mechanics.
    Lines are non dynamic entities.
        
    Class attributes:
        Point_A (2D array): First of two points defining a line segment
        Point_B (2D array): Second of two points defining a line segment
        Length (float):Length of the line segment 
        Angle (float): Angle of the line slope
    """
    def __init__(self, Point_A: list = [0,0], Point_B: list = [0,0]):
        """
        Constructor for Particle class.
        
        Parameters (Optionals):
            Point_A (2D array): First of two points defining a line segment
            Point_B (2D array): Second of two points defining a line segment
        """
        
        self.Point_A = array(Point_A) #First of two points defining a line segment
        self.Point_B = array(Point_B) #Second of two points defining a line segment
        
        self.Length = norm(self.Point_A-self.Point_B) #ength of the line segment 
        self.Angle = atan2(Point_A[1]-Point_B[1], Point_A[0]-Point_B[0]) #Angle of the line slope
                
            
        
__all__ = ['Particle', 'Line']