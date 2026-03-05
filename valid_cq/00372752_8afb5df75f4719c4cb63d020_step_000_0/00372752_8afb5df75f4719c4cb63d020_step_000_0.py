import cadquery as cq

# Parametric dimensions for the model
radius = 10.0
cylinder_height = 30.0

# Create the cylindrical base
# We start on the XY plane, draw a circle, and extrude it vertically
cylinder = cq.Workplane("XY").circle(radius).extrude(cylinder_height)

# Create the hemispherical top
# We create a new workplane at the top of the cylinder
# Placing a sphere here centers it at (0, 0, cylinder_height)
# The bottom half of the sphere will be inside the cylinder
dome = cq.Workplane("XY").workplane(offset=cylinder_height).sphere(radius)

# Combine the cylinder and the dome into a single solid
result = cylinder.union(dome)