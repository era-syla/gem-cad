import cadquery as cq

# Parametric dimensions
width = 10.0   # Dimension along X axis
depth = 10.0   # Dimension along Y axis
height = 40.0  # Dimension along Z axis

# Create a rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(width, depth, height)