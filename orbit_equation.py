from body import Body
from operations import operations 
import numpy as np
import math

class OrbitEquation:
    G = 6.67408 * (10 ** -11) # value of uneversal constant of gravity in N m^2 kg^-2
    oper = operations()

    def __init__(self, small_body, big_body):
        self.small_body = small_body
        self.big_body = big_body
    
    def setup(self):
        self.MASS_BIG = self.big_body.mass
        self.MASS_SMALL = self.small_body.mass

        self.MU = (self.MASS_BIG * self.MASS_SMALL) / (self.MASS_BIG + self.MASS_SMALL)

        # ENERGY == START ==
        velocity_mag = self.oper.magnitude([self.small_body.vx, self.small_body.vy])
        distance_mag = self.oper.magnitude(
            self.oper.minus(
                [self.small_body.px, self.small_body.py],
                [self.big_body.px, self.big_body.py]
            )
        )

        kinetic_energy = 0.5 * self.MU * (velocity_mag ** 2)
        potential_energy = -(self.G * self.MASS_SMALL * self.MASS_BIG) / distance_mag
        self.ENERGY = kinetic_energy + potential_energy
        # ENERGY == END ==

        # ANGULAR_MOMENTUM == START ==
        small_position = [self.small_body.px, self.small_body.py]
        big_position = [self.big_body.px, self.big_body.py]

        small_velocity = [self.small_body.vx, self.small_body.vy]
        big_velocity = [self.big_body.vx, self.big_body.vy]

        relative_position = self.oper.minus(small_position, big_position)
        relative_velocity = self.oper.minus(small_velocity, big_velocity)

        self.ANGULAR_MOMENTUM = self.oper.cross_product(
            relative_position,
            self.oper.multi(
                relative_velocity,
                self.MASS_SMALL
            )
        )
        # ANGULAR_MOMENTUM == END ==

        # ECCENTRICITY == START ==
        top = 2 * self.ENERGY * (self.ANGULAR_MOMENTUM ** 2)
        bottom = self.MU * ((self.G * self.small_body.mass * self.big_body.mass) ** 2)
        right_value = top / bottom
        self.ECCENTRICITY = np.sqrt(1 + right_value)
        # ECCENTRICITY == END ==

    def info(self):
        print("== INFO ==")
        print(f"\tANGULAR_MOMENTUM = {self.ANGULAR_MOMENTUM}")
        print(f"\tENERGY           = {self.ENERGY}")
        print(f"\tECCENTRICITY     = {self.ECCENTRICITY}")
        print(f"\tANGLE SMALL BODY = {self.get_angle(self.small_body)}")
        print("== END ==")

    def get_angle(self, obj):
        angle_radians = math.atan2(obj.py, obj.px)
        return angle_radians
   
    def get_current_thetta(self):
        try:
            small_position = [self.small_body.px, self.small_body.py]
            big_position = [self.big_body.px, self.big_body.py]

            constant = (self.ANGULAR_MOMENTUM ** 2) / (self.MU * self.G * self.MASS_SMALL * self.MASS_BIG)
            r = self.oper.magnitude(
                self.oper.minus(small_position, big_position)
            )

            ecos = 1 - 1 / (r / constant)
            thetta = np.arccos(ecos / self.ECCENTRICITY)

            return thetta
        except:
            return 0
    
    def get_positive(self, fixed_thetta):
        thetta = fixed_thetta - self.get_angle(self.small_body) + self.get_current_thetta()

        left_part = (self.ANGULAR_MOMENTUM ** 2) / (self.MU * self.G * self.MASS_SMALL * self.MASS_BIG)
        right_part = 1 / (1 - self.ECCENTRICITY * np.cos(thetta))

        r = left_part * right_part

        return r

    def get_negative(self, fixed_thetta):
        thetta = fixed_thetta - self.get_angle(self.small_body) - self.get_current_thetta()

        left_part = (self.ANGULAR_MOMENTUM ** 2) / (self.MU * self.G * self.MASS_SMALL * self.MASS_BIG)
        right_part = 1 / (1 - self.ECCENTRICITY * np.cos(thetta))

        r = left_part * right_part

        return r

    def get(self, thetta):
        return [self.get_positive(thetta), self.get_negative(thetta)]
    
    def polar_to_cartesian(self, r, thetta):
        x = r * np.cos(thetta)
        y = r * np.sin(thetta)
        return x, y


