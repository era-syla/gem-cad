import cadquery as cq

# Parametric dimensions based on visual proportions
height = 90.0
width = 60.0
thickness = 10.0

# Create a rectangular block (rectangular prism)
# We use the XY plane as the base and align the dimensions to match the vertical slab appearance
# box(x_len, y_len, z_len) creates a box centered at the origin
result = cq.Workplane("XY").box(width, thickness, height)