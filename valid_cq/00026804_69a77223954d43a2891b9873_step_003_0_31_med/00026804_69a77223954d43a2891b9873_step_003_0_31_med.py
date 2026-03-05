import cadquery as cq

# Parameters
radius = 2.5
length = 100.0

# Create the cylindrical rod
result = (
    cq.Workplane("YZ")
    .circle(radius)
    .extrude(length)
)