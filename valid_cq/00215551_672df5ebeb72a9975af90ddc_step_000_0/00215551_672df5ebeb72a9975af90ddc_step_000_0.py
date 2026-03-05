import cadquery as cq

# Define parametric dimensions
plate_length = 300.0
plate_width = 250.0
thickness = 3.0
hole_diameter = 6.0
hole_margin = 10.0  # Distance from edge to center of hole

# Calculate spacing between hole centers
x_spacing = plate_length - (2 * hole_margin)
y_spacing = plate_width - (2 * hole_margin)

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, thickness)
    .faces(">Z")
    .workplane()
    .rect(x_spacing, y_spacing, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)