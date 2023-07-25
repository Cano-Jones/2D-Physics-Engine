"""
Physics_Engine library

This python library provides the tools to perform a simulation of the behaviour of a system of rigid-body particles 
represented as circles on a particular environment. The main objects to consider are:
    Particles: Massive particles representad as circles, they may be dynamic or not.
        Particles might bounce off other particles, lines or the boundary.
    Lines: Non dynamic segments over which particles might bounce.
    Boundary: Limit conditions of the system.
The engine is equipped with a graphic interface based on the pygame library, having used only its drawing functionalities;
all object collisions and responsed are hand programed.

In order to start the simulation, the 'Engine' function must be called. Posible arguments of this function include:
    Boundaries: Closed_Box_Boundary, Periodic_Boundary, Closed_Circle_Boundary
    Background: Circle_Boundary_Background
    Forces: Const_Gravity
    Utilities: Particle_Particle_Distance, Particle_Line_Distance, Random_Color

Author: Cano Jones, Alejandro
linkedin: www.linkedin.com/in/alejandro-cano-jones-5b20a7136
github: https://github.com/Cano-Jones
"""

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' #Used so no wellcome message from pygame appears

from Physics_Engine.Objects import *
from Physics_Engine.Functions import *