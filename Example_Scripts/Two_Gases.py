from Physics_Engine import *
from numpy.random import uniform as ran

Window=[1000,600]
line_1=Line(Point_A=[500,0], Point_B=[500,250])
line_2=Line(Point_A=[500,350], Point_B=[500,600])
Line_System=[line_1, line_2]

blue=[Particle(Position=[ran(0,490), ran(0,600)], Velocity=[ran(-200,200), ran(-200,200)], Color='blue') for n in range(50)]
red=[Particle(Position=[ran(510,1000), ran(0,600)], Velocity=[ran(-100,100), ran(-100,100)], Color='red') for n in range(50)]
Particle_System=blue+red

Engine(Particle_System=Particle_System, Line_System=Line_System, Window_Size=Window)