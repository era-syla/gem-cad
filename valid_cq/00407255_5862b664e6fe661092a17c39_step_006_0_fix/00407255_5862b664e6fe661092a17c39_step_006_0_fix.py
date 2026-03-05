import cadquery as cq
import math

# Parameters
thickness = 5
width = 10
lengths = [80, 60, 40]
angles = [0, 120, 240]
hole_diameter = 6

# Build arms
base = cq.Workplane("XY")
combined = None
for L, angle in zip(lengths, angles):
    arm = base.transformed(rotate=(0, 0, angle)).rect(L, width).extrude(thickness)
    combined = arm if combined is None else combined.union(arm)

# Drill holes at arm ends
hole_points = [
    (L * math.cos(math.radians(a)), L * math.sin(math.radians(a)))
    for L, a in zip(lengths, angles)
]
result = combined.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)