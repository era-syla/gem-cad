import cadquery as cq

# Parameters for the rod
radius = 1.0
length = 100.0

# Create the 3D model
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)