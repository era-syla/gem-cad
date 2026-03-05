import cadquery as cq

# Define parametric dimensions for the plate
length = 100.0
width = 100.0
thickness = 5.0

# Create the rectangular plate geometry
# We use the XY plane and create a box centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)