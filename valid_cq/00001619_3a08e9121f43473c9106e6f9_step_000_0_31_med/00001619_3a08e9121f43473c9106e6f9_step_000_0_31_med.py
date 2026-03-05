import cadquery as cq
import math

# --- Parameters ---
main_r = 18       # Main journal radius
main_w = 20       # Main journal width
pin_r = 15        # Crankpin radius
pin_w = 18        # Crankpin width
stroke = 25       # Crank offset (half of total stroke)
web_t = 12        # Web thickness
width = 30        # Web connecting width
cw_offset = 15    # Counterweight offset from center
cw_r = 26         # Counterweight outer radius

# Firing angles for a typical straight-6 engine
angles = [0, 120, 240, 240, 120, 0]

def get_web(angle):
    """Generates a single crank web at the given angle."""
    w = cq.Workplane("XY")
    # Counterweight lobe
    cw = w.center(-cw_offset, 0).cylinder(web_t, cw_r)
    # Crankpin base connection
    pin = w.center(stroke, 0).cylinder(web_t, pin_r)
    # Connector from center to crankpin
    b1 = w.center(stroke/2, 0).box(stroke, width, web_t)
    # Connector from center to counterweight
    b2 = w.center(-cw_offset/2, 0).box(cw_offset, width, web_t)
    # Main journal hub
    hub = w.center(0, 0).cylinder(web_t, main_r)
    
    # Combine the web components and rotate to the correct phase angle
    web = cw.union(pin).union(b1).union(b2).union(hub)
    return web.rotate((0, 0, 0), (0, 0, 1), angle)

# Array to hold all solid components before final union
parts = []
z = 0

# --- Rear Flange Section ---
parts.append(cq.Workplane("XY").workplane(offset=z + 6).cylinder(12, 28))
z += 12

parts.append(cq.Workplane("XY").workplane(offset=z + 5).cylinder(10, main_r))
z += 10

# First Main Journal
parts.append(cq.Workplane("XY").workplane(offset=z + main_w/2).cylinder(main_w, main_r))
z += main_w

# --- Cylinder Throws Loop ---
for a in angles:
    # Forward Web
    web1 = get_web(a).translate((0, 0, z + web_t/2))
    parts.append(web1)
    z += web_t
    
    # Crankpin
    pin_x = stroke * math.cos(math.radians(a))
    pin_y = stroke * math.sin(math.radians(a))
    pin_solid = cq.Workplane("XY").workplane(offset=z + pin_w/2).center(pin_x, pin_y).cylinder(pin_w, pin_r)
    parts.append(pin_solid)
    z += pin_w
    
    # Rearward Web
    web2 = get_web(a).translate((0, 0, z + web_t/2))
    parts.append(web2)
    z += web_t
    
    # Main Journal
    mj = cq.Workplane("XY").workplane(offset=z + main_w/2).cylinder(main_w, main_r)
    parts.append(mj)
    z += main_w

# --- Front Shaft Extension ---
parts.append(cq.Workplane("XY").workplane(offset=z + 15).cylinder(30, 10))

# --- Boolean Assembly ---
result = parts[0]
for p in parts[1:]:
    result = result.union(p)

# Optional: orient the model nicely for viewing
result = result.rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 1, 0), -45)