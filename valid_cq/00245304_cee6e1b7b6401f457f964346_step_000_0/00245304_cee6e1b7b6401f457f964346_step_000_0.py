import cadquery as cq

# Parametric dimensions
length = 150.0
width = 100.0
thickness = 10.0
hole_diameter = 6.0

# Hole pattern parameters
num_holes_length = 5
num_holes_width = 2
margin_length = 20.0  # Distance from the short edges
margin_width = 15.0   # Distance from the long edges

# Calculate spacing for the rectangular array
# x_spacing is the distance between adjacent holes along the length
x_spacing = (length - (2 * margin_length)) / (num_holes_length - 1)

# y_spacing is the distance between the two rows of holes
y_spacing = width - (2 * margin_width)

# Create the CAD model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .rarray(x_spacing, y_spacing, num_holes_length, num_holes_width)
    .hole(hole_diameter)
)