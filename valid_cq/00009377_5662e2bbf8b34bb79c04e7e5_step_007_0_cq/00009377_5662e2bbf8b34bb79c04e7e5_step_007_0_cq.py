import cadquery as cq

# Define parameters for the rectangular prism
length = 40.0
width = 20.0
height = 10.0

# Create the box (rectangular prism)
# Centered=True is commonly used but not strictly required. 
# Based on the image showing a solid block in isometric view, 
# a simple box operation is sufficient.
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want specific origin placement (e.g., corner at 0,0,0):
# result = cq.Workplane("XY").box(length, width, height, centered=False)

# But the standard centered box is the most idiomatic CadQuery starting point.