import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
# The object appears to be a thin, tall rectangular panel
height = 100.0
width = 40.0
thickness = 3.0

# Create the solid geometry
# We generate a box centered at the origin
# The dimensions map to X (width), Y (thickness), and Z (height) to create a standing panel
result = cq.Workplane("XY").box(width, thickness, height)