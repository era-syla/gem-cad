import cadquery as cq

# Define parameters for the rod
length = 100.0  # Length of the rod
diameter = 2.0  # Diameter of the rod
radius = diameter / 2.0

# Create the cylindrical rod
# We align the cylinder along the Z-axis, centered at the origin for the XY plane
result = cq.Workplane("XY").circle(radius).extrude(length)

# Alternatively, using the primitive cylinder method which is often cleaner for simple shapes:
# result = cq.Workplane("XY").cylinder(height=length, radius=radius)