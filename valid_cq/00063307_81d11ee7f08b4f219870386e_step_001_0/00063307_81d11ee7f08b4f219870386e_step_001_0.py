import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the box
width = 50.0    # Width of the box
height = 20.0   # Height/Thickness of the box

# Create the rectangular prism (box)
result = cq.Workplane("XY").box(length, width, height)