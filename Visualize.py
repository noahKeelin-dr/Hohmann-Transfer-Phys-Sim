"""
AI GENERATED CODE
Phase 6a - Orbit visualization (matplotlib).

Reads a populated System.history (flat records of
(t, name, x, y, vx, vy)) and draws each body's path in the x-y plane.

Usage (after your Task-1 wiring runs the sim and fills system.history):
    import visualize
    visualize.plot_orbit(system, system.history, 'orbit.png')
"""

import matplotlib.pyplot as plt


def trajectory(history, name):
    """Pull one body's path out of the flat history -> (xs, ys).

    Kept as its own function so the plotting code stays at one level of
    abstraction: the filter lives here, the drawing lives in plot_orbit.
    """
    xs = [rec[2] for rec in history if rec[1] == name]
    ys = [rec[3] for rec in history if rec[1] == name]
    return xs, ys


def _primary(system):
    """Most massive body -- drawn as the central marker."""
    return max(system.bodies, key=lambda b: b.mass)


def plot_orbit(system, history, filename='orbit.png'):
    """Plot every body's trajectory; star-mark the primary, dot-mark each start.

    set_aspect('equal') is the critical line: without it a circular orbit
    is squashed into an ellipse by the axis scaling and looks wrong even
    when the physics is right.
    """
    prim = _primary(system)
    fig, ax = plt.subplots(figsize=(6, 6))

    for body in system.bodies:
        xs, ys = trajectory(history, body.name)
        if not xs:
            continue
        if body is prim:
            # the heavy body barely moves; mark its location with a star
            ax.scatter(xs[0], ys[0], marker='*', s=260, color='goldenrod',
                       edgecolor='black', linewidth=0.5, zorder=5, label=body.name)
        else:
            ax.plot(xs, ys, linewidth=1.2, label=body.name)
            ax.scatter(xs[0], ys[0], marker='o', s=28, zorder=4)  # start point

    ax.set_aspect('equal')                       # <-- the orbit gotcha
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Orbit trajectory')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    fig.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename

