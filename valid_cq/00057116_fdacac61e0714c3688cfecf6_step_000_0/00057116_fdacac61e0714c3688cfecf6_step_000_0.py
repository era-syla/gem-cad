import cadquery as cq

# Parametric dimensions for the plate
width = 100.0      # Dimension along the X axis
height = 120.0     # Dimension along the Y axis
thickness = 5.0    # Dimension along the Z axis (thickness)

# Create the rectangular solid geometry
# Using box() creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(width, height, thickness)