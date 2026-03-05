import cadquery as cq

# Define parametric dimensions
cylinder_radius = 20.0  # Radius of the cylinder
cylinder_height = 40.0  # Height of the cylinder

# Create the cylinder
# cq.Workplane("XY") starts a sketching plane on the XY plane
# .circle(cylinder_radius) draws a circle
# .extrude(cylinder_height) extrudes the circle into a cylinder
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)