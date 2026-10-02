"""
Velocity Verlet N-Body simulation.


"""

import Body as B
import analytic_physics as ap
import Vector as V
from copy import copy
import System
import Report as rep
import Visualize as vis



# ============================================================
# PHYSICS HELPERS
# ============================================================

def compute_accelerations(system):
    """Fill every body's nxt_ac with its net gravitational acceleration at the current positions.
            * Builds from zero each call
    """
    for b in system:
        b.nxt_ac = V.Vector(0, 0)
    for b in system:
        for other in system:
            if other is b:
                continue
            b.nxt_ac = b.nxt_ac + b.grav_acc_from(other)


def total_energy(system):
    """System energy = sum of kinetic energy + graviational potential energy over each pair.
        For a closed system, this must stay constant to preserve the law: Conservation of
        Energy. Tracking the values drift is a measure of the integrators accuracy."""
    KE = 0.0
    for b in system:
        KE += 0.5 * b.mass * b.velocity.magnitude()**2
    
    PE = 0.0
    for i in range(len(system)):
        for j in range(i + 1, len(system)):
            r = (system.bodies[j].position - system.bodies[i].position).magnitude()
            PE += -B.G * system.bodies[i].mass * system.bodies[j].mass / r
    
    return KE + PE


def find_collision(system):
    """Return the first colliding pair (or None) 
        -- the distance is below the sum of the radii"""
    for i in range(len(system)):
        for j in range(i + 1, len(system)):
            distance = (system.bodies[j].position - system.bodies[i].position).magnitude()
            if distance < system.bodies[i].radius + system.bodies[j].radius:
                return system.bodies[i], system.bodies[j]
    return None

# AI WRITTEN - stuck on solution
def primary(system):
    """The most massive body -- treated as the gravitational center for
    escape checks."""
    return max(system, key=lambda b: b.mass)

# AI WRITTEN - stuck on solution
def has_escaped(body, primary_body):
    """True if body is on an unbound trajectory relative to the primary.
    
    Bound vs. unbound is decided by the sign of the specific orbital energy,
    v_rel**2 / 2 - mu / r : a negative means a closed orbit, a positive means
    it will never return. This is a *computed* property, so unlike a flag it
    will always be correct for each body.
    """
    if body is primary_body:
        return False
    r = (body.position - primary_body.position).magnitude()
    v_rel = (body.velocity - primary_body.velocity).magnitude()
    mu = B.G * primary_body.mass
    specific_energy = 0.5 * v_rel**2 - mu / r
    return specific_energy > 0



# ============================================================
# VELOCITY VERLET INTEGRATOR
# ============================================================
 
def simulate(system, dt, total_time, report_every=500):
    """Advance the system with Velocity Verlet and report energy drift.
 
    The per-step order is the standard Verlet:
        1. drift positions using a(t)            -> cur_ac
        2. recompute acceleration                -> nxt_ac = a(t+dt)
        3. kick velocities with the average      0.5*(cur_ac + nxt_ac)
        4. hand off: cur_ac <- nxt_ac
    """
    
    # first compute current acceleration into nxt_ac then seed cur_ac with values
    compute_accelerations(system)
    for b in system:
        b.cur_ac = copy(b.nxt_ac)   # shallow copy used
    
    e0 = total_energy(system)
    escaped_reported = set()
    steps = int(total_time / dt)

    print(f'Starting energy: {e0:.6e} J')

    for step in range(steps):
        t = step * dt

        # 1) drift positions with current acceleration
        for b in system:
            b.position = b.position + b.velocity * dt + 0.5 * b.cur_ac * (dt**2)

        # 2) acceleration at the new positions -> nxt_ac
        compute_accelerations(system)

        # 3) kick velocities with the averaged acceleration
        for b in system:
            b.velocity = b.velocity + 0.5 * (b.cur_ac + b.nxt_ac) * dt
        
        # 4) store trajectory history once per step (record() already loops bodies);
        #    keep t numeric so Report can sort and subtract times
        system.record(t)

        # 5) hand off a(t+dt) -> a(t) for the next step
        for b in system:
            b.cur_ac = copy(b.nxt_ac)

        # --- diagnostics (Phase 3 conditionals) ---
        hit = find_collision(system)
        if hit:
            a, c = hit
            print(f't={t:.0f}s: {a.name} and {c.name} collided. Stopping.')
            return
        
        prim = primary(system)
        for b in system:
            if has_escaped(b, prim) and b.name not in escaped_reported:
                print(f't={t:.0f}s: {b.name} is on an escape trajectory from {prim.name}.')
                escaped_reported.add(b.name)

        if step % report_every == 0:
            e = total_energy(system)
            drift = abs((e - e0) / e0) if e0 != 0 else 0.0
            print(f't={t:7.0f}s  energy={e:.6e} J  drift={drift:.2e}')
    
    # print final summary
    e_final = total_energy(system)
    drift = abs((e_final - e0) / e0) if e0 != 0 else 0.0
    print(f'\nFinal energy:    {e_final:.6e} J')
    print(f'Energy drift over run: {drift:.2e}  (smaller is better)')

    # mission report + figures (Phase 6)
    rep.mission_report(system.history, system, 'Sat')
    vis.plot_orbit(system, system.history, 'orbit.png')
    rep.plot_energy(system.history, system, 'energy.png')





