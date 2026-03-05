import cadquery as cq

# Parameters for the plate dimensions
length = 160.0
width = 80.0
thickness = 10.0
corner_radius = 10.0
hole_diameter = 6.0

# Hole layout parameters
# Outer holes (near the corners)
outer_x_offset = length / 2 - 12.0
outer_y_offset = width / 2 - 12.0

# Inner holes (grouped vertically, inset from sides)
inner_x_offset = length / 2 - 45.0
inner_y_offset = 18.0

# Define list of hole coordinates (x, y)
hole_points = [
    # Outer Corner Holes
    (outer_x_offset, outer_y_offset),
    (outer_x_offset, -outer_y_offset),
    (-outer_x_offset, outer_y_offset),
    (-outer_x_offset, -outer_y_offset),
    
    # Inner Vertical Pairs
    (inner_x_offset, inner_y_offset),
    (inner_x_offset, -inner_y_offset),
    (-inner_x_offset, inner_y_offset),
    (-inner_x_offset, -inner_y_offset)
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)  # Create base rectangular prism
    .edges("|Z")                    # Select vertical edges
    .fillet(corner_radius)          # Round the corners
    .faces(">Z")                    # Select top face
    .workplane()
    .pushPoints(hole_points)        # Place points for holes
    .hole(hole_diameter)            # Cut holes through the solid
)