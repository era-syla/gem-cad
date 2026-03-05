import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
length = 100.0
width = 50.0
thickness = 5.0

# Create a solid rectangular box centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)