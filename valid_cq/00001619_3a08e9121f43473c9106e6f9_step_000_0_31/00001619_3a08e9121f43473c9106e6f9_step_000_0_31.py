import cadquery as cq
import math

# Parametric dimensions
main_r = 15
main_l = 16
pin_r = 12
pin_l = 16
web_t = 8
R = 20
cw_r = 24
ph_r = 16
flange_r = 30
flange_l = 10
ext_r = 10
ext_l = 30

def make_web(origin_y, angle):
    """Create a web shape (two circles + connecting rect) at given Y and angle."""
    rad = math.radians(angle)
    # Counterweight center at (-10, 0) rotated by angle
    cx1 = -10 * math.cos(rad)
    cz1 = -10 * math.sin(rad)
    # Pin hole center at (R, 0) rotated by angle
    cx2 = R * math.cos(rad)
    cz2 = R * math.sin(rad)
    # Mid point and half-length for connecting bar
    mx = (cx1 + cx2) / 2
    mz = (cz1 + cz2) / 2
    bar_len = math.sqrt((cx2 - cx1)**2 + (cz2 - cz1)**2)
    bar_h = min(cw_r, ph_r) * 2

    c1 = cq.Workplane("XZ", origin=(0, origin_y, 0)).center(cx1, cz1).circle(cw_r).extrude(web_t)
    c2 = cq.Workplane("XZ", origin=(0, origin_y, 0)).center(cx2, cz2).circle(ph_r).extrude(web_t)
    bar = (
        cq.Workplane("XZ", origin=(0, origin_y, 0))
        .center(mx, mz)
        .transformed(rotate=(0, 0, angle))
        .rect(bar_len, bar_h)
        .extrude(web_t)
    )
    return c1.union(c2).union(bar)

# Start building along the Y axis (which corresponds to up-right in isometric view)
y = 0

# 1. Rear Flange
crankshaft = cq.Workplane("XZ", origin=(0, y, 0)).circle(flange_r).extrude(flange_l)
y += flange_l

# 2. Main Journal 7 (Rearmost)
main_7 = cq.Workplane("XZ", origin=(0, y, 0)).circle(main_r).extrude(main_l)
crankshaft = crankshaft.union(main_7)
y += main_l

# Angles for a standard inline-6 crankshaft (firing order 1-5-3-6-2-4)
# Corresponding to pins 6 to 1 (rear to front)
angles = [0, 120, 240, 240, 120, 0]

for i, angle in enumerate(angles):
    # Web before pin
    web1 = make_web(y, angle)
    crankshaft = crankshaft.union(web1)
    y += web_t
    
    # Crankpin
    pin = (
        cq.Workplane("XZ", origin=(0, y, 0))
        .transformed(rotate=(0, 0, angle))
        .center(R, 0)
        .circle(pin_r)
        .extrude(pin_l)
    )
    
    # Radial oil hole in the crankpin
    py = y + pin_l / 2
    hole = (
        cq.Workplane("XZ", origin=(0, py, 0))
        .transformed(rotate=(0, 0, angle))
        .transformed(rotate=(0, 90, 0))
        .workplane(offset=R)
        .circle(1.5)
        .extrude(pin_r * 2.5, both=True)
    )
    pin = pin.cut(hole)
    
    crankshaft = crankshaft.union(pin)
    y += pin_l
    
    # Web after pin
    web2 = make_web(y, angle)
    crankshaft = crankshaft.union(web2)
    y += web_t
    
    # Main Journal (added between pins)
    if i < 5:
        main_j = cq.Workplane("XZ", origin=(0, y, 0)).circle(main_r).extrude(main_l)
        crankshaft = crankshaft.union(main_j)
        y += main_l

# Main Journal 1 (Frontmost)
main_1 = cq.Workplane("XZ", origin=(0, y, 0)).circle(main_r).extrude(main_l)
crankshaft = crankshaft.union(main_1)
y += main_l

# Front Extension (Pulley/Damper mount)
ext = cq.Workplane("XZ", origin=(0, y, 0)).circle(ext_r).extrude(ext_l)
crankshaft = crankshaft.union(ext)
y += ext_l

# Final output geometry
result = crankshaft