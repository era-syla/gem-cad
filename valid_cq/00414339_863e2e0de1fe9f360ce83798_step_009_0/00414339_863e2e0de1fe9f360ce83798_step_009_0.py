import cadquery as cq

# Parametric dimensions
length = 10.0  # Dimension along X axis
width = 10.0   # Dimension along Y axis
height = 40.0  # Dimension along Z axis

# Create a rectangular prism (box)
result = cq.Workplane("XY").box(length, width, height)