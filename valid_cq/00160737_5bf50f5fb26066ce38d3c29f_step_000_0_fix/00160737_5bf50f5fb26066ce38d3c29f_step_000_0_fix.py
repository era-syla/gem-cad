import cadquery as cq
import math

# Parameters
outer_diam = 80
base_thickness = 20
stub_diam = 30
stub_height = 10
boss_diam = 40
boss_height = 8
hole_count = 16
hole_circle_diam = 60
hole_diam = 5
central_hole_diam = 12

# Build base flange
result = cq.Workplane("XY").circle(outer_diam/2).extrude(base_thickness)

# Add back stub
result = result.faces("<Z").workplane().circle(stub_diam/2).extrude(-stub_height)

# Add front boss
result = result.faces(">Z").workplane().circle(boss_diam/2).extrude(boss_height)

# Drill central hole
result = result.faces(">Z").workplane().hole(central_hole_diam)

# Drill bolt circle holes
pts = [
    (
        (hole_circle_diam/2) * math.cos(2*math.pi*i/hole_count),
        (hole_circle_diam/2) * math.sin(2*math.pi*i/hole_count)
    )
    for i in range(hole_count)
]
result = result.faces(">Z").workplane().pushPoints(pts).hole(hole_diam)