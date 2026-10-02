import Vector as V
from math import e

# Single source for the graviational constant
G = 6.674 * 10**(-11)


class Body():
    """An object with mass, a position vector, and a velocity vector.
    
    Attributes:
        name        : label used in reports and (later) System lookups
        mass        : kg
        position    : Vector (m)
        velocity    : Vector (m/s)
        radius      : m (used for collision detection)
        cur_ac      : acceleration at the current step, a(t)    (Vector)
        nxt_ac      : acceleration at the next step,    a(t+dt) (Vector)
        
    Methods:
        grav_acc_from(other) -> vector
            gravitational acceleration on *this* body due to *other*,
            as a vector pointing from self toward other.
        """

    def __init__(self, name, mass, position, velocity, radius):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius

        self.cur_ac = V.Vector(0, 0)
        self.nxt_ac = V.Vector(0, 0)


    def grav_acc_from(self, other):
        """Acceleration on self due to other's gravity, as a Vector.
        
        a = G * m_other / r**2, directed from self toward other.
        """

        r_vec = other.position - self.position
        r = r_vec.magnitude()
        a_mag = G * other.mass / r**2
        return r_vec.normalize() * a_mag

    
    def __repr__(self):
        return f'Body({self.name!r}, {self.mass}, {self.position}, {self.velocity})'
    

class Planet(Body):
    """A Body that also carries a human-readable identity as a planet.

    (Used as its own class for later implementation of planet-only data,
    e.g. atmosphere or rotation, without touching Body.)
    """


    def __init__(self, name, mass, position, velocity, radius):
        super().__init__(name, mass, position, velocity, radius)



class Spacecraft(Body):
    """A Body that can spend fuel to change its velocity.

    Adds:
        dry_mass            : kg (structure without fuel)
        fuel                : kg
    Methods:
        apply_burn(delta_v) : changes velocity, decrements fuel
    """

    def __init__(self, name, mass, position, velocity, radius, dry_mass, fuel):
        super().__init__(name, mass, position, velocity, radius)
        self.dry_mass = dry_mass
        self.fuel = fuel

    def apply_burn(self, delta_v):
        """Apply an instantaneous velocity change and spend fuel.

        NOTE TODO): the rocket-equation fuel model below is still a
        placeholder. The velocity change itself is correct; the fuel
        accounting needs a real exhaust velocity before the capstone.

        """

        """
        exhaust_velocity = V.Vector(1,1)        # TODO: this is technically e ** e_vel
        total_initial_mass = self.fuel + self.dry_mass                                       
        total_final_mass = total_initial_mass * (e ** (-1 * delta_v.dot(exhaust_velocity)))  
        self.fuel = self.fuel - (total_initial_mass - total_final_mass)
        """
        
        # Change in Velocity (delta_v is sign sensitive)
        self.velocity = self.velocity + delta_v

        return f'Spacecraft({self.mass}, {self.position}, {self.velocity}, {self.dry_mass}, {self.fuel})'