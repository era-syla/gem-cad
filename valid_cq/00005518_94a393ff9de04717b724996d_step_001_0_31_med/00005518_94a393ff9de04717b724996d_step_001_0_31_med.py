import cadquery as cq

# Parametric dimensions
width = 100.0
height = 60.0
thickness = 10.0
depth = 5.0
cylinder_radius = 8.0

# Create the main rectangular frame
frame = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2 * thickness, height - 2 * thickness)
    .extrude(depth)
)

# Create the cylinder at the bottom-right outer corner
cylinder = (
    cq.Workplane("XY")
    .center(width / 2.0, -height / 2.0)
    .circle(cylinder_radius)
    .extrude(depth)
)

# Combine the geometries into the final result
result = frame.union(cylinder)