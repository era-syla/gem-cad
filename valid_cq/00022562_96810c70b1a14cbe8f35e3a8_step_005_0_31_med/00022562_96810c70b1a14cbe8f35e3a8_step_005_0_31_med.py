import cadquery as cq

# Parameters
length = 100.0
radius = 2.0

# Create the 3D model
result = cq.Workplane("YZ").cylinder(length, radius)