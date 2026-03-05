import cadquery as cq

# Parameter definitions based on visual estimation
# The object is a simple thin rectangular plate
length = 100.0
height = 30.0
thickness = 1.5

# Generate the 3D geometry
# Creating a box centered at the origin
# The dimensions are mapped to X (length), Y (thickness), and Z (height)
# to create a vertically standing plate orientation.
result = cq.Workplane("XY").box(length, thickness, height)