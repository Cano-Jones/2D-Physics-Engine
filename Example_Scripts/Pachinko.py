from Physics_Engine import *
from numpy.random import uniform as ran

Window=[600,500]

line_1=Line(Point_A=[0,0], Point_B=[250,150])
line_2=Line(Point_A=[600,0], Point_B=[350, 150])
line_3=Line(Point_A=[300,200], Point_B=[250,250])
line_4=Line(Point_A=[300,200], Point_B=[350,250])
line_5=Line(Point_A=[200,300], Point_B=[250,350])
line_6=Line(Point_A=[200,300], Point_B=[150,350])
line_7=Line(Point_A=[400,300], Point_B=[450,350])
line_8=Line(Point_A=[400,300], Point_B=[350,350])

Particle_System=[Particle(Position=[ran(200,400), ran(75,100)], Color=Random_Color()) for n in range(25)]
Line_System=[line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8]

Engine(Window_Size=Window, Particle_System=Particle_System, Line_System=Line_System, Force = Const_Gravity(100))