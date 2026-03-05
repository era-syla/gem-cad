import cadquery as cq

# Parametric dimensions
length = 150.0
width = 50.0
thickness = 6.0
hole_diameter = 6.0
csk_diameter = 12.0
csk_angle = 90.0
hole_spacing = 30.0
hole_margin_from_edge = 15.0

# Create the base rectangular plate centered at the origin
# The dimensions are length (x), width (y), thickness (z)
result = cq.Workplane("XY").box(length, width, thickness)

# Calculate the X coordinate for the holes (near one end of the plate)
# box() centers the geometry, so the edge is at length/2
hole_x_pos = (length / 2) - hole_margin_from_edge

# Define the centers for the two holes
# Symmetrically spaced across the width (Y-axis)
hole_locations = [
    (hole_x_pos, hole_spacing / 2),
    (hole_x_pos, -hole_spacing / 2)
]

# Select the top face and create countersunk holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)