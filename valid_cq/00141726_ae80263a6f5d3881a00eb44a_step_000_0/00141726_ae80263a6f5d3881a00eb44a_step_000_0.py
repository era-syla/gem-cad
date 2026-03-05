import cadquery as cq

# Parametric dimensions based on visual estimation of the rectangular bar
length = 100.0
width = 10.0
thickness = 4.0

# Create the rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)