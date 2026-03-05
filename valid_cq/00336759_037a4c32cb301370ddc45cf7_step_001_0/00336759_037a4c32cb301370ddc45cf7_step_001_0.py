import cadquery as cq

# Define parametric dimensions based on the image proportions
# The object appears to be a rectangular plate or block
height = 80.0      # Vertical dimension
width = 50.0       # Horizontal dimension
thickness = 10.0   # Depth/Thickness

# Create the solid geometry
# We use the box operation to create a rectangular prism centered at the origin
# Dimensions correspond to x (width), y (height), and z (thickness)
result = cq.Workplane("XY").box(width, height, thickness)