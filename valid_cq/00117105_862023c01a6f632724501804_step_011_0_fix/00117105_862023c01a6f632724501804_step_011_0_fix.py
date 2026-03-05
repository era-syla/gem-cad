import cadquery as cq
import math

# Parameters
outer_diameter = 100
thickness = 5
hole_diameter = 8
hole_radius = 35
square_side = 12

# Create base disk
result = cq.Workplane("XY").circle(outer_diameter/2).extrude(thickness)

# Cut central square hole
result = (
    result.faces(">Z")
          .workplane()
          .rect(square_side, square_side)
          .cutThruAll()
)

# Cut three mounting holes at 120° spacing
angles = [90, 210, 330]
points = [
    (hole_radius * math.cos(math.radians(a)), hole_radius * math.sin(math.radians(a)))
    for a in angles
]
result = (
    result.faces(">Z")
          .workplane()
          .pushPoints(points)
          .hole(hole_diameter)
)