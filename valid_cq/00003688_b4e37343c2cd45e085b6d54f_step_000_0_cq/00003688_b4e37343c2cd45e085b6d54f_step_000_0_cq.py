import cadquery as cq

# Define parameters for the cube
length = 10.0
width = 10.0
height = 10.0

# Create a simple cube using the box method
# center=True centers the box at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, height, centered=True)