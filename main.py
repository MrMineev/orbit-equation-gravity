import math
from body import Body
import pygame
import sys
from gravity import gravity
from rocket import rocket

# The gravitational constant G
G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
#SCALE = 250 / AU
SCALE = 35000 / AU
#SCALE = 250000 / AU

def main():
    earth = Body()
    earth.name = 'Earth'
    earth.mass = 5.9742e24
    earth.color = (88, 222, 249)
    earth.radius = 6378000

    rocket = Body()
    rocket.name = 'Rocket'
    rocket.mass = 500
    rocket.px = 6_378_000
    rocket.py = 0
    rocket.vy = 0
    rocket.color = (255, 0, 0)
    rocket.radius = 3 #5,6134
    
    rocket.thrust = 5000 # N
    rocket.direction = [1, 0]

    space = gravity()
    space.angle = 90
    space.timestep = 1
    
    space.loop([earth, rocket], main=0, rocket=1)

if __name__ == '__main__':
    main()
