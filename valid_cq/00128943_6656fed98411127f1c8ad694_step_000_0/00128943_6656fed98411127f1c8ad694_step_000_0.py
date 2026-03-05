import cadquery as cq

# Parametric dimensions
plate_length = 120.0
plate_height = 60.0
plate_thickness = 5.0
hole_diameter = 6.0
hole_margin_x = 10.0  # Distance from side edges to hole centers
hole_margin_y = 12.0  # Distance from top/bottom edges to hole centers

# Calculate offsets from center (0,0)
x_offset = plate_length / 2.0 - hole_margin_x
y_offset = plate_height / 2.0 - hole_margin_y

# Define the list of points for the 4 holes
hole_points = [
    (-x_offset, y_offset),  # Top Left
    (-x_offset, -y_offset), # Bottom Left
    (x_offset, y_offset),   # Top Right
    (x_offset, -y_offset)   # Bottom Right
]

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)