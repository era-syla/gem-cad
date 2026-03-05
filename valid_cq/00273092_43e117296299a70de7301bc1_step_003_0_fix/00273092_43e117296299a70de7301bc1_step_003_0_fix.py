import cadquery as cq
import math

# Parameters
side = 30
height_prism = 40
fillet_radius = 2
dome_radius = 20

# Calculate triangle vertices for an equilateral triangle of given side length
h_tri = side / math.sqrt(3)
pts = [
    (0,  2*h_tri/3),             # top vertex
    (-side/2, -h_tri/3),         # bottom-left
    ( side/2, -h_tri/3)          # bottom-right
]

# Build triangular prism
prism = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(height_prism)
)

# Build a sphere centered at top plane to form the dome
dome = (
    cq.Workplane("XY")
      .sphere(dome_radius)
      .translate((0, 0, height_prism))
)

# Union prism and dome, then fillet all edges
result = (
    prism.union(dome)
         .edges()
         .fillet(fillet_radius)
)