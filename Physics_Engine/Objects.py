from numpy import array


class Particle():
    def __init__(self, Position: list = [0,0], Velocity: list = [0,0], Mass: float = 10, Radius: float = 10,
                 Charge: float = 1, Color: str = 'black'):
        
        self.Position = array(Position)
        self.Velocity = array(Velocity)
        self.Mass = Mass
        self.Radius = Radius
        self.Charge = Charge
        self.Color = Color
        self.Force = lambda self: [0,0]
        self.Boundary = lambda self: None 
    
    def Move(self, TimeStep: float = 0.1):
        
        self.Velocity=self.Velocity+0.5*array(self.Force(self))/self.Mass*TimeStep
        self.Position=self.Position+self.Velocity*TimeStep
        self.Velocity=self.Velocity+0.5*array(self.Force(self))/self.Mass*TimeStep
        
        self.Boundary(self)
        
__all__ = ['Particle']
        


