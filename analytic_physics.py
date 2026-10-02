"""
Analytic orbital-mechanic helpers

Doctests model a spacecraft going from LEO to GEO around Earth

mu_earth = 3.986e14 (m^3 / s^2).
"""

import math as m


def circular_velocity(mu, r):
    """Speed for a circular orbit of radius r about a body with parameter mu


    >>> circular_velocity(3.986 * 10**14, 6628 * 10**3)
    7754.921345146096
    """
    v = m.sqrt(mu / r)
    return v


def escape_velocity(mu, r):
    """Escape speed at a radius r from a body with parameter mu

    
    >>> escape_velocity(3.986 * 10**11, 6628)
    10967.114941442216
    """
    v_e = m.sqrt(2) * circular_velocity(mu, r)
    return v_e


def vis_viva(mu, r, a):
    """Speed at a distance r on an orbit with semi-major axis a.

    When r == a the orbit is circular, so vis-viva must agree with circular velocity

    
    >>> round(vis_viva(3.986e14, 6628e3, 6628e3), 6) == round(circular_velocity(3.986e14, 6628e3), 6)
    True
    """
    
    speed = m.sqrt(mu * (2 / r - 1 / a));
    return speed

def orbital_period(a, mu):
    """Computes the period for semi-major axis a about parameter mu

    
    >>> round(orbital_period(6628e3, 3.986e14), 1)
    5370.1
    """
    T = 2 * m.pi * m.sqrt((a**3) / mu)
    return T

def hohmann_transfer(r1, r2, mu):
    """Two-burn Hohmann transfer between circular orbit r1 and r2.

    A burn is a 'change' in speed, not an orbital speed: at each end we take
    the difference in transfer-ellipse speed against the circular-orbit speed.
    Returns(burn1, burn2, total_delta_v), all in (m / s)

    LEO (~250 km ) to GEO is a ~3.9 km / s transfer
    

    >>> burn1, burn2, total = hohmann_transfer(6628e3, 42164e3, 3.986e14)
    >>> round(total, 1)
    3912.2
    """
    # semi major axis of the elliptical transfer orbit
    a = (r1 + r2) / 2

    # circular speeds at each radius
    v_c1 = circular_velocity(mu, r1)
    v_c2 = circular_velocity(mu, r2)

    # transfer-ellipse speeds at each radius (vis-viva)
    v_tr1 = vis_viva(mu, r1, a)
    v_tr2 = vis_viva(mu, r2, a)

    # each burn is the magnitude of the speed change at that point
    burn1 = abs(v_tr1 - v_c1)
    burn2 = abs(v_c2 - v_tr2)
    delta_v = burn1 + burn2

    return (burn1, burn2, delta_v)



# run doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)