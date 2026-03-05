import cadquery as cq
import math

# Parameters
r1 = 20        # Radius of the larger end
r2 = 10        # Radius of the smaller end
dx = 45        # Distance between circle centers along X
thickness = 8  # Plate thickness
hole_dia = 8   # Diameter of the through hole

# Compute tangent points for the convex profile
angle = math.acos((r1 - r2) / dx)
b1 = (r1 * math.cos(angle),  r1 * math.sin(angle))
b2 = (r1 * math.cos(angle), -r1 * math.sin(angle))
s1 = (dx + r2 * math.cos(angle),  r2 * math.sin(angle))
s2 = (dx + r2 * math.cos(angle), -r2 * math.sin(angle))

# Build the 2D profile and extrude, then add the hole
result = (
    cq.Workplane("XY")
      .moveTo(*b1)
      .lineTo(*s1)
      .threePointArc((dx - r2, 0), s2)
      .lineTo(*b2)
      .threePointArc((-r1, 0), b1)
      .close()
      .extrude(thickness)
      .faces(">Z")
      .workplane()
      .center(dx, 0)
      .hole(hole_dia)
)