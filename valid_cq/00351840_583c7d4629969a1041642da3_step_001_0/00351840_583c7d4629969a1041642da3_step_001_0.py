import cadquery as cq

# Parametric dimensions for the plate
length = 150.0  # Dimension along the X axis
width = 100.0   # Dimension along the Y axis
thickness = 5.0 # Dimension along the Z axis

# Create the solid rectangular plate
# The box method creates a cuboid centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)