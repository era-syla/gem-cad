import cadquery as cq

# Parameters for the cylinder
cylinder_radius = 20.0  # Radius of the cylinder
cylinder_height = 10.0  # Height (thickness) of the cylinder

# Create the cylinder using CadQuery's Workplane
# We start on the XY plane and extrude a circle
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# Alternatively, using the primitive cylinder method:
# result = cq.Workplane("XY").cylinder(cylinder_height, cylinder_radius)