import cadquery as cq

# Parametric dimensions based on visual aspect ratio
# The object appears to be a long rectangular prism (square bar)
width = 10.0      # Cross-sectional width
depth = 10.0      # Cross-sectional depth
height = 200.0    # Total length/height of the bar

# Generate the 3D model
# Creates a box centered at the origin
result = cq.Workplane("XY").box(width, depth, height)