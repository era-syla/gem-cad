import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
# The object is a long, thin rectangular strip (flat bar)
length = 150.0
width = 6.0
thickness = 1.0

# Create the 3D model
# box() creates a rectangular prism centered at the origin by default
result = cq.Workplane("XY").box(length, width, thickness)