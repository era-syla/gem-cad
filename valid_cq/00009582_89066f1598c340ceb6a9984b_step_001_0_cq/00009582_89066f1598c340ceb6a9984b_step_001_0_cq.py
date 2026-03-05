import cadquery as cq

# Parametric dimensions
# Based on visual estimation from the isometric view
length = 40.0  # Length along the longest dimension
width = 15.0   # Width (depth)
height = 20.0  # Height

# Create the rectangular prism (box)
# centered=False will place the corner at the origin (0,0,0)
# centered=True would center the box at the origin.
# Using True for symmetry is common practice, but False is also valid.
result = cq.Workplane("XY").box(length, width, height, centered=True)