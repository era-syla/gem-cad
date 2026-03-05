import cadquery as cq

# Define parametric dimensions
rod_length = 250.0
rod_radius = 2.5

# Create the cylindrical rod
# We start on the XY plane, draw a circle, and extrude it along the Z axis
result = (
    cq.Workplane("XY")
    .circle(rod_radius)
    .extrude(rod_length)
)