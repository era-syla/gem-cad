import cadquery as cq

# Define dimensions
length = 10.0  # Length of the cube
width = 10.0   # Width of the cube
height = 10.0  # Height of the cube

# Create the cube
result = cq.Workplane("XY").box(length, width, height)