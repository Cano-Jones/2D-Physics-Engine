from Physics_Engine import *

particle_1=Particle(Position=[200,100], Velocity=[100,0], Mass=30, Radius=30, Color='red')
particle_2=Particle(Position=[400,100], Velocity=[20,0], Mass=20, Radius=20, Color='blue')
particle_3=Particle(Position=[300,300], Velocity=[0,0], Mass=15, Radius=35, Color='green')
Particle_System=[particle_1, particle_2, particle_3]
Engine(Particle_System=Particle_System, Force = Const_Gravity(200), Boundary=Closed_Circle_Boundary, Background=Circle_Boundary_Background)