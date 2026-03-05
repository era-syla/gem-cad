import cadquery as cq

# Define parametric dimensions
cylinder_radius = 20.0  # Radius of the cylinder
cylinder_length = 50.0  # Length of the cylinder

# Create the cylindrical geometry
# The default cylinder is centered on the origin and aligned with the Z axis.
# We create a simple solid cylinder.
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_length)

# Alternatively, using the dedicated solid generator:
# result = cq.Solid.makeCylinder(cylinder_radius, cylinder_length)