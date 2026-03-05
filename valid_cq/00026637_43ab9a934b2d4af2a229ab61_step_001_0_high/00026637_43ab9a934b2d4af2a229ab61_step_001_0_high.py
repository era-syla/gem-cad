import cadquery as cq

# Parametric dimensions
length = 60.0    # Dimension along X axis
height = 50.0    # Dimension along Z axis
width = 10.0     # Dimension along Y axis (thickness)

# Create a rectangular prism (box) centered at the origin
# The box method takes (length, width, height) arguments
result = cq.Workplane("XY").box(length, width, height)