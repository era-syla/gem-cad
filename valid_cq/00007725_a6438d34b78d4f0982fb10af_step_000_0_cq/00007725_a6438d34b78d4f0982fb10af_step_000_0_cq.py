import cadquery as cq

# Parametric Dimensions
outer_diameter = 100.0
inner_diameter = 60.0
thickness = 5.0
bolt_circle_diameter = 80.0
num_holes = 8
hole_diameter = 5.0
countersink_diameter = 10.0
countersink_angle = 90.0

# Base Geometry: The ring
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# Adding Countersunk Holes
# We select the top face to start the hole operations
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_diameter / 2, 0, 360, num_holes)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)