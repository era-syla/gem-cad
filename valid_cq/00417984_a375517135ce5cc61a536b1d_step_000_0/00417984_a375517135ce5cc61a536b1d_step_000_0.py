import cadquery as cq

# Parametric dimensions
length = 90.0
width = 30.0
thickness = 5.0
hole_diameter = 10.0
hole_spacing = 60.0  # Distance between hole centers
corner_radius = 2.0

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)])
    .hole(hole_diameter)
)