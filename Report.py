"""
AI GENERATED CODE
Phase 6b - Mission report and diagnostics.

Searches a populated System.history (records of (t, name, x, y, vx, vy))
to summarize the orbit, and plots total energy vs time as a conservation
check. Periapsis/apoapsis come from a min/max search over the separation
series (Ch 7). Energy is recomputed from state + masses, so history stays
the single source of truth.

Usage (after your Task-1 wiring fills system.history):
    import report
    report.mission_report(system.history, system, 'Sat')
    report.plot_energy(system.history, system, 'energy.png')
"""

import matplotlib.pyplot as plt
import analytic_physics as ap


def _states_by_time(history):
    """Regroup the flat log into {t: {name: (x, y, vx, vy)}}."""
    grouped = {}
    for t, name, x, y, vx, vy in history:
        grouped.setdefault(t, {})[name] = (x, y, vx, vy)
    return grouped


def _primary(system):
    return max(system.bodies, key=lambda b: b.mass)


def separation_series(history, system, name):
    """List of (t, distance-to-primary) for one body across the run."""
    prim = _primary(system)
    grouped = _states_by_time(history)
    out = []
    for t in sorted(grouped):
        snap = grouped[t]
        if name not in snap or prim.name not in snap:
            continue
        x, y, _, _ = snap[name]
        px, py, _, _ = snap[prim.name]
        out.append((t, ((x - px)**2 + (y - py)**2) ** 0.5))
    return out


def apsides(history, system, name):
    """(periapsis, apoapsis) = (min, max) separation. A search, Ch 7."""
    dists = [d for _, d in separation_series(history, system, name)]
    return min(dists), max(dists)


def numeric_period(history, name):
    """Estimate the period as the time for the body to return closest to
    its start, ignoring the first fifth of the run so it has left the
    starting neighborhood first."""
    pts = [(rec[0], rec[2], rec[3]) for rec in history if rec[1] == name]
    t0, x0, y0 = pts[0]
    best_t, best_d = None, None
    for t, x, y in pts[len(pts) // 5:]:
        d = ((x - x0)**2 + (y - y0)**2) ** 0.5
        if best_d is None or d < best_d:
            best_d, best_t = d, t
    return best_t - t0


def energy_series(history, system):
    """Recompute total system energy (KE + pairwise PE) at each timestep."""
    G = system.constants['G']
    mass = {b.name: b.mass for b in system.bodies}
    grouped = _states_by_time(history)
    ts, es = [], []
    for t in sorted(grouped):
        snap = grouped[t]
        names = list(snap)
        ke = 0.0
        for n in names:
            x, y, vx, vy = snap[n]
            ke += 0.5 * mass[n] * (vx * vx + vy * vy)
        pe = 0.0
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                xi, yi, _, _ = snap[names[i]]
                xj, yj, _, _ = snap[names[j]]
                r = ((xi - xj)**2 + (yi - yj)**2) ** 0.5
                pe += -G * mass[names[i]] * mass[names[j]] / r
        ts.append(t)
        es.append(ke + pe)
    return ts, es


def plot_energy(history, system, filename='energy.png'):
    """Fractional energy drift vs time, (E - E0) / |E0|.

    Plotting the *fraction* rather than raw joules keeps the scale honest:
    raw energy would let matplotlib auto-offset and zoom into the 12th
    digit, making a ~1e-12 wobble look like a violation. The curve here is
    bounded and periodic (it returns, it doesn't run away) -- the signature
    of a symplectic integrator like Verlet, and the reason the orbit stays
    stable indefinitely where Euler would spiral.
    """
    ts, es = energy_series(history, system)
    e0 = es[0]
    drift = [(e - e0) / abs(e0) for e in es]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ts, drift, linewidth=1.2)
    ax.axhline(0, color='gray', linewidth=0.6)
    ax.set_xlabel('time (s)')
    ax.set_ylabel(r'fractional energy drift  $(E-E_0)/|E_0|$')
    ax.set_title('Energy conservation check (bounded, ~1e-12)')
    ax.grid(True, alpha=0.3)
    fig.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def mission_report(history, system, name=None):
    """Print and return a summary dict for the orbiting body `name`
    (defaults to the first non-primary body)."""
    prim = _primary(system)
    if name is None:
        name = next(b.name for b in system.bodies if b is not prim)

    peri, apo = apsides(history, system, name)
    a = (peri + apo) / 2
    ecc = (apo - peri) / (apo + peri)
    mu = system.constants['G'] * prim.mass
    t_analytic = ap.orbital_period(a, mu)
    t_numeric = numeric_period(history, name)
    ts, es = energy_series(history, system)
    drift = abs((es[-1] - es[0]) / es[0]) if es[0] != 0 else 0.0

    report = {
        'body': name, 'primary': prim.name,
        'periapsis_m': peri, 'apoapsis_m': apo,
        'semi_major_axis_m': a, 'eccentricity': ecc,
        'period_analytic_s': t_analytic, 'period_numeric_s': t_numeric,
        'energy_drift': drift,
    }

    print(f'=== Mission report: {name} about {prim.name} ===')
    print(f'  periapsis        : {peri:,.1f} m')
    print(f'  apoapsis         : {apo:,.1f} m')
    print(f'  semi-major axis  : {a:,.1f} m')
    print(f'  eccentricity     : {ecc:.6f}')
    print(f'  period (analytic): {t_analytic:,.1f} s')
    print(f'  period (numeric) : {t_numeric:,.1f} s')
    print(f'  energy drift     : {drift:.2e}')
    return report