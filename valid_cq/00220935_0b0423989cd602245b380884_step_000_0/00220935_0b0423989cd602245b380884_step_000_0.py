import cadquery as cq

# Parametric dimensions
cylinder_height = 100.0  # Length of the rod
cylinder_radius = 4.0    # Radius of the rod

# Create the cylinder geometry
# Start on the XY plane, create a circle, and extrude it to create the rod
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)