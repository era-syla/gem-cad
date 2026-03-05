import cadquery as cq

# Parameters for the rod
length = 100.0  # Length of the rod
radius = 2.0    # Radius of the rod

# Create a cylindrical rod by extruding a circle
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)