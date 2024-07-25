import math
from body import Body
import pygame
import sys
from gravity import gravity
from rocket import rocket

def main():
    earth = Body()
    earth.name = 'Earth'
    earth.mass = 5.9742e24
    earth.color = (88, 222, 249)
    earth.radius = 6_378_000

    rocket = Body()
    rocket.name = 'Rocket'
    rocket.mass = 500
    rocket.py = 6_378_000
    rocket.vy = 0
    rocket.color = (255, 0, 0)
    rocket.radius = 3 #5,6134
    
    rocket.thrust = 5000 # N
    rocket.direction = [1, 0]

    space = gravity()
    space.angle = 0
    space.timestep = 1
    
    space.loop([earth, rocket], main=0, rocket=1)

if __name__ == '__main__':
    main()
