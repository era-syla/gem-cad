import cadquery as cq

# Define parametric dimensions for the plate
length = 100.0  # Dimension along X axis
width = 100.0   # Dimension along Y axis
thickness = 2.0 # Dimension along Z axis (thickness)

# Create the solid geometry
# We create a workplane on the XY plane and generate a box
# centered at the origin with the specified dimensions.
result = cq.Workplane("XY").box(length, width, thickness)