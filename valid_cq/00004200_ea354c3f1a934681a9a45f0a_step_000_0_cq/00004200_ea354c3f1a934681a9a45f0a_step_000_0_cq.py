import cadquery as cq

# Define the parameter for the sphere
radius = 10.0

# Create the sphere
# CadQuery's sphere is centered at the origin by default
result = cq.Workplane("XY").sphere(radius)

# Return the result
result