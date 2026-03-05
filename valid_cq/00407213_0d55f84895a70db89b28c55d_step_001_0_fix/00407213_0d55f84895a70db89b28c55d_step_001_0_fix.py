import cadquery as cq
import math

# Parameters
outer_radius = 10
height = 60
turns = 10
flute_depth = 2
flute_width = 5
pitch = height / turns

# Create the main cylinder
rod = cq.Workplane("XY").circle(outer_radius).extrude(height)

# Define a helix path as a parametric curve
def helix(t):
    angle = 2 * math.pi * turns * t
    x = outer_radius * math.cos(angle)
    y = outer_radius * math.sin(angle)
    z = height * t
    return cq.Vector(x, y, z)

path_wire = cq.Workplane("XY").parametricCurve(helix, N=200).val()

# Create the rectangular cutter profile and sweep it along the helix
cutter = (
    cq.Workplane("YZ", origin=(outer_radius, 0, 0))
    .rect(flute_depth, flute_width)
    .sweep(path_wire)
)

# Subtract the cutter from the rod to form the spiral flute
result = rod.cut(cutter)