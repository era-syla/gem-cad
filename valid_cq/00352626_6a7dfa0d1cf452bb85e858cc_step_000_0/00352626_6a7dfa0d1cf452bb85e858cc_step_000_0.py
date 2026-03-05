import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
length = 100.0
width = 60.0
thickness = 10.0

# Create the simple rectangular plate (cuboid)
# .box() creates a solid centered at the origin by default
result = cq.Workplane("XY").box(length, width, thickness)