import cadquery as cq

# Parametric dimensions based on estimated proportions from the image
length = 100.0
height = 50.0
thickness = 5.0

# Create a rectangular prism (box)
# Using XY workplane and specifying dimensions for length (x), thickness (y), and height (z)
# to create a vertical plate-like shape.
result = cq.Workplane("XY").box(length, thickness, height)