import cadquery as cq

# Define parametric dimensions based on visual proportions
part_height = 100.0  # Vertical dimension
part_width = 30.0    # Horizontal dimension
part_thickness = 5.0 # Depth dimension

# Create the solid geometry
# We create a box on the XY plane.
# The dimensions map to x (width), y (thickness), and z (height) to match the vertical orientation.
result = cq.Workplane("XY").box(part_width, part_thickness, part_height)