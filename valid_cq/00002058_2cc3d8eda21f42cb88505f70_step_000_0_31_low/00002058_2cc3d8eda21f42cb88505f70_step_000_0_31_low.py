import cadquery as cq

# Parameters
length = 100.0  # Length of the box
width = 20.0    # Width of the box
height = 10.0   # Height of the box

# Create the box
result = cq.Workplane("XY").box(length, width, height)