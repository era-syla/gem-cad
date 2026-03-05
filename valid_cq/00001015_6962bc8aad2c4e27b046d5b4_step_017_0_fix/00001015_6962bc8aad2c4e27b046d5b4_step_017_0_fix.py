import cadquery as cq
from math import sin, cos, pi

# Parameters
R = 15                          # Base semi-circle radius
rect_depth = 20                 # Depth of the rectangular part of the base
base_thickness = 5              # Thickness of the base
cyl_radius = 10                 # Radius of the central cylinder
cyl_height = 40                 # Height of the central cylinder
inner_bore_radius = 4           # Radius of the bore through the cylinder
hole_diameter = 4               # Diameter of the bolt holes
hole_pattern_radius = 12        # Radius at which the bolt holes are placed
num_holes = 6                   # Number of bolt holes

# Create the base (rectangle + semi-circle)
result = (
    cq.Workplane("XY")
      .polyline([(-R, 0), (-R, -rect_depth), (R, -rect_depth), (R, 0)])
      .threePointArc((0, R), (-R, 0))
      .close()
      .extrude(base_thickness)
)

# Drill the bolt holes in the base
holes_pts = [
    (
        hole_pattern_radius * cos(2 * pi * i / num_holes),
        hole_pattern_radius * sin(2 * pi * i / num_holes)
    )
    for i in range(num_holes)
]
result = result.faces(">Z").workplane().pushPoints(holes_pts).hole(hole_diameter)

# Extrude the central cylinder
result = result.faces(">Z").workplane().circle(cyl_radius).extrude(cyl_height)

# Bore through the cylinder
result = result.faces(">Z").workplane().circle(inner_bore_radius).cutThruAll()