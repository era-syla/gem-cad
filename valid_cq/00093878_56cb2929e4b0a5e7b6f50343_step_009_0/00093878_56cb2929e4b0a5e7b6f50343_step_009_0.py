import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
length = 100.0
width = 15.0
thickness = 4.0

# Create the rectangular bar using the box operation
# By default, box() creates a centered solid
result = cq.Workplane("XY").box(length, width, thickness)