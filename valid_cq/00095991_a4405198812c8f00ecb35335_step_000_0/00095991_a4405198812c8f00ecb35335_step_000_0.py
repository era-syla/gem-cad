import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
# The object appears to be a rectangular prism with a square base
width = 40.0    # X dimension
depth = 40.0    # Y dimension
height = 100.0  # Z dimension (Tallest dimension)

# Create the rectangular prism (box)
# The box is created on the XY plane and centered at the origin
result = cq.Workplane("XY").box(width, depth, height)