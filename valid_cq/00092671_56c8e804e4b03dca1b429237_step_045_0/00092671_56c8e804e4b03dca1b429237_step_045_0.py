import cadquery as cq

# Define parametric dimensions for the plate
length = 100.0
width = 80.0
thickness = 5.0

# Create the rectangular plate geometry
# The box method creates a cuboid centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)