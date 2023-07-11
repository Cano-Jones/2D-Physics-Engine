from numpy import array
from numpy.linalg import norm
from math import atan2


class Particle():
    
    def __init__(self, Position: list = [0,0], Velocity: list = [0,0], Mass: float = 10, Radius: float = 10,
                 Charge: float = 1, Color: str = 'black', Dynamic: bool = True):
        
        self.Position = array(Position)
        self.Velocity = array(Velocity)
        self.Mass = Mass
        self.Radius = Radius
        self.Charge = Charge
        self.Color = Color
        self.Force = lambda self: [0,0]
        self.Boundary = lambda self: None 
        self.Dynamic = Dynamic
    
    def Move(self, TimeStep: float = 0.1):
        
        if self.Dynamic:
        
            self.Velocity=self.Velocity+0.5*array(self.Force(self))/self.Mass*TimeStep
            self.Position=self.Position+self.Velocity*TimeStep
            self.Velocity=self.Velocity+0.5*array(self.Force(self))/self.Mass*TimeStep
            
            self.Boundary(self)

class Line():
    def __init__(self, Point_A: list = [0,0], Point_B: list = [0,0]):
        self.Point_A=array(Point_A)
        self.Point_B=array(Point_B)
        self.Length=norm(self.Point_A-self.Point_B)
        self.Angle=atan2(Point_A[1]-Point_B[1], Point_A[0]-Point_B[0])
        
        
__all__ = ['Particle', 'Line']
        


