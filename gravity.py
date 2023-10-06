import pygame
import sys
from operations import operations
import math
import numpy as np

from orbit_equation import OrbitEquation

oper = operations()

# The gravitational constant G
G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
#SCALE = 250 / AU

LINE_SCALE = 10

RADIUS_SCALE = 500
FONT_SIZE = 25

class gravity:
    INC = 0.001

    START = 0

    #SCALE = 35000 / AU
    SCALE = 35000 / AU

    MOVEMENT = 10
    ZOOMING = 10000

    timestep = 24 * 3600

    x, y = 0, 0

    angle = 0

    def update_info(self, step, bodies):
        """(int, [Body])
        
        Displays information about the status of the simulation.
        """
        print('Step #{}'.format(step))
        for body in bodies:
            s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
                body.name, body.px/AU, body.py/AU, body.vx, body.vy)
            print(s)
        print()

    def check_existance(self, mas, name):
        ans = False
        for i in range(len(mas)):
            if mas[i] == name:
                return True
        return False

    def get_text(self, stats):
        font = pygame.font.Font(None, FONT_SIZE)  # You can change the font and size as needed
        text = font.render(stats, True, (255, 255, 255))
        return text

    def loop(self, bodies, main=None, plot=None, rocket=None):
        """([Body])

        Never returns; loops through the simulation, updating the
        positions of all the provided bodies.
        """

        pygame.init()

        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((1200, 700))

        pygame.display.set_caption('Space Age Game')

        background = (24, 39, 95)

        step = 1

        answer = []

        current_time = 0

        while True:
            for body in bodies:
                body.prx = body.px
                body.pry = body.py
                body.prvx = body.vx
                body.prvy = body.vy


            RADIUS_SCALE = 1 / self.SCALE

            clock.tick(120)

            screen.fill(background)

            orbit_equations = OrbitEquation(bodies[rocket], bodies[main])
            orbit_equations.setup()
            orbit_equations.info()
            for thetta in np.arange(0, 2 * np.pi, self.INC):
                r = orbit_equations.get(thetta)

                x, y = orbit_equations.polar_to_cartesian(r[0], thetta)
                PURPLE = (128, 0, 128)
                YELLOW = (255, 255, 0)

                location = (300 + (bodies[main].px - x) * self.SCALE + self.x, 300 + (bodies[main].py - y) * self.SCALE + self.y)
                pygame.draw.circle(screen, PURPLE, location, 5, 20)  

                x, y = orbit_equations.polar_to_cartesian(r[1], thetta)
                PURPLE = (128, 0, 128)
                location = (300 + (bodies[main].px - x) * self.SCALE + self.x, 300 + (bodies[main].py - y) * self.SCALE + self.y)
                pygame.draw.circle(screen, YELLOW, location, 5, 20)  

            # self.update_info(step, bodies)

            # self.update_info(step, bodies)

            rocket_old_x = bodies[rocket].px
            rocket_old_y = bodies[rocket].py
            new_rocket_x = 0
            new_rocket_y = 0

            step += 1

            force = {}
            for body in bodies:
                # Add up all of the forces exerted on 'body'.
                total_fx = total_fy = 0.0
                for other in bodies:
                    # Don't calculate the body's attraction to itself
                    if body is other:
                        continue
                    fx, fy = body.attraction(other)
                    total_fx += fx
                    total_fy += fy
                force[body] = (total_fx, total_fy)

            for body in bodies:
                if body.name == 'Rocket':
                    fx, fy = force[body]
                    TIME_MORE = 2 ** 5 
                    new_rocket_x = body.px + (body.vx + (fx / body.mass) * (self.timestep * TIME_MORE)) * (self.timestep * TIME_MORE)
                    new_rocket_y = body.py + (body.vy + (fy / body.mass) * (self.timestep * TIME_MORE)) * (self.timestep * TIME_MORE)

                    # print(f"x: {new_rocket_x}, y: {new_rocket_y}")

                fx, fy = force[body]
                body.vx += fx / body.mass * self.timestep
                body.vy += fy / body.mass * self.timestep

                body.px += body.vx * self.timestep
                body.py += body.vy * self.timestep

                if plot != None and plot == body.name:
                    with open('planet_orbit.txt', 'a') as f:
                        f.write(str(body.px) + " " + str(body.py) + "\n")
                        print("inserted !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    f.close()
                if main == None:
                    pygame.draw.circle(screen, body.color, (300 + body.px*self.SCALE, 300 + body.py*self.SCALE), body.radius / RADIUS_SCALE, 20)  
                if body.name == 'Rocket':
                    if (oper.magnitude(oper.minus([body.px, body.py], [bodies[main].px, bodies[main].py]))) <= bodies[main].radius - 1:
                        position = oper.minus([body.px, body.py], [bodies[main].px, bodies[main].py])
                        mag = oper.magnitude(position)
                        unit_vec = oper.divide(position, mag)
                        result_vec = oper.plus(oper.multi(unit_vec, bodies[main].radius), [bodies[main].px, bodies[main].py])


                        body.px = result_vec[0]
                        body.py = result_vec[1]

                        body.vx = 0
                        body.vy = 0

                    pygame.draw.line(screen, body.color, (300 + (bodies[main].px - body.px) * self.SCALE + self.x, 300 + (bodies[main].py - body.py) * self.SCALE + self.y), (300 + (bodies[main].px - body.px) * self.SCALE + self.x + body.direction[0] * LINE_SCALE, 300 + (bodies[main].py - body.py) * self.SCALE + self.y + body.direction[1] * LINE_SCALE), 5)
                    
                else:
                    if body.name == bodies[main].name:
                        pygame.draw.circle(
                            screen,
                            body.color,
                            (300 + self.x, 300 + self.y),
                            body.radius / RADIUS_SCALE,
                            1000
                        )
                    else:
                        pygame.draw.circle(
                            screen,
                            body.color,
                            (300 + (bodies[main].px - body.px) * self.SCALE + self.x,
                            300 + (bodies[main].py - body.py) * self.SCALE + self.y),
                            body.radius / RADIUS_SCALE,
                            20
                        )
                #answer.append([body.px * SCALE, body.py * SCALE])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.y += self.MOVEMENT
                    elif event.key == pygame.K_s:
                        self.y -= self.MOVEMENT
                    elif event.key == pygame.K_a:
                        self.x += self.MOVEMENT
                    elif event.key == pygame.K_d:
                        self.x -= self.MOVEMENT
                    elif event.key == pygame.K_p:
                        self.MOVEMENT += 10
                    elif event.key == pygame.K_l:
                        self.MOVEMENT -= 10
                    elif event.key == pygame.K_z:
                        self.SCALE = (self.SCALE * AU + self.ZOOMING) / AU
                    elif event.key == pygame.K_x:
                        self.SCALE = (self.SCALE * AU - self.ZOOMING) / AU
                    elif event.key == pygame.K_b:
                        self.ZOOMING *= 2
                    elif event.key == pygame.K_n:
                        self.ZOOMING /= 2
                    elif event.key == pygame.K_y:
                        self.timestep *= 2
                    elif event.key == pygame.K_h:
                        self.timestep /= 2
                    elif event.key == pygame.K_i:
                        self.START = 1
                    elif event.key == pygame.K_j:
                        self.START = 0
                    elif event.key == pygame.K_9:
                        self.angle += 15
                    elif event.key == pygame.K_0:
                        self.angle -= 15
                    elif event.key == pygame.K_1:
                        bodies[rocket].thrust -= 100
                    elif event.key == pygame.K_2:
                        bodies[rocket].thrust += 100
            
            bodies[rocket].direction[0] = math.cos(self.angle * math.pi / 180)
            bodies[rocket].direction[1] = math.sin(self.angle * math.pi / 180)

            if self.START == 1:
                velocity = (bodies[rocket].thrust * self.timestep) / bodies[rocket].mass * self.timestep
                res = oper.multi(bodies[rocket].direction, velocity)

                bodies[rocket].vx += res[0]
                bodies[rocket].vy += res[1]

            pygame.draw.line(
                screen,
                (0, 255, 0),
                (300 + (bodies[main].px - rocket_old_x) * self.SCALE + self.x, 300 + (bodies[main].py - rocket_old_y) * self.SCALE + self.y),
                (300 + (bodies[main].px - new_rocket_x) * self.SCALE + self.x, 300 + (bodies[main].py - new_rocket_y) * self.SCALE + self.y),
                width=3
            )

            velocity_x = "{:.2f}".format(body.vx)
            velocity_y = "{:.2f}".format(body.vy)
            distance = oper.magnitude(oper.minus([body.px, body.py], [bodies[main].px, bodies[main].py]))
            velocity_mag = oper.magnitude([body.vx, body.vy])
            mass = bodies[rocket].mass

            mu = (bodies[main].mass * bodies[rocket].mass) / (bodies[main].mass + bodies[rocket].mass)

            kinetic_energy = mu * (velocity_mag ** 2) / 2
            potential_energy = - G * (bodies[main].mass * bodies[rocket].mass) / distance
            energy = kinetic_energy + potential_energy
            engine_on = "ON" if self.START else "OFF"

            texts = [
                f"Engine = {engine_on}",
                f"Timestep = {self.timestep} s",
                f"Distance = {distance} m",
                f"Mass of Rocket = {bodies[rocket].mass} kg",
                f"Velocity = [{velocity_x} m/s, {velocity_y} m/s]",
                f"Momentum = {bodies[rocket].mass * velocity_mag} kg m/s",
                f"Current Time = {current_time // 60} min {current_time % 60} sec",
                f"",
                f"== ENERGY START ==",
                f"  Kinetic = {kinetic_energy} J",
                f"  Potential = {potential_energy} J",
                f"  Total = {energy} J",
                f"== ENERGY END =="
            ]

            for i in range(len(texts)):
                screen.blit(self.get_text(texts[i]), (10, FONT_SIZE * (i + 1)))

            current_time += self.timestep

            pygame.display.update()
