import cadquery as cq

# Define parametric dimensions for the box
# Since the image shows a generic rectangular prism, we'll define reasonable defaults
length = 50.0  # Dimension along X-axis
width = 50.0   # Dimension along Y-axis
height = 30.0  # Dimension along Z-axis

# Create the box geometry
# centered=True places the center of the box at the origin (0,0,0)
# centered=(True, True, False) would place the center of the base at the origin
result = cq.Workplane("XY").box(length, width, height)