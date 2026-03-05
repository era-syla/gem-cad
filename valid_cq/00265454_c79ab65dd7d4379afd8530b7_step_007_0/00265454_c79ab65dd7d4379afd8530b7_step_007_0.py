import cadquery as cq

# Dimensions
length = 90.0
width = 35.0
thickness = 12.0
corner_radius = 10.0

# Hole dimensions
hole_diameter = 9.0
hole_spacing = 30.0
csk_diameter = 16.0
csk_angle = 90.0

# Create the base geometry
# Start with a box centered on the XY plane
# Fillet the vertical edges to create rounded corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the countersunk holes
# Select the top face, define hole locations, and cut the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing, 0), (0, 0), (hole_spacing, 0)])
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)