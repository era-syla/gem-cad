import cadquery as cq

# Parametric dimensions for the plate
length = 100.0  # Dimension along the X axis
width = 100.0   # Dimension along the Y axis
thickness = 5.0 # Dimension along the Z axis

# Create the rectangular plate geometry
# The box method creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)