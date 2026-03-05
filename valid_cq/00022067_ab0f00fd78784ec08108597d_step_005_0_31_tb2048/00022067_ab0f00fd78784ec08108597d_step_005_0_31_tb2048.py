import cadquery as cq

# Parameters
diameter = 5.0
length = 100.0

# Create the solid model
result = (
    cq.Workplane("YZ")
    .circle(diameter / 2.0)
    .extrude(length)
)