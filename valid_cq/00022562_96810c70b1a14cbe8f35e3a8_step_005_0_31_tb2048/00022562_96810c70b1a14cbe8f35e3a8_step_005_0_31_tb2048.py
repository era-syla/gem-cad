import cadquery as cq

# Parameters for the cylindrical rod
radius = 2.5
length = 100.0

# Create the 3D model
result = (
    cq.Workplane("YZ")
    .circle(radius)
    .extrude(length)
)