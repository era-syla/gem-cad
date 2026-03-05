import cadquery as cq

# Define dimensions
length = 10.0  # Length of the box (x-axis)
width = 6.0    # Width of the box (y-axis)
height = 4.0   # Height of the box (z-axis)

# Create the box
result = cq.Workplane("XY").box(length, width, height)