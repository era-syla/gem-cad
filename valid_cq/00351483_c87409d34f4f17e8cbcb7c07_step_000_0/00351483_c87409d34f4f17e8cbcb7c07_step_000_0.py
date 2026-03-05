import cadquery as cq

# Define parametric dimensions
cylinder_height = 50.0
cylinder_radius = 6.0

# Generate the cylindrical model
# Start on the XY plane, draw a circle, and extrude it to create the solid cylinder
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)