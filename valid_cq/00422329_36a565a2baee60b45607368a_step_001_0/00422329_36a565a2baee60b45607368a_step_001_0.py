import cadquery as cq

# Parametric dimensions for the rectangular prism
length = 100.0  # Length of the box
width = 30.0    # Width of the box
height = 30.0   # Height of the box

# Create the solid geometry
# Using the XY workplane and creating a box centered at the origin
result = cq.Workplane("XY").box(length, width, height)