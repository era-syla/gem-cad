import cadquery as cq

# Parametric dimensions
length = 50.0  # Long dimension
width = 15.0   # Depth
height = 15.0  # Vertical height

# Create a rectangular prism (box)
# The box is created on the XY plane and centered at the origin
result = cq.Workplane("XY").box(length, width, height)