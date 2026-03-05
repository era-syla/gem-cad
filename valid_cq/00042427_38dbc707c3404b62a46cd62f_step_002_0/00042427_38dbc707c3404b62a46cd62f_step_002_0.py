import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the image
# The object appears to be a long, flat rectangular bar
length = 150.0
width = 15.0
thickness = 4.0

# Create the 3D model
# We establish a workplane on the XY plane and create a box (rectangular prism)
# The box method creates the geometry centered at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, thickness)