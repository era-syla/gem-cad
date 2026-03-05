import cadquery as cq

# Parameters
length = 100.0
diameter = 5.0
chamfer_size = 0.2

# Create the cylindrical rod
result = (
    cq.Workplane("YZ")
    .circle(diameter / 2.0)
    .extrude(length)
    .edges(">X or <X")
    .chamfer(chamfer_size)
)