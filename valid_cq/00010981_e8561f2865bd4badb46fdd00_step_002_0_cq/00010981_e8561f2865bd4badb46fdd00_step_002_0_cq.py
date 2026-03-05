import cadquery as cq

# Define parameters for the plate
length = 150.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 5.0 # Thickness of the plate

# Define parameters for the holes
hole_diameter = 6.0   # Diameter of the mounting holes
hole_margin_x = 10.0  # Distance from the edge along the length
hole_margin_y = 10.0  # Distance from the edge along the width

# Calculate hole positions relative to the center
# We want holes at four corners
x_pos = (length / 2.0) - hole_margin_x
y_pos = (width / 2.0) - hole_margin_y

# Create the base plate
# We start with a workplane, sketch a rectangle, and extrude it
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (x_pos, y_pos),
        (x_pos, -y_pos),
        (-x_pos, y_pos),
        (-x_pos, -y_pos)
    ])
    .hole(hole_diameter)
)