import cadquery as cq

# Parameters
length = 100.0
height = 10.0
strip_thickness = 2.0
middle_block_length = 20.0
plate_thickness = 5.0

# Compute center and half‐lengths
center_x = length/2
half_block = middle_block_length/2

# Define the 2D outline of the shape
points = [
    (0, 0),
    (length, 0),
    (length, strip_thickness),
    (center_x + half_block, strip_thickness),
    (center_x + half_block, height - strip_thickness),
    (length, height - strip_thickness),
    (length, height),
    (0, height),
    (0, height - strip_thickness),
    (center_x - half_block, height - strip_thickness),
    (center_x - half_block, strip_thickness),
    (0, strip_thickness),
]

# Build the solid by extruding the 2D profile
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(plate_thickness)
)