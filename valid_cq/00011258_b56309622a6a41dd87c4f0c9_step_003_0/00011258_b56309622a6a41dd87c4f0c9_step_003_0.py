import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Dimension along X axis
width = 75.0    # Dimension along Y axis
thickness = 2.0 # Dimension along Z axis (thickness)

# Create the solid geometry
# box() creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)