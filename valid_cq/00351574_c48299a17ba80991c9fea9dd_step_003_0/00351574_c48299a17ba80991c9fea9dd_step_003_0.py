import cadquery as cq

# Parametric dimensions
plate_width = 110.0
plate_height = 160.0
plate_thickness = 5.0

# Hole dimensions
hole_diameter = 6.0
csk_diameter = 11.0
csk_angle = 90.0

# Hole pattern geometry
# Distance from center to hole columns (X axis)
x_spacing_half = 45.0 

# Distance from center to hole rows (Y axis)
y_outer = 70.0  # Near the top/bottom edges
y_inner = 30.0  # Intermediate holes

# Define the list of hole centers based on the 8-hole pattern
# Left and Right columns
hole_points = []
for x in [-x_spacing_half, x_spacing_half]:
    for y in [y_outer, y_inner, -y_inner, -y_outer]:
        hole_points.append((x, y))

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)