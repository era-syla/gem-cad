import cadquery as cq
import math

# Parametric dimensions
af = 12.0  # Across flats for hex
hex_dia = af / math.cos(math.radians(30))
bolt_h = 5.0
shaft_d = 8.0
shaft_l = 25.0
nut_h = 5.0
pitch = 1.0
thread_depth = 0.4
thread_width = 0.4

# --- BOLT ---
# Create the base bolt head
bolt = cq.Workplane("XY").polygon(6, hex_dia).extrude(bolt_h)

# Chamfer the top edges of the hex head
bolt = bolt.edges(">Z").chamfer(0.5)

# Add the cylindrical shaft
bolt = bolt.faces(">Z").workplane().circle(shaft_d / 2).extrude(shaft_l)

# Chamfer the top edge of the shaft
bolt = bolt.edges(">Z").chamfer(0.8)

# Cut simulated threads (grooves) into the shaft
z = bolt_h + 1.5
while z < bolt_h + shaft_l - 1.5:
    ring = (
        cq.Workplane("XY", origin=(0, 0, z))
        .circle(shaft_d / 2 + 0.1)
        .circle(shaft_d / 2 - thread_depth)
        .extrude(thread_width)
    )
    bolt = bolt.cut(ring)
    z += pitch

# --- NUT ---
# Create the base nut
nut = cq.Workplane("XY").polygon(6, hex_dia).extrude(nut_h)

# Cut the central hole
nut = nut.faces(">Z").workplane().circle(shaft_d / 2 - thread_depth / 2).cutThruAll()

# Chamfer top and bottom edges of the nut
nut = nut.edges(">Z or <Z").chamfer(0.5)

# Cut simulated internal threads
z = 0.5
while z < nut_h - 0.5:
    ring = (
        cq.Workplane("XY", origin=(0, 0, z))
        .circle(shaft_d / 2 + thread_depth)
        .circle(shaft_d / 2 - thread_depth / 2 - 0.1)
        .extrude(thread_width)
    )
    nut = nut.cut(ring)
    z += pitch

# --- POSITIONING ---
# Position the nut to the left to match the image
nut = nut.translate((-20, 0, 0))

# Combine into the final result
result = bolt.union(nut)