import cadquery as cq

# Parametric dimensions for the rectangular prism
width = 10.0   # Dimension along X axis
depth = 10.0   # Dimension along Y axis
height = 30.0  # Dimension along Z axis (tall prism)

# Create the solid box geometry
# We create a workplane on the XY plane and extrude a box
result = cq.Workplane("XY").box(width, depth, height)