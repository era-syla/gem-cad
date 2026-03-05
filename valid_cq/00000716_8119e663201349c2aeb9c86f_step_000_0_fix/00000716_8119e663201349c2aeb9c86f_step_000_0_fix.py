import cadquery as cq
import math

# Parameters
hex_flat = 15.0
hex_diameter = hex_flat / math.cos(math.pi/6)  # circumscribed circle diameter for hexagon
hex_thickness = 6.0
boss_thickness = 2.0
flange_thickness = 1.5
boss_diameter = hex_flat
flange_diameter = 20.0
hole_diameter = 8.0

# Create hexagonal body
hex_body = cq.Workplane("XY").polygon(6, hex_diameter).extrude(hex_thickness)

# Create boss protrusion on back
boss = cq.Workplane("XY").circle(boss_diameter/2).extrude(-boss_thickness)

# Create outer flange
flange = cq.Workplane("XY").circle(flange_diameter/2).extrude(-flange_thickness)

# Combine parts and cut through-hole
result = (
    hex_body
    .union(boss)
    .union(flange)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)