"""
# ============================================================
# SCENARIO 1
# ============================================================
 
# --- ACTIVE: satellite in circular LEO around Earth ---
# constructor order is now (name, mass, position, velocity, radius)
earth = B.Planet('Earth', 5.972e24, V.Vector(0, 0), V.Vector(0, 0), 6.378e6)
sat   = B.Body('Sat', 1000, V.Vector(6.678e6, 0), V.Vector(0, 7725.56), 1.0)
bodies = [earth, sat]

system = System.System(bodies)

dt = 1
total_time = 5432          # ~ one orbital period
 
if __name__ == "__main__":
    simulate(system, dt, total_time, report_every=500)
 
    # analytic cross-check (preview of the capstone): for a near-circular
    # orbit the semi-major axis is ~ the orbit radius.
    a = (sat.position - earth.position).magnitude()
    print(f'\nAnalytic period for this radius: {ap.orbital_period(a, B.G * earth.mass):.1f}s')
"""


# ============================================================
# SCENARIO 2
# ============================================================
 
# --- ACTIVE: satellite in circular LEO around Earth ---
# --- orbits once t = orbital period
# ---   burn1 applied to reach GEO
# --- at apoapsis: time = half of orbital period(transfer orbit semi major axis, mu)
# ---   burn 2 applied
# --- orbits once at t = orbital period

# constructor order is now (name, mass, position, velocity, radius)
earth = B.Planet('Earth', 5.972e24, V.Vector(0, 0), V.Vector(0, 0), 6.378e6)
sat   = B.Spacecraft('Sat', 2000, V.Vector(6.678e6, 0), V.Vector(0, 7725.56), 1.0, 1200, 800)
bodies = [earth, sat]

system = System.System(bodies)



dt = 1
total_time = 5432          # ~ one orbital period
 
if __name__ == "__main__":
    
    leo = 6.678e6
    geo = 4.216e7
    burns = ap.hohmann_transfer(leo, geo, B.G * earth.mass)
    first_orbital_t = ap.orbital_period(leo, B.G * earth.mass)
    transfer_orbital_t = ap.orbital_period((leo + geo) / 2, B.G * earth.mass)
    second_orbital_t = ap.orbital_period(geo, B.G * earth.mass)


    simulate(system, dt, first_orbital_t, report_every=500)

    sat.apply_burn(burns[0] * sat.velocity.normalize())

    simulate(system, dt, transfer_orbital_t / 4, report_every=500)

    sat.apply_burn(burns[1] * sat.velocity.normalize())

    simulate(system, dt, second_orbital_t, report_every=500)
 
    # analytic cross-check (preview of the capstone): for a near-circular

    # orbit the semi-major axis is ~ the orbit radius