import cadquery as cq

# Parametric dimensions for the rectangular bar
length = 200.0  # Long dimension
width = 10.0    # Cross-section width
height = 5.0    # Cross-section height

# Create the solid rectangular prism
# .box() centers the geometry at the origin (0,0,0) by default
result = cq.Workplane("XY").box(length, width, height)