import cadquery as cq

# Parametric dimensions based on the image proportions
length = 100.0
width = 50.0
thickness = 5.0

# Create the rectangular plate geometry
# Utilizing the box method for a simple rectangular prism
result = cq.Workplane("XY").box(length, width, thickness)