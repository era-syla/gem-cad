import cadquery as cq

length = 50
width = 10
height = 5
chamfer_size = 2

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z")
    .chamfer(chamfer_size)
)